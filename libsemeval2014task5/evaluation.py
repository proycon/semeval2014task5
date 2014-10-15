#!/usr/bin/env python

from __future__ import print_function, unicode_literals, division, absolute_import

import argparse
import sys
import os
import io

from libsemeval2014task5.format import Reader, Fragment
from libsemeval2014task5.common import log, runcmd, red, yellow, white


VERSION = "2.0"

def main():
    parser = argparse.ArgumentParser(description="Evaluation")
    parser.add_argument('--mtevaldir',type=str, help="Path to MT evaluation scripts",action='store',default="")
    parser.add_argument('--ref',type=str,help='Reference file', action='store',required=True)
    parser.add_argument('--out',type=str,help='Output file', action='store',required=True)
    parser.add_argument('--workdir','-w',type=str,help='Work directory', action='store',default=".")
    parser.add_argument('-i',dest='casesensitive',help='Measure translation accuracy without regard for case',action='store_false',default=True)
    parser.add_argument('-a',dest='oof',help='Out of five evaluation, considers up to four additional alternatives in system output',action='store_true',default=False)
    #parser.add_argument('-C',dest='forcecontext',help='Force context from input, even if system-supplied context is different',action='store_true',default=False)
    parser.add_argument('-I',dest='ignoreinputmismatch',help='Ignore input mismatch',action='store_true',default=False)
    args = parser.parse_args()

    totalavgaccuracy, totalwordavgaccuracy, totalavgrecall, matrexsrcfile, matrextgtfile, matrexoutfile = evaluate(Reader(args.ref), Reader(args.out), args.mtevaldir, args.workdir, args.casesensitive, args.oof, args.ignoreinputmismatch)

    outprefix = '.'.join(args.out.split('.')[:-1])

    if args.mtevaldir:
        mtscore(args.mtevaldir, matrexsrcfile, matrextgtfile, matrexoutfile, totalavgaccuracy, totalwordavgaccuracy, totalavgrecall, outprefix, args.workdir)
    else:
        f = io.open(outprefix + '.summary.score','w')
        s = "Accuracy Word-Accuracy Recall"
        f.write(s+ "\n")
        log(s)
        s = str(totalavgaccuracy) + " " + str(totalwordavgaccuracy) + " " + str(totalavgrecall)
        f.write(s + "\n")
        log(s)
        f.close()


def strippunct(t):
    t2 = []
    for x in t:
        if not ( x in ',;.?¿¡!'):
            t2.append(x)
    n = []
    for x in reversed(t2):
        if not ( x in ',;.?¿¡!'):
            n.append(x)
    return tuple(reversed(n))


def replace(t, match, replacement):
    l = list(t)
    newlist = []
    match = list(match)
    replacement = list(replacement)
    i = 0
    while i < len(l):
        sublist = l[i:i+len(match)]
        if sublist == match:
            newlist += replacement
            i += len(match) - 1
        else:
            newlist.append(l[i])
        i += 1
    return tuple(newlist)


def normalizetext(t, L2):
    if L2 == 'es':
        t = replace(t, ('de','el'), ('del',) )
        t = replace(t, ('a','el'), ('al',) )
        t = replace(t, ('De','el'), ('Del',) )
        t = replace(t, ('A','el'), ('Al',) )
    return strippunct(t)

def subtuples(t):
    for i in range(0,len(t)):
        for l in reversed(range(1,len(t) - i+1)):
            yield t[i:i+l]



def longestsubmatch(t,t2,eq):
    """Returns the longest consecutive submatch"""
    longest = tuple()
    for subtup in subtuples(t):
        for subtup2 in subtuples(t2):
            if eq(subtup,subtup2):
                if len(subtup)>len(subtup2):
                    match = subtup
                else:
                    match = subtup2
                if len(match) > len(longest):
                    longest = match
    return longest



def comparefragments(outfragment, reffragment, casesensitive, oof, L2):
    global matches, wordmatches, misses, wordmisses, missedrecall
    if casesensitive:
        eq = lambda x,y: "".join(x) == "".join(y)
    else:
        eq = lambda x,y: "".join(x).lower() == "".join(y).lower()


    if not outfragment.value or len(outfragment.value) == 0:
        missedrecall += 1
        misses += 1
        wordmisses += 1
        return 0
    else:
        outvalues = [normalizetext(outfragment.value,L2)]
        if oof and outfragment.alternatives:
            for alt in outfragment.alternatives[:4]:
                outvalues.append( normalizetext(alt.value,L2) )

        refvalues = [normalizetext(reffragment.value,L2)]
        for alt in reffragment.alternatives:
            refvalues.append( normalizetext(alt.value,L2) )


        wordmatchscores = []

        for outvalue in outvalues:
            for refvalue in refvalues:
                if eq(outvalue, refvalue):
                    wordmatchscore = 1
                else:
                    wordmatchscore = len(longestsubmatch(outvalue,refvalue, eq)) / max(len(outvalue), len(refvalue))
                wordmatchscores.append(wordmatchscore)

        wordmatchscore = max(wordmatchscores)
        wordmatches += wordmatchscore
        wordmisses += (1 - wordmatchscore)
        if wordmatchscore == 1:
            matches += 1
        else:
            misses += 1
        return wordmatchscore





def evaluate(ref, out, mtevaldir, workdir, casesensitive=True, oof=False, ignoreinputmismatch=False):
    global matches, wordmatches, misses, wordmisses, missedrecall

    if not ref.L1  or ref.L1 == "unknown":
        raise Exception("Reference set must specify L1")
    if not ref.L2  or ref.L2 == "unknown":
        raise Exception("Reference set must specify L2")

    ref_it = iter(ref )
    out_it = iter(out)


    accuracies = []
    wordaccuracies = []
    recalls = []


    maxaltcount = 0

    matrexsrcfile = out.filename.replace('.xml','') + '.matrex-src.xml'
    matrextgtfile = out.filename.replace('.xml','') + '.matrex-ref.xml'
    matrexoutfile = out.filename.replace('.xml','') + '.matrex-out.xml'



    matrexsrc = io.open(matrexsrcfile ,'w', encoding='utf-8')
    matrextgt = io.open(matrextgtfile ,'w', encoding='utf-8')
    matrexout = io.open(matrexoutfile ,'w', encoding='utf-8')

    for t,f in (('src',matrexsrc),('ref',matrextgt),('tst',matrexout)):
        f.write( "<" + t + "set setid=\"mteval\" srclang=\"src\" trglang=\"tgt\">\n")
        f.write("<DOC docid=\"colibrita\" sysid=\"colibrita\">\n")

    while True:
        try:
            ref_s = next(ref_it)
            out_s = next(out_it)
            if out_s.id != ref_s.id:
                print("WARNING: Sentence ID mismatch, sentence missing in reference? Skipping output ID " + out_s.id + " in an attempt to compensate" ,file=sys.stderr)
                out_s = next(out_it)
        except StopIteration:
            break

        if ref_s.id != out_s.id:
            raise Exception("Sentence ID mismatch in reference and output! " + str(ref_s.id) + " vs " + str(out_s.id))
        elif out_s.input and ref_s.input != out_s.input:
            if not ignoreinputmismatch:
                raise Exception("Sentence input mismatch in reference and output! " , ref_s.input,  " vs " , out_s.input)
        elif not ref_s.ref:
            raise Exception("No reference for sentence " + str(ref_s.id))
        elif not out_s.output:
            raise Exception("No output for sentence " + str(out_s.id))

        matrexsrc.write("<seg id=\"" + str(ref_s.id) + "\">" + ref_s.inputstr() + "</seg>\n")
        matrextgt.write("<seg id=\"" + str(ref_s.id) + "\">" + ref_s.refstr() + "</seg>\n")
        matrexout.write("<seg id=\"" + str(out_s.id) + "\">" + out_s.outputstr() + "</seg>\n")


        matches = 0
        misses = 0

        wordmatches = 0
        wordmisses = 0
        missedrecall = 0


        outputfragments = out_s.outputfragmentsdict()
        reffragments = ref_s.reffragmentsdict()
        for f in reffragments.values():
            maxaltcount = max(maxaltcount, len(f.alternatives) )
        for inputfragment in ref_s.inputfragmentsdict().values():
            if not inputfragment.id in reffragments:
                raise Exception("No reference fragment found for fragment " + str(inputfragment.id) + " in sentence " + str(ref_s.id))

            if not inputfragment.id in outputfragments:
                print("WARNING: Input fragment " + str(inputfragment.id) + " in sentence " + str(ref_s.id) + " is not translated!", file=sys.stderr)
                misses += 1
                wordmisses += 1
                missedrecall += 1
            else:
                comparefragments( outputfragments[inputfragment.id], reffragments[inputfragment.id], casesensitive, oof, ref.L2)

            if missedrecall == matches +misses:
                recall = 0.0
            else:
                recall = (matches+misses)/((matches+misses)-missedrecall)

            print("Recall for sentence " + str(ref_s.id) + " = " + str(recall)  )
            recalls.append(recall)

            accuracy = matches/(matches+misses)
            print("Accuracy for sentence " + str(ref_s.id) + " = " + str(accuracy))
            accuracies.append(accuracy)

            wordaccuracy = wordmatches/(wordmatches+wordmisses)
            print("Word accuracy for sentence " + str(ref_s.id) + " = " + str(wordaccuracy))
            wordaccuracies.append(wordaccuracy)

    if recalls:
        totalavgrecall = sum(recalls) / len(recalls)
        print("Total average recall = " + str(totalavgrecall))
    if accuracies:
        totalavgaccuracy = sum(accuracies) / len(accuracies)
        print("Total average accuracy = " + str(totalavgaccuracy))
    if wordaccuracies:
        totalwordavgaccuracy = sum(wordaccuracies) / len(wordaccuracies)
        print("Total word average accuracy = " + str(totalwordavgaccuracy))

    if maxaltcount > 0:
        matrextgt.write("</DOC>\n")
        for i in range(0, maxaltcount):
            matrextgt.write("<DOC docid=\"colibrita\" sysid=\"colibrita.alt." + str(i+1) + "\">\n")
            ref.reset()
            ref_it = iter(ref )
            while True:
                try:
                    ref_s = next(ref_it)
                except StopIteration:
                    break

                reffragments = ref_s.reffragmentsdict()
                for f in reffragments.values():
                    for j, alt in enumerate(f.alternatives):
                        if j == i:
                            print("Inserting alternative " + str(i) + ": " +  " ".join(alt.value) ,file=sys.stderr)
                            ref_s.ref = ref_s.replacefragment(f, Fragment(alt.value), ref_s.ref)
                matrextgt.write("<seg id=\"" + str(ref_s.id) + "\">" + ref_s.refstr() + "</seg>\n")

            matrextgt.write("</DOC>\n")
        matrextgt.write("</refset>")
    else:
        matrextgt.write("</DOC>\n</refset>")

    for t,f in (('src',matrexsrc),('tst',matrexout)):
        f.write("</DOC>\n</" + t + "set>")
        f.close()
    matrextgt.close()

    return totalavgaccuracy, totalwordavgaccuracy, totalavgrecall,matrexsrcfile, matrextgtfile, matrexoutfile


def mtscore(mtevaldir, sourcexml, refxml, targetxml, totalavgaccuracy, totalwordavgaccuracy, totalavgrecall, outprefix, WORKDIR = '.'):

    per = 0
    wer = 0
    bleu = 0
    meteor = 0
    nist = 0
    ter = 0

    EXEC_MATREX_WER = mtevaldir + '/eval/WER_v01.pl'
    EXEC_MATREX_PER = mtevaldir + '/eval/PER_v01.pl'
    EXEC_MATREX_BLEU = mtevaldir + '/eval/bleu-1.04.pl'
    EXEC_MATREX_METEOR = mtevaldir + '/meteor-0.6/meteor.pl'
    EXEC_MATREX_MTEVAL = mtevaldir + '/mteval-v11b.pl'
    EXEC_MATREX_TER = mtevaldir + '/tercom.jar'
    EXEC_PERL = 'perl'
    EXEC_JAVA = 'java'

    errors = False
    if EXEC_MATREX_BLEU and os.path.exists(EXEC_MATREX_BLEU):
        if not runcmd(EXEC_PERL + ' ' + EXEC_MATREX_BLEU + " -r " + refxml + ' -t ' + targetxml + ' -s ' + sourcexml + ' -ci > ' + outprefix + '.bleu.score',  'Computing BLEU score'): errors = True
        if not errors:
            try:
                f = io.open(WORKDIR + '/' + outprefix + '.bleu.score')
                for line in f:
                    if line[0:9] == "BLEUr1n4,":
                        bleu = float(line[10:].strip())
                        print("BLEU score: ", bleu, file=sys.stderr)
                f.close()
            except Exception as e:
                log("Error reading bleu.score:" + str(e),red)
                errors = True
    else:
        log("Skipping BLEU (no script found ["+EXEC_MATREX_BLEU+"])",yellow)

    if EXEC_MATREX_WER and os.path.exists(EXEC_MATREX_WER):
        if not runcmd(EXEC_PERL + ' ' + EXEC_MATREX_WER + " -r " + refxml + ' -t ' + targetxml + ' -s ' + sourcexml + '  > ' + outprefix + '.wer.score', 'Computing WER score'): errors = True
        if not errors:
            try:
                f = io.open(WORKDIR + '/' + outprefix + '.wer.score','r',encoding='utf-8')
                for line in f:
                    if line[0:11] == "WER score =":
                        wer = float(line[12:19].strip())
                        log("WER score: " + str(wer), white)
                f.close()
            except Exception as e:
                log("Error reading wer.score:" + str(e),red)
                errors = True
    else:
        log("Skipping WER (no script found ["+EXEC_MATREX_WER+"]) ",yellow)

    if EXEC_MATREX_PER and os.path.exists(EXEC_MATREX_PER):
        if not runcmd(EXEC_PERL + ' ' + EXEC_MATREX_PER + " -r " + refxml + ' -t ' + targetxml + ' -s ' + sourcexml + '  > ' + outprefix + '.per.score',  'Computing PER score'): errors = True
        if not errors:
            try:
                f = io.open(WORKDIR + '/' + outprefix +'.per.score','r',encoding='utf-8')
                for line in f:
                    if line[0:11] == "PER score =":
                        per = float(line[12:19].strip())
                        log("PER score: " + str(per), white)
                f.close()
            except Exception as e:
                log("Error reading per.score" + str(e),red)
                errors = True
    else:
        log("Skipping PER (no script found ["+EXEC_MATREX_PER+"])",yellow)

    if EXEC_MATREX_METEOR and os.path.exists(EXEC_MATREX_METEOR):
        if not runcmd(EXEC_PERL + ' -I ' + os.path.dirname(EXEC_MATREX_METEOR) + ' ' + EXEC_MATREX_METEOR + " -s colibrita -r " + refxml + ' -t ' + targetxml + ' --modules "exact"  > ' + outprefix + '.meteor.score',  'Computing METEOR score'): errors = True
        if not errors:
            try:
                f = io.open(WORKDIR + '/' + outprefix + '.meteor.score','r',encoding='utf-8')
                for line in f:
                    if line[0:6] == "Score:":
                        meteor = float(line[7:].strip())
                        log("METEOR score: " + str(meteor), white)
                f.close()
            except Exception as e:
                log("Error reading meteor.score:" + str(e),red)
                errors = True
    else:
        log("Skipping METEOR (no script found ["+EXEC_MATREX_METEOR+"])",yellow)

    if EXEC_MATREX_MTEVAL and os.path.exists(EXEC_MATREX_MTEVAL):
        if not runcmd(EXEC_PERL + ' ' + EXEC_MATREX_MTEVAL + " -r " + refxml + ' -t ' + targetxml + ' -s ' + sourcexml +  '  > ' + outprefix + '.mteval.score',  'Computing NIST & BLEU scores'): errors = True
        if not errors:
            try:
                f = io.open(WORKDIR + '/' + outprefix + '.mteval.score','r',encoding='utf-8')
                for line in f:
                    if line[0:12] == "NIST score =":
                        nist = float(line[13:21].strip())
                        log("NIST score: ", nist)
                    if line[21:33] == "BLEU score =":
                        try:
                            bleu2 = float(line[34:40].strip())
                            if bleu == 0:
                                bleu = bleu2
                                log("BLEU score: " + str(bleu), white)
                            elif abs(bleu - bleu2) > 0.01:
                                log("blue score from MTEVAL scripts differs too much: " + str(bleu) + " vs " + str(bleu2) +  ", choosing highest score")
                                if bleu2 > bleu:
                                    bleu = bleu2
                            else:
                                log("BLEU score (not stored): " + str(float(line[34:40].strip())))
                        except:
                            raise
                f.close()
            except Exception as e:
                log("Error reading mteval.score: " + str(e),red)
                errors = True
    else:
        log("Skipping MTEVAL (BLEU & NIST) (no script found)", yellow)

    if EXEC_MATREX_TER and os.path.exists(EXEC_MATREX_TER):
        if not runcmd(EXEC_JAVA + ' -jar ' + EXEC_MATREX_TER + " -r " + refxml + ' -h ' + targetxml + '  > ' + outprefix + '.ter.score',  'Computing TER score'): errors = True
        try:
            f = io.open(WORKDIR +'/' + outprefix + '.ter.score','r',encoding='utf-8')
            for line in f:
                if line[0:10] == "Total TER:":
                    ter = float(list(line[11:].split(' '))[0])
                    log("TER score: " + str(ter),white)
            f.close()
        except Exception as e:
            log("Error reading ter.score: " + str(e),red)
    else:
        log("Skipping TER (no script found)",yellow)


    log("SCORE SUMMARY\n===================\n")
    f = io.open(WORKDIR + '/' + outprefix + '.summary.score','w')
    s = "Accuracy Word-Accuracy Recall BLEU METEOR NIST TER WER PER"
    f.write(s+ "\n")
    log(s)
    s = str(totalavgaccuracy) + " " + str(totalwordavgaccuracy) + " " + str(totalavgrecall) + " " + str(bleu) + " " + str(meteor) + " " + str(nist)  + " " + str(ter) + " " + str(wer)  + " " + str(per)
    f.write(s + "\n")
    log(s)
    f.close()


    return not errors




