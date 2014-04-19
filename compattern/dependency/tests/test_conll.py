# encoding: utf8

from compattern.dependency import conll


def test_read_french():
    """Test that conll.read understands French Bonsai output"""
    line = (u"6\tchauffé\tchauffer\tV\tVPP\tg=m|m=part|n=s|t=past\t"
            u"1100011\t5\tdep_coord\t_\t_")
    sentence = conll.read([line, '\n'])[0]
    assert len(sentence) == 1
    token = sentence[0]
    assert token.id == 6
    assert token.lemma == "chauffer"
    assert token.cpos == "V"
    assert token.pos == "VPP"
    assert token.feat[0].startswith("g=m")  # morpho features
    assert token.feat[1].startswith("110")  # cluster path
    assert token.head == 5
    assert token.deprel == "dep_coord"
    # Don't really care what happens with undefined phead and pdeprel


def test_read_turboparser():
    line = "11\tvaccines\tvaccine\tNNS\tNNS\t_\t10\tPMOD"
    sentence = conll.read([line, '\n'])[0]
    assert len(sentence) == 1
    token = sentence[0]
    assert token.id == 11
    assert token.form == "vaccines"
    assert token.lemma == "vaccine"
    assert token.cpos == "NNS"
    assert token.pos == "NNS"
    assert token.head == 10
    assert token.deprel == "PMOD"


def test_read_wacky():
    line = "was\tbe\tVBD\t18\t11\tPRD"
    sentence = conll.read([line, '\n'])[0]
    assert len(sentence) == 1
    token = sentence[0]
    assert token.id == 18
    assert token.form == "was"
    assert token.lemma == "be"
    assert token.pos == "VBD"
    assert token.head == 11
    assert token.deprel == "PRD"
