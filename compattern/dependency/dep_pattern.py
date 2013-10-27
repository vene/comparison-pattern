from itertools import product


def _iter_pattern(pattern):
    bag = [pattern]
    while bag:
        curr_p = bag.pop()
        yield curr_p
        kids = curr_p.get('kids', [])
        bag.extend([kid for kid in kids if kid])


def _iter_deptree(root):
    bag = [root]
    while bag:
        curr_token = bag.pop()
        yield curr_token
        if hasattr(curr_token, 'kids'):
            bag.extend(curr_token.kids)


def _match(node, pattern):
    def _local_match():
        match = True
        form = pattern.get('form')
        pos = pattern.get('pos')
        deprel = pattern.get('deprel')
        for query, data in zip([form, pos, deprel],
                               [node.form, node.pos, node.deprel]):
            if query is not None:
                if hasattr(query, '__call__'):  # callable matcher
                    match = query(data)
                elif hasattr(query, 'lower'):  # string matcher
                    match = query.lower() == data.lower()
                else:
                    raise ValueError("Match value {query!r} unsupported in "
                                     "pattern {pattern!r}. Please provide "
                                     "either a string or a bool-returning "
                                     "callable.".format(query=query,
                                                        pattern=pattern))
            if not match:
                break
        return match

    required_slots = [subpattern['slot']
                      for subpattern in _iter_pattern(pattern)
                      if not subpattern.get('optional', False)]

    kid_matches = []
    all_matches = []
    if _local_match():
        slot = pattern.get('slot')
        for kid in pattern.get('kids', []):
            this_kid_matches = [m for k in node.kids for m in _match(k, kid)]
            this_kid_matches = filter(lambda x: x is not None,
                                      this_kid_matches)
            if this_kid_matches or not kid.get('optional', False):
                                    # uglyish; means: don't append optional
                                    # slots
                kid_matches.append(this_kid_matches)

        for assignment in product(*kid_matches):
            incompatible_duplicate = False
            d = {slot: node}
            for kid_match in assignment:
                for label, matched_tok in kid_match.items():
                    add_it = True
                    for other_label, other_tok in d.items():
                        if matched_tok == other_tok:
                            if other_label in required_slots:
                                if label in required_slots:
                                    incompatible_duplicate = True
                                add_it = False
                            else:
                                del d[other_label]
                    if incompatible_duplicate:
                        break
                    if add_it:
                        d[label] = matched_tok
                if incompatible_duplicate:
                    continue
            #if len(d) != len(set([item.id for item in d.values()])):
            #    # A node was matched twice and this is not cool
            #    continue
            if all(slot in d.keys() for slot in required_slots):
                all_matches.append(d)
    return all_matches


def match(tree, pattern):
    """Matches the pattern against all nodes in tree"""
    matches = [_match(node, pattern) for node in _iter_deptree(tree)]
    return [m for local_matches in matches for m in local_matches]
