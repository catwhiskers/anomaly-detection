from typing import *

import sys
import re

from prefixspan import PrefixSpan
from extratools.dicttools import invert, remap
from extratools.printtools import print2


def checkArg(arg, cond):
    # type: (str, Callable[[int], bool]) -> int
    try:
        val = int(argv[arg])
        if not cond(val):
            raise ValueError
    except ValueError:
        print2("ERROR: Cannot parse {}.".format(arg))
        print2(__doc__)
        sys.exit(1)

    return val


def checkFunc(arg):
    # type: (str) -> Callable[..., bool]
    try:
        return eval(argv[arg])
    except:
        print2("ERROR: Cannot parse {}.".format(arg))
        print2(__doc__)
        sys.exit(1)


def mine_string_patterns(doc):
    id, lines = doc
    docs = []

    for i, line in enumerate(lines):
        lr = []
        line = re.sub(r'\d+', '', line)
        toks = line.strip().split(' ')
        for t in toks:
            if t:
                lr.append(t)
        docs.append(lr)

    wordmap = {} # type: Dict[str, int] #problematic!
    idx = 0
    for doc in docs:
        for tok in doc:
            if tok not in wordmap:
                wordmap[tok] = idx
                idx += 1
    doc_vecs = []
    for doc in docs:
        doc_vec = []
        for tok in doc:
            doc_vec.append(wordmap[tok])
        doc_vecs.append(doc_vec)
    db = doc_vecs
    ps = PrefixSpan(db)
    invwordmap = invert(wordmap)
    func = ps.frequent
    # lambda function for sorting
    key = None
    # upper bound
    bound = None
    # filter lambda function
    filter = None
    threshold = 2
    closed = True
    generator = False
    ps.minlen=2
    ps.maxlen=10
    results = []
    for freq, patt in func(
            threshold, closed=closed, generator=generator,
            key=key, bound=bound,
            filter=filter
        ):
        pattern = ' '.join(
            (invwordmap[i] for i in patt))
        results.append([pattern, freq])

    return id, results