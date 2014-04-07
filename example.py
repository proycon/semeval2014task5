#!/usr/bin/env python

#####################################################################
# SemEval 2014 task 5 - L2 Writing Assistant
#       Example system in Python
#
#
# This example system takes two arguments, the trial/test set and the file to
# output to.
#
# Instead of translating the fragments from L2 to L1. This example
# simply converts the fragments to uppercase.
#
#####################################################################

#We import from the future to get Python 3 like functionality in Python 2.6+, if you're already on three this does nothing
from __future__ import print_function, unicode_literals, division, absolute_import

import sys

#Here we import the format library for this task:
import libsemeval2014task5.format as format

try:
    inputfilename, outputfilename = sys.argv[1:]
except:
    print("ERROR: Specify a trial/test set to load and an output filename",file=sys.stderr)
    sys.exit(2)

#We open the XML reader
reader = format.Reader(inputfilename)

#At the same time, we open the XML writer for writing the system output
writer = format.Writer(outputfilename, reader.L1, reader.L2)

#Then we iterate over all sentence pairs in the set
for sentencepair in reader:
    #The following attributes are available
    # - sentencepair.id
    # - sentencepair.L1
    # - sentencepair.L2
    # - sentencepair.input  - A tuple of words and a Fragment instance,  representing the input sentence (L2) with L1 fragment
    # - sentencepair.output  - A tuple of words and a Fragment instance , representing the reference sentence (L2) with the system translation of the fragment (L2)
    # - sentencepair.ref  - A tuple of words and a Fragment instance, representing the reference sentence (L2) with the correct L2 fragment

    #We iterate over the fragment in the input (there will be only one iteration by default, each sentence in this task only has one fragment)
    for leftcontext, fragment, rightcontent in sentencepair.inputfragments():
        #leftcontext is a tuple of words to the left of the fragment
        #rightcontent is a tuple of words to the right of the fragment
        #fragment is an instance of format.Fragment. fragment.value is a tuple of the words that are in the fragment, or None if unknown
        assert isinstance(fragment, format.Fragment)


        ###############################################################################################
        #Convert the fragment's textual value to uppercase, this is our dummy translation step

        translatedvalue = [x.upper() for x in fragment.value]

        ###############################################################################################



        #now we create a new fragment for the new value, it must carry the same ID
        translatedfragment = format.Fragment(tuple(translatedvalue), fragment.id)

        #if you can not provide a translation at all (the system doesn't know),
        #then you can create an empty fragment as follows:
        #  translatedfragment = format.Fragment(None, fragment.id)

        #In out-of-five mode, you may add up to four extra alternatives:
        #This you can do as follows:
        #  translatedfragment.alternatives.append( format.Alternative(tuple("your","alternative")) )


        #Now we can set the system output by copying the input sentence
        #(the context after all will stay the same, we only change the fragment)
        #And then replacing the old fragment with the translated one. All done in this single method:
        sentencepair.output = sentencepair.replacefragment(fragment, translatedfragment, sentencepair.input)

        #write this modified sentencepair to the output file, using the writer:
        writer.write(sentencepair)

        #(If you want to create a new sentencepair from scratch, use something like:
        #  newsentencepair = format.SentencePair(id,input,output,ref)
        #the arguments  input,output,ref may be set to None if not applicable

        #Just for fun, let's also print the input and output with nice coloured markers. Omit the two arguments to get a plain string
        print("Input: " + sentencepair.inputstr(True,"blue"))
        print("Output: " + sentencepair.outputstr(True,"yellow"))

        #There will be only one iteration, so this is not necessary, but just to prevent confusion:
        break


#Don't forget to close the reader and writer
writer.close()
reader.close()

