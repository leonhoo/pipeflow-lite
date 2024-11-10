import asyncio
import inspect
import logging
import os
import pathlib
import re
import sys
import time
from abc import ABC
from collections import defaultdict
from functools import wraps
from importlib import import_module
from types import MappingProxyType
from typing import List, Dict

from pipeflow.core.exceptions import ClassNotFoundError
from pipeflow.core.pipeflow_action import PipeflowAction

logger = logging.getLogger(__name__)


def load_from_directory(actions_path: str, root_path: str = '') -> List:
    """
    Load action classes from path
    :param actions_path: Relative to the project root path, or just use the absolute path
    :param root_path: If not specified, make sure that the project root is set correctly (os.chdir) in the entry file.
    :return:
    """
    implementation_classes = []

    def _is_subclass_and_not_abstract_(cls, base_cls):
        return (
                inspect.isclass(cls) and
                issubclass(cls, base_cls) and
                not inspect.isabstract(cls) and
                cls != base_cls
        )

    def _get_module_(module_file_path: str):
        module_name = module_file_path.replace(os.path.sep, '.').rstrip('.py')
        module_name = re.sub("\\.+", '.', module_name).lstrip('.')
        if module_name in sys.modules:
            return sys.modules[module_name]
        else:
            m = import_module(module_name)
            sys.modules[module_name] = m
            return m

    if not root_path or len(root_path) < 1:
        root_path = os.getcwd()

    if actions_path.startswith(root_path):
        actions_full_path = str(pathlib.Path(actions_path).absolute())
    else:
        actions_full_path = str(pathlib.Path(rf"{root_path}{os.path.sep}{actions_path}").absolute())
    for full_subdir, _, files in os.walk(actions_full_path):
        subdir = full_subdir[len(root_path):]
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(subdir, file)
                module = _get_module_(file_path)
                if module:
                    all_classes = [fullname for (clsname, fullname) in inspect.getmembers(module, inspect.isclass)]
                    classes = list(filter(lambda x: _is_subclass_and_not_abstract_(x, PipeflowAction), all_classes))
                    implementation_classes = implementation_classes + classes

    return list(sorted(set(implementation_classes), key=lambda x: x.__name__))


def _get_obj_name_(clazz):
    return rf"{clazz.__module__}.{clazz.__name__}"


def timer_wrapper(func, header=None, tail=None):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if header:
            logger.debug(f"{header}")

        if asyncio.iscoroutinefunction(func):
            start_time = time.monotonic()
            result = await func(*args, **kwargs)
            end_time = time.monotonic()
        else:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

        elapsed_time = end_time - start_time

        message = (tail if tail else f"Function '{func.__name__}' executed in") + f": {elapsed_time:.4f} seconds"
        logger.debug(message)

        return result

    return wrapper


class PipeflowContext(ABC):
    _action_classes_: [] = []
    """
    List of action classes
    """
    _action_names_: [] = []
    """
    List of action names
    """
    _name_action_graph_: {} = {}
    """
    The relationship between action_name and action_obj\n
    { action_name: action_obj }
    """
    _name_class_graph_: {} = {}
    """
    The relationship between action_name and action_class\n
    { action_name: action_class }
    """
    _action_name_downstream_graph_: {} = {}
    """
    The relationship between upstream action name and downstream action name\n
    { upstream_action_name: downstream_action_name }
    """
    _action_result_graph_: {} = {}
    """
    The relationship between action name and action result\n
    { action_name: action_result_obj }
    """
    _sorted_downstream_level_hierarchical_graph_: {} = {}
    """
    The relationship between run level and action name\n
    { level: action_name }
    """

    def __init__(self, action_classes: []):
        self._action_classes_ = action_classes
        # Initiate
        for action_class in action_classes:
            action = action_class()
            action_name = _get_obj_name_(action_class)
            action.set_context(self)
            self._action_names_.append(action_name)
            self._name_class_graph_[action_name] = action_class
            self._name_action_graph_[action_name] = action
            self._action_result_graph_[action_name] = None

        # For downstream
        self._action_name_downstream_graph_ = self._name_downstream_()
        self._sorted_downstream_level_hierarchical_graph_ = self._downstream_hierarchical_()

    def _name_downstream_(self):
        downstream = {}
        for action_name, action in self._name_action_graph_.items():
            upstream_list = action.upstream()
            if upstream_list and len(upstream_list) > 0:
                for upstream in upstream_list:
                    upstream_name = _get_obj_name_(upstream)
                    if upstream_name not in downstream:
                        downstream[upstream_name] = []
                    downstream[upstream_name].append(action_name)
        return downstream

    def _downstream_hierarchical_(self) -> Dict:
        hierarchical_dict = {key: 0 for key in self._action_names_}  # 0 is the first level

        def hierarchical_ordering(name: str) -> Dict:
            downstream_name_list = self._action_name_downstream_graph_.get(name)
            if downstream_name_list and len(downstream_name_list) > 0:
                for downstream_name in downstream_name_list:
                    if hierarchical_dict[downstream_name] <= hierarchical_dict[name]:
                        hierarchical_dict[downstream_name] = hierarchical_dict[name] + 1
                        hierarchical_ordering(downstream_name)

        for action_name in self._action_names_:
            hierarchical_ordering(action_name)
        hierarchical_ordering_level_dict = defaultdict(list)
        for key, value in hierarchical_dict.items():
            hierarchical_ordering_level_dict[value].append(key)
        sorted_keys = sorted(hierarchical_ordering_level_dict.keys())
        return {key: hierarchical_ordering_level_dict[key] for key in sorted_keys}

    async def _run_action_(self, action_name: str, params: {}):
        """Run a single action"""
        header = rf'Starting action <{action_name}>'
        tail = rf"Action <{action_name}> completed in"

        async def _run_():
            result = await self._name_action_graph_[action_name].execute(params)
            self._action_result_graph_[action_name] = result  # Record action result

        func = timer_wrapper(_run_, header, tail)
        await func()

    def _final_results_(self):
        """Get the results of the last level"""
        last_level = max(self._sorted_downstream_level_hierarchical_graph_.keys())
        action_name_list = self._sorted_downstream_level_hierarchical_graph_[last_level]
        return {
            action_name: self.result_of(self._name_class_graph_.get(action_name))
            for action_name in action_name_list
        }

    async def execute_async(self, initial_params: {}) -> Dict:
        """Asynchronous run"""

        # def callback(act_name, _):
        #     if self._completed_:
        #         self._completed_(act_name)

        header = rf"Starting pipeline <{_get_obj_name_(self.__class__)}>"
        tail = rf"Pipeline <{_get_obj_name_(self.__class__)}> completed in"
        params = MappingProxyType(initial_params)

        async def _run_actions_():
            for level, action_name_list in self._sorted_downstream_level_hierarchical_graph_.items():
                tasks = []
                for name in action_name_list:
                    task = asyncio.create_task(self._run_action_(name, params))
                    # task.add_done_callback(partial(callback, name))
                    tasks.append(task)
                await asyncio.gather(*tasks)

        func = timer_wrapper(_run_actions_, header, tail)
        await func()
        return self._final_results_()

    def execute(self, initial_params: {}) -> Dict:
        """Synchronous run"""
        return asyncio.run(self.execute_async(initial_params))

    def result_of(self, clazz):
        """Obtain the result of a specified action based on the action type"""
        if clazz and clazz in self._action_classes_:
            return self._action_result_graph_.get(_get_obj_name_(clazz))
        else:
            raise ClassNotFoundError()
