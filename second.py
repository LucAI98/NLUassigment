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

    # read the corpus of the conll file
    test_sents = conll.read_corpus_conll('data/conll2003/test.txt', ' ')
    # train_sents = conll.read_corpus_conll('data/conll2003/train.txt', ' ')
    # chunks_test = conll.get_chunks('data/conll2003/test.txt', fs=' ')

    list_of_token = cut_separator(test_sents)
    doc_list = load_list_into_spacy(nlp, list_of_token)

    # getting references and hypothesis
    refs = [[(text, iob) for text, pos, chunk, iob in sent]for sent in list_of_token]
    hyps = load_hyps(doc_list)

    # compute the performances of NER
    results = conll.evaluate(refs, hyps)
    acc = accuracy(refs, hyps)

    # show the results
    print('\n--- Accuracy of the model ---')
    for key in acc.keys():
        print('{}: {}'.format(key, acc[key]))
    print('\n')

    pd_tbl = pd.DataFrame().from_dict(results, orient='index')
    pd_tbl.round(decimals=3)
    print('--- chunk level performance ---')
    print('{}\n'.format(pd_tbl))

    # group the entities and show the most used combination
    entity_groups = []
    for doc in doc_list:
        entity_group = grouping_entities(doc)
        entity_groups.append(list(entity_group))

    freq = frequency_check(entity_groups)

    print('--- best frequencies of group entities ---')
    for i, k in enumerate(freq.keys()):
        if i <= 20:
            print('{} : {}'.format(k, freq[k]))

    new_hyp = []
    [new_hyp.append(list(extend_noun_compound(doc))) for doc in doc_list]

    results2 = conll.evaluate(refs, new_hyp)
    acc = accuracy(refs, new_hyp)

    # show the results
    print('\n--- Accuracy of the model ---')
    for key in acc.keys():
        print('{}: {}'.format(key, acc[key]))
    print('\n')

    pd_tbl = pd.DataFrame().from_dict(results2, orient='index')
    pd_tbl.round(decimals=3)
    print('--- chunk level performance ---')
    print('{}\n'.format(pd_tbl))


# cut from the list the separator sentence (-DOCSTART-)
def cut_separator(sents):
    list_of_token = []
    flag = True

    # appends only the sentence that have more then one element
    for sent in sents:
        if len(sent) <= 1:
            flag = False
        if flag:
            list_of_token.append(list(sent))
        flag = True

    return list_of_token


# take the data of conll and covert them in doc
def load_list_into_spacy(nlp, data):

    doc_list = []

    for sent in data:
        doc = Doc(nlp.vocab, words=[w[0] for w in sent])
        for name, proc in nlp.pipeline:
            doc = proc(doc)
        doc_list.append(doc)

    return doc_list


# convert the doc list in a list (text, ent)
def load_hyps(doc_list):
    hyps = []

    for doc in doc_list:
        aux_list = []
        for token in doc:
            tmp = token.ent_iob_
            if token.ent_iob_ != 'O':
                tmp += '-' + map.spacy_to_conll[token.ent_type_]     # convert the type
            aux_list.append((token.text, tmp))
        hyps.append(aux_list)

    return hyps


# compute the total and class accuracy and save them
def accuracy(refs, hyps):
    accuracy_class = {}
    count = {'total': [0, 0]}

    # error in case the length of the list are different
    if len(hyps) != len(refs):
        raise ValueError(
            "Size Mismatch: ref: {} & hyp: {}".format(len(refs), len(hyps)))

    # control of the element in the same position and save the result in dict
    for i, sent in enumerate(hyps):
        for j, hyp in enumerate(sent):
            count['total'][1] += 1
            if hyp == refs[i][j]:
                count['total'][0] += 1

    accuracy_class['total'] = count['total'][0] / count['total'][1]
    return accuracy_class


# group entities that belong to the same chunks
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


# compute the frequency of the entity group (the class are all counted as different).
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

    return frequency_dict


# extend noun if the dep_ is compound following IOB scheme
def extend_noun_compound(doc):

    ent_iob = [t.ent_iob_ for t in doc]
    ent_types = [t.ent_type_ for t in doc]

    for token in doc:

        if token.dep_ == 'compound' and token.head.ent_type_ != "":     # check the dependencies
            ent_types[token.i] = token.head.ent_type_                   # change the entity

            # put the IOB tag
            if token.head.i < token.i:
                ent_iob[token.i] = 'I'
            elif token.head.ent_iob_ == 'B':
                ent_iob[token.head.i] = 'I'
                ent_iob[token.i] = 'B'
            else:
                ent_iob[token.i] = 'B'

    a = [(t.text, ent_iob + ("-" if ent_type != "" else "") + map.spacy_to_conll[ent_type]) for t, ent_iob, ent_type in
                    zip(doc, ent_iob, ent_types)]
    return a


if __name__ == '__main__':
    test_function()