# Query Thesaurus X

import urllib2
from xml.etree import cElementTree as ET

THEREX = "http://ngrams.ucd.ie/therex2/"
THEREX_SHARED = THEREX + "common-nouns/share.action?word1={}&word2={}&xml=true"
THEREX_POETIC = THEREX + "common-nouns/poetic.action?member={}&xml=true"

def shared_category(a, b):
    res = urllib2.urlopen(THEREX_SHARED.format(a, b))
    members = [(member.text.strip(), int(member.get('weight')))
               for member in ET.parse(res).find('Members')]
    members.sort(key=lambda x: x[1], reverse=True)
    return members


def poetic_properties(a):
    res = urllib2.urlopen(THEREX_POETIC.format(a))
    members = [(member.text.strip(), int(member.get('weight')))
               for member in ET.parse(res).find('PoeticQualities')]
    members.sort(key=lambda x: x[1], reverse=True)
    return members
