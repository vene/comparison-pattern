#from __future__ import print_function

import cPickle
import sys
from compattern.dependency import match
from compattern.dependency.seed_patterns import patterns


class PUkWaC(object):
    def __iter__(self):
        buf = []
        sent = ""
        for f in self.files:
            print f
            for line in open(f):
                if line.startswith('<text'):
                    continue
                elif line.startswith('</text>'):
                    yield buf
                elif line.startswith('<s>'):
                    sent = ""
                elif line.startswith('</s>'):
                    buf.append(sent)
                else:
                    sent += line

    def __init__(self, files):
        self.files = files

if __name__ == '__main__':
    from compattern.dependency.conll import read

    corpus = PUkWaC(["/home/vniculae/corpora/pukwac/ukwac{}.xml".format(k)
                     for k in (1, 2, 3, 4, 5)])
    all_matches = []
    for nr, text in enumerate(corpus):
        text_l = "\n".join(text).lower()
        if not (text_l.startswith("like\t") or text_l.startswith("as\t") or
                "\nlike\t" in text_l or "\nas\t" in text_l):
            continue
        del text_l
        if nr % 100:
            sys.stdout.write(".")
            sys.flush()
        text = [k for sent in text for k in sent.split("\n")]
        text = filter(len, text)
        try:
            for sent, root in read(text, return_tree=True):
                matches = [m for pat in patterns for m in match(root, pat)]
                all_matches.extend(matches)
        except KeyboardInterrupt:
            break
    cPickle.dump(all_matches, open("wacky_matches.pkl", "w"), -1)
