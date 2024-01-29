#!/usr/bin/env python
# Change nonASCII into ASCII

import sys

ord_exceptions = set()

ord_ascii = {}
with open("/home/projects/ku_10024/scratch/esmaeil/0-Tagger/scripts/utf8ascii.tsv", "r") as fp:
    for line in fp:
        hex, ascii = line[:-1].split("\t")
	ord_ascii[int(hex, 16)] = ascii

for line in sys.stdin:
    out = []
    for uch in unicode(line, "utf8", "replace"):
        point = ord(uch)
        if point > 127 and point not in ord_ascii:
            if point not in ord_exceptions:
                print >> sys.stderr, "ERROR: %s\t%i" % (uch.encode("utf8"), point)
                out.append('*')
        if point in ord_ascii:
            out.append(ord_ascii[point])
        else:
            out.append(uch)
    sys.stdout.write(line)
    out = ''.join(out).encode("utf8")
    if out != line:
	    sys.stdout.write(out)
sys.stdout.flush()
