import csv
from collections import defaultdict

def find_roots(input_path, output_path):
    # 读取数据并建立父子关系字典
    ancestor_map = {}
    with open(input_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        rows = [row for row in reader]  # 先缓存所有行数据
        fieldnames = reader.fieldnames + ['root']  # 添加新列

    # 建立ID到祖先的映射
    for row in rows:
        ancestor_map[row['id']] = row['ancestor']

    # 缓存已找到的根节点
    root_cache = {}

    # 递归查找根节点函数
    def get_root(node_id):
        ancestor = ancestor_map.get(node_id, '-1')
        if ancestor == '-1':  # 找到根节点
            return node_id
        if node_id not in root_cache:
            root_cache[node_id] = get_root(ancestor)
        return root_cache[node_id]

    # 为每行添加root列并按id升序排列
    for row in rows:
        row['root'] = get_root(row['id'])
    
    # 按id升序排序
    sorted_rows = sorted(rows, key=lambda x: int(x['id']))

    # 写入结果文件
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(sorted_rows)

import pandas as pd

def process_tsv(input_path, output_path, N):
    # 读取TSV文件并按ID升序排列
    df = pd.read_csv(input_path, sep='\t').sort_values('id')

    # 获取所有birth==0的行
    birth_zero = df[df['birth'] == 0]
    
    # 如果总行数大于N，保留最后N行
    if len(birth_zero) > N:
        to_keep = birth_zero.tail(N)
        to_remove = birth_zero.iloc[:-N]
        # 删除这些行
        df = df.drop(to_remove.index)
    else:
        to_keep = birth_zero
    
    # 修改保留行的ancestor为-1
    df.loc[to_keep.index, 'ancestor'] = -1
    
    # 保存结果
    df.to_csv(output_path, sep='\t', index=False)


import sys

if __name__ == '__main__':
    arguments = sys.argv[1:]
    N = int(arguments[0])
    sample = arguments[1]
    process_tsv(f'{sample}/population.tsv', f'{sample}/processed_population.tsv', N)
    find_roots(f'./{sample}/processed_population.tsv', f'{sample}/population_with_roots.tsv')
