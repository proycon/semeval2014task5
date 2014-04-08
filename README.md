SemEval 2014 - Task 5 - L2 Writing Assistant
============================================
    
*Maarten van Gompel, Iris Hendrickx, Antal van den Bosch, Radboud University Nijmegen*
*Els Lefever, Véronique Hoste, Ghent University*

http://alt.qcri.org/semeval2014/task5/


Introduction
----------------------

This SemEval task was organised for SemEval 2014 and offer a new cross-lingual
and application-oriented task for SemEval that finds itself in the area where
techniques from Word Sense Disambiguation and Machine Translation meet.

The task concerns the translation of L1 fragments, i.e words or phrases, in an
L2 context. This type of translation can be applied in writing assistance
systems for language learners in which users write in their target language,
but are allowed to occasionally back off to their native L1 when they are
uncertain of the proper word or expression in L2. These L1 fragments are
subsequently translated, along with the L2 context, into L2 fragments.

Thus, participants are asked to build a translation/writing assistance system
that translates specifically marked L1 fragments, in an L2 context, to their
proper L2 translation.

The task find itself on the boundary of Cross-Lingual Word Sense Disambiguation
and Machine Translation. Full-on machine translation typically concerns the
translation of whole sentences or texts from L1 to L2. This task, in contrast,
focuses on smaller fragments, side-tracking the problem of full word
reordering.

In this task we focus on the following language combinations of L1 and L2
pairs: English-German, English-Spanish, French-English, and Dutch-English. Task
participants may participate for all language pairs or any subset thereof.

Task Description
----------------------

In this task we ask the participants to build a translation assistance system
rather than a full machine translation system. The general form of such a
translation assistance system allows a translator or L2-language student to
write in L2, but allowing him or her to back off to L1 where he is uncertain of
the correct lexical or grammatical form in L2. The L1 expression, a word or
phrase, is translated by the system to L2, given the L2 context already
present, including right-side context if available. The aim here, as in all
translation, is to carry the semantics of the L1 fragment over to L2 and find
the most suitable L2 expression given the already present L2 context.

The task essentially addresses a core problem of WSD, with cross-lingual
context, and a sub-problem of Phrase-based Machine Translation; that of finding
the most suitable translation of a word or phrase.  In MT this would be
modelled by the translation model. Our task does not address the full
complexity of sentential translation, thus evading problems associated with
reordering and syntax. Instead it emphasizes the local semantic aspect of
phrasal or word translation in context. The user group we have in mind is that
of intermediate and advanced language learners, whom you generally want to
encourage to use their target language as much as possible, but may often feel
the need to fall back to their native language.

Currently, language learners are forced to fall back to a bilingual dictionary
when in doubt. These do not take the L2 context into account and are generally
more constrained to single words or short expressions. The proposed
application automatically generates context-dependent translation suggestions
as writing progresses. The task tests how effective participating systems
accomplish this.

The following example sentence pairs illustrate the idea:

 * Input (L1=English,L2=Spanish): “Hoy vamos a the **swimming pool**”.
 * Desired output: “Hoy vamos a **la piscina**”
 * Input (L1=English, L2=German): “Das wetter ist wirklich **abominable**”.
 * Desired output: “Das wetter ist wirklich **ekelhaft**”
 * Input (L1=French,L2=English): “I return home **parce'qu je suis fatigué**”
 * Desired output: “I return home **because I am tired**”.
 * Input (L1=Dutch, L2=English): “Workers are facing a massive **aanval op** their employment and social right.”
 * Desired output: “Workers are facing a massive **attack on** their employment and social rights”

The L2 writing assistant task can be related to two tasks that were offered in
previous years of SemEval: Lexical Substitution (Mihalcea et al, 2010) and
Cross-lingual Word Sense Disambiguation (Lefever and Hoste, 2010, 2013). When
comparing this task to the Cross-Lingual Word-Sense Disambiguation task,
notable differences are the fact that this task concerns not just words, but
also phrases. Another essential difference is the nature of the context; the
context is in L2 instead of L1.

Evaluation
---------------

Several metrics are available for automatic evaluation. First, we measure the
absolute accuracy $$a = c/n$$, where c is the number of fragment translations from
the system output that precisely match the corresponding fragments in the
reference translation, and n is the total number of translatable fragments,
including those for which no translation was found. We also introduce a
word-based accuracy, which unlike the absolute accuracy, still gives some
credits to mismatches that show partial overlap with the reference
translation. The system with the highest word-based accuracy wins the
competition.

A recall metric simply measures the number of fragments for which the system
generated a translation, as a proportion of the total number of fragments. As
no selection is made in L1 words or phrases that may appear in a an L2 context,
and due to the way evaluation is conducted, it is important that participating
systems produce output for as many  possible words and phrases as possible, and
thus achieve a high recall.

In addition to these task-specific metrics, standard MT metrics such as BLEU,
NIST, METEOR and error rates such as WER, PER and TER, are included in the
evaluation script as well. Scores such as BLEU will generally be high (> 0.95),
as a large portion of the sentence is already translated and only a specific
fragment remains to be evaluated. Nevertheless, these generic metrics are
proven to follow the same trend as the more task-specific evaluation metrics.

It regularly occurs that multiple translations are possible. In the creation of
the test set will take this into account by explicitly encoding valid
alternatives. A match with an alternative counts as a valid match. Likewise, a
translation assistance system may output multiple alternatives as well. We
therefore allow two different types of runs, following the example of the
Cross-Lingual Lexical Substitution and Cross-Lingual Word Sense Disambiguation
tasks:

 * **Best** - The system must output its best guess;
 * **Out of Five** - The system may output up to five alternatives.

Up to three runs may be submitted per language-pair and evaluation type
(totalling 24 runs in total if you participate for all language pairs and all
evaluation types)

An evaluation script that implements all these measures will be made available
to the participants. This same script will be used to compute the final
evaluation of this task.

Data and Tools
------------------------

 We provide material for the following L1 and L2 pairs:

 * English-German
 * English-Spanish
 * French-English
 * Dutch-English

Both trial and test data will be offered in a clear and simple XML format. The
test data will be delivered in tokenised format. This tokenisation is done
using ucto. System output is expected to adhere to this same XML format so it
can be automatically evaluated. Output should not be detokenised, it should
however respect case as evaluation will be case-sensitive. We do not provide
any training data for this task. Participants are fee to use any suitable
training material such as parallel corpora, wordnets or bilingual lexica.

Participants are encouraged to participate in as many of the four language
pairs as possible, but may also choose any subset.

The task organizers have compiled a test data set for the selected language pairs of
almost 500 sentences each. In the selection of test data we aim for realism, by
selecting words and phrases that may prove challenging for language learners.
To achieve this, we gather language learning exercises with gaps and
cloze-tests, as well as learner corpora with annotated errors to act as the
basis for our test set. When L2 sentences with such marked error fragments are
gathered, or gaps specifically designed to test a specific aspect of language
ability, we manually translate these fragments into L1, effectively forming a
sentence pair for the test set. Note that the test sentences will not contain
other L2 learner errors, we only use the errors of the L2 learners to get more
natural places to insert the L1 phrases. 

We also provide trial data for the selected language pairs consisting of 500
sentences as well. This trial data is semi-automatically generated using a
parallel corpus, namely the Europarl corpus (Koehn, 2005). We performed a
manual selection to get sentences that contain translations of appropriate
words or phrases that mimick the L2 writing assistant task as naturally as
possible. It has to be noted that this trial set is less optimised for realism
than the test data. Nevertheless, it suffices to measure relative system
performance, and it is a sufficiently large set.

The trial data, test data and tools are included in this github repository.
Installation of the tools will be explained one of the next chapters.
 
Learner Corpus
=========================================

We have compiled a learner corpus for each of the four
language pairs. It is contained in this repository:

See http://github.com/proycon/semeval2014task5/corpus/ 

Results
=========================================

Six teams from all over the world participated in this task with their
translation assistance system. The system output of all participants, as well
as the evaluation is contained in this repository. Participants output and the
evaluation output is found in the ``evaluation/`` directory.

 * Evaluation results (static): [evaluation/semeval_results.html](http://raw.github.com/proycon/semeval2014task5/raw/master/evaluation/semeval_results.html)
 * Evaluation results (IPython 3 Notebook): [evaluation/semeval_results.ipynb](http://raw.github.com/proycon/semeval2014task5/raw/master/evaluation/semeval_results.ipynb)


The evaluation has been implemented in an IPython 3 Notebook, you can run it to
reproduce the evaluation. You may also add additional system output to the
``evaluation/`` directory, it will be automatically included in the evaluation
so you can measure against the SemEval participants. To run the IPython
Notebook:

 * Make sure you have Python 3,  IPython3, numpy, matplotlib,  and libsemeval2014task5 installed (the latter is explained in the next chapter)
 * Clone this git repository
 * ipython3 notebook evaluation/semeval_results.ipynb
 * Point your browser to http://localhost:8080
 * Adapt the DIR variable in the notebook to reflect your own installation


Tools & Python Library - Version 2.0
=========================================


Installation
--------------

System-wide installation:

    $ sudo python ./setup.py install

Python usually defaults to Python 2, but you may also use Python 3, this is
required if you want to use the IPython Notebook with the results:

    $ sudo python3 ./setup.py install

If you obtain an import error then make sure the package ``python-setuptools`` is
installed in your distribution. You also need the package ``python-lxml``. 

If you have no sudo-rights, then you can install the library locally
using the ``--prefix`` switch, make sure the target prefix is in your ``$PYTHONPATH``.

Tools
--------------

The following tools are included:


 * ``semeval2014task5-setview``  - This tool simply prints a set to standard output in a terminal, it takes one XML file as argument

 * ``semeval2014task5-evaluate`` - This is the evaluation script for evaluating your system's output against the trial/test set.


Evaluation
--------------

The evaluation script should be run as follows:

    $ semeval2014task5-evaluate --ref trialdata.xml --out systemout.xml

If you want additional Machine Translation evaluation metrics (BLEU, METEOR,
NIST,TER, WER, PER), you need to download the MT Evaluation Scripts from 
http://lst-science.ru.nl/~proycon/mtevalscripts.tar.gz and explicitly pass 
the path to where you decompressed those using ``--mtevaldir=/path/to/mtevalscripts`` .

For out-of-five mode you need to add the ``-a`` flag to take into account alternatives.

For case-insensitive scoring, add the ``-i`` flag. 

Format Library
---------------

The semeval2014task5.format module enables you to easily read and write the XML
format for this task.  Import the format library in your Python source as
follows:

    import libsemeval2014task5 format as format

An example system that shows the functionality of this library has been
implemented in example.py, which has been heavily commented. Please consult
this to learn how the library works. It implements a full system that
'translates' fragments to upper-case instead of doing actual translation from
L1 to L2.


XML Format Specification
==========================================================================

The trial data and test data for this task are delivered in a straightforward
XML format using the UTF-8 character encoding.  The output of your system has
to adhere to this format as well, facilitating automatic evaluation.

Consider the following example set with English as L1 and Spanish as L2,
containing only two sentence pairs:


    <sentencepairs L1="en" L2="es">
        <s id="1">
            <input>Quiero <f id="1">know whether</f> 
            se puede hacer este tipo de objeción a lo que sólo es un 
            informe , no una propuesta legislativa , y si es algo que 
            puedo plantear el jueves .</input>
            <ref>Quiero <f id="1">saber si</f>  se
            puede hacer este tipo de objeción a lo que sólo es un informe 
            , no una propuesta legislativa , y si es algo que puedo 
            plantear el jueves .</ref>
        </s>
        <s id="2">
            <input>Este reacondicionamiento , que <f id="1">lasted</f>  varios
            meses , cortó esta importante vía de transporte entre el norte y
            el sur de Europa .</input>
            <ref>Este reacondicionamiento , que <f id="1">duró</f>  varios 
            meses , cortó esta importante vía de transporte entre
            el norte y el sur de Europa .</ref>
        </s>
    </sentencepairs>


The format's root tag is ``<sentencepairs>``, within it are numerous sentence pairs
in ``<s>`` blocks. Each sentence pair consists of an ``<input>`` sentence in L2 with a
marked fragment in L1 and a ``<ref>`` (reference) sentence in L2, in which the same
fragment is marked, this time in L2. The fragment is marked using the ``<f>``
element. Both the sentence as well as the fragment carry an ID, the fragment's
ID will always be one as we do only one fragment per sentence at a time.

Your output data has to adhere to this format, but instead of ``<ref>`` you have to
use ``<output>``, an example:

    <sentencepairs L1="en" L2="es">
    <s id="1">
        <input>Quiero <f id="1">know whether</f> 
        se puede hacer este tipo de objeción a lo que sólo es un 
        informe , no una propuesta legislativa , y si es algo que 
        puedo plantear el jueves .</input>
        <output>Quiero <f id="1">saber si</f>  se
        puede hacer este tipo de objeción a lo que sólo es un informe 
        , no una propuesta legislativa , y si es algo que puedo 
        plantear el jueves .</output>
    </s>
    <s id="2">
        <input>Este reacondicionamiento , que <f id="1">lasted</f>  varios
        meses , cortó esta importante vía de transporte entre el norte y
        el sur de Europa .</input>
        <output>Este reacondicionamiento , que <f id="1">duró</f>  varios 
        meses , cortó esta importante vía de transporte entre
        el norte y el sur de Europa .</output>
    </s>
    </sentencepairs>

You're not obliged to repeat the input as done here, mere output elements would be sufficient.

The out-of-five evaluation method allows you to output alternatives, this is
done as follows; we show an excerpt of a fragment with alternatives:

    <f id="1">option1<alt>option2</alt><alt>option3</alt><alt>option4</alt><alt>option5</alt></f> 

Always ensure that your system output is valid XML, you can test this with an XML tool such as
``xmllint``. 



