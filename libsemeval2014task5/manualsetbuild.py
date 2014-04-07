#!/usr/bin/env python3

from __future__ import print_function, unicode_literals, division, absolute_import

import sys
import os
import readline
from collections import defaultdict
from libsemeval2014task5.format import Reader, Writer, SentencePair, Fragment, Alternative

sources = defaultdict(int)
categories = defaultdict(int)

def main():
    global sources, categories
    if len(sys.argv) < 4:
        print("Syntax: set L1 L2",file=sys.stderr)
        sys.exit(2)
    setfile= sys.argv[1]
    l1= sys.argv[2]
    l2= sys.argv[3]

    sentencepairs = []
    if os.path.exists(setfile):
        print("Loading existing file: ", setfile)
        reader = Reader(setfile)
        for sentencepair in reader:
            sentencepairs.append(sentencepair)
            if sentencepair.source:
                sources[sentencepair.source] += 1
            if sentencepair.category:
                categories[sentencepair.category] += 1
        print(str(len(sentencepairs)) + " sentences loaded")
    else:
        print("New file: ", setfile,file=sys.stderr)

    print("Type h for help")

    cursor = None

    quit = False
    while not quit:
        cmd = input("> ")
        if cmd.lower() == 'q':
            writer = Writer(setfile,l1,l2)
            for sentencepair in sentencepairs:
                writer.write(sentencepair)
            writer.close()
            quit = True
        elif cmd.lower() == 'h':
            print("q\tSave and quit",file=sys.stderr)
            print("n\tNew sentence pair",file=sys.stderr)
            print("d\tDelete sentence pair",file=sys.stderr)
            print("a\tAdd alternative",file=sys.stderr)
            print(">\tNext sentence pair",file=sys.stderr)
            print("<\tPrevious sentence pair",file=sys.stderr)
            print("12\tGo to sentence pair #12", file=sys.stderr)
            print("w\tWrite changes to disk", file=sys.stderr)
            print("s\tSource list", file=sys.stderr)
        elif cmd.lower() == "<":
            if cursor is None:
                cursor = len(sentencepairs) - 1
            else:
                cursor = cursor - 1
                if cursor < 0:
                    cursor = len(sentencepairs) - 1
            showsentencepair(sentencepairs, cursor)
        elif cmd.lower() == ">":
            if cursor is None:
                cursor = 0
            else:
                cursor = cursor + 1
                if cursor >= len(sentencepairs):
                    cursor = 0
            showsentencepair(sentencepairs, cursor)
        elif cmd.lower().isdigit():
            cursor = int(cmd.lower()) - 1
            if cursor < 0:
                cursor = 0
            if cursor >= len(sentencepairs):
                cursor = len(sentencepairs) - 1
        elif cmd.lower() == 'n':
            cursor = newsentencepair(sentencepairs)
        elif cmd.lower() == 'w':
            writer = Writer(setfile,l1,l2)
            for sentencepair in sentencepairs:
                writer.write(sentencepair)
            writer.close()
        elif cmd.lower() == 'p':
            if cursor is None:
                cursor = 0
            showsentencepair(sentencepairs, cursor)
        elif cmd.lower() == 'a':
            if cursor is None:
                cursor = 0
            addalternative(sentencepairs[cursor])
        elif cmd.lower() == 's':
            listsources()
        else:
            print("No such command, type h for help", file=sys.stderr)


def showsentencepair(sentencepairs, cursor):
    sentencepair = sentencepairs[cursor]
    print("------------------ #" + str(cursor+1) + " of " + str(len(sentencepairs)) + "----------------",file=sys.stderr)
    print("Input:     " + sentencepair.inputstr(True,"blue"))
    print("Reference: " + sentencepair.refstr(True,"green"))
    fragment = None
    for f in sentencepair.ref:
        if isinstance(f, Fragment):
            fragment = f
            break
    if fragment.alternatives:
        for alt in fragment.alternatives:
            print("Alternative: " + str(alt))
    if sentencepair.source:
        print("Source: " + sentencepair.source)
    if sentencepair.category:
        print("Category: " + sentencepair.category)

def makesentence(s):
    if not s:
        return False
    if s.count('*') != 2:
        print("Expected marked fragment, not found!",file=sys.stderr)
        return False
    begin = None
    for i,c in enumerate(s):
        if c == '*':
            if begin is None:
                begin = i
            else:
                end = i
                break
    left = s[:begin]
    fragment = (s[begin+1:i],)
    right = s[end+1:]
    sentence = (left, Fragment(fragment), right)
    return sentence


def addalternative(sentencepair):
    alt = input("Alternative: ")
    fragment = None
    for f in sentencepair.ref:
        if isinstance(f, Fragment):
            fragment = f
            break
    if fragment:
        fragment.alternatives.append(Alternative(tuple(alt.split(' '))))





def newsentencepair(sentencepairs):
    global sources, categories
    cursor = len(sentencepairs)
    print("------------------ #" + str(cursor+1) + ": New sentence pair ----------------")
    print("Enter untokenised text (L2), mark fragment in *asterisks*")
    ref = input("Reference sentence: ")
    ref = makesentence(ref.strip())
    if not ref:
        print("No sentence provided",file=sys.stderr)
        return False
    fragment = input("L1 fragment: ")
    fragment = Fragment(tuple(fragment.strip().split(" ")))
    f = None
    for x in ref:
        if isinstance(x,Fragment):
            f = x
    assert f
    inputsentence = SentencePair.replacefragment(f, fragment, ref)
    choices = listsources()
    src = input("Source: ")
    if src.isdigit():
        if int(src) in choices:
            src = choices[int(src)]
            print("Selected " + src,file=sys.stderr)
        else:
            print("Invalid source, leaving empty",file=sys.stderr)
            src = None
    if src:
        sources[src] += 1
    choices = listcats()
    cat = input("Category: ")
    if cat.isdigit():
        if int(cat) in choices:
            cat = choices[int(cat)]
            print("Selected " + cat,file=sys.stderr)
        else:
            print("Invalid category, leaving empty",file=sys.stderr)
            cat = None
    sentencepairs.append( SentencePair(cursor, inputsentence,None,ref, src, cat) )
    return cursor

def listsources():
    choices = {}
    for i, (source,_) in enumerate(sorted(sources.items(), key=lambda x: -1 * x[1])):
        choices[i+1] = source
        print(" " + str(i+1) + ") " + source)
    return choices

def listcats():
    choices = {}
    for i, (cat,_) in enumerate(sorted(categories.items(), key=lambda x: -1 * x[1])):
        choices[i+1] = cat
        print(" " + str(i+1) + ") " + cat)
    return choices




if __name__ == '__main__':
    main()
