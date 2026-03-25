"""
GraphRAG - Implementação MASWOS Academic
Usa grafos de conhecimento com Neo4j para organizar entidades e relações.
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class EntityType(Enum):
    """Tipos de entidades em grafos de conhecimento."""
    PERSON = "PESSOA"
    ORGANIZATION = "ORGANIZACAO"
    CONCEPT = "CONCEITO"
    LOCATION = "LOCAL"
    DOCUMENT = "DOCUMENTO"
    CITATION = "CITACAO"
    INSTITUTION = "INSTITUICAO"


class RelationType(Enum):
    """Tipos de relações em grafos de conhecimento."""
    CITES = "CITA"
    AUTHORED_BY = "AUTOR_DE"
    AFFILIATED_WITH = "AFILIADO_A"
    RELATED_TO = "RELACIONADO_A"
    PUBLISHED_IN = "PUBLICADO_EM"
    DEFINES = "DEFINE"


@dataclass
class Entity:
    """Representa uma entidade no grafo."""
    id: str
    name: str
    type: EntityType
    properties: Dict[str, Any] = field(default_factory=dict)
    description: Optional[str] = None


@dataclass
class Relation:
    """Representa uma relação entre entidades."""
    source_id: str
    target_id: str
    type: RelationType
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0


@dataclass
class KnowledgeGraph:
    """Container para o grafo de conhecimento."""
    entities: Dict[str, Entity] = field(default_factory=dict)
    relations: List[Relation] = field(default_factory=list)
    
    def add_entity(self, entity: Entity):
        """Adiciona entidade ao grafo."""
        self.entities[entity.id] = entity
    
    def add_relation(self, relation: Relation):
        """Adiciona relação ao grafo."""
        self.relations.append(relation)
    
    def get_neighbors(self, entity_id: str) -> List[Tuple[Entity, Relation]]:
        """Retorna vizinhos de uma entidade."""
        neighbors = []
        
        for rel in self.relations:
            if rel.source_id == entity_id:
                if rel.target_id in self.entities:
                    neighbors.append((self.entities[rel.target_id], rel))
            elif rel.target_id == entity_id:
                if rel.source_id in self.entities:
                    neighbors.append((self.entities[rel.source_id], rel))
        
        return neighbors


class Neo4jConnector:
    """
    Conector para Neo4j.
    
    Gerencia conexão e queries Cypher.
    """
    
    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        username: str = "neo4j",
        password: str = "password",
        database: str = "neo4j"
    ):
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        
        self._driver = None
        self._init_driver()
    
    def _init_driver(self):
        """Initialize Neo4j driver."""
        try:
            from neo4j import GraphDatabase
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
        except ImportError:
            print("Neo4j driver not installed. GraphRAG will use in-memory fallback.")
            self._driver = None
    
    def close(self):
        """Close connection."""
        if self._driver:
            self._driver.close()
    
    def execute_query(self, query: str, parameters: Optional[Dict] = None):
        """Executa query Cypher."""
        if not self._driver:
            return []
        
        with self._driver.session(database=self.database) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def create_entity(self, entity: Entity):
        """Cria entidade no Neo4j."""
        query = """
        MERGE (e:Entity {id: $id})
        SET e.name = $name,
            e.type = $type,
            e.description = $description
        """
        properties = {
            'id': entity.id,
            'name': entity.name,
            'type': entity.type.value,
            'description': entity.description or ''
        }
        properties.update(entity.properties)
        
        self.execute_query(query, properties)
    
    def create_relation(self, relation: Relation):
        """Cria relação no Neo4j."""
        query = """
        MATCH (a:Entity {id: $source_id})
        MATCH (b:Entity {id: $target_id})
        MERGE (a)-[r:RELATION {type: $type}]->(b)
        SET r.weight = $weight
        """
        self.execute_query(query, {
            'source_id': relation.source_id,
            'target_id': relation.target_id,
            'type': relation.type.value,
            'weight': relation.weight
        })
    
    def find_entities(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca entidades porsimilaridade."""
        cypher = """
        MATCH (e:Entity)
        WHERE e.name CONTAINS $query OR e.description CONTAINS $query
        RETURN e
        LIMIT $limit
        """
        return self.execute_query(cypher, {'query': query, 'limit': limit})
    
    def get_communities(self) -> List[Dict]:
        """Retorna comunidades detectadas."""
        query = """
        MATCH (e:Entity)
        WHERE e.communityId IS NOT NULL
        RETURN e.communityId as community, collect(e) as entities
        """
        return self.execute_query(query)
    
    def get_community_summary(self, community_id: int) -> Optional[str]:
        """Retorna resumo de uma comunidade."""
        query = """
        MATCH (c:Community {id: $id})
        RETURN c.summary as summary
        """
        results = self.execute_query(query, {'id': community_id})
        return results[0].get('summary') if results else None


class EntityExtractor:
    """
    Extrator de entidades e relações de texto.
    """
    
    def __init__(
        self,
        llm: Any = None,
        entity_types: Optional[List[EntityType]] = None,
        relation_types: Optional[List[RelationType]] = None
    ):
        self.llm = llm
        self.entity_types = entity_types or list(EntityType)
        self.relation_types = relation_types or list(RelationType)
    
    def extract_from_text(
        self,
        text: str,
        schema: Optional[Dict] = None
    ) -> KnowledgeGraph:
        """
        Extrai entidades e relações de texto.
        
        Args:
            text: Texto fonte
            schema: Esquema de tipos permitidos
            
        Returns:
            KnowledgeGraph com entidades e relações extraídas
        """
        if not self.llm:
            return self._rule_based_extraction(text)
        
        entity_types_str = ', '.join([e.value for e in self.entity_types])
        relation_types_str = ', '.join([r.value for r in self.relation_types])
        
        prompt = f"""Extraia entidades e relações do texto abaixo.

Texto:
{text[:2000]}

Tipos de entidade permitidos: {entity_types_str}
Tipos de relação permitidos: {relation_types_str}

Retorne JSON:
{{
    "entities": [
        {{"id": "unique_id", "name": "nome", "type": "TIPO", "description": "desc"}}
    ],
    "relations": [
        {{"source": "id_origem", "target": "id_destino", "type": "TIPO_RELACAO"}}
    ]
}}

JSON:"""
        
        try:
            response = self.llm.generate(prompt)
            data = json.loads(response.text)
            
            kg = KnowledgeGraph()
            
            for ent_data in data.get('entities', []):
                entity = Entity(
                    id=ent_data['id'],
                    name=ent_data['name'],
                    type=EntityType(ent_data['type']),
                    description=ent_data.get('description')
                )
                kg.add_entity(entity)
            
            for rel_data in data.get('relations', []):
                relation = Relation(
                    source_id=rel_data['source'],
                    target_id=rel_data['target'],
                    type=RelationType(rel_data['type'])
                )
                kg.add_relation(relation)
            
            return kg
            
        except Exception as e:
            print(f"LLM extraction failed: {e}")
            return self._rule_based_extraction(text)
    
    def _rule_based_extraction(self, text: str) -> KnowledgeGraph:
        """Extração baseada em regras (fallback)."""
        import re
        
        kg = KnowledgeGraph()
        
        citation_pattern = r'\[(\d+)\]'
        citations = re.findall(citation_pattern, text)
        
        for i, cite in enumerate(set(citations)):
            entity = Entity(
                id=f"cite_{cite}",
                name=f"Referência {cite}",
                type=EntityType.CITATION,
                description=f"Citação [{cite}]"
            )
            kg.add_entity(entity)
        
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)
        
        for year in set(years):
            entity = Entity(
                id=f"year_{year}",
                name=year,
                type=EntityType.CONCEPT,
                description=f"Ano {year}"
            )
            kg.add_entity(entity)
        
        return kg


class GraphRAG:
    """
    Implementação do GraphRAG para MASWOS Academic.
    
    Usa grafos de conhecimento para recuperação de informações
    e geração de respostas com base em relações estruturais.
    """
    
    def __init__(
        self,
        neo4j_connector: Optional[Neo4jConnector] = None,
        vector_store: Any = None,
        entity_extractor: Optional[EntityExtractor] = None,
        llm: Any = None,
        **kwargs
    ):
        self.neo4j = neo4j_connector
        self.vector_store = vector_store
        self.entity_extractor = entity_extractor or EntityExtractor(llm)
        
        self._kg = KnowledgeGraph()
        
        self._encoder = None
        self._augmenter = None
        self._generator = None
    
    def _init_components(self):
        """Initialize remaining components."""
        if self._encoder is None:
            from ..base.encoder import Encoder
            self._encoder = Encoder()
        
        if self._augmenter is None:
            from ..base.augmenter import Augmenter
            self._augmenter = Augmenter()
        
        if self._generator is None:
            from ..base.generator import Generator, AcademicGenerator
            self._generator = AcademicGenerator()
    
    def index_document(
        self,
        document_id: str,
        text: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Indexa documento extraindo entidades e relações.
        
        Args:
            document_id: ID único do documento
            text: Conteúdo do documento
            metadata: Metadados do documento
            
        Returns:
            Estatísticas da indexação
        """
        kg = self.entity_extractor.extract_from_text(text)
        
        if self.neo4j:
            for entity in kg.entities.values():
                entity.properties['document_id'] = document_id
                self.neo4j.create_entity(entity)
            
            for relation in kg.relations:
                self.neo4j.create_relation(relation)
        
        self._kg = kg
        
        return {
            'document_id': document_id,
            'entities_extracted': len(kg.entities),
            'relations_extracted': len(kg.relations)
        }
    
    def query(
        self,
        query: str,
        retrieval_mode: str = "hybrid",
        top_k: int = 5,
        include_graph_context: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query no GraphRAG.
        
        Args:
            query: Query do usuário
            retrieval_mode: 'vector', 'graph', ou 'hybrid'
            top_k: Número de resultados
            include_graph_context: Se inclui contexto do grafo
            
        Returns:
            Resposta com contexto do grafo
        """
        self._init_components()
        
        query_embedding = self._encoder.encode(query)
        
        if retrieval_mode == "vector":
            return self._vector_search(query, query_embedding, top_k, **kwargs)
        elif retrieval_mode == "graph":
            return self._graph_search(query, top_k, **kwargs)
        else:
            return self._hybrid_search(query, query_embedding, top_k, include_graph_context, **kwargs)
    
    def _vector_search(
        self,
        query: str,
        query_embedding: Any,
        top_k: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Busca vetorial pura."""
        if not self.vector_store:
            return {'answer': 'Vector store not configured', 'error': True}
        
        results = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            k=top_k
        )
        
        return {
            'answer': 'Vector search results',
            'mode': 'vector',
            'results': results
        }
    
    def _graph_search(
        self,
        query: str,
        top_k: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Busca puramente em grafo."""
        if not self.neo4j:
            return {'answer': 'Neo4j not configured', 'error': True}
        
        entities = self.neo4j.find_entities(query, limit=top_k)
        
        context_parts = []
        
        for ent_record in entities:
            entity = ent_record.get('e', {})
            entity_id = entity.get('id')
            
            if entity_id:
                neighbors = self._kg.get_neighbors(entity_id)
                
                context_parts.append(f"Entidade: {entity.get('name')}")
                
                for neighbor, relation in neighbors[:3]:
                    context_parts.append(
                        f"  - {relation.type.value} -> {neighbor.name}"
                    )
        
        context = "\n".join(context_parts) if context_parts else "Nenhuma entidade encontrada."
        
        prompt = f"""Com base no seguinte contexto do grafo de conhecimento:

{context}

Responda à pergunta: {query}

Resposta:"""
        
        result = self._generator.generate(prompt)
        
        return {
            'answer': result.text,
            'mode': 'graph',
            'entities_found': len(entities),
            'graph_context': context_parts
        }
    
    def _hybrid_search(
        self,
        query: str,
        query_embedding: Any,
        top_k: int,
        include_graph_context: bool,
        **kwargs
    ) -> Dict[str, Any]:
        """Busca híbrida vetorial + grafo."""
        vector_results = []
        graph_context = []
        
        if self.vector_store:
            vector_results = self.vector_store.similarity_search(
                query_embedding=query_embedding,
                k=top_k
            )
        
        if include_graph_context and self.neo4j:
            entities = self.neo4j.find_entities(query, limit=top_k)
            
            for ent_record in entities:
                entity = ent_record.get('e', {})
                graph_context.append({
                    'name': entity.get('name'),
                    'type': entity.get('type'),
                    'description': entity.get('description')
                })
        
        combined_context = []
        
        for r in vector_results:
            combined_context.append({
                'source': 'vector',
                'text': r.get('text', '')[:300],
                'score': r.get('score', 0)
            })
        
        for e in graph_context:
            combined_context.append({
                'source': 'graph',
                'text': f"{e['name']}: {e.get('description', '')}",
                'type': e.get('type')
            })
        
        augmented = self._augmenter.augment(query, combined_context)
        
        result = self._generator.generate(augmented.augmented_prompt)
        
        return {
            'answer': result.text,
            'mode': 'hybrid',
            'vector_results': len(vector_results),
            'graph_entities': len(graph_context),
            'combined_context': combined_context[:top_k * 2]
        }
    
    def get_graph_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do grafo."""
        return {
            'total_entities': len(self._kg.entities),
            'total_relations': len(self._kg.relations),
            'entity_types': list(set([e.type.value for e in self._kg.entities.values()])),
            'neo4j_configured': self.neo4j is not None,
            'vector_store_configured': self.vector_store is not None
        }
