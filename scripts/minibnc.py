import sys

PATH = '/Users/vene/bnc/similes/{}/'.format(sys.argv[1])

from glob import glob
from codecs import open
from yaml import dump, load
from pyglarf import GlarfTree
from compattern.pyglarf_args import get_args, find_comparison_nodes
from compattern.dependency import match
from compattern.dependency.seed_patterns import patterns

from compattern.dependency.conll import read
dep_parse = read(open('../data/bnc_{}_lemma.conll'.format(sys.argv[1])),
                 return_tree=True)
examples = []
for f in glob(PATH + '*.yaml'):
    f = open(f, encoding='utf-8')
    examples.extend(load(f))

sents, ctxs, gfs, gts = zip(*examples)
f = None
only_glarf = open("bnc_similes/{}/only_glarf.txt".format(sys.argv[1]), "w",
                  encoding="utf-8")
only_dep = open("bnc_similes/{}/only_dep.txt".format(sys.argv[1]), "w",
                encoding="utf-8")
matches = 0
dep_matches = 0
for ii, (sent, ctx, gf, gt, dep) in enumerate(zip(sents, ctxs, gfs, gts,
                                                  dep_parse)):
    dep = dep[1]
    if ii % 20 == 0:
        print '.'
        if f:
            f.close()
        f = open('bnc_similes/{}/{:03d}.txt'.format(sys.argv[1], ii / 20), 'w',
                 encoding='utf-8')
    try:
        tree = GlarfTree.glarf_parse(gf, gt)
        args = [get_args(*node) for node in find_comparison_nodes(tree)]
        args = [arg_dict for arg_dict in args
                if arg_dict['C'].lower() == sys.argv[1]
                and 'V' in arg_dict and arg_dict['V'].strip() != ""]
    except ValueError:
        args = []
        continue

    dep_args = [m for pat in patterns[:2] for m in match(dep, pat)
                if m['C'].form.lower() == sys.argv[1]]

    if args:
        matches += 1
    if dep_args:
        dep_matches += 1

    print_to = [f]
    if args and not dep_args:
        print_to.append(only_glarf)
    elif dep_args and not args:
        print_to.append(only_dep)

    for dest in print_to:
        print >> dest, sent
        print >> dest
        print >> dest, "Glarf:"
        for arg in args:
            print >> dest, "T: {T}\nE: {E}\nP: {P}\nC: {C}\nV: {V}\n".format(
                **arg)
        print >> dest, "\nDep:"
        for arg in dep_args:
            arg = {key: unicode(val.form, errors="ignore")
                   for key, val in arg.iteritems()}
            for K in 'TEPCV':
                if K not in arg:
                    arg[K] = '--'
            print >> dest, "T: {T}\nE: {E}\nP: {P}\nC: {C}\nV: {V}\n".format(
                **arg)
        print >> dest, "==="

print matches
print dep_matches
