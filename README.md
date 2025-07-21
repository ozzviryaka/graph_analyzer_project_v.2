# GAP - Graph Analyzer Project v.2

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.11-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**GAP (Graph Analyzer Project)** is an advanced desktop application for graph theory analysis and visualization. Built with PyQt5, it provides a comprehensive suite of graph algorithms, interactive visualization, and educational tools for students, researchers, and professionals working with graph structures.

## 🚀 Features

### Core Functionality
- **Interactive Graph Creation**: Create vertices and edges with intuitive mouse controls
- **Multiple Graph Types**: Support for directed/undirected and weighted/unweighted graphs
- **Real-time Visualization**: Dynamic graph rendering with customizable themes
- **Multi-language Support**: Available in English, Ukrainian, and French
- **Session Management**: Save and load multiple graphs in organized sessions

### Graph Algorithms

#### Shortest Path Algorithms
- **Dijkstra's Algorithm**: Single-source shortest path for non-negative weights
- **Bellman-Ford Algorithm**: Single-source shortest path with negative weight support
- **Floyd-Warshall Algorithm**: All-pairs shortest paths

#### Spanning Tree Algorithms
- **Prim's Algorithm**: Minimum spanning tree for connected graphs
- **Kruskal's Algorithm**: Minimum spanning tree using edge sorting

#### Flow Algorithms
- **Ford-Fulkerson Algorithm**: Maximum flow in flow networks
- **Minimum Cut Algorithm**: Find minimum cut in flow networks

#### Special Path Finding
- **Simple Path**: Basic path finding between vertices
- **Longest Simple Path**: Find the longest acyclic path
- **Hamiltonian Path**: Path visiting each vertex exactly once
- **Eulerian Path**: Path traversing each edge exactly once

#### Graph Traversal
- **Breadth-First Search (BFS)**: Level-order graph traversal
- **Depth-First Search (DFS)**: Deep exploration traversal
- **Connected Components**: Find all connected subgraphs
- **Cycle Detection**: Identify cycles in the graph

### Analysis Tools
- **Graph Statistics**: Comprehensive graph metrics and properties
- **Matrix Representations**: Adjacency and incidence matrices
- **Structural Analysis**: Redundancy, compactness, and centralization measures
- **Export Capabilities**: Export results to TXT, CSV, PNG formats

## 📋 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM recommended
- **Display**: 1280x720 or higher resolution

## 🛠️ Installation

### Method 1: Using pip (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ozzviryaka/graph_analyzer_project_v.2.git
   cd graph_analyzer_project_v.2
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv graph_analyzer_env
   
   # On Windows:
   graph_analyzer_env\Scripts\activate
   
   # On macOS/Linux:
   source graph_analyzer_env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Method 2: Manual Installation

Install the required packages manually:
```bash
pip install PyQt5==5.15.11
pip install numpy==2.3.1
pip install matplotlib==3.10.3
```

## 🎮 Usage

### Starting the Application

Run the main application:
```bash
python main.py
```

The application will start with a splash screen and then open the main interface.

### Basic Operations

#### Creating Graphs
1. **Add Vertex**: Left-click on empty space in the canvas
2. **Delete Vertex**: Right-click on vertex
3. **Move Vertex**: Left-click and drag vertex
4. **Select Vertex**: Left-click on vertex (highlights for edge creation)

#### Working with Edges
1. **Add Edge**: Select first vertex, then Ctrl+Left-click on second vertex
2. **Delete Edge**: Right-click on the middle of an edge
3. **Edit Edge**: Double-click on edge (for weighted graphs)
4. **Select Edge**: Left-click on the middle of an edge

#### Graph Settings
- **Graph Type**: Toggle between directed/undirected using the switch above canvas
- **Graph Weight**: Toggle between weighted/unweighted graphs
- **Automatic Naming**: Enable/disable automatic vertex naming
- **Manual Naming**: When disabled, custom vertex naming dialog appears

### Advanced Features

#### Graph Management
- Use **"Select Graph"** button to open graph management window
- Create, rename, delete, or duplicate graphs
- Work with multiple graphs in one session
- Switch between graphs easily

#### Analysis Tools
1. **Shortest Paths Tab**: Access Dijkstra, Bellman-Ford, Floyd-Warshall algorithms
2. **Spanning Trees Tab**: Use Prim and Kruskal algorithms
3. **Special Paths Tab**: Find simple, longest, Hamiltonian, Eulerian paths
4. **Traversal Tab**: Perform BFS, DFS, connected components, cycle detection
5. **Flow Tab**: Calculate maximum flow and minimum cut
6. **Matrix Tab**: View adjacency and incidence matrices

#### Import/Export
- **Export Graph**: Use .json/.txt export buttons below canvas
- **Import Graph**: Use 'Import from .json' button below canvas
- **Session Management**: Export/import multiple graphs and settings
- **Matrix Export**: Export matrices to CSV or PNG format

#### Customization
- **Themes**: Choose from modern/classic styles with multiple color schemes
- **Languages**: Switch between Ukrainian, English, and French
- **Undo/Redo**: Use Ctrl+Z / Ctrl+Y for action history

## 📁 Project Structure

```
graph_analyzer_project_v.2/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── settings.json                    # Application settings
├── res/                            # Resources
│   ├── icon.png                    # Application icon
│   └── settings_icon.png           # Settings icon
│
├── core/                           # Core graph functionality
│   ├── algorithms/                 # Graph algorithms implementation
│   │   ├── flow/                   # Flow algorithms (Ford-Fulkerson, Min-Cut)
│   │   ├── matrices/               # Matrix operations
│   │   ├── shortest_paths/         # Shortest path algorithms
│   │   ├── spanning_trees/         # Spanning tree algorithms
│   │   ├── special_paths/          # Special path finding algorithms
│   │   ├── traversal/              # Graph traversal algorithms
│   │   └── graph_info.py           # Graph statistics and analysis
│   │
│   ├── convertations/              # Graph conversion utilities
│   │   ├── edge_converter.py       # Edge type conversions
│   │   └── graph_converter.py      # Graph type conversions
│   │
│   ├── graph_components/           # Basic graph building blocks
│   │   ├── base_edge.py            # Base edge class
│   │   ├── directed_edge.py        # Directed edge implementation
│   │   ├── undirected_edge.py      # Undirected edge implementation
│   │   └── node.py                 # Graph node/vertex implementation
│   │
│   └── graph_models/               # Graph data structures
│       ├── graph.py                # Base graph class
│       ├── directed_graph.py       # Directed graph implementation
│       └── undirected_graph.py     # Undirected graph implementation
│
├── data_utils/                     # Data management utilities
│   ├── graph_loader.py             # Graph loading functionality
│   ├── graph_saver.py              # Graph saving functionality
│   ├── session_exporter.py         # Session export functionality
│   ├── session_importer.py         # Session import functionality
│   ├── adjacency_matrix_exporter.py # Adjacency matrix export
│   └── incidence_matrix_exporter.py # Incidence matrix export
│
├── gui/                            # User interface components
│   ├── main_window.py              # Main application window
│   ├── splash_screen.py            # Application startup screen
│   │
│   ├── additionals/                # Additional GUI components
│   │   ├── graph_canvas.py         # Interactive graph canvas
│   │   ├── readonly_graph_canvas.py # Read-only graph display
│   │   ├── toggle_switch.py        # Custom toggle switch widget
│   │   └── tab_shortcut_event_filter.py # Keyboard shortcuts
│   │
│   ├── dialogs/                    # Dialog windows
│   │   ├── edge_edit_dialog.py     # Edge editing dialog
│   │   ├── vertex_edit_dialog.py   # Vertex editing dialog
│   │   ├── graph_select_dialog.py  # Graph selection dialog
│   │   ├── language_select_dialog.py # Language selection
│   │   ├── theme_select_dialog.py  # Theme selection
│   │   └── instruction_dialog.py   # Help and instructions
│   │
│   ├── tabs/                       # Main application tabs
│   │   ├── graph_analysis_tab.py   # Graph analysis interface
│   │   ├── graph_combined_tab.py   # Combined graph view
│   │   ├── graph_tabs_widget.py    # Tab container widget
│   │   ├── matrix_tabs_widget.py   # Matrix view tabs
│   │   └── traversal_tab.py        # Graph traversal interface
│   │
│   ├── themes/                     # Application theming
│   │   ├── theme_manager.py        # Theme management system
│   │   ├── classic/                # Classic theme resources
│   │   └── modern/                 # Modern theme resources
│   │
│   └── widgets/                    # Specialized widgets
│       ├── graph_settings_widget.py # Graph configuration widget
│       └── analysis_tab_widgets/   # Analysis-specific widgets
│
├── locales/                        # Internationalization
│   ├── locale_manager.py           # Localization manager
│   ├── en_locale.json              # English translations
│   ├── uk_locale.json              # Ukrainian translations
│   └── fr_locale.json              # French translations
│
└── utils/                          # Utility modules
    ├── logger.py                   # Application logging
    ├── txt_exporter.py             # Text export functionality
    ├── undo_redo_manager.py        # Undo/redo system
    └── undo_redo_event_filter.py   # Undo/redo event handling
```

## 🔧 Algorithm Details

### Shortest Path Algorithms

#### Dijkstra's Algorithm
- **Time Complexity**: O((V + E) log V)
- **Use Case**: Single-source shortest path with non-negative weights
- **Features**: Optimal for weighted graphs without negative edges

#### Bellman-Ford Algorithm
- **Time Complexity**: O(VE)
- **Use Case**: Single-source shortest path with negative weight support
- **Features**: Detects negative cycles, works with negative edge weights

#### Floyd-Warshall Algorithm
- **Time Complexity**: O(V³)
- **Use Case**: All-pairs shortest paths
- **Features**: Computes shortest paths between all vertex pairs

### Spanning Tree Algorithms

#### Prim's Algorithm
- **Time Complexity**: O(E log V)
- **Use Case**: Minimum spanning tree for connected graphs
- **Features**: Grows tree from a single vertex

#### Kruskal's Algorithm
- **Time Complexity**: O(E log E)
- **Use Case**: Minimum spanning tree using edge sorting
- **Features**: Uses union-find data structure

### Flow Algorithms

#### Ford-Fulkerson Algorithm
- **Time Complexity**: O(Ef) where f is maximum flow
- **Use Case**: Maximum flow in flow networks
- **Features**: Augmenting path method

#### Minimum Cut Algorithm
- **Time Complexity**: O(Ef)
- **Use Case**: Find minimum cut in flow networks
- **Features**: Based on max-flow min-cut theorem

## 🎨 Customization

### Themes
The application supports multiple themes:
- **Classic**: Traditional interface design
- **Modern**: Contemporary flat design
- **Color Schemes**: Dark, Light, Green, Blue, Red, Yellow

### Languages
Full localization support for:
- **English**: Complete interface translation
- **Ukrainian**: Native language support
- **French**: Comprehensive French localization

## 🐛 Troubleshooting

### Common Issues

1. **Application won't start**:
   - Verify Python version (3.8+)
   - Check all dependencies are installed
   - Run `pip install -r requirements.txt`

2. **Graph visualization issues**:
   - Update graphics drivers
   - Check display resolution settings
   - Try different theme settings

3. **Algorithm errors**:
   - Ensure graph meets algorithm requirements
   - Check for disconnected components
   - Verify edge weights are valid

4. **Import/Export problems**:
   - Check file permissions
   - Verify file format (.json for graphs)
   - Ensure sufficient disk space

### Performance Tips

- For large graphs (>1000 vertices), consider using simpler visualization
- Complex algorithms may take time on large datasets
- Use session export for backup before major changes
- Regular cleanup of temporary files improves performance

## 🤝 Contributing

We welcome contributions to the Graph Analyzer Project! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-algorithm`
3. **Commit your changes**: `git commit -am 'Add new algorithm'`
4. **Push to the branch**: `git push origin feature/new-algorithm`
5. **Create a Pull Request**

### Development Guidelines
- Follow PEP 8 coding standards
- Add comprehensive docstrings
- Include unit tests for new algorithms
- Update localization files for UI changes
- Test on multiple platforms when possible

## 📚 Educational Use

This project is designed with education in mind:

- **Interactive Learning**: Visual representation helps understand graph concepts
- **Algorithm Visualization**: Step-by-step algorithm execution
- **Comprehensive Coverage**: Wide range of graph theory topics
- **Multiple Languages**: Accessible to international students
- **Export Capabilities**: Generate reports and documentation

### Recommended for:
- Computer Science students learning graph theory
- Researchers working with network analysis
- Educators teaching algorithms and data structures
- Software developers needing graph analysis tools

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **ozzviryaka** - *Project Creator and Lead Developer*

## 🙏 Acknowledgments

- PyQt5 community for excellent GUI framework
- NetworkX for inspiration in graph algorithm implementation
- Graph theory educational resources that influenced the design
- Beta testers and early users for valuable feedback

## 📞 Support

For support, feature requests, or bug reports:
- Create an issue on GitHub
- Contact the development team
- Check the documentation and troubleshooting guide

---

**Happy Graph Analyzing!** 📊🔍
