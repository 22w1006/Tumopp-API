import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_and_visualize_tree(verbose, file_dir, N):
    # 读取数据
    df = pd.read_csv(file_dir + "population_with_roots.tsv", sep='\t')
    df['id'] = df['id'].astype(int)
    df['ancestor'] = df['ancestor'].astype(int)
    df['root'] = df['root'].astype(int)
    
    # 获取前N行作为根节点
    roots = df.head(N)['id'].tolist()
    
    # 创建有向图
    G = nx.DiGraph()
    
    # 为每个根节点分配颜色
    colors = plt.cm.tab10(np.linspace(0, 1, N))  # 使用tab10色图，最多支持10种颜色
    
    # 添加节点和边
    for _, row in df.iterrows():
        node_id = row['id']
        ancestor = row['ancestor']
        
        # 添加节点
        G.add_node(int(node_id))
        
        # 如果不是根节点且祖先节点存在，添加边
        if ancestor != -1 and node_id not in roots:
            G.add_edge(int(ancestor), int(node_id))
    
    # 创建多个子图
    plt.figure(figsize=(12, 8))
    
    # 计算每棵树的水平偏移量
    x_offset = 0
    tree_spacing = 50  # 每棵树之间的间距
    
    # 首先计算所有树的布局，确保根节点在同一高度
    all_positions = {}
    max_height = 0
    
    # 第一次遍历：获取所有树的最大高度
    for i, root in enumerate(roots):
        tree_nodes = nx.descendants(G, root) | {root}
        subgraph = G.subgraph(tree_nodes)
        pos = nx.drawing.nx_agraph.graphviz_layout(subgraph, prog='dot', root=root)
        current_max_height = max(v[1] for v in pos.values())
        if current_max_height > max_height:
            max_height = current_max_height
    
    # 第二次遍历：调整所有树的y坐标，使根节点对齐
    for i, root in enumerate(roots):
        tree_nodes = nx.descendants(G, root) | {root}
        subgraph = G.subgraph(tree_nodes)
        pos = nx.drawing.nx_agraph.graphviz_layout(subgraph, prog='dot', root=root)
        
        # 计算当前树的高度
        current_max_height = max(v[1] for v in pos.values())
        
        # 调整y坐标，使根节点对齐
        y_offset = max_height - current_max_height
        pos = {k: (v[0] + x_offset, v[1] + y_offset) for k, v in pos.items()}
        all_positions.update(pos)
        
        # 增加水平偏移量，改为使用树的宽度而不是最大x坐标
        tree_width = max(v[0] for v in pos.values()) - min(v[0] for v in pos.values())
        x_offset += tree_spacing + tree_width
        
        # 绘制节点
        nx.draw_networkx_nodes(subgraph, all_positions, 
                             node_color=[colors[i]]*len(tree_nodes),
                             node_size=10,
                             alpha=0.8)
        
        # 绘制边
        nx.draw_networkx_edges(subgraph, all_positions, 
                             edge_color=colors[i],
                             width=1.5,
                             alpha=0.6,
                             arrowstyle='-')
        if verbose == '1':
            # 绘制标签
            nx.draw_networkx_labels(subgraph, all_positions, font_size=10)
    
    # 设置图形属性
    plt.title(f'Tree Visualization (N={N})')
    plt.axis('off')
    plt.savefig(file_dir + 'tree_plot.png')

import sys
if __name__ == '__main__':
    # 输入N值
    arguments = sys.argv[1:]
    N = int(arguments[0])
    sample = arguments[1]
    verbose = int(arguments[2])
    create_and_visualize_tree(verbose, f'./{sample}/', N)