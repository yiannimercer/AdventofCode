# %% 

from statistics import median
from dotenv import load_dotenv
from utils.grid import Grid, Direction
from collections import deque
load_dotenv()
from aocd import get_data, submit
import math
import networkx as nx
from itertools import combinations

# %% 

# ------------------------------------------------
# LOAD DATA 
# ------------------------------------------------

# Networkx graph approach - https://networkx.org/documentation/stable/tutorial.html#analyzing-graphs

data = get_data(day=8, year=2025).splitlines()
sample = [
    '162,817,812',
    '57,618,57',
    '906,360,560',
    '592,479,940',
    '352,342,300',
    '466,668,158',
    '542,29,236',
    '431,825,988',
    '739,650,466',
    '52,470,668',
    '216,146,977',
    '819,987,18',
    '117,168,530',
    '805,96,715',
    '346,949,466',
    '970,615,88',
    '941,993,340',
    '862,61,35',
    '984,92,344',
    '425,690,689'
]

data = [tuple(list(map(int, line.split(',')))) for line in data]
sample = [tuple(list(map(int, line.split(',')))) for line in sample]

# %%

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

# Create all unique pairs
data_pairs = list(combinations(data, 2))

# Calculate Euclidean distances for each pair
distances = {f"{p1}, {p2}": math.dist(p1, p2) for p1, p2 in data_pairs}

# Define the number of connections to process
JUNCTION_BOXES_TO_CONNECT = 1000

# Find the min distance and corresponding pair
min_pairs = sorted(distances, key=distances.get)[:JUNCTION_BOXES_TO_CONNECT]

edges = []

for pair in min_pairs:
    p1, p2 = pair.split('), (')
    p1 = tuple(map(int, p1.strip('()').split(',')))
    p2 = tuple(map(int, p2.strip('()').split(',')))
    edges.append((p1, p2))

G = nx.Graph()
G.add_edges_from(edges)
        
circuits = list(nx.connected_components(G))
circuit_sizes = [len(circuit) for circuit in circuits]

# Calculate the product of the sizes of the three largest circuits
largest_sizes = sorted(circuit_sizes, reverse=True)[:3]
answer_a = math.prod(largest_sizes)


# %%

submit(answer_a, part="a", day=8, year=2025)

# %%

# ------------------------------------------------
# PUZZLE 2 - WHAT COORDINATE GETS US TO ONE CIRCUIT
# ------------------------------------------------

# Create all unique pairs
data_pairs = list(combinations(sample, 2))

# Calculate Euclidean distances for each pair
distances = {f"{p1}, {p2}": math.dist(p1, p2) for p1, p2 in data_pairs}

edges = []

for pair in distances.keys():
    p1, p2 = pair.split('), (')
    p1 = tuple(map(int, p1.strip('()').split(',')))
    p2 = tuple(map(int, p2.strip('()').split(',')))
    edges.append((p1, p2))

# Sort edges by distance
edges = sorted(edges, key=lambda e: math.dist(e[0], e[1]))

# Get all unique nodes
all_nodes = set()
for p1, p2 in edges:
    all_nodes.add(p1)
    all_nodes.add(p2)
    
# Start with all nodes unconnected
G = nx.Graph()
G.add_nodes_from(all_nodes)

for p1, p2 in edges:
    
    # Check if p1 and p2 are already in the same circuit (are connected)
    has_connection = nx.has_path(G, p1, p2)  # has_connection == in_circuit
    
    # If they are connected/in circuit, skip it
    if has_connection:
        continue
    
    # If not, add the edge/connection between these two points
    G.add_edge(p1, p2)
    
    # Count how many "circuits" (connected components) there are, where a standalone node is a components/circuit of 1
    # GOAL: Stop when there is only 1 component/circuit - this means every node is reachable from every other node (all in one circuit)
    component_cnt = nx.number_connected_components(G)
    print(component_cnt)
    if component_cnt == 1:
        print(f"Final edge/connection: {p1} -- {p2}")
        
    



# %% 

# ------------------------------------------------
# SAME AS ABOVE BUT PLOTTING NETWORK GRAPH AS WE ADD EDGES/CONNECTIONS 
# ------------------------------------------------

import matplotlib.pyplot as plt

# Get all nodes
all_nodes = set()
for p1, p2 in edges:
    all_nodes.add(p1)
    all_nodes.add(p2)

# Create graph with all nodes
G = nx.Graph()
G.add_nodes_from(all_nodes)

# Simplify node labels for readability
label_map = {node: chr(65 + i) for i, node in enumerate(sorted(all_nodes))}
# {(0,0,0): 'A', (1,1,1): 'B', (2,2,2): 'C', ...}

# Create figure with subplots for each step
fig, axes = plt.subplots(2, 10, figsize=(25, 20))
axes = axes.flatten()

# Use consistent layout
pos = nx.spring_layout(G, seed=42)

# Plot initial state
ax = axes[0]
nx.draw(G, pos, ax=ax, with_labels=True, labels=label_map, 
        node_color='lightblue', node_size=500, font_size=12)
ax.set_title(f"Start: {nx.number_connected_components(G)} components")

# Process edges and plot each step
plot_idx = 1
for p1, p2 in edges:
    if nx.has_path(G, p1, p2):
        continue
    
    G.add_edge(p1, p2)
    n_components = nx.number_connected_components(G)
    
    # Color nodes by component
    components = list(nx.connected_components(G))
    colors = ['lightcoral', 'lightgreen', 'lightyellow', 'lightblue', 'plum', 'peachpuff']
    node_colors = []
    for node in G.nodes():
        for i, comp in enumerate(components):
            if node in comp:
                node_colors.append(colors[i % len(colors)])
                break
    
    ax = axes[plot_idx]
    nx.draw(G, pos, ax=ax, with_labels=True, labels=label_map,
            node_color=node_colors, node_size=500, font_size=12,
            edge_color='gray', width=2)
    ax.set_title(f"Add {label_map[p1]}--{label_map[p2]}: {n_components} component(s)")
    
    plot_idx += 1
    
    if n_components == 1:
        ax.set_title(f"Add {label_map[p1]}--{label_map[p2]}: ✓ ALL CONNECTED!")
        break

# Hide unused subplots
for i in range(plot_idx, len(axes)):
    axes[i].axis('off')

plt.tight_layout()
plt.savefig('graph_steps.png')
plt.show()

# %%
