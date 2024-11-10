from pipeflow.core.pipeflow_context import PipeflowContext, load_from_directory


class OneContext(PipeflowContext):

    def __init__(self):
        action_classes = load_from_directory("example/actions")

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
