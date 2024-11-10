import asyncio
from types import MappingProxyType
from typing import Any

from pipeflow.core.pipeflow_action import PipeflowAction


class EAction(PipeflowAction):
    def upstream(self):
        return []

    async def execute(self, params: MappingProxyType) -> Any:
        await asyncio.sleep(2)
        return 'E'
