import asyncio
from types import MappingProxyType
from typing import Any

from pipeflow.core.pipeflow_action import PipeflowAction
from example.actions.a_action import AAction
from example.actions.b_action import BAction
from example.actions.c_action import CAction
from example.actions.e_action import EAction


class DAction(PipeflowAction):
    def upstream(self):
        return [AAction, BAction, CAction, EAction]

    async def execute(self, params: MappingProxyType) -> Any:
        a_result = self.result_of(AAction)
        b_result = self.result_of(BAction)
        c_result = self.result_of(CAction)
        e_result = self.result_of(EAction)
        print(rf'ResultA: {a_result},ResultB: {b_result}, ResultC: {c_result}, ResultE: {e_result}')
        await asyncio.sleep(2)
        return a_result + b_result + c_result + e_result + 'D'
