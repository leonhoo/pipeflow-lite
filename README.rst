# Overview

Pipeflow-lite is a flexible and powerful data processing pipeline framework designed to simplify the flow of data from
sources to destinations such as databases, file systems, APIs, and more. It leverages a plugin-based architecture that
allows users to easily extend functionality as needed while keeping the core logic simple and efficient.

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