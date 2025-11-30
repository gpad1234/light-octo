# NLP Domain Graph Builder - Technical Specification

## Overview

The NLP Domain Graph Builder is a web-based application that enables users to create and visualize semantic knowledge graphs. It allows users to define domain entities as nodes and establish relationships between them as directed edges, facilitating the modeling of complex domain ontologies and knowledge networks.

## Architecture

### Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: Vis.js (graph visualization library)
- **Data Storage**: In-memory dictionaries and lists
- **API**: RESTful JSON API

### Project Structure

```
reactor/
├── app.py                    # Flask application & API endpoints
├── templates/
│   └── nlp.html             # Frontend UI & client-side logic
├── requirements.txt         # Python dependencies
├── test_app.py             # Unit tests
└── README.md               # Setup & usage guide
```

## Core Features

### 1. Node Management

**Description**: Create, read, update, and delete domain entities (nodes) in the knowledge graph.

**Capabilities**:
- **Create Nodes**: Users can add new nodes with:
  - Unique ID (identifier)
  - Label (display name)
  - Type classification (Person, Organization, Location, Concept, Event, Default)
  - Positional metadata (x, y coordinates)

- **View Nodes**: List all nodes with their types displayed
- **Delete Nodes**: Remove individual nodes (cascades edge deletion)
- **Update Nodes**: Modify node properties via PUT request

**API Endpoints**:
```
POST   /api/nodes           - Create new node
GET    /api/nodes           - Retrieve all nodes
GET    /api/nodes/<id>      - Retrieve specific node
PUT    /api/nodes/<id>      - Update node properties
DELETE /api/nodes/<id>      - Delete node (removes connected edges)
```

**Example Node**:
```json
{
  "id": "person_1",
  "label": "John Doe",
  "type": "person",
  "x": 100,
  "y": 200
}
```

### 2. Edge Management

**Description**: Create and manage semantic relationships between nodes.

**Capabilities**:
- **Create Edges**: Connect two nodes with a semantic relationship
  - Source node ID
  - Target node ID
  - Relationship label (e.g., "works_at", "manages", "located_in")
  - Directional (from source to target)

- **View Edges**: Retrieve all edges in the graph
- **Delete Edges**: Remove individual relationships
- **Prevent Duplicates**: Block duplicate edges between same node pairs

**API Endpoints**:
```
POST   /api/edges           - Create new edge
GET    /api/edges           - Retrieve all edges
GET    /api/edges/<id>      - Retrieve specific edge
DELETE /api/edges/<id>      - Delete edge
```

**Example Edge**:
```json
{
  "id": "person_1-org_1",
  "source": "person_1",
  "target": "org_1",
  "relation": "works_at"
}
```

### 3. Graph Operations

**Description**: Manage the entire graph as a single entity, including import/export capabilities.

**Capabilities**:
- **Export Graph**: Download the entire graph as a JSON file with metadata
  - Includes timestamp and version information
  - Automatically named with export timestamp
  - Contains all node and edge data

- **Import Graph**: Load a previously exported graph or externally created graph
  - Validates JSON structure before import
  - Confirms user wants to replace current graph
  - Validates all node/edge references
  - Skips duplicate edges automatically
  - Provides import summary (node/edge count)

- **Clear Graph**: Delete all nodes and edges (with confirmation)
- **Retrieve Graph**: Get complete graph state (all nodes and edges)

**API Endpoints**:
```
GET    /api/graph           - Retrieve entire graph
POST   /api/graph/import    - Import graph from JSON
DELETE /api/graph/clear     - Clear all nodes and edges
```

### 4. Interactive Visualization

**Description**: Real-time visual representation of the knowledge graph on an interactive canvas.

**Capabilities**:
- **Physics Simulation**: Auto-layout with force-directed graph algorithms
- **Color Coding**: Nodes colored by type for quick identification
- **Interactive Navigation**: 
  - Pan and zoom on canvas
  - Drag nodes to reposition
  - Hover tooltips showing node/edge details
- **Edge Visualization**:
  - Directed arrows showing relationship direction
  - Labeled edges with relationship names
  - Visual highlighting on interaction
- **Responsive Design**: Adapts to different screen sizes

**Color Scheme**:
| Type | Color | Hex |
|------|-------|-----|
| Person | Purple | #667eea |
| Organization | Deep Purple | #764ba2 |
| Location | Pink | #f093fb |
| Concept | Blue | #4facfe |
| Event | Green | #43e97b |
| Default | Gray | #888 |

### 7. User Interface

**Description**: Generate database schemas and statistical reports from domain models.

**Capabilities**:
- **SQL Schema Generation**:
  - Creates tables for each node type
  - Generates junction tables for relationships
  - Includes foreign key constraints
  - Auto-timestamps and indexing recommendations
  - MySQL/PostgreSQL compatible

- **MongoDB Schema Generation**:
  - Generates BSON validation schemas
  - Denormalized document structure
  - Relationship embedding recommendations
  - Index suggestions for performance
  - TTL and uniqueness constraints

- **Graph Statistics**:
  - Node/edge counts
  - Node type distribution
  - Relationship type distribution
  - Node degree analysis (in-degree, out-degree)
  - Graph density metrics
  - Average degree calculations

**API Endpoints**:
```
GET    /api/schemas/sql           - Generate SQL schema
GET    /api/schemas/mongodb       - Generate MongoDB schema
GET    /api/report/graph-stats    - Get graph statistics
```

### 6. MongoDB Sample Database Import

**Description**: Import MongoDB sample databases directly into the knowledge graph.

**Supported Databases**:
- `sample_mflix` - Movie database with users and movies
- `sample_airbnb` - Airbnb listings and reviews
- `sample_analytics` - Customer and account analytics data
- `sample_restaurants` - Restaurant information

**Capabilities**:
- **Database Listing**: View all available MongoDB sample databases
- **Metadata Preview**: See collection count, sample nodes, and relationships
- **One-Click Import**: Import selected database as knowledge graph
- **Automatic Node/Edge Generation**: Creates sample nodes and edges from schema
- **Collection Mapping**: Maps collections to node types (Person, Organization, Concept, etc.)
- **Relationship Inference**: Auto-generates edges based on collection relationships

**Import Process**:
1. Click "🍃 Import MongoDB" button
2. Modal shows available databases with metadata
3. Click database card to import
4. Confirmation dialog appears
5. Graph replaces with imported data
6. Visualization auto-updates

**API Endpoints**:
```
GET    /api/mongodb/databases          - List available databases
POST   /api/mongodb/import/<db_name>   - Import specific database
```

**Description**: Tab-based interface with multiple views.

**Layout**:
- **Left Sidebar** (320px wide):
  - Node/Edge creation forms
  - Nodes list with quick actions
  - Import/Export/Clear buttons

- **Main Content Area** (Flex):
  - Tab navigation (Graph, Reports & Schemas)
  - Graph tab: Vis.js canvas
  - Reports tab: Statistics and schema previews

**Tabs**:
1. **Graph Tab**:
   - Interactive visualization canvas
   - Real-time node/edge rendering
   - Physics-based auto-layout

2. **Reports & Schemas Tab**:
   - Statistics dashboard (node/edge counts)
   - SQL schema preview with copy button
   - MongoDB schema preview with copy button
   - Color-coded report cards

**Components**:
- **Node Creation Panel**:
  - Input fields for ID, Label
  - Dropdown selector for node type
  - "Add Node" button with validation
  - Success/error message feedback

- **Edge Creation Panel**:
  - Input fields for source ID, target ID, relationship name
  - "Connect Nodes" button with validation
  - Success/error message feedback

- **Nodes List**:
  - Scrollable list of all nodes
  - Quick-delete buttons for each node
  - Type badges for visual identification

- **Action Buttons**:
  - "📥 Export Graph" - Download graph as JSON file
  - "📤 Import Graph" - Load graph from JSON file
  - "🍃 Import MongoDB" - Load MongoDB sample database (opens modal)
  - "🗑️ Clear All" - Remove entire graph

- **MongoDB Import Modal**:
  - Lists all available MongoDB sample databases
  - Shows collection count, sample nodes, and edges for each
  - Click to select and import
  - Confirmation before replacing current graph

- **Reports Panel**:
  - Stats grid showing key metrics
  - SQL schema card with syntax highlighting
  - MongoDB schema card with JSON formatting
  - Copy buttons for easy integration

### 6. Data Validation

**Description**: Input validation and error handling.

**Validation Rules**:
- **Node Creation**:
  - ID and Label required (non-empty)
  - ID must be unique
  - Type must be from predefined list

- **Edge Creation**:
  - Source and Target IDs required
  - Both nodes must exist
  - Duplicate edges prevented
  - Default relationship is "related_to"

**Error Responses**:
- 400: Missing or invalid parameters
- 404: Resource not found
- 409: Conflict (duplicate ID/edge)

## API Reference

### Response Format

All endpoints return JSON with standard structure:

**Success Response**:
```json
{
  "node": { "id": "...", "label": "...", ... },
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

**Error Response**:
```json
{
  "error": "Description of error"
}
```

### Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Duplicate or conflict |

## Data Model

### Export/Import JSON Format

```json
{
  "nodes": [
    {
      "id": "person_1",
      "label": "John Doe",
      "type": "person",
      "x": 100,
      "y": 200
    }
  ],
  "edges": [
    {
      "id": "person_1-org_1",
      "source": "person_1",
      "target": "org_1",
      "relation": "works_at"
    }
  ],
  "exportedAt": "2025-11-24T12:34:56.789Z",
  "version": "1.0"
}
```

### Node Object

```typescript
{
  id: string              // Unique identifier
  label: string           // Display name
  type: string            // Classification (person|organization|location|concept|event|default)
  x: number              // X coordinate (optional)
  y: number              // Y coordinate (optional)
}
```

### Edge Object

```typescript
{
  id: string              // Auto-generated: "{source}-{target}"
  source: string          // Source node ID
  target: string          // Target node ID
  relation: string        // Relationship name (e.g., "works_at")
}
```

## Client-Side Features

### State Management

- **Nodes**: Vis.js DataSet for reactive updates
- **Edges**: Vis.js DataSet for reactive updates
- **Network**: Vis.js Network instance for rendering

### Event Handling

- Form submissions trigger API calls
- Async/await for network requests
- Auto-refresh UI on successful operations
- User feedback via toast messages (3-second display)

### Export Functionality

- Generates JSON file of current graph state
- Downloads as `graph_export.json`
- Can be imported into other tools or databases

## Testing

### Unit Tests (`test_app.py`)

- **test_home_page**: Verify root endpoint
- **test_health_check**: Verify health status endpoint
- **test_invalid_route**: Verify 404 handling
- **test_node_creation**: Verify node creation with valid data
- **test_edge_creation**: Verify edge creation with valid nodes
- **test_duplicate_prevention**: Verify duplicate detection

**Run tests**:
```bash
pytest -v
```

## Performance Considerations

- In-memory storage (suitable for graphs up to ~10,000 nodes)
- Physics simulation iterations configurable (default: 200)
- Lazy loading of edges on demand
- Client-side rendering for better responsiveness

## Security Considerations

- Input validation on all endpoints
- No SQL injection risk (no database)
- CORS not implemented (same-origin only)
- No authentication/authorization currently
- Consider adding in production environment

## Future Enhancement Opportunities

1. **Persistent Storage**: PostgreSQL/MongoDB integration
2. **Advanced Querying**: Graph traversal, path finding
3. **Import/Export Formats**: Support for RDF, GraphML, OWL
4. **Collaborative Features**: Real-time multi-user editing
5. **NLP Integration**: Auto-extraction of entities and relationships from text
6. **Advanced Visualization**: Multiple layout algorithms, clustering
7. **Analytics**: Graph metrics, centrality analysis, community detection
8. **Version Control**: Graph history and undo/redo functionality
9. **Search & Filter**: Find nodes/edges by properties
10. **Custom Styling**: User-defined colors, icons, and shapes

## Deployment

### Local Development

```bash
# Setup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run
python app.py
# Visit http://localhost:5000/nlp
```

### Production Deployment

- Use production WSGI server (Gunicorn, uWSGI)
- Implement persistent storage
- Add database migration tools
- Configure environment variables
- Enable CORS if needed
- Implement authentication/authorization
- Set up monitoring and logging

## Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/nlp` | NLP interface (HTML page) |
| POST | `/api/nodes` | Create node |
| GET | `/api/nodes` | List all nodes |
| GET | `/api/nodes/<id>` | Get specific node |
| PUT | `/api/nodes/<id>` | Update node |
| DELETE | `/api/nodes/<id>` | Delete node |
| POST | `/api/edges` | Create edge |
| GET | `/api/edges` | List all edges |
| GET | `/api/edges/<id>` | Get specific edge |
| DELETE | `/api/edges/<id>` | Delete edge |
| GET | `/api/graph` | Get entire graph |
| POST | `/api/graph/import` | Import graph from JSON |
| DELETE | `/api/graph/clear` | Clear all data |
| GET | `/api/schemas/sql` | Generate SQL schema |
| GET | `/api/schemas/mongodb` | Generate MongoDB schema |
| GET | `/api/report/graph-stats` | Get graph statistics |
| GET | `/api/mongodb/databases` | List MongoDB sample databases |
| POST | `/api/mongodb/import/<db_name>` | Import MongoDB database |

## Schema Generation Details

### SQL Schema Output

**Generated Elements**:
- Entity tables (one per node type)
- Junction tables for relationships
- Foreign key constraints
- Timestamps (created_at, updated_at)
- Unique constraints on relationships

**Example Output**:
```sql
CREATE TABLE persons (
    id VARCHAR(255) PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE person_to_organization (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_id VARCHAR(255) NOT NULL,
    target_id VARCHAR(255) NOT NULL,
    relation VARCHAR(255) NOT NULL DEFAULT 'works_at',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES persons(id),
    FOREIGN KEY (target_id) REFERENCES organizations(id),
    UNIQUE KEY unique_relation (source_id, target_id, relation)
);
```

### MongoDB Schema Output

**Generated Elements**:
- Collection schemas with BSON validation
- Document structure with type definitions
- Relationship arrays for embedding
- Index suggestions
- TTL recommendations

**Example Output**:
```json
{
  "database": "knowledge_graph",
  "collections": {
    "persons": {
      "collectionName": "persons",
      "validator": {
        "$jsonSchema": {
          "bsonType": "object",
          "required": ["_id", "label", "type"],
          "properties": {
            "_id": {"bsonType": "string"},
            "label": {"bsonType": "string"},
            "type": {"bsonType": "string"},
            "relationships": {
              "bsonType": "array",
              "items": {
                "properties": {
                  "targetId": {"bsonType": "string"},
                  "relation": {"bsonType": "string"},
                  "metadata": {"bsonType": "object"}
                }
              }
            },
            "createdAt": {"bsonType": "date"},
            "updatedAt": {"bsonType": "date"}
          }
        }
      }
    }
  },
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
```

### Graph Statistics Output

**Metrics Provided**:
- `total_nodes`: Count of all nodes
- `total_edges`: Count of all relationships
- `node_types`: Distribution by type
- `relationship_types`: Distribution of relationship types
- `node_degrees`: Individual node metrics
  - `in_degree`: Number of incoming edges
  - `out_degree`: Number of outgoing edges
  - `total_degree`: Sum of in and out degrees
- `density`: Graph density (0-1 scale)
- `average_degree`: Mean degree across all nodes

**Example Output**:
```json
{
  "total_nodes": 5,
  "total_edges": 4,
  "node_types": {
    "person": 2,
    "organization": 2,
    "location": 1
  },
  "relationship_types": {
    "works_at": 2,
    "located_in": 1,
    "manages": 1
  },
  "node_degrees": {
    "person_1": {"in_degree": 1, "out_degree": 2, "total_degree": 3},
    "org_1": {"in_degree": 2, "out_degree": 0, "total_degree": 2}
  },
  "density": 0.1,
  "average_degree": 1.6
}

## Import/Export Workflow

### Exporting a Graph

1. Click "📥 Export" button
2. Browser downloads `graph_export_[timestamp].json`
3. File contains all nodes, edges, and metadata

### Importing a Graph

1. Click "📤 Import" button
2. File picker opens
3. Select a `.json` file (must contain `nodes` and `edges` arrays)
4. Confirmation dialog shows node/edge count
5. Confirm to replace current graph
6. API validates structure and node/edge references
7. Success message shows number of imported items
8. Visualization updates automatically

### Validation Rules

**Import Validation**:
- JSON must contain `nodes` array
- JSON must contain `edges` array
- Each node must have `id` and `label` fields
- Each edge must have `source` and `target` fields
- Edge source/target must reference existing nodes
- Duplicate edges are skipped automatically
- Type defaults to "default" if not specified

## Visualization Framework: Vis.js

### Overview

The application uses **Vis.js**, a powerful JavaScript visualization library designed for network graphs and timelines. Vis.js provides real-time physics-based graph rendering with interactive controls, making it ideal for knowledge graph visualization.

### Why Vis.js?

| Feature | Benefit |
|---------|---------|
| Physics Engine | Auto-layout with force-directed simulation |
| Performance | Handles thousands of nodes/edges efficiently |
| Interactivity | Native pan, zoom, drag-and-drop support |
| Customization | Extensive styling and configuration options |
| Mobile-Friendly | Touch gestures and responsive design |
| Community | Active maintenance and extensive documentation |
| Lightweight | Minimal dependencies, ~300KB minified |

### Core Components

#### 1. DataSets

```javascript
let nodes = new vis.DataSet();
let edges = new vis.DataSet();
```

**DataSet Characteristics**:
- Reactive data structure from Vis.js
- Automatically triggers re-renders on data changes
- Supports add, remove, update, clear operations
- Maintains unique IDs for each item
- Efficient change tracking

**Node DataSet**:
```javascript
nodes.add({
  id: 'person_1',
  label: 'John Doe',
  color: '#667eea',
  title: 'Person entity',
  x: 100,
  y: 200
});
```

**Edge DataSet**:
```javascript
edges.add({
  id: 'person_1-org_1',
  from: 'person_1',
  to: 'org_1',
  label: 'works_at',
  title: 'Person works at Organization'
});
```

#### 2. Network Instance

```javascript
const data = { nodes, edges };
const options = { /* configuration */ };
const network = new vis.Network(container, data, options);
```

**Network Responsibilities**:
- Manages graph rendering
- Handles user interactions (click, drag, zoom, pan)
- Applies physics simulation
- Renders nodes and edges to canvas
- Maintains zoom/pan state

#### 3. Physics Simulation

```javascript
physics: {
  enabled: true,
  stabilization: {
    iterations: 200
  }
}
```

**Physics Engine Features**:
- **Force-Directed Layout**: Nodes repel each other, edges attract connected nodes
- **Stabilization**: Automatically arranges graph layout
- **Damping**: Gradually reduces motion for stable visualization
- **Convergence**: Detects when layout is stable

**Physics Algorithms**:
- Prevents node overlapping through repulsive forces
- Creates natural, organized layouts
- Iteratively improves over time
- Customizable for performance tuning

### Node Configuration

```javascript
nodes: {
  shape: 'dot',              // Node shape (dot, box, circle, etc.)
  scaling: {
    label: {
      enabled: true,
      min: 14,              // Minimum font size
      max: 30               // Maximum font size
    }
  },
  font: {
    size: 16,
    face: 'Tahoma'
  }
}
```

**Node Styling**:
- **Shape**: Dot shape for semantic entities
- **Color**: Dynamically assigned by node type
- **Label**: Scales with zoom level for readability
- **Title**: Hover tooltip with full information

**Color Mapping**:
```javascript
const colorMap = {
  person: '#667eea',           // Purple
  organization: '#764ba2',     // Deep Purple
  location: '#f093fb',         // Pink
  concept: '#4facfe',          // Blue
  event: '#43e97b',            // Green
  default: '#888'              // Gray
};
```

### Edge Configuration

```javascript
edges: {
  width: 2,                    // Edge thickness
  color: {
    color: '#ccc',             // Default color
    highlight: '#667eea'       // Hover color
  },
  font: {
    size: 12,
    align: 'middle'            // Label alignment
  },
  arrows: {
    to: {
      enabled: true,           // Show direction arrow
      scaleFactor: 0.5
    }
  }
}
```

**Edge Styling**:
- **Arrows**: Directional indicators showing relationship flow
- **Labels**: Relationship names displayed on edges
- **Color Transitions**: Visual feedback on hover/selection
- **Smooth Curves**: Natural-looking connections between nodes

### Interaction Configuration

```javascript
interaction: {
  navigationButtons: true,    // Show zoom/pan buttons
  keyboard: true             // Enable keyboard shortcuts
}
```

**User Interactions**:
| Action | Behavior |
|--------|----------|
| Scroll Wheel | Zoom in/out |
| Drag Background | Pan across graph |
| Drag Node | Move node (physics adjusts) |
| Click Node | Select and highlight |
| Hover Node | Show tooltip |
| Double-Click | Fit to view |
| Right-Click | Context menu (disabled) |
| Keyboard Arrows | Pan |
| Plus/Minus | Zoom |

### Rendering Pipeline

```
1. Data Changes
   ↓
2. DataSet Triggers Update
   ↓
3. Network Detects Changes
   ↓
4. Physics Engine Calculates Positions
   ↓
5. Canvas Renderer Draws Frame
   ↓
6. Redraw Complete
```

### Performance Optimization

**Viewport Rendering**:
- Only renders visible nodes/edges
- Culls off-screen elements
- Reduces rendering load

**Level-of-Detail (LOD)**:
- Simplified rendering at high zoom-out
- Full detail at zoom-in
- Font scaling adapts to zoom level

**Event Batching**:
- Groups multiple changes before redraw
- Reduces DOM thrashing
- Improves frame rate

### Data Flow: Adding a Node

```javascript
// 1. User submits form
async function createNode() {
  const nodeData = { id, label, type };
  
  // 2. API call to backend
  const response = await fetch('/api/nodes', {
    method: 'POST',
    body: JSON.stringify(nodeData)
  });
  
  // 3. Backend validates and stores
  // 4. Client receives confirmation
  
  // 5. Add to Vis.js DataSet
  nodes.add({
    id: nodeData.id,
    label: nodeData.label,
    color: colorMap[nodeData.type],
    title: `${nodeData.label} (${nodeData.type})`
  });
  
  // 6. Vis.js automatically:
  //    - Re-renders network
  //    - Runs physics simulation
  //    - Updates DOM
  //    - Animates layout change
}
```

### Data Flow: Adding an Edge

```javascript
async function createEdge() {
  const edgeData = { source, target, relation };
  
  // API call and validation...
  
  // Add to Vis.js DataSet
  edges.add({
    id: `${source}-${target}`,
    from: source,
    to: target,
    label: relation,
    title: `${source} → ${target} [${relation}]`
  });
  
  // Vis.js automatically:
  // - Adds visual connection
  // - Runs physics recalculation
  // - Repositions nodes
  // - Animates transition
}
```

### Canvas Rendering Details

**Technology Stack**:
- **Canvas API**: 2D drawing context
- **WebGL**: Optional hardware acceleration
- **Requestsframe**: 60 FPS target

**Rendering Process**:
```
1. Clear canvas
2. Draw background
3. Draw edges (bottom layer)
4. Draw nodes (middle layer)
5. Draw labels (top layer)
6. Draw selection highlights
7. Draw UI elements
8. Composite to display
```

### Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | Best performance |
| Firefox | ✅ Full | Excellent support |
| Safari | ✅ Full | Requires iOS 11+ |
| Edge | ✅ Full | Chromium-based |
| IE 11 | ⚠️ Limited | No WebGL acceleration |

### Memory Management

**Efficient Storage**:
- Nodes stored in HashMap for O(1) lookup
- Edges indexed by source/target for optimization
- DataSets use weak references where possible
- Automatic garbage collection when items removed

**Large Graph Handling**:
- 1,000 nodes: Smooth performance
- 5,000 nodes: Good performance with optimization
- 10,000+ nodes: Requires clustering/filtering

### Advanced Vis.js Features Used

#### 1. Physics Solver
- Force-directed layout algorithm
- Iterative convergence to stable state
- Configurable time and iteration limits

#### 2. Clustering (Future Enhancement)
```javascript
// Nodes can be grouped visually
network.cluster({
  processProperties: function(clusterOptions, nodeProperties, nodeId) {
    // Define clustering logic
  }
});
```

#### 3. Pathfinding (Future Enhancement)
```javascript
// Find shortest path between nodes
const path = network.getConnectedNodes(nodeId);
```

#### 4. Event System
```javascript
network.on('click', function(params) {
  console.log('Clicked:', params.nodes);
});

network.on('dragEnd', function(params) {
  console.log('Dragged node:', params.nodes);
});
```

### Network State Management

**Current Implementation**:
```javascript
let network;  // Global reference to Network instance

function initNetwork() {
  const container = document.getElementById('graph-canvas');
  const data = { nodes, edges };
  const options = { /* config */ };
  
  network = new vis.Network(container, data, options);
  
  // Attach event listeners
  network.on('click', handleNodeClick);
  network.on('dragEnd', handleNodeDrag);
}
```

**Future Improvements**:
- State management library (Redux/Vuex)
- Undo/redo functionality using event history
- Graph snapshots for comparison
- Animation timeline control

### Import/Export with Vis.js

**Export Process**:
```javascript
function exportGraph() {
  const visNodes = nodes.get();
  const visEdges = edges.get();
  
  // Transform to standard format
  const exportData = {
    nodes: visNodes,
    edges: visEdges.map(e => ({
      id: e.id,
      source: e.from,
      target: e.to,
      relation: e.label
    })),
    exportedAt: new Date().toISOString(),
    version: '1.0'
  };
  
  return JSON.stringify(exportData);
}
```

**Import Process**:
```javascript
function importGraph(data) {
  // Clear existing
  nodes.clear();
  edges.clear();
  
  // Add imported nodes
  data.nodes.forEach(node => {
    nodes.add({
      id: node.id,
      label: node.label,
      color: colorMap[node.type],
      title: `${node.label} (${node.type})`
    });
  });
  
  // Add imported edges
  data.edges.forEach(edge => {
    edges.add({
      id: edge.id,
      from: edge.source,
      to: edge.target,
      label: edge.relation
    });
  });
  
  // Vis.js automatically re-renders
}
```

### Resource Requirements

**Client-Side**:
- **Browser Memory**: 50-100MB for typical graphs
- **CPU**: 5-10% for interactive use
- **Network**: Minimal after initial load

**Network Bandwidth**:
- Initial load: ~300KB (Vis.js library)
- Graph data: 1KB per 10 nodes/edges average
- Real-time updates: ~100 bytes per change

### Troubleshooting Visualization Issues

| Issue | Solution |
|-------|----------|
| Nodes overlapping | Increase physics iterations |
| Slow performance | Reduce node count or enable clustering |
| Nodes flying off-screen | Reset zoom/pan, increase edge strength |
| Labels cut off | Increase canvas size or adjust font |
| Touch unresponsive | Enable touch interaction in options |

### Future Visualization Enhancements

1. **3D Visualization**: Use Three.js for 3D graph layout
2. **Hierarchical Layout**: Implement tree/hierarchy rendering
3. **Animated Transitions**: Smooth node/edge creation animations
4. **Custom Renderers**: Replace canvas with WebGL
5. **Graph Analytics**: Display metrics on-screen
6. **Recording/Playback**: Video export of graph changes
7. **Annotations**: Add text boxes and notes
8. **Themes**: Dark mode, custom color schemes
9. **Comparison View**: Side-by-side graph comparison
10. **Real-time Collaboration**: Live multi-user cursors

### Vis.js Documentation References

- **Official Docs**: https://visjs.org/
- **Network Examples**: https://visjs.github.io/vis-network/examples/
- **API Reference**: https://visjs.github.io/vis-network/docs/network/
- **Physics Guide**: https://visjs.github.io/vis-network/docs/network/physics/
