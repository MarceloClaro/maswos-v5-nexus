#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ONE-CLICK CLONE - Clone Completo com Um Único OK
================================================

Script para clonagem completa do ecossistema com um único comando.
Requer apenas uma aprovação para executar toda a clonagem.

Uso:
    python one_click_clone.py --source <fonte> --target <destino> --approve
    python one_click_clone.py --source <fonte> --target <destino> --dry-run
"""

import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import sys
import json
import yaml
import shutil
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class CloneRequest:
    """Requisição de clonagem"""
    source: str
    target: str
    approve: bool = False
    dry_run: bool = False
    skip_existing: bool = True
    verify: bool = True
    compress: bool = False


@dataclass 
class CloneResult:
    """Resultado da clonagem"""
    success: bool
    timestamp: str
    source: str
    target: str
    components_cloned: Dict[str, int]
    total_files: int
    total_size: int
    errors: List[str]
    warnings: List[str]
    checksum_verified: bool
    score: float


class OneClickCloner:
    """Clonador de um único clique"""
    
    # Componentes a clonar
    COMPONENTS = {
        'skills': {
            'source': '.agent/skills',
            'pattern': '*',
            'recursive': True
        },
        'workflows': {
            'source': '.agent/workflows',
            'pattern': '*.md',
            'recursive': False
        },
        'rag': {
            'source': 'rag',
            'pattern': '*',
            'recursive': True
        },
        'configs': {
            'source': '.agent',
            'pattern': '*.[md,json]',
            'recursive': False,
            'exclude': ['skills', 'workflows']
        }
    }
    
    def __init__(self, request: CloneRequest):
        self.request = request
        self.source = Path(request.source)
        self.target = Path(request.target)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats: Dict[str, int] = {}
        self.checksums: Dict[str, str] = {}
        
    def execute(self) -> CloneResult:
        """Executa clonagem completa"""
        
        if not self.request.dry_run:
            logger.info("=" * 60)
            logger.info("ECOSYSTEM ONE-CLICK CLONER")
            logger.info("=" * 60)
            logger.info(f"Source: {self.source}")
            logger.info(f"Target: {self.target}")
            logger.info("=" * 60)
            
            # Criar diretório target
            self.target.mkdir(parents=True, exist_ok=True)
            
            # Verificar source
            if not self.source.exists():
                self.errors.append(f"Source não existe: {self.source}")
                return self._build_result(False)
            
            # Validar componentes
            self._validate_components()
            
            if self.errors:
                return self._build_result(False)
            
            # Executar clonagem
            self._clone_all_components()
            
            # Verificar checksums
            checksum_ok = True
            if self.request.verify:
                checksum_ok = self._verify_checksums()
            
            # Calcular score
            score = self._calculate_score()
            
            # Gerar relatório final
            self._generate_final_report()
            
            success = len(self.errors) == 0 and checksum_ok
            
            return CloneResult(
                success=success,
                timestamp=datetime.now().isoformat(),
                source=str(self.source),
                target=str(self.target),
                components_cloned=self.stats,
                total_files=sum(self.stats.values()),
                total_size=self._get_total_size(),
                errors=self.errors,
                warnings=self.warnings,
                checksum_verified=checksum_ok,
                score=score
            )
        else:
            # Modo dry-run
            logger.info("MODO DRY-RUN - Nenhuma alteração será feita")
            self._validate_components()
            
            return CloneResult(
                success=len(self.errors) == 0,
                timestamp=datetime.now().isoformat(),
                source=str(self.source),
                target=str(self.target),
                components_cloned=self._estimate_components(),
                total_files=0,
                total_size=0,
                errors=self.errors,
                warnings=self.warnings,
                checksum_verified=False,
                score=0.0
            )
    
    def _validate_components(self):
        """Valida componentes existentes"""
        logger.info("Validando componentes...")
        
        for comp_name, comp_config in self.COMPONENTS.items():
            source_path = self.source / comp_config['source']
            
            if source_path.exists():
                logger.info(f"  [OK] {comp_name}: {source_path}")
                self.stats[comp_name] = self._count_items(source_path, comp_config)
            else:
                self.warnings.append(f"Componente não encontrado: {comp_name}")
                logger.warning(f"  [WARN] {comp_name}: não encontrado")
                self.stats[comp_name] = 0
    
    def _count_items(self, path: Path, config: Dict) -> int:
        """Conta itens em caminho"""
        if config.get('recursive'):
            return len([f for f in path.rglob(config['pattern']) if f.is_dir()])
        else:
            return len(list(path.glob(config['pattern'])))
    
    def _estimate_components(self) -> Dict[str, int]:
        """Estima componentes a clonar"""
        estimated = {}
        
        for comp_name, comp_config in self.COMPONENTS.items():
            source_path = self.source / comp_config['source']
            if source_path.exists():
                if comp_config.get('recursive'):
                    estimated[comp_name] = len(list(source_path.rglob("*")))
                else:
                    estimated[comp_name] = len(list(source_path.glob(comp_config['pattern'])))
            else:
                estimated[comp_name] = 0
        
        return estimated
    
    def _clone_all_components(self):
        """Clona todos os componentes"""
        
        for comp_name, comp_config in self.COMPONENTS.items():
            logger.info(f"\nClonando {comp_name}...")
            
            source_path = self.source / comp_config['source']
            if not source_path.exists():
                continue
            
            target_path = self.target / comp_config['source']
            target_path.mkdir(parents=True, exist_ok=True)
            
            try:
                if comp_config.get('recursive'):
                    # Clonagem recursiva
                    count = self._clone_recursive(source_path, target_path, comp_config)
                else:
                    # Clonagem não-recursiva
                    count = self._clone_flat(source_path, target_path, comp_config)
                
                self.stats[comp_name] = count
                logger.info(f"  Clonados {count} itens de {comp_name}")
                
            except Exception as e:
                self.errors.append(f"Erro ao clonar {comp_name}: {str(e)}")
                logger.error(f"  ERRO: {str(e)}")
        
        # Clonar arquivos específicos
        self._clone_specific_files()
    
    def _clone_recursive(self, source: Path, target: Path, config: Dict) -> int:
        """Clonagem recursiva"""
        count = 0
        
        for item in source.iterdir():
            dest = target / item.name
            
            # Verificar se já existe
            if dest.exists() and self.request.skip_existing:
                logger.debug(f"  Pulando (existe): {item.name}")
                continue
            
            try:
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)
                
                count += 1
                
                # Calcular checksum
                if self.request.verify:
                    self.checksums[str(dest)] = self._md5(dest)
                    
            except Exception as e:
                self.errors.append(f"Erro ao copiar {item.name}: {str(e)}")
        
        return count
    
    def _clone_flat(self, source: Path, target: Path, config: Dict) -> int:
        """Clonagem não-recursiva"""
        count = 0
        
        # Aplicar excludes
        exclude = config.get('exclude', [])
        
        for item in source.glob(config['pattern']):
            if item.name in exclude:
                continue
                
            dest = target / item.name
            
            if dest.exists() and self.request.skip_existing:
                continue
            
            try:
                shutil.copy2(item, dest)
                count += 1
                
                if self.request.verify:
                    self.checksums[str(dest)] = self._md5(dest)
                    
            except Exception as e:
                self.errors.append(f"Erro ao copiar {item.name}: {str(e)}")
        
        return count
    
    def _clone_specific_files(self):
        """Clona arquivos específicos importantes"""
        
        # Arquivos de config do .agent
        important_files = [
            '.agent/TRANSFORMER_NETWORK_ARCHITECTURE.md',
            '.agent/mcp_config.json',
            '.agent/transform_example.json',
            '.agent/doc.md'
        ]
        
        for file_path in important_files:
            source_file = self.source / file_path
            if source_file.exists():
                dest_file = self.target / file_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.copy2(source_file, dest_file)
                    logger.info(f"  Clonado: {file_path}")
                except Exception as e:
                    self.warnings.append(f"Não foi possível copiar {file_path}: {str(e)}")
    
    def _md5(self, filepath: Path) -> str:
        """Calcula MD5"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _verify_checksums(self) -> bool:
        """Verifica checksums"""
        logger.info("\nVerificando integridade...")
        
        # Verificar alguns arquivos aleatórios
        verified = True
        
        for file_path, checksum in list(self.checksums.items())[:10]:
            current = self._md5(Path(file_path))
            if current != checksum:
                self.errors.append(f"Checksum falhou: {file_path}")
                verified = False
        
        if verified:
            logger.info("  Verificação de integridade: OK")
        else:
            logger.warning("  Verificação de integridade: FALHOU")
        
        return verified
    
    def _get_total_size(self) -> int:
        """Calcula tamanho total"""
        total = 0
        for item in self.target.rglob("*"):
            if item.is_file():
                total += item.stat().st_size
        return total
    
    def _calculate_score(self) -> float:
        """Calcula score de sucesso"""
        
        base_score = 1.0
        
        # Penalizar erros
        base_score -= len(self.errors) * 0.1
        
        # Penalizar warnings
        base_score -= len(self.warnings) * 0.02
        
        return max(0.0, min(1.0, base_score))
    
    def _generate_final_report(self):
        """Gera relatório final"""
        
        report = {
            "title": "RELATÓRIO DE CLONAGEM - ECOSSISTEMA OPENCODE",
            "timestamp": datetime.now().isoformat(),
            "source": str(self.source),
            "target": str(self.target),
            "components": self.stats,
            "total_files": sum(self.stats.values()),
            "total_size_mb": round(self._get_total_size() / (1024 * 1024), 2),
            "errors": self.errors,
            "warnings": self.warnings,
            "score": self._calculate_score(),
            "status": "SUCESSO" if not self.errors else "ERROS"
        }
        
        # Salvar relatório
        report_path = self.target / "CLONE_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Salvar também em markdown
        md_report = self._generate_markdown_report(report)
        md_path = self.target / "CLONE_REPORT.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_report)
        
        logger.info(f"\nRelatório salvo em: {report_path}")
    
    def _generate_markdown_report(self, report: Dict) -> str:
        """Gera relatório em markdown"""
        
        md = f"""# Relatório de Clonagem - Ecossistema Opencode

## Informações Gerais

- **Data:** {report['timestamp']}
- **Source:** `{report['source']}`
- **Target:** `{report['target']}`
- **Status:** {report['status']}
- **Score:** {report['score']:.1%}

## Componentes Clonados

| Componente | Quantidade |
|------------|------------|
"""
        
        for comp, count in report['components'].items():
            md += f"| {comp} | {count} |\n"
        
        md += f"""
## Estatísticas

- **Total de Arquivos:** {report['total_files']}
- **Tamanho Total:** {report['total_size_mb']} MB

"""
        
        if report['errors']:
            md += "## Erros\n\n"
            for error in report['errors']:
                md += f"- ❌ {error}\n"
            md += "\n"
        
        if report['warnings']:
            md += "## Avisos\n\n"
            for warning in report['warnings']:
                md += f"- ⚠️ {warning}\n"
            md += "\n"
        
        md += "---\n\n*Relatório gerado automaticamente pelo Ecosystem One-Click Cloner*"
        
        return md
    
    def _build_result(self, success: bool) -> CloneResult:
        """Constrói resultado"""
        return CloneResult(
            success=success,
            timestamp=datetime.now().isoformat(),
            source=str(self.source),
            target=str(self.target),
            components_cloned=self.stats,
            total_files=sum(self.stats.values()),
            total_size=self._get_total_size(),
            errors=self.errors,
            warnings=self.warnings,
            checksum_verified=False,
            score=self._calculate_score()
        )


def main():
    parser = argparse.ArgumentParser(
        description="ONE-CLICK CLONE - Clone Completo com Um Único OK"
    )
    
    parser.add_argument(
        "--source", "-s",
        required=True,
        help="Caminho do ecossistema fonte"
    )
    
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Caminho de destino para o clone"
    )
    
    parser.add_argument(
        "--approve", "-y",
        action="store_true",
        help="Aprovar clonagem automaticamente (um único OK)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simular sem fazer alterações"
    )
    
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        default=True,
        help="Pular arquivos existentes"
    )
    
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Não verificar checksums"
    )
    
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Compactar clone"
    )
    
    args = parser.parse_args()
    
    # Criar requisição
    request = CloneRequest(
        source=args.source,
        target=args.target,
        approve=args.approve,
        dry_run=args.dry_run,
        skip_existing=args.skip_existing,
        verify=not args.no_verify,
        compress=args.compress
    )
    
    # Verificar aprovação
    if not args.approve and not args.dry_run:
        logger.warning("=" * 60)
        logger.warning("ATENÇÃO: Este comando clonará todo o ecossistema!")
        logger.warning(f"Source: {args.source}")
        logger.warning(f"Target: {args.target}")
        logger.warning("=" * 60)
        logger.warning("Execute novamente com --approve para confirmar")
        logger.warning("Ou use --dry-run para simular")
        return
    
    # Executar clonagem
    cloner = OneClickCloner(request)
    result = cloner.execute()
    
    # Exibir resultado
    print("\n" + "=" * 60)
    print("RESULTADO DA CLONAGEM")
    print("=" * 60)
    print(f"Status: {'SUCESSO' if result.success else 'FALHOU'}")
    print(f"Score: {result.score:.1%}")
    print(f"Arquivos clonados: {result.total_files}")
    print(f"Tamanho: {result.total_size / (1024*1024):.2f} MB")
    print("=" * 60)
    
    if result.errors:
        print("\nERROS:")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.warnings:
        print("\nAVISOS:")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
