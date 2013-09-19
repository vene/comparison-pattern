from compattern.dependency import Slot

like = (None, lambda pos: pos.startswith('VB'), None,
        Slot(label="E", required=True),
        [
            ('like', 'IN', None, Slot(label="C", required=True),
             [
                 (None, None, 'PMOD', Slot(label="V", required=True), [])
             ]),
            (None, None, 'SUB', Slot(label="T", required=False), []),
            (None, None, 'PRD', Slot(label="P", required=False), [])
        ])

like_tr = (None, lambda pos: pos.startswith('VB'), None, Slot(label="_E"),
           [
               (None, lambda pos: pos.startswith('VB'), 'VC',
                Slot(label="E", required=True),
                [
                    ('like', 'IN', None, Slot(label="C", required=True),
                     [
                         (None, None, 'PMOD', Slot(label="V", required=True),
                          [])
                     ]),
                    (None, None, 'PRD', Slot(label="P", required=False), [])
                ]),
          (None, None, 'SUB', Slot(label="T", required=False), [])])

as_1 = (None, lambda pos: pos.startswith('VB'), None,
        Slot(label="E", required=True),
        [
            (None, None, 'SUB', Slot(label="T", required=False), []),
            (None, None, 'PRD', Slot(label="P", required=True),
             [
                 ('as', 'RB', 'AMOD', Slot(label="_C", required=True), []),
                 ('as', 'IN', 'AMOD', Slot(label="C", required=True),
                  [
                      (None, None, None, Slot(label='V', required=True), [])
                  ])
             ])
        ])

as_2 = (None, lambda pos: pos.startswith('VB'), None,
        Slot(label="E", required=True),
        [
            (None, None, 'SUB', Slot(label="T", required=False), []),
            ('as', 'IN', 'VMOD', Slot(label="_C", required=True),
             [
                 (None, None, None, Slot(label='P', required=True), [])
             ]),
            ('as', 'IN', 'VMOD', Slot(label="C", required=True),
             [
                 (None, None, None, Slot(label='V', required=True), [])
             ])
        ])

as_3 = (None, lambda pos: pos.startswith('VB'), None,
        Slot(label="E", required=True),
        [
            (None, None, 'SUB', Slot(label="T", required=False), []),
            ('as', 'RB', 'VMOD', Slot(label="_C", required=True),
             [
                 (None, None, 'AMOD', Slot(label="P", required=True), []),
                 ('as', 'IN', 'AMOD', Slot(label="C", required=True),
                  [
                      (None, None, None, Slot(label="V", required=True), [])
                  ])
             ])
        ])

patterns = [like, like_tr, as_1, as_2, as_3]
