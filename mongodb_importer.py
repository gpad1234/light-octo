"""
MongoDB Sample Database Importer for Knowledge Graph

This module provides utilities to import MongoDB sample databases
into the knowledge graph structure.
"""

# Sample MongoDB databases that can be imported
SAMPLE_DATABASES = {
    'sample_mflix': {
        'collections': {
            'movies': {
                'node_type': 'concept',
                'id_field': '_id',
                'label_field': 'title',
                'sample_size': 5
            },
            'users': {
                'node_type': 'person',
                'id_field': '_id',
                'label_field': 'name',
                'sample_size': 5
            }
        },
        'relationships': [
            {
                'source_collection': 'users',
                'target_collection': 'movies',
                'relation': 'watched'
            }
        ]
    },
    'sample_airbnb': {
        'collections': {
            'listingsAndReviews': {
                'node_type': 'concept',
                'id_field': '_id',
                'label_field': 'name',
                'sample_size': 5
            }
        },
        'relationships': []
    },
    'sample_analytics': {
        'collections': {
            'customers': {
                'node_type': 'person',
                'id_field': '_id',
                'label_field': 'username',
                'sample_size': 5
            },
            'accounts': {
                'node_type': 'concept',
                'id_field': '_id',
                'label_field': 'account_title',
                'sample_size': 5
            }
        },
        'relationships': [
            {
                'source_collection': 'customers',
                'target_collection': 'accounts',
                'relation': 'owns'
            }
        ]
    },
    'sample_restaurants': {
        'collections': {
            'restaurants': {
                'node_type': 'concept',
                'id_field': '_id',
                'label_field': 'name',
                'sample_size': 10
            }
        },
        'relationships': []
    }
}


def get_sample_graph(database_name):
    """
    Generate a sample knowledge graph from MongoDB sample database structure.
    
    Args:
        database_name: Name of the MongoDB sample database
        
    Returns:
        dict: Graph structure with nodes and edges
    """
    if database_name not in SAMPLE_DATABASES:
        return None
    
    db_schema = SAMPLE_DATABASES[database_name]
    nodes = []
    edges = []
    
    # Generate nodes from collections
    for collection_name, collection_info in db_schema.get('collections', {}).items():
        node_type = collection_info['node_type']
        label_field = collection_info['label_field']
        sample_size = collection_info.get('sample_size', 3)
        
        # Create sample nodes for each collection
        for i in range(sample_size):
            node_id = f"{collection_name}_{i}"
            label = f"{collection_name.title()} {i+1}"
            nodes.append({
                'id': node_id,
                'label': label,
                'type': node_type
            })
    
    # Generate edges from relationships
    for rel in db_schema.get('relationships', []):
        source_collection = rel['source_collection']
        target_collection = rel['target_collection']
        relation = rel['relation']
        
        # Create a few sample edges
        for i in range(min(3, sample_size)):
            source_id = f"{source_collection}_{i}"
            target_id = f"{target_collection}_{i}"
            edges.append({
                'source': source_id,
                'target': target_id,
                'relation': relation
            })
    
    return {
        'nodes': nodes,
        'edges': edges,
        'database': database_name,
        'exportedAt': __import__('datetime').datetime.now().isoformat(),
        'version': '1.0'
    }


def list_available_databases():
    """Return list of available MongoDB sample databases."""
    return list(SAMPLE_DATABASES.keys())


def get_database_info(database_name):
    """Get detailed info about a MongoDB sample database."""
    if database_name not in SAMPLE_DATABASES:
        return None
    
    db_schema = SAMPLE_DATABASES[database_name]
    collections = list(db_schema.get('collections', {}).keys())
    relationships = db_schema.get('relationships', [])
    
    return {
        'name': database_name,
        'collections': collections,
        'collection_count': len(collections),
        'relationship_count': len(relationships),
        'relationships': relationships,
        'total_sample_nodes': sum(
            coll.get('sample_size', 3) 
            for coll in db_schema.get('collections', {}).values()
        ),
        'total_sample_edges': len(relationships) * 3  # Rough estimate
    }
