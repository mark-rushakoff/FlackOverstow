#!/usr/bin/env python

from collections import defaultdict
import random

__author__ = "Mark Rushakoff"
__license__ = "MIT"

def markovchain(text, chainlen, numchains):
    chaindict = defaultdict(list)
    words = text.split()
    for i, word in enumerate(words):
        chaindict[word].append(i)
    numwords = i
    randomword = random.choice(words)
    out = [randomword.capitalize()]
    for i in xrange(numchains):
        try:
            idx = random.choice(chaindict[randomword]) + 1
            if idx >= numwords:
                randomword = random.choice(words)
                continue
        except IndexError:
            randomword = random.choice(words)
            continue
        if out[-1][-1] in (".!?"): # last word ended in ending punctuation
            out.append(words[idx].capitalize())
            out.extend(words[idx+1:idx+chainlen])
        else:
            out.extend(words[idx:idx+chainlen])
        randomword = out[-1]
    if out[-1][-1] not in ".!?":
        out[-1] += random.choice(list('?.....!'))

    return ' '.join(out)
