import os
import unittest

from example.actions.a_action import AAction
from example.actions.b_action import BAction
from example.actions.c_action import CAction
from example.actions.d_action import DAction
from example.actions.e_action import EAction
from pipeflow.core.pipeflow_context import load_from_directory


class TestClassLoaded(unittest.TestCase):
    def test_load_from_directory(self):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        actions = load_from_directory(r'example/actions')
        self.assertListEqual(actions, [
            AAction,
            BAction,
            CAction,
            DAction,
            EAction
        ])
        pass
