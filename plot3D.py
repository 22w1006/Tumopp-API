import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_scatter(file_dir):
    # 读取数据
    df = pd.read_csv(file_dir + "population_with_roots.tsv", sep='\t')
    
    # 创建3D图形
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 将root转换为分类类型
    df['root'] = df['root'].astype('category')
    
    # 使用浅色配色方案
    light_colors = {1: 'red', 2: 'blue', 3: 'purple', 4: 'yellow', 5: 'green', 6: 'orange', 7: 'brown', 8: 'pink', 9: 'gray', 10: 'cyan'}
    scatter_colors = df['root'].map(light_colors)
    
    # 绘制带黑色轮廓的散点图
    scatter = ax.scatter(df['x'], df['y'], df['z'],
                        c=scatter_colors,
                        edgecolor='black',  # 添加黑色轮廓
                        linewidth=0.2,     # 轮廓线宽
                        s=10, alpha=0.6)    # 增大点的大小
    
    # 添加颜色条
    cbar = plt.colorbar(scatter)
    cbar.set_label('Root Category')
    
    # 设置坐标轴标签
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    
    # 调整视角
    ax.view_init(elev=10, azim=10)  # elev控制上下视角，azim控制左右旋转
    
    # 设置图形标题
    plt.title('3D Scatter Plot by Root Category')
    
    # 保存图形为PNG文件
    plt.savefig(file_dir + '3d_scatter_plot.png')

import sys
if __name__ == '__main__':
    arguments = sys.argv[1:]
    sample = arguments[0]

    plot_3d_scatter(f'./{sample}/')