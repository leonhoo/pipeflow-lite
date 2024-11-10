from graphviz import Digraph

from pipeflow.core.pipeflow_context import PipeflowContext


# Export the process structure

def draw(context: PipeflowContext):
    actions_graph = context._name_action_graph_
    hierarchical = context._sorted_downstream_level_hierarchical_graph_

    dot = Digraph(comment='Pipeflow-OneContext', filename="one_context.gv", )
    dot.attr(rankdir='LR', size='10,5', splines='spline')
    for v_list in hierarchical.values():
        for v in v_list:
            action = actions_graph[v]
            action_name = action.__class__.__name__
            dot.node(action_name, _attributes={'color': 'gray', 'shape': 'plaintext', 'style': 'dotted'})
            us_list = action.upstream()
            if us_list and len(us_list) > 0:
                for us in us_list:
                    upstream_name = us.__name__
                    dot.edge(upstream_name, action_name, _attributes={'color': 'blue'})

    dot.view()
