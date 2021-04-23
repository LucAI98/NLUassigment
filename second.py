import conll
import spacy
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath('../data/'))


def test_function():
    nlp = spacy.load('en_core_web_sm')

    sents = conll.read_corpus_conll('data/conll2003/test.txt')

    # Remove DOC separator
    list_of_token = []
    flag = True
    for sent in sents:
        if len(sent) <= 1:
            flag = False
        if flag:
            list_of_token.append(list(sent))
        flag = True

    list_of_string = []
    for el in list_of_token:
        list_of_split = []
        for token in el:
            splitted = token[0].split()
            list_of_split.append(splitted[0])
        list_of_string.append(list(list_of_split))

    list_input = []
    for el in list_of_string:
        aux = ''
        for i in range(len(el)):
            aux += el[i] + ' '

        list_input.append(aux)

    for el in list_input:
        doc = nlp(el)
        print([ent.text for ent in doc.ents])
        print([(t.ent_type_, t.ent_iob_) for t in doc])
    '''
    # getting references (note that it is testb this time)
    refs = [[(text, iob) for text, pos, iob in sent] for sent in conll2002.iob_sents('esp.testb')]
    print(refs[0])
    # getting hypotheses
    hyps = [hmm_ner.tag(s) for s in conll2002.sents('esp.testb')]
    print(hyps[0])

    results = evaluate(refs, hyps)
    '''


if __name__ == '__main__':
    test_function()