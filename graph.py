import os
import time
import queue
import shutil
import imageio
import networkx as nx
import matplotlib.pyplot as plt

def order_bfs(graph, start_node):
    visited = set()
    q = queue.Queue()
    q.put(start_node)
    order = []
    while not q.empty():
        vertex = q.get()
        if vertex not in visited:
            order.append(vertex)
            visited.add(vertex)
            for node in graph[vertex]:
                if node not in visited:
                    q.put(node)

    return order

def order_dfs(graph, start_node, visited=None):
    if visited is None:
        visited = set()
    order = []

    if start_node not in visited:
        order.append(start_node)
        visited.add(start_node)

    for node in graph[start_node]:
        if node not in visited:
            order.extend(order_dfs(graph, node, visited))

    return order

def floodFill(graph, start_node, visited=None):
    visited = set()
    q = []
    level = 0
    levelDict = {}
    # Enqueue root and initialize height
    q.append(start_node)
 
    while q:
 
        # nodeCount (queue size) indicates number
        # of nodes at current level.
        count = len(q)
 
        # Dequeue all nodes of current level and
        # Enqueue all nodes of next level
        arr = []
        while count > 0:
            temp = q.pop(0)
            arr.append(temp)
            print(temp, end=' ')
            if temp not in visited:
                visited.add(temp)
            for node in graph[temp]:
                if node not in visited:
                    q.append(node)
            count -= 1
        print(' ')
        levelDict[level] = arr
        level += 1

    return levelDict

def visualize_search(order, title, G, pos):
    plt.figure()
    plt.title(title)

    for i, node in enumerate(order, start=1):
        plt.clf()
        plt.title(title)
        nx.draw(G, pos, with_labels=True, node_color=['r' if n == node else 'g' for n in G.nodes])
        plt.draw()
        plt.pause(1.5)
    
    plt.show()
    time.sleep(0.5)

def generate_gif(temp_dir, length):
    images = []
    for i in range(1, length):
        filepath = os.path.join(temp_dir, f"plot_{i}.png")
        images.append(imageio.imread(filepath))
    gif_path = "plots.gif"
    imageio.mimsave(gif_path, images, fps=1) # `fps` controls the speed of the GIF

    # Clean up the temporary directory if desired
    shutil.rmtree(temp_dir) # Be careful with this command

def visualize_flood_fill(levelDict, title, G, pos):
    plt.figure()
    plt.title(title)
    # Create a temporary directory to store the images
    temp_dir = "temp_plots"
    os.makedirs(temp_dir, exist_ok=True)
    depth = 2
    node_red = []
    i = 1
    for key, value in levelDict.items():
        if key <= depth:
            node_red.extend(value)
            plt.clf()
            plt.title(title)
            
            nx.draw(G, pos, with_labels=True, node_color=['r' if n in node_red else 'g' for n in G.nodes])
            plt.draw()
            plt.text(-0.7, 0.6,s='Initial Target: Hospital\nDepth: 2', bbox=dict(facecolor='green', alpha=0.5), horizontalalignment='center')
            manager = plt.get_current_fig_manager()
            if i == 1:
                manager.full_screen_toggle()
            filepath = os.path.join(temp_dir, f"plot_{i}.png")
            plt.savefig(filepath)
            plt.pause(1.5)
            i += 1
    plt.show()
    time.sleep(0.5)
    generate_gif(temp_dir, i)

G = nx.MultiGraph()
# G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('D', 'K'), ('E', 'L'), ('G', 'H'), ('F', 'J')])
G.add_edges_from(
    [
        ('Hospital', 'Airport'),
        ('Hospital', 'Road Infrastructure'),
        ('Hospital', 'Social Media'),
        ('Airport', 'Road Infrastructure'),
        ('Airport', 'Social Media'),
        ('Road Infrastructure', 'Airport'),
        ('Road Infrastructure', 'Social Media'),
        ('School', 'Road Infrastructure'),
        ('School', 'Social Media'),
        ('Fuel Infrastructure', 'Power Plants'),
        ('Fuel Infrastructure', 'Transportation'),
        ('Fuel Infrastructure', 'Social Media'),
        ('Transportation', 'Fuel Station'),
        ('Transportation', 'Social Media'),
        ('Water and Sewage', 'Hospital'),
        ('Water and Sewage', 'Transportation'),
        ('Water and Sewage', 'Road Infrastructure'),
        ('Water and Sewage', 'Social Media'),
        ('Power Plant', 'Social Media'),
        ('Power Plant', 'Fuel Infrastructure'),
        ('Law Enforcement', 'Social Media'),
        ('Law Enforcement', 'Finance Infrastructure'),
        ('Finance Infrastructure', 'Social Media'),
    ]
)
pos = nx.spring_layout(G)

start_node = 'Hospital'
x = floodFill(G, start_node)
print(x)

visualize_flood_fill(floodFill(G, start_node), 'CCAAS Visualization', G, pos)