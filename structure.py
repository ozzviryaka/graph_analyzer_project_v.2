# graphanalyzer/
# ├── main.py
# ├── config.py
# ├── core/
# │   ├── __init__.py
# │   ├── graph_model/    # Нова папка для компонентів моделі графа
# │   │   ├── __init__.py
# │   │   ├── node.py     # Клас Node
# │   │   ├── edge.py     # Клас Edge
# │   │   └── graph.py    # Клас Graph (залежить від Node та Edge)
# │   ├── graph_operations.py
# │   ├── algorithms/
# │   │   ├── __init__.py
# │   │   ├── shortest_path.py
# │   │   ├── centrality.py
# │   │   └── clustering.py
# ├── gui/
# │   ├── __init__.py
# │   ├── main_window.py
# │   ├── graph_display_widget.py
# │   ├── algorithm_settings_widget.py
# │   └── dialogs/
# │       ├── __init__.py
# │       ├── import_graph_dialog.py
# │       └── export_results_dialog.py
# ├── data_utils/
# │   ├── __init__.py
# │   ├── graph_loader.py
# │   └── graph_saver.py
# ├── utils/
# │   ├── __init__.py
# │   ├── logger.py
# │   └── helpers.py
# ├── tests/
# │   ├── __init__.py
# │   ├── test_graph_model.py
# │   ├── test_graph_operations.py
# │   └── test_algorithms.py
# ├── resources/
# │   ├── images/
# │   └── icons/
# ├── requirements.txt
# └── README.md