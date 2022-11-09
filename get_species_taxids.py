import argparse
import pickle
from anytree import Walker, LevelOrderIter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help=" a file contains taxonomy ID pre line will get taxonomy IDs at specific taxonomy rank level ")
    parser.add_argument("-l", "--level", help=" ncbi taxonomy rank level ", default='species', required=False)
    parser.add_argument("--tree", help=" prebuild tree path ", default='nodes.pkl', required=False)
    args = parser.parse_args()

    with open(args.tree, 'rb') as f:
        nodes = pickle.load(f)

    root = nodes['1']
    w = Walker()
    results = set()

    with open(args.t) as t:
        for line in t.readlines():
            taxid = line.strip('\n')
            node = nodes[taxid]

            if node.rank == args.level:
                results.add(node.tax_id)
                continue

            skip_child = False
            ancestors = w.walk(node, root)[0]
            for a in ancestors:
                if a.rank == args.level:
                    results.add(a.tax_id)
                    skip_child = True
                    break

            if skip_child:
                continue

            for child in LevelOrderIter(node):
                if child.rank == args.level:
                    results.add(child.tax_id)

    for r in results:
        print(r)


if __name__ == '__main__':
    main()
