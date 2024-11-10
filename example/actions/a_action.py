import asyncio
from types import MappingProxyType
from typing import Any

from pipeflow.core.pipeflow_action import PipeflowAction


class AAction(PipeflowAction):
    def upstream(self) -> []:
        pass

    async def execute(self, params: MappingProxyType) -> Any:
        await asyncio.sleep(2)  # Simulate time-consuming operations.
        return "A"  # Returns the result of the action's calculation
