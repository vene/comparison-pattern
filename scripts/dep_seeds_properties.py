from __future__ import print_function
import fileinput

from compattern.dependency import match
from compattern.dependency.seed_patterns import patterns


def _lemma_or_form(tok):
    return tok.form.lower() if tok.lemma == '_' else tok.lemma.lower()

if __name__ == '__main__':
    from compattern.dependency.conll import read
    from compattern.resources.therex import shared_category, poetic_properties

    from pprint import pprint
    sents = read(fileinput.input(), return_tree=True)
    n_matches = 0
    for sent, root in sents:
        matches = [m for pat in patterns for m in match(root, pat)]
        if matches:
            n_matches += len(matches)
            print(" ".join(tok.form for tok in sent))
            for m in matches:
                pprint(m)
                V_head = _lemma_or_form(m['V'])
                print(poetic_properties(V_head))
                if 'T' in m:
                    T_head = _lemma_or_form(m['T'])
                    print("{} x {}".format(T_head, V_head))
                    print(shared_category(T_head, V_head))
    print(n_matches)
