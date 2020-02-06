from pyglarf import GlarfTree

def _safe_filter_comparator(node_or_string):
    """Returns True when passed a comparison trigger node, False elsewhere"""
    return (hasattr(node_or_string, 'node') and node_or_string.node == 'IN' and
            node_or_string[0] == 'like')

def _safe_filter_as_unary(arg):
    anchor = arg[arg.leaf_treeposition(0)[:-1]]
    return hasattr(anchor, 'node') and anchor.node == 'IN' and anchor[0] == 'as'


def _safe_head(node):
    if (hasattr(node, 'head')):
        head = node.head()
        if head:
            return head[0]


def _get_sbj(rel):
    for role_a, role_b, _, arg_tree in list(rel.args.values()):
        if (any('SBJ' in role for role in role_a) or 'SBJ' in role_b) and (
                arg_tree is not None):
            return arg_tree


def find_comparison_nodes(tree):
    comparison_nodes = []
    for rel in tree.rels():
        for _, _, _, arg_trees in list(rel.args.values()):
            for arg_tree in arg_trees:
                if _safe_filter_comparator(_safe_head(arg_tree[0])):
                    comparison_nodes.append((rel, arg_tree))
                #if _safe_filter_as_unary(arg_tree):
                #    comparison_nodes.append((rel, arg_tree))
        for _, _, arg_tree in list(rel.advs.values()):
            if _safe_filter_comparator(_safe_head(arg_tree)):
                comparison_nodes.append((rel, arg_tree))
            if _safe_filter_as_unary(arg_tree):
                comparison_nodes.append((rel, arg_tree))
            #for pos in arg_tree.treepositions():
                #    if _safe_filter_comparator(arg_tree[pos]):
                #        comparison_nodes.append((rel, arg_tree))
    return comparison_nodes


def get_args(rel, comparison_arg):
    try:
        sbj = _get_sbj(rel)[0].most_specific_head()
        if len(comparison_arg) > 1:
            veh = comparison_arg[1].most_specific_head()
        else:
            veh = comparison_arg[0][1].most_specific_head()
        if comparison_arg.node == 'ADJP':
            gnd = comparison_arg.head()[0].head()
            veh = comparison_arg[1, 0, 1, 0, 1, 0].head()
        elif comparison_arg[0].node == 'ADJP':
            gnd = comparison_arg.most_specific_head()
            veh = comparison_arg[0, 1, 0, 1, 0, 1, 0].head()
        else:
            gnd = None  # we accept partial matches that don't find the gnd
    except:
        sbj = GlarfTree('', [])
        veh = GlarfTree('', [])
        gnd = None
    return {
        'T': sbj[0].print_flat(False, False, False, False) if sbj else "",
        'E': rel.head,
        'C': comparison_arg.leaves()[0],
        'V': veh.print_flat(False, False, False, False) if veh else "",
        'P': gnd.print_flat(False, False, False, False) if gnd else "",
    }

def wn_categ(args):
    from nltk import wordnet
    from nltk.stem import WordNetLemmatizer
    lmtzr = WordNetLemmatizer()
    sbj = lmtzr.lemmatize(args['T'].lower())
    veh = lmtzr.lemmatize(args['V'].lower())
    return (wordnet.wordnet.lemmas(sbj),
            wordnet.wordnet.lemmas(veh))
