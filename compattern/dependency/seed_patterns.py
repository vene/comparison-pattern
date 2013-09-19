from __future__ import print_function

from compattern.dependency import Slot, match

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
as_ = (None, lambda pos: pos.startswith('VB'), None,
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

patterns = [like, like_tr, as_]

if __name__ == '__main__':
    from compattern.dependency.conll import read
    from compattern.resources.therex import shared_category, poetic_properties

    from pprint import pprint
    with open("/Users/vene/Dropbox/similes_2013/data/"
              "hanks_turboparsed/hanks_turboparsed.txt") as f:
        vuamc = read(f, return_tree=True)
                     #"/hanks_rest.txt")
    #vuamc = open_conll("/Users/vene/corpora/2541/vuamc.conll")
    #vuamc = open_conll("/Users/vene/code/conll-depchunks/property.txt")
    n_matches = 0
    for sent, root in vuamc:
        matches = [m for pat in patterns for m in match(root, pat)]
        if matches:
            n_matches += len(matches)
            print(" ".join(tok.form for tok in sent))
            for m in matches:
                pprint(m)
                V_head = m['V'].form.lower()
                print(poetic_properties(V_head))
                if 'T' in m:
                    T_head = m['T'].form.lower()
                    print("{} x {}".format(T_head, V_head))
                    print(shared_category(T_head, V_head))
    #print(n_matches)
