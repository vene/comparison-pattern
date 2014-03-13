# common lambdas:
is_verb = lambda pos: pos.startswith('V')
is_subject = lambda dep: dep in ['SUB', 'SBJ']

like = dict(slot="E",
            pos=is_verb,
            kids=[
                dict(slot="C",
                     form='like',
                     pos='IN',
                     kids=[dict(slot="V",
                                deprel='PMOD')
                           ]),
                dict(slot="T",
                     deprel=is_subject,
                     optional=True),
                dict(slot='P',
                     optional=True,
                     deprel='PRD'),
            ])

# transparent like 1: he may -> be <- dead
like_t1 = dict(slot='_E',
               pos='MD',
               kids=[
                   dict(slot='E',
                        pos=is_verb,
                        deprel='VC',
                        kids=[
                            dict(slot='C',
                                 form='like', pos='IN',
                                 kids=[dict(slot='V', deprel='PMOD')]),
                            dict(slot='P', deprel='PRD', optional=True)
                        ]),
                   dict(slot='T',
                        optional=True,
                        deprel=is_subject)
               ])


# transparent like 1: he may <- be <- dead
like_t2 = dict(slot='_E',
               pos='MD',
               kids=[
                   dict(slot='E',
                        pos=is_verb,
                        deprel='VC',
                        kids=[dict(slot='P', deprel='PRD', optional=True)]),
                    dict(slot='C',
                         form='like', pos='IN',
                         kids=[dict(slot='V', deprel='PMOD')]),
                   dict(slot='T',
                        optional=True,
                        deprel=is_subject)
               ])


as_1 = dict(slot='E',
            pos=is_verb,
            kids=[
                dict(slot='T',
                     deprel=is_subject,
                     optional=True),
                dict(slot='P',
                     deprel='PRD',
                     kids=[
                         dict(slot='_C',
                              form='as', pos='RB', deprel='AMOD'),
                         dict(slot='C',
                              form='as', pos='IN', deprel='AMOD',
                              kids=[dict(slot='V')])
                     ])
            ])

as_2 = dict(slot='E',
            pos=is_verb,
            kids=[
                dict(slot='T',
                     deprel=is_subject,
                     optional=True),
                dict(slot='_C',
                     form='as', pos='IN', deprel='VMOD',
                     kids=[dict(slot='P')]),
                dict(slot='C',
                     form='as', pos='IN', deprel='VMOD',
                     kids=[dict(slot='V')])
            ])


as_3 = dict(slot='E',
            pos=is_verb,
            kids=[
                dict(slot='T',
                     deprel=is_subject,
                     optional=True),
                dict(slot='_C',
                     form='as', pos='RB', deprel='VMOD',
                     kids=[
                         dict(slot='P',
                              deprel='AMOD'),
                         dict(slot='C',
                              form='as', pos='IN', deprel='AMOD',
                              kids=[dict(slot='V')])
                     ])
            ])


# that's better than opening ...
than_1 = dict(slot='E',
              pos=is_verb,
              kids=[
                  dict(slot='T',
                       deprel=is_subject,
                       optional=True),
                  dict(slot='P',
                       pos='JJR',
                       kids=[dict(slot='C',
                                  form='than',
                                  pos='IN',
                                  kids=[dict(slot='V')])])
              ])


# that's more advanced than ...
# could be too general
than_2 = dict(slot='E',
              pos=is_verb,
              kids=[
                  dict(slot='T',
                       deprel=is_subject,
                       optional=True),
                  dict(slot='P',
                       kids=[
                           dict(slot='P_',
                                pos='RBR'),
                           dict(slot='C',
                                form='than',
                                pos='IN',
                                kids=[dict(slot='V')])])
              ])

patterns = [like, like_t1, like_t2, as_1, as_2, as_3, than_1, than_2]
