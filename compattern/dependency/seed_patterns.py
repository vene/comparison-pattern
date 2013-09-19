like = dict(slot="E",
            pos=lambda pos: pos.startswith('VB'),
            kids=[
                dict(slot="C",
                     form='like',
                     pos='IN',
                     kids=[dict(slot="V",
                                deprel='PMOD')
                           ]),
                dict(slot="T",
                     deprel='SUB',
                     optional=True),
                dict(slot='P',
                     optional=True,
                     deprel='PRD'),
            ])

like_tr = dict(slot='_E',
               pos=lambda pos: pos.startswith('VB'),
               kids=[
                   dict(slot='E',
                        pos=lambda pos: pos.startswith('VB'),
                        deprel='VC',
                        kids=[
                            dict(slot='C',
                                 form='like', pos='IN',
                                 kids=[dict(slot='V', deprel='PMOD')]),
                            dict(slot='P',
                                 deprel='PMOD', optional=True)
                        ]),
                   dict(slot='T',
                        optional=True,
                        deprel='SUB')
               ])

as_1 = dict(slot='E',
            pos=lambda pos: pos.startswith('VB'),
            kids=[
                dict(slot='T',
                     deprel='SUB', optional=True),
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
            pos=lambda pos: pos.startswith('VB'),
            kids=[
                dict(slot='T',
                     deprel='SUB', optional=True),
                dict(slot='_C',
                     form='as', pos='IN', deprel='VMOD',
                     kids=[dict(slot='P')]),
                dict(slot='C',
                     form='as', pos='IN', deprel='VMOD',
                     kids=[dict(slot='V')])
            ])


as_3 = dict(slot='E',
            pos=lambda pos: pos.startswith('VB'),
            kids=[
                dict(slot='T',
                     deprel='SUB', optional=True),
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

patterns = [like, like_tr, as_1, as_2, as_3]
