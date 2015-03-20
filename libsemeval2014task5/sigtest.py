#!/usr/bin/env python

from __future__ import print_function, unicode_literals, division, absolute_import
from scipy import stats
import sys



def sigtest(referencefile, systemfile):
    refdata = {}
    sysdata = {}

    for filename, data in ( (referencefile, refdata), (systemfile, sysdata) ):
        with open(filename) as f:
            for line in f:
                if line:
                    fields = line.split("\t")
                    sentenceid = fields[0]
                    accuracy, wordaccuracy, recall = ( float(x) for x in fields[1:] )
                    data[sentenceid] =  wordaccuracy


    #flatten the data
    refarray = [ refdata[sentenceid] for sentenceid in refdata ]
    sysarray = [ sysdata[sentenceid] if sentenceid in sysdata else 0.0 for sentenceid in refdata ]  #keys in refdata

    #conduct test:
    pvalue = stats.ttest_rel(refarray, sysarray)[1]
    print("p=" + str(pvalue))
    return pvalue

def main():
    try:
        referencefile, systemfile = sys.argv[1:]
    except:
        print("Performs significance testing using paired t-test between reference system and system output, on the word accuracy metric, outputs p-value.\nSyntax: sigtest reference.persentence.score system.persentence.score",file=sys.stderr)
        sys.exit(2)

    sigtest(referencefile, systemfile)



if __name__ == '__main__':
    main()
