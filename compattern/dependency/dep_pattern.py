from itertools import product


class Slot(object):
    def __init__(self, label, required=False):
        self.label = label
        self.required = required


def _iter_pattern(pattern):
    bag = [pattern]
    while bag:
        curr_p = bag.pop()
        yield curr_p
        form, pos, role, slot, kids = curr_p
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
        form, pos, role, _, _ = pattern
        for query, data in zip([form, pos, role],
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

    required_slots = [slot.label
                      for _, _, _, slot, _ in _iter_pattern(pattern)
                      if slot.required]

    kid_matches = []
    all_matches = []

    if _local_match():
        _, _, _, slot, kids = pattern
        for kid in kids:
            this_kid_matches = [m for k in node.kids for m in _match(k, kid)]
            this_kid_matches = filter(lambda x: x is not None,
                                      this_kid_matches)
            _, _, _, kid_slot, _ = kid
            if this_kid_matches or (hasattr(kid_slot, 'required') and
                                    kid_slot.required):
                                    # uglyish; means: don't append optional
                                    # slots
                kid_matches.append(this_kid_matches)
        for assignment in product(*kid_matches):
            d = {slot.label: node}
            for kid_match in assignment:
                d.update(kid_match)
            if len(d) != len(set([item.id for item in d.values()])):
                # A node was matched twice and this is not cool
                continue
            if all(slot in d.keys() for slot in required_slots):
                all_matches.append(d)
    return all_matches


def match(tree, pattern):
    """Matches the pattern against all nodes in tree"""
    matches = [_match(node, pattern) for node in _iter_deptree(tree)]
    return [m for local_matches in matches for m in local_matches]
