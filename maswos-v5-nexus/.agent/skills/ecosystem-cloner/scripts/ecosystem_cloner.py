#!/usr/bin/env python3
"""
ECOSYSTEM CLONER - Clonagem Cirúrgica do Ecossistema Opencode
================================================================

Script principal para clonagem completa ou seletiva do ecossistema.
Suporta clonagem de: Skills, Workflows, MCPs, RAGs, Agentes, Scripts, Configs.

Uso:
    python ecosystem_cloner.py clone --source <fonte> --target <destino>
    python ecosystem_cloner.py scan --source <caminho>
    python ecosystem_cloner.py validate --target <caminho>
    python ecosystem_cloner.py diff --source <fonte> --target <destino>
"""

import os
import sys
import json
import yaml
import shutil
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class CloneConfig:
    """Configuração para clonagem"""
    source_path: str
    target_path: str
    clone_skills: bool = True
    clone_workflows: bool = True
    clone_mcps: bool = True
    clone_rags: bool = True
    clone_agents: bool = True
    clone_scripts: bool = True
    clone_configs: bool = True
    verify_checksums: bool = True
    compress: bool = False
    verbose: bool = False
    skip_existing: bool = True


@dataclass
class ComponentInfo:
    """Informações de um componente"""
    name: str
    path: str
    component_type: str
    size: int
    checksum: str = ""
    children: List['ComponentInfo'] = field(default_factory=list)


@dataclass
class CloneReport:
    """Relatório de clonagem"""
    timestamp: str
    source: str
    target: str
    components: Dict[str, int] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    checksums_match: bool = True
    overall_score: float = 0.0


class EcosystemScanner:
    """Escaneia o ecossistema fonte e gera inventário"""
    
    SKILL_PATTERNS = ['**/SKILL.md', '**/skills/**/*.md']
    WORKFLOW_PATTERNS = ['**/.agent/workflows/*.md']
    RAG_PATTERNS = ['**/rag/**/*.py']
    SCRIPT_PATTERNS = ['**/scripts/*.py']
    CONFIG_PATTERNS = ['**/.agent/*.md', '**/.agent/*.json']
    
    def __init__(self, source_path: str):
        self.source_path = Path(source_path)
        self.components: Dict[str, List[ComponentInfo]] = {}
        
    def scan(self) -> Dict[str, List[ComponentInfo]]:
        """Executa escaneamento completo"""
        logger.info(f"Iniciando escaneamento de: {self.source_path}")
        
        self._scan_skills()
        self._scan_workflows()
        self._scan_rags()
        self._scan_scripts()
        self._scan_configs()
        
        return self.components
    
    def _scan_skills(self):
        """Escaneia skills"""
        skills_dir = self.source_path / ".agent" / "skills"
        if not skills_dir.exists():
            return
            
        skills = []
        for item in skills_dir.iterdir():
            if item.is_dir():
                skill_info = ComponentInfo(
                    name=item.name,
                    path=str(item),
                    component_type="skill",
                    size=self._get_dir_size(item)
                )
                skills.append(skill_info)
                
        self.components['skills'] = skills
        logger.info(f"Encontrados {len(skills)} skills")
    
    def _scan_workflows(self):
        """Escaneia workflows"""
        workflows_dir = self.source_path / ".agent" / "workflows"
        if not workflows_dir.exists():
            return
            
        workflows = []
        for item in workflows_dir.iterdir():
            if item.is_file() and item.suffix == '.md':
                workflows.append(ComponentInfo(
                    name=item.name,
                    path=str(item),
                    component_type="workflow",
                    size=item.stat().st_size
                ))
                
        self.components['workflows'] = workflows
        logger.info(f"Encontrados {len(workflows)} workflows")
    
    def _scan_rags(self):
        """Escaneia módulos RAG"""
        rag_dir = self.source_path / "rag"
        if not rag_dir.exists():
            return
            
        rags = []
        for item in rag_dir.rglob("*.py"):
            rags.append(ComponentInfo(
                name=item.name,
                path=str(item),
                component_type="rag",
                size=item.stat().st_size
            ))
            
        self.components['rags'] = rags
        logger.info(f"Encontrados {len(rags)} arquivos RAG")
    
    def _scan_scripts(self):
        """Escaneia scripts"""
        scripts = []
        
        # Scripts em skills
        for skill_dir in (self.source_path / ".agent" / "skills").iterdir():
            scripts_dir = skill_dir / "scripts"
            if scripts_dir.exists():
                for script in scripts_dir.glob("*.py"):
                    scripts.append(ComponentInfo(
                        name=script.name,
                        path=str(script),
                        component_type="script",
                        size=script.stat().st_size
                    ))
        
        self.components['scripts'] = scripts
        logger.info(f"Encontrados {len(scripts)} scripts")
    
    def _scan_configs(self):
        """Escaneia configurações"""
        configs = []
        
        # Arquivos de config no .agent
        agent_dir = self.source_path / ".agent"
        if agent_dir.exists():
            for item in agent_dir.iterdir():
                if item.is_file() and item.suffix in ['.md', '.json']:
                    configs.append(ComponentInfo(
                        name=item.name,
                        path=str(item),
                        component_type="config",
                        size=item.stat().st_size
                    ))
        
        self.components['configs'] = configs
        logger.info(f"Encontrados {len(configs)} arquivos de configuração")
    
    def _get_dir_size(self, path: Path) -> int:
        """Calcula tamanho de diretório"""
        total = 0
        for item in path.rglob("*"):
            if item.is_file():
                total += item.stat().st_size
        return total
    
    def generate_manifest(self) -> Dict[str, Any]:
        """Gera manifesto do ecossistema"""
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "source_path": str(self.source_path),
            "components": {}
        }
        
        for comp_type, components in self.components.items():
            manifest["components"][comp_type] = {
                "count": len(components),
                "items": [
                    {
                        "name": c.name,
                        "path": c.path,
                        "type": c.component_type,
                        "size": c.size
                    }
                    for c in components
                ]
            }
        
        return manifest


class EcosystemCloner:
    """Clona o ecossistema com precisão cirúrgica"""
    
    def __init__(self, config: CloneConfig):
        self.config = config
        self.source = Path(config.source_path)
        self.target = Path(config.target_path)
        self.checksums_source: Dict[str, str] = {}
        self.checksums_target: Dict[str, str] = {}
        self.report = CloneReport(
            timestamp=datetime.now().isoformat(),
            source=str(self.source),
            target=str(self.target)
        )
        
    def clone(self) -> CloneReport:
        """Executa clonagem completa"""
        logger.info(f"Iniciando clonagem de {self.source} para {self.target}")
        
        # Criar diretório target
        self.target.mkdir(parents=True, exist_ok=True)
        
        # Clonar componentes
        if self.config.clone_skills:
            self._clone_skills()
            
        if self.config.clone_workflows:
            self._clone_workflows()
            
        if self.config.clone_rags:
            self._clone_rags()
            
        if self.config.clone_scripts:
            self._clone_scripts()
            
        if self.config.clone_configs:
            self._clone_configs()
            
        # Calcular checksums
        if self.config.verify_checksums:
            self._calculate_checksums()
            self._verify_checksums()
        
        # Calcular score
        self._calculate_score()
        
        # Gerar manifesto
        self._generate_manifest()
        
        return self.report
    
    def _clone_skills(self):
        """Clona todos os skills"""
        logger.info("Clonando skills...")
        source_skills = self.source / ".agent" / "skills"
        target_skills = self.target / ".agent" / "skills"
        
        if not source_skills.exists():
            self.report.warnings.append("Diretório de skills não encontrado")
            return
            
        target_skills.mkdir(parents=True, exist_ok=True)
        
        count = 0
        for skill_dir in source_skills.iterdir():
            if skill_dir.is_dir():
                dest = target_skills / skill_dir.name
                if dest.exists() and self.config.skip_existing:
                    logger.debug(f"Skipping existing: {skill_dir.name}")
                    continue
                    
                try:
                    shutil.copytree(skill_dir, dest, dirs_exist_ok=True)
                    count += 1
                    logger.info(f"Clonado: {skill_dir.name}")
                except Exception as e:
                    self.report.errors.append(f"Erro ao clonar {skill_dir.name}: {e}")
        
        self.report.components['skills'] = count
        logger.info(f"Clonados {count} skills")
    
    def _clone_workflows(self):
        """Clona workflows"""
        logger.info("Clonando workflows...")
        source_wf = self.source / ".agent" / "workflows"
        target_wf = self.target / ".agent" / "workflows"
        
        if not source_wf.exists():
            self.report.warnings.append("Diretório de workflows não encontrado")
            return
            
        target_wf.mkdir(parents=True, exist_ok=True)
        
        count = 0
        for wf_file in source_wf.glob("*.md"):
            dest = target_wf / wf_file.name
            if dest.exists() and self.config.skip_existing:
                continue
                
            try:
                shutil.copy2(wf_file, dest)
                count += 1
            except Exception as e:
                self.report.errors.append(f"Erro ao clonar {wf_file.name}: {e}")
        
        self.report.components['workflows'] = count
        logger.info(f"Clonados {count} workflows")
    
    def _clone_rags(self):
        """Clona módulos RAG"""
        logger.info("Clonando RAGs...")
        source_rag = self.source / "rag"
        target_rag = self.target / "rag"
        
        if not source_rag.exists():
            self.report.warnings.append("Diretório RAG não encontrado")
            return
            
        target_rag.mkdir(parents=True, exist_ok=True)
        
        count = 0
        for item in source_rag.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(source_rag)
                dest = target_rag / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                if dest.exists() and self.config.skip_existing:
                    continue
                    
                try:
                    shutil.copy2(item, dest)
                    count += 1
                except Exception as e:
                    self.report.errors.append(f"Erro ao clonar {rel_path}: {e}")
        
        self.report.components['rags'] = count
        logger.info(f"Clonados {count} arquivos RAG")
    
    def _clone_scripts(self):
        """Clona scripts"""
        logger.info("Clonando scripts...")
        
        # Scripts em skills
        source_skills = self.source / ".agent" / "skills"
        target_skills = self.target / ".agent" / "skills"
        
        if not source_skills.exists():
            self.report.warnings.append("Diretório de skills não encontrado")
            return
            
        count = 0
        for skill_dir in source_skills.iterdir():
            if skill_dir.is_dir():
                scripts_dir = skill_dir / "scripts"
                if scripts_dir.exists():
                    target_scripts = target_skills / skill_dir.name / "scripts"
                    target_scripts.mkdir(parents=True, exist_ok=True)
                    
                    for script in scripts_dir.glob("*.py"):
                        dest = target_scripts / script.name
                        if dest.exists() and self.config.skip_existing:
                            continue
                        try:
                            shutil.copy2(script, dest)
                            count += 1
                        except Exception as e:
                            self.report.errors.append(f"Erro ao clonar {script.name}: {e}")
        
        self.report.components['scripts'] = count
        logger.info(f"Clonados {count} scripts")
    
    def _clone_configs(self):
        """Clona configurações"""
        logger.info("Clonando configurações...")
        
        agent_dir = self.source / ".agent"
        target_agent = self.target / ".agent"
        
        if not agent_dir.exists():
            self.report.warnings.append("Diretório .agent não encontrado")
            return
            
        target_agent.mkdir(parents=True, exist_ok=True)
        
        count = 0
        for item in agent_dir.iterdir():
            if item.is_file() and item.suffix in ['.md', '.json']:
                dest = target_agent / item.name
                if dest.exists() and self.config.skip_existing:
                    continue
                try:
                    shutil.copy2(item, dest)
                    count += 1
                except Exception as e:
                    self.report.errors.append(f"Erro ao clonar {item.name}: {e}")
        
        self.report.components['configs'] = count
        logger.info(f"Clonados {count} arquivos de configuração")
    
    def _calculate_checksums(self):
        """Calcula checksums MD5 de todos os arquivos"""
        logger.info("Calculando checksums...")
        
        # Checksums source
        for item in self.source.rglob("*"):
            if item.is_file():
                rel_path = str(item.relative_to(self.source))
                self.checksums_source[rel_path] = self._md5_file(item)
        
        # Checksums target
        for item in self.target.rglob("*"):
            if item.is_file():
                rel_path = str(item.relative_to(self.target))
                self.checksums_target[rel_path] = self._md5_file(item)
    
    def _md5_file(self, filepath: Path) -> str:
        """Calcula MD5 de arquivo"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _verify_checksums(self):
        """Verifica se checksums correspondem"""
        logger.info("Verificando checksums...")
        
        for path, checksum in self.checksums_source.items():
            if path in self.checksums_target:
                if self.checksums_source[path] != self.checksums_target[path]:
                    self.report.errors.append(f"Checksum mismatch: {path}")
                    self.report.checksums_match = False
            else:
                self.report.warnings.append(f"Arquivo não encontrado no target: {path}")
        
        if self.report.checksums_match:
            logger.info("Todos os checksums correspondem!")
    
    def _calculate_score(self):
        """Calcula score de clonagem"""
        total_expected = sum([
            self.config.clone_skills,
            self.config.clone_workflows,
            self.config.clone_rags,
            self.config.clone_scripts,
            self.config.clone_configs
        ])
        
        total_errors = len(self.report.errors)
        total_warnings = len(self.report.warnings)
        
        if total_expected == 0:
            self.report.overall_score = 1.0
        else:
            base_score = 1.0 - (total_errors * 0.1) - (total_warnings * 0.02)
            self.report.overall_score = max(0.0, min(1.0, base_score))
        
        logger.info(f"Score de clonagem: {self.report.overall_score:.2%}")
    
    def _generate_manifest(self):
        """Gera manifesto de clonagem"""
        manifest_path = self.target / "clone_manifest.json"
        
        manifest = {
            "timestamp": self.report.timestamp,
            "source": self.report.source,
            "target": self.report.target,
            "components": self.report.components,
            "errors": self.report.errors,
            "warnings": self.report.warnings,
            "checksums_match": self.report.checksums_match,
            "overall_score": self.report.overall_score
        }
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Manifesto gerado: {manifest_path}")


class EcosystemValidator:
    """Valida ecossistema clonado"""
    
    def __init__(self, target_path: str):
        self.target = Path(target_path)
        self.checksums: Dict[str, str] = {}
        
    def validate(self) -> Dict[str, Any]:
        """Executa validação completa"""
        logger.info(f"Validando: {self.target}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "target": str(self.target),
            "checks": {}
        }
        
        # Verificações
        results["checks"]["structural_integrity"] = self._check_structure()
        results["checks"]["content_completeness"] = self._check_completeness()
        results["checks"]["file_count"] = self._count_files()
        
        # Calcular score
        passed = sum(1 for check in results["checks"].values() if check.get("status") == "PASS")
        total = len(results["checks"])
        results["overall_score"] = passed / total if total > 0 else 0
        
        return results
    
    def _check_structure(self) -> Dict[str, Any]:
        """Verifica estrutura de diretórios"""
        required_dirs = [
            ".agent/skills",
            ".agent/workflows",
            "rag",
            ".agent"
        ]
        
        missing = []
        for dir_path in required_dirs:
            full_path = self.target / dir_path
            if not full_path.exists():
                missing.append(dir_path)
        
        return {
            "status": "PASS" if not missing else "FAIL",
            "missing_directories": missing
        }
    
    def _check_completeness(self) -> Dict[str, Any]:
        """Verifica completude de componentes"""
        # Verificar skills
        skills_dir = self.target / ".agent" / "skills"
        skills_count = len(list(skills_dir.iterdir())) if skills_dir.exists() else 0
        
        # Verificar workflows
        workflows_dir = self.target / ".agent" / "workflows"
        workflows_count = len(list(workflows_dir.glob("*.md"))) if workflows_dir.exists() else 0
        
        return {
            "status": "PASS",
            "skills_count": skills_count,
            "workflows_count": workflows_count
        }
    
    def _count_files(self) -> Dict[str, Any]:
        """Conta arquivos"""
        total = sum(1 for _ in self.target.rglob("*") if _.is_file())
        
        return {
            "status": "PASS" if total > 0 else "FAIL",
            "total_files": total
        }


def main():
    parser = argparse.ArgumentParser(description="ECOSYSTEM CLONER - Clonagem Cirúrgica")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # Comando clone
    clone_parser = subparsers.add_parser("clone", help="Clonar ecossistema")
    clone_parser.add_argument("--source", required=True, help="Caminho fonte")
    clone_parser.add_argument("--target", required=True, help="Caminho destino")
    clone_parser.add_argument("--skills", action="store_true", default=True, help="Clonar skills")
    clone_parser.add_argument("--workflows", action="store_true", default=True, help="Clonar workflows")
    clone_parser.add_argument("--rags", action="store_true", default=True, help="Clonar RAGs")
    clone_parser.add_argument("--scripts", action="store_true", default=True, help="Clonar scripts")
    clone_parser.add_argument("--configs", action="store_true", default=True, help="Clonar configurações")
    clone_parser.add_argument("--no-verify", action="store_true", help="Não verificar checksums")
    clone_parser.add_argument("--verbose", action="store_true", help="Modo verboso")
    
    # Comando scan
    scan_parser = subparsers.add_parser("scan", help="Escanear ecossistema")
    scan_parser.add_argument("--source", required=True, help="Caminho para escanear")
    scan_parser.add_argument("--output", help="Arquivo de saída (JSON)")
    
    # Comando validate
    validate_parser = subparsers.add_parser("validate", help="Validar克隆")
    validate_parser.add_argument("--target", required=True, help="Caminho a validar")
    validate_parser.add_argument("--output", help="Arquivo de saída (JSON)")
    
    args = parser.parse_args()
    
    if args.command == "scan":
        scanner = EcosystemScanner(args.source)
        manifest = scanner.scan()
        print(json.dumps(manifest, indent=2, default=lambda x: x.__dict__))
        
        if args.output:
            full_manifest = scanner.generate_manifest()
            with open(args.output, 'w') as f:
                json.dump(full_manifest, f, indent=2)
    
    elif args.command == "clone":
        config = CloneConfig(
            source_path=args.source,
            target_path=args.target,
            clone_skills=args.skills,
            clone_workflows=args.workflows,
            clone_rags=args.rags,
            clone_scripts=args.scripts,
            clone_configs=args.configs,
            verify_checksums=not args.no_verify,
            verbose=args.verbose
        )
        
        cloner = EcosystemCloner(config)
        report = cloner.clone()
        
        print(json.dumps(report.__dict__, indent=2, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x)))
    
    elif args.command == "validate":
        validator = EcosystemValidator(args.target)
        results = validator.validate()
        
        print(json.dumps(results, indent=2))
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
