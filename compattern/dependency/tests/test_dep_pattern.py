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

# Kind of hand modified
example_like_t1 = \
    ['A\ta\tDT\t1\t3\tNMOD',
     'configuration\tconfiguration\tNN\t2\t3\tNMOD',
     'file\tfile\tNN\t3\t4\tSBJ',
     'could\tcould\tMD\t4\t0\tROOT',
     'look\tlook\tVV\t5\t4\tVC',
     'like\tlike\tIN\t6\t5\tADV',
     'this\tthis\tDT\t7\t6\tPMOD',
     '\n']

example_like_t2 = \
    ['A\ta\tDT\t1\t3\tNMOD',
     'configuration\tconfiguration\tNN\t2\t3\tNMOD',
     'file\tfile\tNN\t3\t4\tSBJ',
     'could\tcould\tMD\t4\t0\tROOT',
     'look\tlook\tVV\t5\t4\tVC',
     'like\tlike\tIN\t6\t4\tADV',
     'this\tthis\tDT\t7\t6\tPMOD',
     '\n']

example_rbr = \
    ['in\tin\tIN\t1\t4\tAMOD',
     'reality\treality\tNN\t2\t1\tPMOD',
     'more\tmore\tRBR\t3\t4\tAMOD',
     'often\toften\tRB\t4\t8\tADV',
     'than\tthan\tIN\t5\t4\tAMOD',
     'not\tnot\tRB\t6\t5\tPMOD',
     'they\tthey\tPP\t7\t8\tSBJ',
     'should\tshould\tMD\t8\t0\tROOT',
     'have\thave\tVH\t9\t8\tVC',
     'left\tleave\tVVN\t10\t9\tVC',
     'it\tit\tPP\t11\t13\tSBJ',
     'the\tthe\tDT\t12\t13\tNMOD',
     'way\tway\tNN\t13\t10\tOBJ',
     'it\tit\tPP\t14\t15\tSBJ',
     'was\tbe\tVBD\t15\t13\tNMOD',
     '\n']


example_jjr = \
    ['That\tthat\tDT\t1\t2\tSBJ',
     "'s\tbe\tVBZ\t2\t0\tROOT",
     'better\tgood\tJJR\t3\t2\tPRD',
     'than\tthan\tIN\t4\t3\tAMOD',
     'opening\topen\tVVG\t5\t4\tPMOD',
     'up\tup\tRP\t6\t5\tPRT',
     'a\ta\tDT\t7\t9\tNMOD',
     'huge\thuge\tJJ\t8\t9\tNMOD',
     'range\trange\tNN\t9\t5\tOBJ',
     'of\tof\tIN\t10\t9\tNMOD',
     'ports\tport\tNNS\t11\t10\tPMOD',
     '.\t.\tSENT\t12\t2\tP',
     '\n']


example_as = \
    ['Scenically\tscenically\tRB\t1\t4\tADV',
     ',\t,\t,\t2\t4\tP',
     'it\tit\tPP\t3\t4\tSBJ',
     "'s\tbe\tVBZ\t4\t0\tROOT",
     'not\tnot\tRB\t5\t4\tVMOD',
     'as\tas\tIN\t6\t8\tVMOD',
     'immediately\timmediately\tRB\t7\t8\tADV',
     'appealing\tappeal\tVVG\t8\t4\tVC',
     'as\tas\tIN\t9\t8\tADV',
     'some\tsome\tDT\t10\t9\tPMOD',
     'of\tof\tIN\t11\t10\tNMOD',
     'the\tthe\tDT\t12\t14\tNMOD',
     'other\tother\tJJ\t13\t14\tNMOD',
     'islands\tisland\tNNS\t14\t11\tPMOD',
     '-\t-\t:\t15\t10\tP',
     'as\tas\tIN\t16\t19\tVMOD',
     'the\tthe\tDT\t17\t18\tNMOD',
     'plane\tplane\tNN\t18\t19\tSBJ',
     'comes\tcome\tVVZ\t19\t8\tADV',
     'in\tin\tIN\t20\t19\tADV',
     'to\tto\tTO\t21\t22\tVMOD',
     'land\tland\tVV\t22\t19\tADV',
     'the\tthe\tDT\t23\t24\tNMOD',
     'interior\tinterior\tNN\t24\t22\tOBJ',
     'looks\tlook\tVVZ\t25\t19\tCOORD',
     'quite\tquite\tRB\t26\t27\tAMOD',
     'flat\tflat\tJJ\t27\t25\tPRD',
     ',\t,\t,\t28\t27\tP',
     'dry\tdry\tJJ\t29\t27\tCOORD',
     'and\tand\tCC\t30\t27\tCC',
     'parched\tparched\tJJ\t31\t27\tCOORD',
     '.\t.\tSENT\t32\t4\tP',
     '\n']


def test_like():
    sent, root = read(example_like, return_tree=True)[0]
    matches = match(root, seed_patterns.like)
    assert_greater(len(matches), 0)
    assert_in('T', matches[0].keys())


def test_like_t1():
    sent, root = read(example_like_t1, return_tree=True)[0]
    matches = match(root, seed_patterns.like_t1)
    assert_greater(len(matches), 0)


def test_like_t2():
    sent, root = read(example_like_t2, return_tree=True)[0]
    matches = match(root, seed_patterns.like_t2)
    assert_greater(len(matches), 0)


def test_than():
    sent, root = read(example_rbr, return_tree=True)[0]
    matches = match(root, seed_patterns.than_2)
    assert_greater(len(matches), 0)


def test_jjr():
    sent, root = read(example_jjr, return_tree=True)[0]
    matches = match(root, seed_patterns.than_1)
    assert_greater(len(matches), 0)


def test_as():
    sent, root = read(example_as, return_tree=True)[0]
    matches = match(root, seed_patterns.as_1)
    assert_greater(len(matches), 0)
