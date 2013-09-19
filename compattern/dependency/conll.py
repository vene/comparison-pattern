"""
CoNLL reader

Factored out from the project conllx-to-tikz-dep
https://github.com/tetsuok/conllx-to-tikz-dep
"""

# Author: Tetsuo Kiso <tetsuo-s@is.naist.jp>
# License: New BSD


matrix_separator = '\^'
special_chars = ['{', '}', '$', '&', '%']


class Token(object):
    def __init__(self):
        self.id = None
        self.form = None
        self.lemma = None
        self.cpos = None
        self.pos = None
        self.feat = None
        self.head = None
        self.deprel = None
        self.phead = None
        self.pdeprel = None

    def is_root(self):
        return self.head == 0 or self.head == -1

    def __repr__(self):
        #return "Token({})".format(self.__dict__)
        repr = "Token(id={id}, form={form}, pos={pos}, deprel={deprel})"
        return repr.format(**self.__dict__)


class Sentence(object):

    def __init__(self):
        self.tokens = []
        self.length = 0

    def __getitem__(self, i):
        return self.tokens[i]

    def __setitem__(self, i, t):
        self.tokens[i] = t

    def add(self, t):
        self.tokens.append(t)
        self.length += 1

    def length(self):
        return self.length

    def __str__(self):
        return ' '.join([v.form for v in self.tokens])

    def to_deptext(self):
        base = ' %s ' % matrix_separator
        s = base.join([v.form for v in self.tokens]) + ' \\\\'
        return s

    # returns a tuple of (head, dependent)
    def iterate_edges(self):
        for t in self.tokens:
            if t.is_root():
                continue
            yield (t.id, t.head)

    def iterate_labeled_edges(self):
        for t in self.tokens:
            if t.is_root():
                continue
            yield (t.id, t.head, t.deprel)

    def zip(self, other):
        for tup in zip(self.tokens, other.tokens):
            if len(tup) != 2:
                raise ValueError("Invalid input: {!r}".format(tup))
            elif tup[0].is_root() and tup[1].is_root:
                continue
            yield ((tup[0].id, tup[0].head), (tup[1].id, tup[1].head))


def replace_special(s):
    for c in special_chars:
        s = s.replace(c, '\\' + c)
    return s


def init_token(lis, is_conllx=True):
    t = Token()
    t.id = int(lis[0])
    t.form = replace_special(lis[1])

    t.lemma = lis[2]
    t.cpos = lis[3]
    t.pos = lis[4]
    t.feat = lis[5]
    t.head = int(lis[6])

    if lis[7] == '_':
        t.deprel = ''
    else:
        t.deprel = lis[7]

    if is_conllx:
        t.phead = lis[8]
        t.pdeprel = lis[9]
    return t


def conll_sent_to_tree(sent):
    """Reverses the bottom-up representation to produce a root-centred tree"""
    reverse_deps = [[] for _ in xrange(len(sent.tokens))]
    for fro, to in sent.iterate_edges():
        reverse_deps[to - 1].append(fro - 1)
    root = None
    for i, k in enumerate(sent):
        k.kids = [sent[kid_idx] for kid_idx in reverse_deps[i]]
        if k.is_root():
            root = k
    if not root:
        raise ValueError("Sentence does not have a root: {}".format(
            " ".join(t.form for t in sent.tokens)))
    return root


def open_conll(filename):
    with open(filename) as f:
        return read(f)


def read(f, return_tree=False):
    sents = []
    s = Sentence()
    for l in f:
        if l.startswith('\n'):
            if return_tree:
                s = (s, conll_sent_to_tree(s))
            sents.append(s)
            s = Sentence()
            continue

        lis = l.rstrip().split('\t')
        if len(lis) == 1:
            lis = l.rstrip().split(' ')
        if len(lis) == 0:
            continue
        elif len(lis) == 8:
            s.add(init_token(lis, False))
        elif len(lis) == 10:
            s.add(init_token(lis))
        else:
            raise ValueError('Data format is broken!')
    return sents
