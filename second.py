import conll
import spacy
import os
import sys
import map_spacy_conll as map
import pandas as pd
from spacy.tokens import Doc
sys.path.insert(0, os.path.abspath('../data/'))


def test_function():
    nlp = spacy.load('en_core_web_sm')

    test_sents = conll.read_corpus_conll('data/conll2003/test.txt', ' ')
    train_sents = conll.read_corpus_conll('data/conll2003/train.txt', ' ')

    # Remove DOC separator
    list_of_token = cut_separator(test_sents)
    doc_list = load_list_into_spacy(nlp, list_of_token)

    refs = [[(text, iob) for text, pos, synt_chunck, iob in sent]for sent in list_of_token]
    hyps = load_hyps(doc_list)

    results = conll.evaluate(refs, hyps)
    acc = accuracy(refs, hyps)


def cut_separator(sents):
    list_of_token = []
    flag = True

    for sent in sents:
        if len(sent) <= 1:
            flag = False
        if flag:
            list_of_token.append(list(sent))
        flag = True

    return list_of_token


def load_list_into_spacy(nlp, data):

    doc_list = []

    for sent in data:
        doc = Doc(nlp.vocab, words=[w[0] for w in sent])
        for name, proc in nlp.pipeline:
            doc = proc(doc)
        doc_list.append(doc)

    return doc_list


def load_hyps(doc_list):
    hyps = []

    for doc in doc_list:
        aux_list = []
        for token in doc:
            tmp = token.ent_iob_
            if token.ent_iob_ != 'O':
                tmp += '-' + map.spacy_to_conll[token.ent_type_]
            aux_list.append((token.text, tmp))
        hyps.append(aux_list)

    return hyps


def accuracy(refs, hyps):
    accuracy_class = {}
    count = {'total': [0, 0]}

    if len(hyps) != len(refs):
        raise ValueError(
            "Size Mismatch: ref: {} & hyp: {}".format(len(refs), len(hyps)))

    for i, sent in enumerate(hyps):
        for j, hyp in enumerate(sent):
            key = hyp[1]
            count['total'][1] += 1
            if hyp == refs[i][j]:
                count['total'][0] += 1
            if key in count:
                count[key][1] += 1
                if key == refs[i][j][1]:
                    count[key][0] += 1
            else:
                count[key] = [1, 1]
    for key in count.keys():
        accuracy_class[key] = count[key][0] / count[key][1]
    return accuracy_class


if __name__ == '__main__':
    test_function()