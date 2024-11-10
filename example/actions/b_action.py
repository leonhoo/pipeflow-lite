import asyncio
from types import MappingProxyType
from typing import Any

from pipeflow.core.pipeflow_action import PipeflowAction


class BAction(PipeflowAction):
    def upstream(self) -> []:
        return []

    async def execute(self, params: MappingProxyType) -> Any:
        k = params.get('key1')  # Receives externally passed parameters
        print(rf'Param-key1: {k}')
        await asyncio.sleep(2)  # Simulate time-consuming operations.
        return 'B'  # Returns the result of the action's calculation
