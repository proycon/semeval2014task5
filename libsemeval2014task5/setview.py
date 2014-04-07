#!/usr/bin/env python

#
# This script simply prints an entire set to terminal, using coloured ANSI
# output.
#

from __future__ import print_function, unicode_literals, division, absolute_import


from libsemeval2014task5.format import Reader, Writer
import sys

def main():
    try:
        filename = sys.argv[1]
    except:
        print("Please specify a file to view",file=sys.stderr)
        sys.exit(2)

    sentencepairs = []
    reader = Reader(filename)
    for sentencepair in reader:
        print("----------- Sentence #" + str(sentencepair.id) + " -----------")
        if sentencepair.input:
            print("Input: ", end="")
            print(sentencepair.inputstr(True,"blue"))
        if sentencepair.ref:
            print("Reference: ", end="")
            print(sentencepair.refstr(True,"green"))
        if sentencepair.output:
            print("Output: ", end="")
            print(sentencepair.refstr(True,"yellow"))
    reader.close()

if __name__ == '__main__':
    main()

