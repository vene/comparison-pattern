from nose.tools import assert_greater, assert_in

from compattern.dependency.conll import read
from compattern.dependency import match, seed_patterns

# taken straight from UK WACKY

example_like = \
    ['Go\tgo\tVV\t1\t0\tROOT\n',
     'to\tto\tTO\t2\t1\tADV\n',
     'Old\tOld\tNP\t3\t2\tPMOD\n',
     'Trafford\tTrafford\tNP\t4\t8\tADV\n',
     'now\tnow\tRB\t5\t4\tADV\n',
     ',\t,\t,\t6\t8\tP\n',
     'it\tit\tPP\t7\t8\tSBJ\n',
     "'s\tbe\tVBZ\t8\t1\tOBJ\n",
     'like\tlike\tIN\t9\t8\tPRD\n',
     'going\tgo\tVVG\t10\t9\tPMOD\n',
     'to\tto\tTO\t11\t10\tADV\n',
     'the\tthe\tDT\t12\t14\tNMOD\n',
     'fucking\tfuck\tVVG\t13\t14\tNMOD\n',
     'opera\topera\tNN\t14\t11\tPMOD\n',
     '.\t.\tSENT\t15\t1\tP\n',
     '\n']


def test_like():
    sent, root = read(example_like, return_tree=True)[0]
    matches = match(root, seed_patterns.like)
    assert_greater(len(matches), 0)
    assert_in('T', matches[0].keys())
