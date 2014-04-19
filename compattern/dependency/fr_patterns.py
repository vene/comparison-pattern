""" French language comparison patterns

Designed based on Bonsai parser output using the Est Republicain corpus
"""

_cmp_lemmas = lambda lemma: lemma in ["aussi", "plus", "moins"]

comme = dict(slot="E",
             cpos="V",
             kids=[
                 dict(slot="C",
                      lemma="comme",
                      pos="P",
                      deprel="mod",
                      kids=[dict(slot="V",
                                 deprel="obj",
                                 cpos="N",
                                 kids=[dict(slot="V_", deprel="det")],
                                 )]),
                 dict(slot="T",
                      optional=True,
                      deprel="suj",
                      cpos=lambda x: x in ["N", "CL"])
             ])

comme_pr = dict(slot="E",
                cpos="V",
                kids=[
                    dict(slot="C",
                         lemma="comme",
                         pos="P",
                         deprel="mod",
                         kids=[dict(slot="V",
                                    deprel="obj",
                                    cpos="CL"
                                    )]),
                    dict(slot="T",
                         optional=True,
                         deprel="suj",
                         cpos=lambda x: x in ["N", "CL"])
                ])

aussi = dict(slot="E",
             cpos="V",
             kids=[dict(slot="T",
                        optional=True,
                        deprel="suj"),
                   dict(slot="P",
                        deprel="ats",
                        kids=[dict(slot="C",
                                   lemma=_cmp_lemmas,
                                   pos="ADV",
                                   deprel="mod"),
                              dict(slot="C_",
                                   lemma="que",
                                   kids=[dict(slot="V", deprel="obj")])
                              ])
                   ])

patterns = [comme, comme_pr, aussi]
