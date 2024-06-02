import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def cpm_and_pert(tasks):
 
    earliest_start = defaultdict(int)
    earliest_finish = defaultdict(int)
    expected_duration = defaultdict(int)

    critical_path = []

    G = nx.DiGraph()

    for task in tasks:
        task_name = task['name']
        optimistic_duration = task.get('optimistic_duration', 0)
        pessimistic_duration = task.get('pessimistic_duration', 0)
        most_likely_duration = task.get('most_likely_duration', 0)
        expected_duration[task_name] = (optimistic_duration + 4 * most_likely_duration + pessimistic_duration) / 6

        predecessors = task.get('predecessors', [])
        for predecessor in predecessors:
            G.add_edge(predecessor, task_name, weight=expected_duration[task_name])  

    sorted_tasks = list(nx.topological_sort(G))
    for task_name in sorted_tasks:
        predecessors = list(G.predecessors(task_name))
        if len(predecessors) == 0:
            earliest_start[task_name] = 0
        else:
            earliest_start[task_name] = max(earliest_finish[predecessor] for predecessor in predecessors)
        if predecessors:
            earliest_finish[task_name] = earliest_start[task_name] + G[predecessors[0]][task_name]['weight']  
        else:
            earliest_finish[task_name] = earliest_start[task_name] + G.nodes[task_name].get('weight', 0)

    critical_path = [task for task in sorted_tasks if earliest_start[task] == earliest_finish[task]]

    # Plot graph
    pos = nx.shell_layout(G)  
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=110, arrows=True)
    nx.draw_networkx_nodes(G, pos, nodelist=critical_path, node_color='red', node_size=1500)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)

    plt.title('Critical Path Method (CPM) and Program Evaluation and Review Technique (PERT) Network Diagram')
    plt.show()

    return earliest_finish, critical_path

# Example 
tasks = [
    {'name': 'A', 'optimistic_duration': 1, 'pessimistic_duration': 5, 'most_likely_duration': 3, 'successors': ['B']},
    {'name': 'B', 'optimistic_duration': 2, 'pessimistic_duration': 6, 'most_likely_duration': 4, 'predecessors': ['A'], 'successors': ['C']},
    {'name': 'C', 'optimistic_duration': 3, 'pessimistic_duration': 7, 'most_likely_duration': 5, 'predecessors': ['B'], 'successors': ['D']},
    {'name': 'D', 'optimistic_duration': 4, 'pessimistic_duration': 8, 'most_likely_duration': 6, 'predecessors': ['C']}
]

earliest_finish_times, critical_path = cpm_and_pert(tasks)
print("Earliest Finish Times:", earliest_finish_times)
print("Critical Path:", critical_path)
