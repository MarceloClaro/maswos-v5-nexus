#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLONE VALIDATOR - Validação de Integridade do Clone
====================================================

Script para validar integridade do ecossistema clonado.
Executa verificações completas de estrutura, conteúdo e funcionalidade.

Uso:
    python validate_clone.py --target <caminho> --full
    python validate_clone.py --target <caminho> --quick
    python validate_clone.py --target <caminho> --report
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Resultado de uma validação individual"""
    name: str
    status: str  # PASS, FAIL, WARN
    score: float
    message: str
    details: Dict[str, Any] = None  # type: ignore


@dataclass
class ValidationReport:
    """Relatório completo de validação"""
    timestamp: str
    target_path: str
    validations: List[ValidationResult]
    overall_score: float
    status: str  # PASS, FAIL, PARTIAL
    recommendations: List[str]


class CloneValidator:
    """Validador de clones do ecossistema"""
    
    # Componentes esperados
    EXPECTED_COMPONENTS = {
        '.agent/skills': {
            'type': 'directory',
            'min_items': 30,
            'description': 'Diretório de skills'
        },
        '.agent/workflows': {
            'type': 'directory',
            'min_items': 10,
            'description': 'Diretório de workflows'
        },
        'rag': {
            'type': 'directory',
            'min_items': 5,
            'description': 'Módulos RAG'
        },
        '.agent/TRANSFORMER_NETWORK_ARCHITECTURE.md': {
            'type': 'file',
            'description': 'Arquitetura da rede'
        },
        '.agent/mcp_config.json': {
            'type': 'file',
            'description': 'Configuração de MCPs'
        }
    }
    
    # Skills mínimos esperados
    MIN_SKILLS = [
        'api-patterns', 'app-builder', 'architecture', 'bash-linux',
        'brainstorming', 'code-review-checklist', 'database-design',
        'frontend-design', 'game-development', 'nodejs-best-practices',
        'testing-patterns', 'webapp-testing', 'web-design-guidelines'
    ]
    
    def __init__(self, target_path: str, full_validation: bool = True):
        self.target = Path(target_path)
        self.full_validation = full_validation
        self.results: List[ValidationResult] = []
        
    def validate(self) -> ValidationReport:
        """Executa validação completa"""
        
        logger.info("=" * 60)
        logger.info("CLONE VALIDATOR - Validação de Integridade")
        logger.info("=" * 60)
        logger.info(f"Target: {self.target}")
        logger.info("=" * 60)
        
        # Verificações estruturais
        self._validate_structure()
        
        # Verificação de skills
        self._validate_skills()
        
        # Verificação de workflows
        self._validate_workflows()
        
        # Verificação de RAGs
        self._validate_rags()
        
        # Verificação de arquivos de configuração
        self._validate_configs()
        
        # Verificação de conteúdo
        if self.full_validation:
            self._validate_content()
        
        # Verificação de metadados
        self._validate_metadata()
        
        # Calcular resultado final
        return self._build_final_report()
    
    def _validate_structure(self):
        """Valida estrutura de diretórios"""
        logger.info("\n[1/7] Validando estrutura...")
        
        missing_dirs = []
        
        for comp_path, config in self.EXPECTED_COMPONENTS.items():
            full_path = self.target / comp_path
            
            if config['type'] == 'directory':
                if not full_path.exists():
                    missing_dirs.append(comp_path)
                    self.results.append(ValidationResult(
                        name=f"structure_{comp_path.replace('/', '_')}",
                        status="FAIL",
                        score=0.0,
                        message=f"Diretório ausente: {comp_path}"
                    ))
                elif config.get('min_items'):
                    item_count = len(list(full_path.iterdir()))
                    if item_count < config['min_items']:
                        self.results.append(ValidationResult(
                            name=f"structure_{comp_path.replace('/', '_')}",
                            status="WARN",
                            score=item_count / config['min_items'],
                            message=f"Poucos itens em {comp_path}: {item_count} (esperado: {config['min_items']})"
                        ))
                    else:
                        self.results.append(ValidationResult(
                            name=f"structure_{comp_path.replace('/', '_')}",
                            status="PASS",
                            score=1.0,
                            message=f"Estrutura OK: {comp_path} ({item_count} itens)"
                        ))
            elif config['type'] == 'file':
                if not full_path.exists():
                    missing_dirs.append(comp_path)
                    self.results.append(ValidationResult(
                        name=f"structure_{comp_path.replace('/', '_')}",
                        status="FAIL",
                        score=0.0,
                        message=f"Arquivo ausente: {comp_path}"
                    ))
                else:
                    self.results.append(ValidationResult(
                        name=f"structure_{comp_path.replace('/', '_')}",
                        status="PASS",
                        score=1.0,
                        message=f"Arquivo presente: {comp_path}"
                    ))
        
        if not missing_dirs:
            logger.info("  Estrutura: OK")
        else:
            logger.warning(f"  Estrutura: FALTANDO {len(missing_dirs)} itens")
    
    def _validate_skills(self):
        """Valida skills"""
        logger.info("\n[2/7] Validando skills...")
        
        skills_dir = self.target / ".agent" / "skills"
        
        if not skills_dir.exists():
            self.results.append(ValidationResult(
                name="skills_directory",
                status="FAIL",
                score=0.0,
                message="Diretório de skills não encontrado"
            ))
            return
        
        # Listar skills
        available_skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        
        # Verificar skills mínimos
        found_min_skills = [s for s in self.MIN_SKILLS if s in available_skills]
        
        if len(found_min_skills) >= len(self.MIN_SKILLS):
            self.results.append(ValidationResult(
                name="skills_minimum",
                status="PASS",
                score=1.0,
                message=f"Todos os skills mínimos encontrados: {len(found_min_skills)}"
            ))
        else:
            missing = set(self.MIN_SKILLS) - set(found_min_skills)
            self.results.append(ValidationResult(
                name="skills_minimum",
                status="WARN",
                score=len(found_min_skills) / len(self.MIN_SKILLS),
                message=f"Skills mínimos faltando: {missing}"
            ))
        
        # Verificar SKILL.md em cada skill
        skills_with_md = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    skills_with_md += 1
        
        ratio = skills_with_md / len(available_skills) if available_skills else 0
        
        self.results.append(ValidationResult(
            name="skills_documentation",
            status="PASS" if ratio >= 0.9 else "WARN",
            score=ratio,
            message=f"Skills com SKILL.md: {skills_with_md}/{len(available_skills)} ({ratio:.0%})"
        ))
        
        logger.info(f"  Skills: {len(available_skills)} encontrados, {skills_with_md} com documentação")
    
    def _validate_workflows(self):
        """Valida workflows"""
        logger.info("\n[3/7] Validando workflows...")
        
        workflows_dir = self.target / ".agent" / "workflows"
        
        if not workflows_dir.exists():
            self.results.append(ValidationResult(
                name="workflows_directory",
                status="FAIL",
                score=0.0,
                message="Diretório de workflows não encontrado"
            ))
            return
        
        # Workflows esperados
        expected_workflows = [
            'brainstorm.md', 'create.md', 'debug.md', 'deploy.md',
            'enhance.md', 'orchestrate.md', 'plan.md', 'preview.md',
            'status.md', 'test.md', 'ui-ux-pro-max.md'
        ]
        
        found_workflows = [w.name for w in workflows_dir.glob("*.md")]
        
        missing = set(expected_workflows) - set(found_workflows)
        
        if not missing:
            self.results.append(ValidationResult(
                name="workflows_completeness",
                status="PASS",
                score=1.0,
                message=f"Todos os workflows presentes: {len(found_workflows)}"
            ))
        else:
            self.results.append(ValidationResult(
                name="workflows_completeness",
                status="WARN",
                score=len(found_workflows) / len(expected_workflows),
                message=f"Workflows faltando: {missing}"
            ))
        
        logger.info(f"  Workflows: {len(found_workflows)}/{len(expected_workflows)}")
    
    def _validate_rags(self):
        """Valida módulos RAG"""
        logger.info("\n[4/7] Validando RAGs...")
        
        rag_dir = self.target / "rag"
        
        if not rag_dir.exists():
            self.results.append(ValidationResult(
                name="rag_directory",
                status="FAIL",
                score=0.0,
                message="Diretório RAG não encontrado"
            ))
            return
        
        # Verificar módulos
        rag_modules = list(rag_dir.iterdir())
        
        # Verificar arquivos Python
        py_files = list(rag_dir.rglob("*.py"))
        
        self.results.append(ValidationResult(
            name="rag_modules",
            status="PASS",
            score=min(1.0, len(rag_modules) / 10),
            message=f"Módulos RAG: {len(rag_modules)} diretórios, {len(py_files)} arquivos Python"
        ))
        
        logger.info(f"  RAGs: {len(rag_modules)} módulos, {len(py_files)} arquivos Python")
    
    def _validate_configs(self):
        """Valida arquivos de configuração"""
        logger.info("\n[5/7] Validando configurações...")
        
        configs = []
        
        # Verificar arquivos importantes
        important_files = [
            '.agent/TRANSFORMER_NETWORK_ARCHITECTURE.md',
            '.agent/mcp_config.json',
            '.agent/doc.md'
        ]
        
        for file_path in important_files:
            full_path = self.target / file_path
            if full_path.exists():
                configs.append(file_path)
        
        if len(configs) >= len(important_files):
            self.results.append(ValidationResult(
                name="config_files",
                status="PASS",
                score=1.0,
                message=f"Arquivos de configuração presentes: {len(configs)}"
            ))
        else:
            self.results.append(ValidationResult(
                name="config_files",
                status="WARN",
                score=len(configs) / len(important_files),
                message=f"Arquivos de configuração: {len(configs)}/{len(important_files)}"
            ))
        
        logger.info(f"  Configs: {len(configs)}/{len(important_files)}")
    
    def _validate_content(self):
        """Valida conteúdo de arquivos"""
        logger.info("\n[6/7] Validando conteúdo...")
        
        # Verificar se arquivos estão vazios
        empty_files = []
        
        for md_file in self.target.rglob("*.md"):
            if md_file.stat().st_size < 100:
                empty_files.append(str(md_file.relative_to(self.target)))
        
        # Verificar arquivos Python
        for py_file in self.target.rglob("*.py"):
            if py_file.stat().st_size < 50:
                empty_files.append(str(py_file.relative_to(self.target)))
        
        if empty_files:
            self.results.append(ValidationResult(
                name="content_empty",
                status="WARN",
                score=1.0 - (len(empty_files) / 100),
                message=f"Arquivos potencialmente vazios: {len(empty_files)}",
                details={'empty_files': empty_files[:10]}  # Primeiros 10
            ))
            logger.warning(f"  Conteúdo: {len(empty_files)} arquivos muito pequenos")
        else:
            self.results.append(ValidationResult(
                name="content_empty",
                status="PASS",
                score=1.0,
                message="Nenhum arquivo vazio encontrado"
            ))
            logger.info("  Conteúdo: OK")
    
    def _validate_metadata(self):
        """Valida metadados e manifestos"""
        logger.info("\n[7/7] Validando metadados...")
        
        # Verificar manifesto
        manifest_path = self.target / "clone_manifest.json"
        
        if manifest_path.exists():
            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                self.results.append(ValidationResult(
                    name="metadata_manifest",
                    status="PASS",
                    score=1.0,
                    message="Manifesto encontrado e válido"
                ))
            except Exception as e:
                self.results.append(ValidationResult(
                    name="metadata_manifest",
                    status="WARN",
                    score=0.5,
                    message=f"Manifesto inválido: {str(e)}"
                ))
        else:
            self.results.append(ValidationResult(
                name="metadata_manifest",
                status="WARN",
                score=0.0,
                message="Manifesto não encontrado (clone pode estar incompleto)"
            ))
    
    def _build_final_report(self) -> ValidationReport:
        """Constrói relatório final"""
        
        # Calcular score
        passed = sum(1 for r in self.results if r.status == "PASS")
        failed = sum(1 for r in self.results if r.status == "FAIL")
        warned = sum(1 for r in self.results if r.status == "WARN")
        
        total = len(self.results)
        
        if total == 0:
            overall_score = 0.0
            status = "FAIL"
        elif failed > 0:
            overall_score = passed / total
            status = "FAIL"
        elif warned > 0:
            overall_score = passed / total
            status = "PARTIAL"
        else:
            overall_score = 1.0
            status = "PASS"
        
        # Recomendações
        recommendations = []
        
        if failed > 0:
            recommendations.append("Execute a clonagem novamente para os componentes faltando")
        
        if warned > 0:
            recommendations.append("Revise os componentes com avisos")
        
        if overall_score >= 0.95:
            recommendations.append("Clone está pronto para uso!")
        
        return ValidationReport(
            timestamp=datetime.now().isoformat(),
            target_path=str(self.target),
            validations=self.results,
            overall_score=overall_score,
            status=status,
            recommendations=recommendations
        )


def main():
    parser = argparse.ArgumentParser(
        description="CLONE VALIDATOR - Validação de Integridade"
    )
    
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Caminho do clone a validar"
    )
    
    parser.add_argument(
        "--full",
        action="store_true",
        default=True,
        help="Validação completa"
    )
    
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Validação rápida (apenas estrutura)"
    )
    
    parser.add_argument(
        "--report", "-r",
        help="Salvar relatório em arquivo"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Saída em JSON"
    )
    
    args = parser.parse_args()
    
    # Validar
    validator = CloneValidator(args.target, full_validation=not args.quick)
    report = validator.validate()
    
    # Exibir resultado
    if args.json:
        output = {
            "timestamp": report.timestamp,
            "target": report.target_path,
            "overall_score": report.overall_score,
            "status": report.status,
            "validations": [
                {
                    "name": r.name,
                    "status": r.status,
                    "score": r.score,
                    "message": r.message
                }
                for r in report.validations
            ],
            "recommendations": report.recommendations
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "=" * 60)
        print("RELATÓRIO DE VALIDAÇÃO")
        print("=" * 60)
        print(f"Target: {report.target_path}")
        print(f"Status: {report.status}")
        print(f"Score: {report.overall_score:.1%}")
        print("=" * 60)
        
        print("\nValidações:")
        for result in report.validations:
            icon = "[PASS]" if result.status == "PASS" else ("[WARN]" if result.status == "WARN" else "[FAIL]")
            print(f"  {icon} [{result.status}] {result.name}: {result.message}")
        
        if report.recommendations:
            print("\nRecomendações:")
            for rec in report.recommendations:
                print(f"  • {rec}")
        
        print("=" * 60)
    
    # Salvar relatório
    if args.report:
        output = {
            "timestamp": report.timestamp,
            "target": report.target_path,
            "overall_score": report.overall_score,
            "status": report.status,
            "validations": [
                {
                    "name": r.name,
                    "status": r.status,
                    "score": r.score,
                    "message": r.message
                }
                for r in report.validations
            ],
            "recommendations": report.recommendations
        }
        
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Relatório salvo em: {args.report}")
    
    # Exit code
    sys.exit(0 if report.status == "PASS" else 1)


if __name__ == "__main__":
    main()
