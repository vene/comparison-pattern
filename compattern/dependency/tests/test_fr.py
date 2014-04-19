# encoding: utf8
from nose.tools import assert_greater

from compattern.dependency.conll import read
from compattern.dependency import match
from compattern.dependency.fr_patterns import aussi

ex_aussi = u"""\
1   Au  à   P+D P+D s=def   1111111 0   root    _   _
2   XIe XIe A   ADJ s=ord   _   3   mod _   _
3   siècle  siècle  N   NC  g=m|n=s|s=c 0101001 1   obj _   _
4   ,   ,   PONCT   PONCT   s=w _   0   root    _   _
5   le  le  D   DET g=m|n=s|s=def   100 6   det _   _
6   comte   comte   N   NC  g=m|n=s|s=c 0011111 0   root    _   _
7   de  de  P   P   _   11110   6   dep _   _
8   Bar Bar N   NPP g=m|n=s|s=p 0101011 7   obj _   _
9   ruine   ruine   N   NC  g=f|n=s|s=c 0011100 8   mod _   _
10  le  le  D   DET g=m|n=s|s=def   100 12  det _   _
11  puissant    puissant    A   ADJ g=m|n=s|s=qual  0100100 12  mod _   _
12  évêque  évêque  N   NC  g=m|n=s|s=c 0010101 8   mod _   _
13  de  de  P   P   _   11110   12  dep _   _
14  Verdun  Verdun  N   NPP g=m|n=s|s=p 0101011 13  obj _   _
15  ,   ,   PONCT   PONCT   s=w _   8   ponct   _   _
16  dont    dont    PRO PROREL  s=rel   1100101 19  de_obj  _   _
17  la  le  D   DET g=f|n=s|s=def   100 18  det _   _
18  monnaie monnaie N   NC  g=f|n=s|s=c 0011100 19  suj _   _
19  est être    V   V   m=ind|n=s|p=3|t=pst 1101011 8   mod_rel _   _
20  aussi   aussi   ADV ADV _   1100010 21  mod _   _
21  solide  solide  A   ADJ n=s|s=qual  0100100 19  ats _   _
22  que que C   CS  s=s 1100101 21  dep _   _
23  les le  D   DET n=p|s=def   100 24  det _   _
24  convictions conviction  N   NC  g=f|n=p|s=c 0011111 22  obj _   _
25  religieuses religieux   A   ADJ g=f|n=p|s=qual  0100101 24  mod _   _
26  .   .   PONCT   PONCT   s=s _   6   ponct   _   _\
"""

ex_aussi = ["\t".join(line.split()) for line in ex_aussi.split("\n")] + ["\n"]


def test_aussi_lemma():
    sent, root = read(ex_aussi, return_tree=True)[0]
    matches = match(root, aussi)
    assert_greater(len(matches), 0)
