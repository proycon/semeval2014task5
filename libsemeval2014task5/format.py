####################################################
#
# SemEval 2014 - task 5 - L2 Writing Assistant
#
# This library providers a Reader and a Writer interface
# to the XML file format used in the task.
#
# Licensed under GPLv3
#
####################################################

from __future__ import print_function, unicode_literals, division, absolute_import

import lxml.etree
from lxml.builder import E
import sys
import io

ansicolors = {"red":31,"green":32,"yellow":33,"blue":34,"magenta":35, "bold":1 }
def colorf(color):
    return lambda x: "\x1B[" + str(ansicolors[color]) + "m" + x + "\x1B[0m"


class Reader:
    def __init__(self, filename):
        self.filename = filename
        self.stream = io.open(filename,'rb')
        self.L1 = "unknown"
        self.L2 = "unknown"

        parser = lxml.etree.iterparse(self.stream, events=("start","end"))
        for action, node in parser:
            if action == "end" and node.tag == "sentencepairs":
                if 'L1' in node.attrib:
                    self.L1 = node.attrib['L1']
                if 'L2' in node.attrib:
                    self.L2 = node.attrib['L2']
                break

        self.stream.seek(0)

    def __iter__(self):
        parser = lxml.etree.iterparse(self.stream, events=("start","end"))
        for action, node in parser:
            if action == "end" and node.tag == "sentencepairs":
                if 'L1' in node.attrib:
                    self.L1 = node.attrib['L1']
                if 'L2' in node.attrib:
                    self.L2 = node.attrib['L2']
            elif action == "end" and node.tag == "s":
                yield SentencePair.fromxml(node)

    def close(self):
        self.stream.close()
        self.stream = None


    def reset(self):
        self.stream.seek(0)

    def __del__(self):
        if self.stream: self.stream.close()

class Writer:
    def __init__(self, filename, L1="unknown", L2="unknown"):
        self.filename = filename
        self.stream = io.open(filename, 'w', encoding='utf-8')
        self.stream.write('<sentencepairs L1="' + L1 + '" L2="'+L2+'">\n')

    def write(self, sentencepair):
        assert isinstance(sentencepair, SentencePair)
        if sys.version > '3':
            self.stream.write( str(lxml.etree.tostring(sentencepair.xml(), xml_declaration=False, pretty_print=True, encoding='utf-8'),'utf-8') )
        else:
            self.stream.write( unicode(lxml.etree.tostring(sentencepair.xml(), xml_declaration=False, pretty_print=True, encoding='utf-8'),'utf-8') )

    def close(self):
        self.stream.write('</sentencepairs>\n')
        self.stream.close()
        self.stream = None


    def __del__(self):
        if self.stream: self.close()

class SentencePair:
    def __init__(self, id,input, output, ref=None,source=None,category=None):
        if not isinstance(input, tuple):
            raise ValueError("Input - Expected tuple, got " + str(type(input)), input)
        if not isinstance(output, tuple) and not (output is None):
            raise ValueError("Output - Expected tuple, got " + str(type(output)), output)
        if not isinstance(ref, tuple) and not (ref is None):
            raise ValueError("Ref - Expected tuple, got " + str(type(ref)), ref)
        self.id = id
        self.input = input
        self.output = output
        self.ref = ref
        self.source = source
        self.category = category


    @staticmethod
    def _parsevalue(node):
        content = []
        if node.text:
            for t in node.text.split():
                 if t: content.append(t)
        for subnode in node:
            if subnode.tag == "f":
                if subnode.text:
                    f = Fragment(tuple([ x.strip() for x in subnode.text.split() if x and x.strip() ]), subnode.attrib.get('id',1), subnode.attrib.get('confidence',None) )
                    content.append(f)
                else:
                    f =  Fragment(None, subnode.attrib.get('id',1), subnode.attrib.get('confidence',None))
                    content.append(f)
                for subsubnode in subnode:
                    if subsubnode.tag == 'alt' and subsubnode.text:
                        f.alternatives.append( Alternative(tuple([ x.strip() for x in subsubnode.text.split() if x and x.strip() ]), subsubnode.attrib.get('confidence',None) ) )
            elif subnode.text:
                for t in subnode.text.split():
                    if t: content.append(t)
            if subnode.tail and subnode.tail.strip(): content.append(subnode.tail.strip())
        return tuple(content)


    @staticmethod
    def fromxml(node):
        input = ref = output = None
        for subnode in node:
            if subnode.tag == 'input':
                input = SentencePair._parsevalue(subnode)
            elif subnode.tag == 'ref':
                ref = SentencePair. _parsevalue(subnode)
            elif subnode.tag == 'output':
                output = SentencePair._parsevalue(subnode)
        return SentencePair(node.attrib.get('id',1), input,output,ref, node.attrib.get('source',None), node.attrib.get('category',None))

    def replacefragment(self, old,new,s):
        s2 = []
        if s:
            for x in s:
                if x == old:
                    s2.append(new)
                else:
                    s2.append(x)
        return tuple(s2)


    def fragments(self, s, returndict=False):
        d = {}
        if s:
            for x in s:
                if isinstance(x, Fragment):
                    left = ""
                    right = ""
                    mode = 0
                    for y in s:
                        if isinstance(y,Fragment):
                            if x == y:
                                mode = 1
                        else:
                            if mode == 0:
                                left += " " + y
                            else:
                                right += y + " "
                    if returndict:
                        d[x.id] = x #no context
                    else:
                        d[x.id] = (left.strip(), x, right.strip())
        if returndict:
            return d
        else:
            return d.values()


    def inputfragments(self):
        return self.fragments(self.input)

    def outputfragments(self):
        return self.fragments(self.output)

    def reffragments(self):
        return self.fragments(self.ref)

    def inputfragmentsdict(self): #no context
        return self.fragments(self.input,True)

    def outputfragmentsdict(self):
        return self.fragments(self.output,True)

    def reffragmentsdict(self):
        return self.fragments(self.ref,True)

    def inputstr(self, mark=False,color=None):
        return " ".join(SentencePair._str(self.input,mark,color))

    def outputstr(self, mark=False,color=None):
        return " ".join(SentencePair._str(self.output,mark,color))

    def refstr(self, mark=False, color=None):
        return " ".join(SentencePair._str(self.ref,mark,color))

    def isref(self):
        return bool(self.ref)

    def isoutput(self):
        return bool(self.output)

    @staticmethod
    def _str(t, mark=False, color=None):
        for x in t:
            if isinstance(x, Fragment):
                if x.value:
                    for y in x.value:
                        if color:
                            yield colorf(color)(y)
                        elif mark:
                            yield "*" + y + "*"
                        else:
                            yield y
                else:
                    if color:
                        yield colorf(color)("{?)")
                    elif mark:
                        yield '*{?}*'
                    else:
                        yield '{?}'

            elif isinstance(x, str):
                yield x
            elif sys.version < '3' and isinstance(x, unicode):
                yield x
            else:
                raise ValueError("Expected string or Fragment: got " + str(type(x)))

    @staticmethod
    def _serialisevalue(v):
        result = []
        l = len(v)
        for i, x in enumerate(v):
            if isinstance(x, Fragment):
                if i > 0: result.append(" ")
                result.append(x.xml())
                if i < l - 1: result.append(" ")
            elif result and ( isinstance(result[-1], str) or (sys.version < '3' and isinstance(result[-1],unicode))):
                result[-1] += " " + x
            else:
                result.append(x)
        return result


    def xml(self):
        children = []
        if self.input: children.append( E.input(*SentencePair._serialisevalue(self.input)))
        if self.output: children.append( E.output(*SentencePair._serialisevalue(self.output)))
        if self.ref: children.append( E.ref(*SentencePair._serialisevalue(self.ref)))
        kwargs = {'id': str(self.id)}
        if self.source:
            kwargs['source'] = self.source
        if self.category:
            kwargs['category'] = self.category
        return E.s(*children, **kwargs)

class Fragment:
    def __init__(self, value,id=1, confidence=None):
        assert isinstance(value, tuple) or value is None
        self.id = id
        self.value = value
        self.confidence = confidence
        self.alternatives = []

    def __str__(self, mark=False):
        if mark:
            return "*" + self._str() + "*"
        else:
            if self.value:
                return " ".join(self.value)
            else:
                return "{?}"

    def __len__(self):
        if self.value:
            return len(self.value)
        else:
            return 0

    def __iter__(self):
        if self.value:
            for word in self.value:
                yield word

    def __hash__(self):
        if self.value:
            return hash(self.value)
        else:
            return 0

    def __bool__(self):
        if self.value:
            return True
        else:
            return False

    def xml(self):
        kwargs = {'id': str(self.id)}
        args = []
        if self.value: args.append(" ".join(self.value))
        for a in self.alternatives:
            args.append( a.xml() )
        if not (self.confidence is None):
            kwargs['confidence'] = str(self.confidence)
        return E.f(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, Fragment):
            return (self.id == other.id and self.value == other.value)
        else:
            return False

class Alternative(Fragment):
    def __init__(self, value, confidence=None):
        assert isinstance(value, tuple) or value is None
        self.value = value
        self.confidence = confidence
        self.id = None

    def xml(self):
        kwargs = {}
        if not (self.confidence is None):
            kwargs['confidence'] = str(self.confidence)
        if self.value:
            return E.alt(" ".join(self.value), **kwargs)
        else:
            return E.alt(**kwargs)

