import argparse
import pickle
from anytree import Node


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", help="path of nodes.dmp", default='nodes.dmp')
    parser.add_argument("--output", help="save tree to this file", default='nodes.pkl')
    args = parser.parse_args()

    nodes = {}
    with open('nodes.dmp') as f:
        for line in f.readlines():
            cells = line.split('|')
            tax_id = cells[0].strip()
            parent_id = cells[1].strip()
            rank = cells[2].strip()
            nodes[tax_id] = Node(tax_id, tax_id=tax_id, parent_id=parent_id, rank=rank)

    for n in nodes:
        node = nodes[n]
        if node.parent_id is not node.tax_id:
            node.parent = nodes[node.parent_id]

    with open(args.output, 'wb') as f:
        pickle.dump(nodes, f)


if __name__ == '__main__':
    main()
