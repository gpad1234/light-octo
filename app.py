from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from flask_session import Session
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Session configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configuration flag for OpenAI NLP tab
ENABLE_OPENAI_NLP = os.getenv('ENABLE_OPENAI_NLP', 'true').lower() == 'true'

# Initialize OpenAI client
openai_client = None
if ENABLE_OPENAI_NLP:
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        openai_client = OpenAI(api_key=api_key)

# Store nodes and edges in memory
nodes = {}
edges = []

# Initialize with sample data
def initialize_sample_data():
    """Load sample graph data."""
    sample_nodes = [
        {'id': 'user', 'label': 'User', 'type': 'entity', 'x': 100, 'y': 100},
        {'id': 'order', 'label': 'Order', 'type': 'entity', 'x': 300, 'y': 100},
        {'id': 'product', 'label': 'Product', 'type': 'entity', 'x': 500, 'y': 100},
        {'id': 'payment', 'label': 'Payment', 'type': 'entity', 'x': 300, 'y': 300},
        {'id': 'inventory', 'label': 'Inventory', 'type': 'entity', 'x': 500, 'y': 300},
    ]
    
    sample_edges = [
        {'source': 'user', 'target': 'order', 'relation': 'places'},
        {'source': 'order', 'target': 'product', 'relation': 'contains'},
        {'source': 'order', 'target': 'payment', 'relation': 'has_payment'},
        {'source': 'product', 'target': 'inventory', 'relation': 'tracked_in'},
    ]
    
    for node in sample_nodes:
        nodes[node['id']] = node
    
    for edge in sample_edges:
        edges.append({
            'id': f"{edge['source']}-{edge['target']}",
            'source': edge['source'],
            'target': edge['target'],
            'relation': edge['relation']
        })

# Demo credentials (in production, use a proper database)
VALID_USERS = {
    'user': {'password': 'user123', 'role': 'user'},
    'admin': {'password': 'admin123', 'role': 'admin'}
}

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to require admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify(error='Admin access required'), 403
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Home page route - redirect to login if not authenticated."""
    if 'user_id' in session:
        return redirect(url_for('nlp_screen'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication handler."""
    if request.method == 'POST':
        data = request.json if request.is_json else request.form
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            if request.is_json:
                return jsonify(error='Username and password required'), 400
            return render_template('login.html', error='Username and password required')
        
        if username in VALID_USERS and VALID_USERS[username]['password'] == password:
            session['user_id'] = username
            session['role'] = VALID_USERS[username]['role']
            session['username'] = username
            
            if request.is_json:
                return jsonify(success=True, redirect_url=url_for('nlp_screen'))
            return redirect(url_for('nlp_screen'))
        
        error_msg = 'Invalid username or password'
        if request.is_json:
            return jsonify(error=error_msg), 401
        return render_template('login.html', error=error_msg)
    
    if 'user_id' in session:
        return redirect(url_for('nlp_screen'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify(status='healthy'), 200


@app.route('/nlp')
@login_required
def nlp_screen():
    """NLP screen for creating domain nodes and edges."""
    is_admin = session.get('role') == 'admin'
    return render_template('nlp.html', enable_openai_nlp=ENABLE_OPENAI_NLP, is_admin=is_admin, username=session.get('username'))


@app.route('/api/nodes', methods=['GET', 'POST'])
def manage_nodes():
    """Get all nodes or create a new node."""
    if request.method == 'POST':
        data = request.json
        node_id = data.get('id')
        node_label = data.get('label')
        node_type = data.get('type', 'default')
        
        if not node_id or not node_label:
            return jsonify(error='Node ID and label are required'), 400
        
        if node_id in nodes:
            return jsonify(error='Node with this ID already exists'), 409
        
        nodes[node_id] = {
            'id': node_id,
            'label': node_label,
            'type': node_type,
            'x': data.get('x', 0),
            'y': data.get('y', 0)
        }
        return jsonify(node=nodes[node_id]), 201
    
    return jsonify(nodes=list(nodes.values())), 200


@app.route('/api/nodes/<node_id>', methods=['GET', 'DELETE', 'PUT'])
def manage_node(node_id):
    """Get, update, or delete a specific node."""
    if request.method == 'GET':
        if node_id not in nodes:
            return jsonify(error='Node not found'), 404
        return jsonify(node=nodes[node_id]), 200
    
    elif request.method == 'PUT':
        if node_id not in nodes:
            return jsonify(error='Node not found'), 404
        data = request.json
        nodes[node_id].update(data)
        return jsonify(node=nodes[node_id]), 200
    
    elif request.method == 'DELETE':
        if node_id not in nodes:
            return jsonify(error='Node not found'), 404
        del nodes[node_id]
        # Remove edges connected to this node
        edges[:] = [e for e in edges if e['source'] != node_id and e['target'] != node_id]
        return jsonify(message='Node deleted'), 200


@app.route('/api/edges', methods=['GET', 'POST'])
def manage_edges():
    """Get all edges or create a new edge."""
    if request.method == 'POST':
        data = request.json
        source = data.get('source')
        target = data.get('target')
        relation = data.get('relation', 'related_to')
        
        if not source or not target:
            return jsonify(error='Source and target are required'), 400
        
        if source not in nodes or target not in nodes:
            return jsonify(error='Source or target node not found'), 404
        
        # Check if edge already exists
        for edge in edges:
            if edge['source'] == source and edge['target'] == target:
                return jsonify(error='Edge already exists'), 409
        
        edge = {
            'id': f"{source}-{target}",
            'source': source,
            'target': target,
            'relation': relation
        }
        edges.append(edge)
        return jsonify(edge=edge), 201
    
    return jsonify(edges=edges), 200


@app.route('/api/edges/<edge_id>', methods=['GET', 'DELETE'])
def manage_edge(edge_id):
    """Get or delete a specific edge."""
    if request.method == 'GET':
        for edge in edges:
            if edge['id'] == edge_id:
                return jsonify(edge=edge), 200
        return jsonify(error='Edge not found'), 404
    
    elif request.method == 'DELETE':
        for i, edge in enumerate(edges):
            if edge['id'] == edge_id:
                edges.pop(i)
                return jsonify(message='Edge deleted'), 200
        return jsonify(error='Edge not found'), 404


@app.route('/api/graph', methods=['GET'])
def get_graph():
    """Get the entire graph (nodes and edges)."""
    return jsonify(
        nodes=list(nodes.values()),
        edges=edges
    ), 200


@app.route('/api/graph/clear', methods=['DELETE'])
def clear_graph():
    """Clear all nodes and edges."""
    nodes.clear()
    edges[:] = []
    return jsonify(message='Graph cleared'), 200


@app.route('/api/graph/sample', methods=['POST'])
def load_sample_data():
    """Load sample graph data."""
    nodes.clear()
    edges[:] = []
    initialize_sample_data()
    return jsonify(
        message='Sample data loaded',
        nodes=list(nodes.values()),
        edges=edges
    ), 200


@app.route('/api/graph/import', methods=['POST'])
def import_graph():
    """Import a graph from JSON."""
    try:
        data = request.json
        
        if 'nodes' not in data or 'edges' not in data:
            return jsonify(error='Invalid graph format: must contain nodes and edges'), 400
        
        imported_nodes = data.get('nodes', [])
        imported_edges = data.get('edges', [])
        
        # Validate nodes
        for node in imported_nodes:
            if not isinstance(node, dict) or 'id' not in node or 'label' not in node:
                return jsonify(error='Invalid node format: each node must have id and label'), 400
        
        # Validate edges
        for edge in imported_edges:
            if not isinstance(edge, dict) or 'source' not in edge or 'target' not in edge:
                return jsonify(error='Invalid edge format: each edge must have source and target'), 400
        
        # Clear existing data
        nodes.clear()
        edges[:] = []
        
        # Import nodes
        for node in imported_nodes:
            node_id = node.get('id')
            nodes[node_id] = {
                'id': node_id,
                'label': node.get('label', ''),
                'type': node.get('type', 'default'),
                'x': node.get('x', 0),
                'y': node.get('y', 0)
            }
        
        # Import edges
        for edge in imported_edges:
            source = edge.get('source')
            target = edge.get('target')
            
            # Validate that nodes exist
            if source not in nodes or target not in nodes:
                return jsonify(error=f'Edge references non-existent node: {source} or {target}'), 400
            
            # Check for duplicate
            if any(e['source'] == source and e['target'] == target for e in edges):
                continue  # Skip duplicate edges
            
            edges.append({
                'id': f"{source}-{target}",
                'source': source,
                'target': target,
                'relation': edge.get('relation', 'related_to')
            })
        
        return jsonify(
            message='Graph imported successfully',
            nodes_count=len(nodes),
            edges_count=len(edges)
        ), 200
    
    except Exception as e:
        return jsonify(error=f'Import error: {str(e)}'), 400


@app.route('/api/schemas/sql', methods=['GET'])
def generate_sql_schema():
    """Generate SQL schema from domain model."""
    try:
        sql_statements = []
        
        # Create tables for each node type
        node_types = set(node['type'] for node in nodes.values())
        
        for node_type in node_types:
            type_nodes = [n for n in nodes.values() if n['type'] == node_type]
            
            table_name = node_type.lower() + 's'
            sql = f"""-- Table for {node_type} entities
CREATE TABLE {table_name} (
    id VARCHAR(255) PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
            sql_statements.append(sql)
        
        # Create junction tables for relationships
        for edge in edges:
            junction_table = f"{edge['source']}_to_{edge['target']}"
            sql = f"""-- Relationship table for {edge['relation']}
CREATE TABLE {junction_table} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_id VARCHAR(255) NOT NULL,
    target_id VARCHAR(255) NOT NULL,
    relation VARCHAR(255) NOT NULL DEFAULT '{edge['relation']}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES {edge['source']}(id),
    FOREIGN KEY (target_id) REFERENCES {edge['target']}(id),
    UNIQUE KEY unique_relation (source_id, target_id, relation)
);
"""
            sql_statements.append(sql)
        
        sql_schema = '\n'.join(sql_statements)
        
        return jsonify(
            schema_type='SQL',
            database='MySQL/PostgreSQL',
            schema=sql_schema,
            table_count=len(node_types),
            relationship_count=len(edges)
        ), 200
    except Exception as e:
        return jsonify(error=f'Schema generation error: {str(e)}'), 400


@app.route('/api/schemas/mongodb', methods=['GET'])
def generate_mongodb_schema():
    """Generate MongoDB schema from domain model."""
    try:
        import json
        
        collections = {}
        
        # Create collection schema for each node type
        for node in nodes.values():
            node_type = node['type'].lower()
            
            if node_type not in collections:
                collections[node_type] = {
                    "collectionName": node_type + "s",
                    "validator": {
                        "$jsonSchema": {
                            "bsonType": "object",
                            "required": ["_id", "label", "type"],
                            "properties": {
                                "_id": {
                                    "bsonType": "string",
                                    "description": "Unique identifier"
                                },
                                "label": {
                                    "bsonType": "string",
                                    "description": "Display name"
                                },
                                "type": {
                                    "bsonType": "string",
                                    "enum": [node_type],
                                    "description": "Entity type"
                                },
                                "relationships": {
                                    "bsonType": "array",
                                    "description": "Array of related entities",
                                    "items": {
                                        "bsonType": "object",
                                        "properties": {
                                            "targetId": {"bsonType": "string"},
                                            "relation": {"bsonType": "string"},
                                            "metadata": {"bsonType": "object"}
                                        }
                                    }
                                },
                                "metadata": {
                                    "bsonType": "object",
                                    "description": "Additional properties"
                                },
                                "createdAt": {
                                    "bsonType": "date"
                                },
                                "updatedAt": {
                                    "bsonType": "date"
                                }
                            }
                        }
                    }
                }
        
        # Create relationship metadata
        relationship_types = set(edge['relation'] for edge in edges)
        
        mongodb_schema = {
            "database": "knowledge_graph",
            "collections": collections,
            "relationshipTypes": list(relationship_types),
            "indexSuggestions": {
                "common": [
                    {"key": {"label": 1}},
                    {"key": {"type": 1}},
                    {"key": {"createdAt": -1}}
                ],
                "forSearch": [
                    {"key": {"label": "text"}},
                    {"key": {"relationships.relation": 1}}
                ]
            }
        }
        
        return jsonify(
            schema_type='MongoDB',
            schema=mongodb_schema,
            collection_count=len(collections),
            relationship_count=len(relationship_types)
        ), 200
    except Exception as e:
        return jsonify(error=f'Schema generation error: {str(e)}'), 400


@app.route('/api/report/graph-stats', methods=['GET'])
def get_graph_statistics():
    """Get statistics about the current graph."""
    try:
        node_types = {}
        for node in nodes.values():
            node_type = node['type']
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        relationship_types = {}
        for edge in edges:
            rel = edge['relation']
            relationship_types[rel] = relationship_types.get(rel, 0) + 1
        
        # Calculate graph metrics
        node_degrees = {}
        for node_id in nodes.keys():
            in_degree = sum(1 for e in edges if e['target'] == node_id)
            out_degree = sum(1 for e in edges if e['source'] == node_id)
            node_degrees[node_id] = {
                'in_degree': in_degree,
                'out_degree': out_degree,
                'total_degree': in_degree + out_degree
            }
        
        stats = {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'node_types': node_types,
            'relationship_types': relationship_types,
            'node_degrees': node_degrees,
            'density': len(edges) / (len(nodes) * (len(nodes) - 1)) if len(nodes) > 1 else 0,
            'average_degree': sum(d['total_degree'] for d in node_degrees.values()) / len(nodes) if nodes else 0
        }
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify(error=f'Stats error: {str(e)}'), 400


@app.route('/api/mongodb/databases', methods=['GET'])
def list_mongodb_databases():
    """List available MongoDB sample databases."""
    try:
        from mongodb_importer import list_available_databases, get_database_info
        
        available_dbs = list_available_databases()
        db_infos = []
        
        for db_name in available_dbs:
            info = get_database_info(db_name)
            db_infos.append(info)
        
        return jsonify(databases=db_infos), 200
    except Exception as e:
        return jsonify(error=f'Error listing databases: {str(e)}'), 400


@app.route('/api/mongodb/import/<database_name>', methods=['POST'])
def import_mongodb_sample(database_name):
    """Import a MongoDB sample database as a knowledge graph."""
    try:
        from mongodb_importer import get_sample_graph
        
        graph_data = get_sample_graph(database_name)
        
        if graph_data is None:
            return jsonify(error=f'Database {database_name} not found'), 404
        
        # Clear existing data
        nodes.clear()
        edges[:] = []
        
        # Import nodes
        for node in graph_data['nodes']:
            node_id = node['id']
            nodes[node_id] = {
                'id': node_id,
                'label': node['label'],
                'type': node['type'],
                'x': 0,
                'y': 0,
                'source': database_name
            }
        
        # Import edges
        for edge in graph_data['edges']:
            edges.append({
                'id': f"{edge['source']}-{edge['target']}",
                'source': edge['source'],
                'target': edge['target'],
                'relation': edge['relation']
            })
        
        return jsonify(
            message=f'MongoDB sample database "{database_name}" imported successfully',
            nodes_count=len(nodes),
            edges_count=len(edges),
            source='mongodb_sample'
        ), 200
    
    except Exception as e:
        return jsonify(error=f'Import error: {str(e)}'), 400


@app.route('/api/openai/query', methods=['POST'])
@admin_required
def openai_query():
    """Query OpenAI for general questions - Admin only."""
    if not ENABLE_OPENAI_NLP or not openai_client:
        return jsonify(error='OpenAI NLP feature is disabled'), 403
    
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify(error='Question cannot be empty'), 400
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'user',
                    'content': question
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        answer = response.choices[0].message.content
        
        return jsonify(
            question=question,
            answer=answer,
            model=response.model,
            usage={
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
        ), 200
    
    except Exception as e:
        return jsonify(error=f'OpenAI query error: {str(e)}'), 500


if __name__ == '__main__':
    # Initialize sample data on startup
    initialize_sample_data()
    
    # Only run development server if DEBUG is True
    # In production, use gunicorn instead
    debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
