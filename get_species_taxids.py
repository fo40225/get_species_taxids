import argparse
import pickle
import sys

from anytree import LevelOrderIter, Walker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help=" a file contains taxonomy ID pre line will get taxonomy IDs at specific taxonomy rank level ")
    parser.add_argument("-l", "--level", help=" ncbi taxonomy rank level ", default='species', required=False)
    parser.add_argument("--tree", help=" prebuild tree path ", default='nodes.pkl', required=False)
    parser.add_argument("--merged", help=" merged.tmp ", default='merged.dmp', required=False)
    parser.add_argument("--expand", help=" expand the result to the last leaf ", action="store_true")
    args = parser.parse_args()

    with open(args.tree, 'rb') as f:
        nodes = pickle.load(f)

    root = nodes['1']
    w = Walker()
    results = set()
    dict_merged = {}

    with open(args.t) as t:
        for line in t.readlines():
            taxid = line.strip('\n')

            node = nodes.get(taxid)
            if node is None:
                if len(dict_merged) == 0:
                    with open(args.merged) as f:
                        for l in f.readlines():
                            cells = l.split('|')
                            old_id = cells[0].strip()
                            new_id = cells[1].strip()
                            dict_merged[old_id] = new_id

                new_taxid = dict_merged.get(taxid)
                node = nodes.get(new_taxid)

                if node is None:
                    print(f"taxid not found: {taxid}", file=sys.stderr)
                    continue

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

    if args.expand:
        new_result = set()
        for id in results:
            n = nodes.get(id)
            for child in LevelOrderIter(n):
                new_result.add(child.tax_id)
        results = new_result

    for r in results:
        print(r)


if __name__ == '__main__':
    main()
