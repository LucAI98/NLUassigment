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
    chunks_test = conll.get_chunks('data/conll2003/test.txt', fs=' ')

    # Remove DOC separator
    list_of_token = cut_separator(test_sents)
    doc_list = load_list_into_spacy(nlp, list_of_token)

    refs = [[(text, iob) for text, pos, synt_chunck, iob in sent]for sent in list_of_token]
    hyps = load_hyps(doc_list)

    results = conll.evaluate(refs, hyps)
    acc = accuracy(refs, hyps)

    print('\n--- Accuracy of the model ---')
    for key in acc.keys():
        print('{}: {}'.format(key, acc[key]))
    print('\n')

    pd_tbl = pd.DataFrame().from_dict(results, orient='index')
    pd_tbl.round(decimals=3)
    print('--- chunk level performance ---')
    print('{}\n'.format(pd_tbl))

    entity_groups = []
    for doc in doc_list:
        entity_group = grouping_entities(doc)
        entity_groups.append(list(entity_group))

    freq = frequency_check(entity_groups)

    print('--- frequency of group entities ---')
    for i, k in enumerate(freq.keys()):
        if i <= 20:
            print('{} : {}'.format(k, freq[k]))


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


def grouping_entities(doc):

    chunks = list(doc.noun_chunks)
    ents = list(doc.ents)

    list_chunks_ents = []
    for i, el in enumerate(chunks):
        tmp_list = []
        for e in el:
            tmp_list.append(e.ent_type_)
        list_chunks_ents.append(list(tmp_list))

    chunks_grouped = []
    for ent in list_chunks_ents:
        aux = ' '
        tmp_list = []
        for el in ent:
            if aux != el:
                tmp_list.append(el)
                aux = el
        chunks_grouped.append(list(tmp_list))

    tmp_list = []
    entity_group = []
    i = 0
    for e in ents:
        tmp_list.append(e.label_)
        if i == len(chunks_grouped):
            entity_group.append(list(tmp_list))
            tmp_list = []
        elif len(tmp_list) == len(chunks_grouped[i]):

            if tmp_list == chunks_grouped[i]:
                i += 1
            entity_group.append(list(tmp_list))
            tmp_list = []

    return entity_group


def frequency_check(entity_group):
    frequency_dict = {}

    for group in entity_group:
        for el in group:
            key = "_"
            for e in el:
                key = key + e + '_'

            if key in frequency_dict:
                frequency_dict[key] += 1
            else:
                frequency_dict[key] = 1

    frequency_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True))
    print(frequency_dict)
    return frequency_dict


if __name__ == '__main__':
    test_function()