from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Any, List

from pipeflow.core.exceptions import ActionOrderError


class PipeflowAction(ABC):
    """Base class of action"""

    def __init__(self):
        self._context_ = None

    @abstractmethod
    def upstream(self) -> List:
        return []

    @abstractmethod
    async def execute(self, params: MappingProxyType) -> Any:
        """
        The logical computation of this action
        :param params: Externally Incoming Parameters (Read-Only)
        :return: The result of this action calculation
        """
        pass

    def set_context(self, context):
        self._context_ = context

    def result_of(self, clazz):
        if self._context_:
            if clazz not in self.upstream():
                raise ActionOrderError(rf"{str(clazz)} is not in <{self.__class__.__name__}>.upstream")
            return self._context_.result_of(clazz)
        else:
            return None
