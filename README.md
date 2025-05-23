# Overview

Pipeflow-lite is a flexible and powerful data processing pipeline framework designed to simplify the flow of data from
sources to destinations such as databases, file systems, APIs, and more. It leverages a plugin-based architecture that
allows users to easily extend functionality as needed while keeping the core logic simple and efficient.

# File Structure

The file structure of Pipeflow-lite is as follows:

pipeflow_lite/  
├── core/  
│ ├── exceptions.py # Definitions of all exception types  
│ ├── pipeflow_action.py # Base class for individual actions  
│ └── pipeflow_context.py # Base class for contexts  
├── example/  
│ ├── actions/ # All action nodes for this example  
│ │ ├── a_action.py  
│ │ ├── b_action.py  
│ │ ├── c_action.py  
│ │ ├── d_action.py  
│ │ └── e_action.py  
│ ├── one_context.py # Context object instance for this example  
│ └── main.py # Entry point for running the example  
└── graph/  
└── visualizer.py # Tool for generating flowcharts of action node sequences, allowing easy viewing of upstream and
downstream positions of each action node

# Main Features

- Plugin-based Design: With a modular design, users can quickly integrate custom data sources, processors (actions), and
destinations.
- Data Flow Control: Supports multiple data flow control modes such as sequential, parallel (custom implementation
required), and conditional branching.
- Data Transformation: Implements data transformation and processing by defining different actions.
- Logging & Monitoring (custom implementation required): Provides detailed logging and monitoring capabilities for easy
issue tracking and system optimization.
- Extensibility: Supports creating custom actions by inheriting from the base class in pipeflow_action.py and custom
contexts by inheriting from the base class in pipeflow_context.py.

# Installation

Pipeflow-lite can be installed via Python's package management tool pip (assuming you have packaged the project as an
installable Python package):

```commandline
pip install pipeflow-lite
```

Alternatively, if you are developing locally, you can use the project's source code directly:

```commandline
python setup.py develop  
```

# Quick Start

## 1. Configure the Environment

Ensure your Python environment has Pipeflow-lite and its dependencies installed.

## 2. Define Actions

Create your action files

```python
from pipeflow.core.pipeflow_action import PipeflowAction
from types import MappingProxyType
from typing import Any


class AAction(PipeflowAction):
    async def execute(self, params: MappingProxyType) -> Any:
        # Implement your data processing logic  
        # Access and modify data in the context  
        pass


class BAction(PipeflowAction):
    async def execute(self, params: MappingProxyType) -> Any:
        # ...
        pass


class CAction(PipeflowAction):
    def upstream(self):
        return [AAction, BAction]

    async def execute(self, params: MappingProxyType) -> Any:
        # ... 
        pass
# class D and E...
```

## 3. Define Context

Create your context file, e.g., one_context.py:

```python
from pipeflow.core.pipeflow_context import PipeflowContext, load_from_directory


class OneContext(PipeflowContext):
    def __init__(self):
        # Load from path
        # Relative to the project root path, or just use the absolute path
        action_classes = load_from_directory("./example")

        # # Or load by type
        # from example.actions.a_action import AAction
        # from example.actions.b_action import BAction
        # from example.actions.c_action import CAction
        # from example.actions.d_action import DAction
        # from example.actions.e_action import EAction
        # action_classes = [
        #     AAction,
        #     BAction,
        #     CAction,
        #     DAction,
        #     EAction
        # ]

        super().__init__(action_classes)
```

## 4. Run the Pipeline

Write code in example/main.py to create and run your pipeline:

```python
from example.one_context import OneContext

# Create a context instance  
pipeline = OneContext()
result = pipeline.execute(initial_params={"key1": "value1"})
```  

## 5. Visualize the Flow

Use view.py to generate and view the flowchart of your action node sequences:

```commandline
python view.py 
```

Note: The visualization part above is a hypothetical example. The actual visualizer.py will need to be implemented by
you using a specific graph visualization library such as Graphviz, Matplotlib, etc.

# Custom Plugins

You can create custom actions by inheriting from the PipeflowAction base class in core/pipeflow_action.py and custom
contexts by inheriting from the PipeflowContext base class in core/pipeflow_context.py.

# Contributions & Community

Pipeflow-lite is an open-source project, and contributions in any form are welcome, including code submissions, documentation
improvements, and feedback. You can participate in the following ways:

- Report Issues: Report problems or suggestions you encounter in the GitHub repository.
- Contribute Code: Fork the repository, develop new features or fix bugs, and then submit pull requests.
- Update Documentation: Help improve the README and other documentation to make it clearer and easier to understand.

# License

Pipeflow-lite follows the MIT license, which means you can freely use, modify, and distribute the project while retaining the
original author's copyright information.

