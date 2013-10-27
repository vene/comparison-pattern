import fileinput

from compattern.dependency import match
from compattern.dependency.seed_patterns import patterns


def _lemma_or_form(tok):
    return tok.form.lower() if tok.lemma == '_' else tok.lemma.lower()

if __name__ == '__main__':
    from compattern.dependency.conll import read
    #from compattern.resources.therex import shared_category, poetic_properties

    from pprint import pprint
    sents = read(fileinput.input(), return_tree=True)
    n_matches = 0
    matchlist = []
    for k, (sent, root) in enumerate(sents):
        matches = [m for pat in patterns[:2] for m in match(root, pat)]
        print " ".join(tok.form for tok in sent)
        for m in matches:
            print m
        print
        if matches:
            matchlist.append(k)
    print(matchlist)
