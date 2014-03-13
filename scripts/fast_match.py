"""Low-level-ish script to match comparison patterns in a super-fast way.

Tricks used:
- joblib for multiprocessing.  This uses joblib imported from scikit-learn, but
you could just install joblib itself and replace the import line.

- memory mapping to read large files efficiently.

- delimiter-aware chunking.  We have CONLL-style files, so we can't chunk
at any end-of-line, we have to chunk at sentence delimiters.

Most of the speed tricks here were inspired by [1].

[1] http://effbot.org/zone/wide-finder.htm
"""

# Author: Vlad Niculae <vniculae@mpi-sws.org>
# License: BSD 2-clause

import sys
import time
import mmap
import os
import cPickle
import argparse

from sklearn.externals.joblib import Parallel, delayed

import numpy as np

from compattern.dependency import match
from compattern.dependency.seed_patterns import patterns
from compattern.dependency.conll import read

filemap = None


def get_sents_wacky(f):
    """Hacky pseudo-xml function to extract everything between <s> and </s>"""
    sent = None
    for line in f:
        header = line[:3]
        if header[0] == '<':
            if header[1] == 's':
                sent = []
            elif header[1] == '/' and header[2] == 's':
                if sent is not None:
                    yield sent
            continue
        else:
            if sent is not None:
                sent.append(line)


def get_sents(f):
    """conll file with no wacky xmlish tags"""
    sent = []
    for line in f:
        if line.strip():
            sent.append(line)
        else:
            if len(sent):
                yield sent
            sent = []


def get_chunks(fname, block_size=2 ** 20, delim="<s>"):
    size = os.path.getsize(fname)
    if size < block_size:
        block_size = 2 ** (np.floor(np.log2(size)) - 2)
        #block_size = size / 35
    f = open(fname)
    file_ended = False
    while not file_ended:
        start = f.tell()
        f.seek(block_size, 1)
        s = f.readline()
        while True:
            s = f.readline()
            if not s:
                yield start, f.tell() - start
                file_ended = True
                break
            if s.strip() == delim:
                yield start, f.tell() - start
                break


def _nested(submatch, match):
    """Check whether submatch is nested in match"""
    ids_submatch = set((key, tok.id) for key, tok in submatch.items())
    id_match = set((key, tok.id) for key, tok in match.items())
    return set.issubset(ids_submatch, id_match)


def deduplicate(matches):
    """Removes nested matches on the same sentence.

    Two matches are considered nested if all (key, val) pairs of
    the first one appear in the second one too.

    Parameters
    ----------
    matches, list of (int, dict)
    List of tupes containing the pattern number and the dict of slots matched
    by that pattern.
    """
    matches = sorted(matches, key=lambda x: len(x[1]))
    new_matches = []
    for k, submatch in enumerate(matches):
        found_supermatch = False
        for supermatch in matches[k + 1:]:
            if _nested(submatch[1], supermatch[1]):
                found_supermatch = True
                break
        if not found_supermatch:
            new_matches.append(submatch)
    return new_matches


def process(fname, chunk, fmt='turboparser'):
    """Process a memmapped chunk of a large file.

    The comparison detection logic is called from here.

    Parameters
    ----------

    fname : string
        The path to the file to be opened.

    chunk : tuple (int, int)
        Beginning and ending offsets in the file.  The code essentially
        processes `f.seek(chunk[0]).read(chunk[1])`.

    fmt : ('turboparser'|'wacky')
        CONLL dependency format to use.

    Returns
    -------
    chunk_matches : list
        List of tuples (sentence, matches) where the second element is a list
        of (pattern_no, dict) containing the slots matched by the pattern.

    """

    global filemap, fileobj
    chunk_matches = []
    if filemap is None or fileobj.name != fname:
        fileobj = open(fname)
        filemap = mmap.mmap(fileobj.fileno(), os.path.getsize(fname),
                            access=mmap.ACCESS_READ)

    filemap.seek(chunk[0])
    lines = filemap.read(chunk[1]).splitlines()
    sents = get_sents_wacky(lines) if fmt == 'wacky' else get_sents(lines)
    for sent in sents:
        try:
            for s, root in read(sent + ["\n"], return_tree=True):
                matches = [(pat_no, m)
                           for pat_no, pat in enumerate(patterns)
                           for m in match(root, pat)]
                if matches:
                    matches = deduplicate(matches)
                    chunk_matches.append((str(s), matches))
        except ValueError:
            pass  # sentence without root
    return chunk_matches


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Fast comparison pattern matcher from CoNLL files")
    parser.add_argument('infile', type=str, help="input file")
    parser.add_argument('outfile', type=argparse.FileType('w'),
                        help="output file (pickle format)")
    parser.add_argument('--format', type=str,
                        help="turboparser (default)|wacky")
    args = parser.parse_args()

    fmt = args.format if args.format else 'turboparser'
    if fmt not in ['turboparser', 'wacky']:
        raise argparse.ArgumentError('format should be turboparser or wacky')
    delim = '<s>' if fmt == 'wacky' else ''
    print("Processing {}".format(sys.argv[1]))
    t0 = time.time()
    matches = Parallel(n_jobs=32, verbose=1)(delayed(process)(args.infile,
                                                              chunk, fmt)
                                             for chunk
                                             in get_chunks(args.infile,
                                                           delim=delim))
    print("{} sentences matched".format(sum(len(m) for m in matches)))
    print("Completed in {:.2f}".format(time.time() - t0))
    cPickle.dump(matches, args.outfile)
