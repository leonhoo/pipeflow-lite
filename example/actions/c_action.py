import asyncio
from types import MappingProxyType
from typing import Any

from pipeflow.core.pipeflow_action import PipeflowAction
from example.actions.a_action import AAction
from example.actions.b_action import BAction


class CAction(PipeflowAction):
    def upstream(self):
        return [AAction, BAction]

    async def execute(self, params: MappingProxyType) -> Any:
        a_result = self.result_of(AAction)  # Received results of the previous actions
        b_result = self.result_of(BAction)
        print(rf'ResultA: {a_result}, ResultB: {b_result}')
        await asyncio.sleep(2)

        return a_result + b_result + 'C'
