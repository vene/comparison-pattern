""" Match comparisons from parsed corpus

This script shows the simple way of using this package to extract
comparisons from a parsed English corpus.
For example, you can run it against the 'data/hanks_tp_lemma.conll' file
provided.

By default this prints the dependency root of each comparison slot (topic,
vehicle, etc) but the entire subtrees are extracted and available.
"""
from __future__ import print_function
import fileinput

from compattern.dependency import match
from compattern.dependency.seed_patterns import patterns


def _lemma_or_form(tok):
    return tok.form.lower() if tok.lemma == '_' else tok.lemma.lower()

if __name__ == '__main__':
    from compattern.dependency.conll import read

    sents = read(fileinput.input(), return_tree=True)
    for sent, root in sents:
        print(sent)
        for pat in patterns:
            for m in match(root, pat):
                print("\n".join("{}: {}".format(key, val.form)
                                for key, val in m.items()))
                print()
