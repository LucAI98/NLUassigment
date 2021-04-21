import spacy
from spacy import displacy
from nltk import Tree


def test_function():
    piano_text = 'Gus is learning piano with his teacher.'  # test sentence

    # show the dependency tree of the sentence
    nlp = spacy.load('en_core_web_sm')
    piano_doc = nlp(piano_text)
    [to_nltk_tree(sent.root).pretty_print() for sent in piano_doc.sents]

    # first function
    print('\n --- Paths for each tokens ---')
    paths = extraction_paths(piano_text)

    # second function
    trees = extraction_subtree_of_each_tokens(piano_text)
    print('\n --- Subtree for each tokens ---')
    for subtree in trees:
        print(subtree)

    # third function
    print('\n --- Check if a list of token is a subtree ---')
    flag = is_subtree_of_sentence(trees[4], piano_text)
    print_flag(flag, trees[4])
    trees[4].pop(1)
    flag = is_subtree_of_sentence(trees[4], piano_text)
    print_flag(flag, trees[4])

    # forth function
    print('\n --- Head of a span ---')
    print(piano_doc[3:5])
    print(head_span(piano_doc[3:5].text))

    # fifth function
    print('\n --- Extracted info of the sentence ---')
    print(extract_info_in_spans(piano_text))
    """ Displacy potraits the dependency tree on the web page below
    # http://127.0.0.1:5000 
    displacy.serve(piano_doc, style='dep')"""


# extract a path of dependency relations from the ROOT to a token
def extractiom_root_token1(root, token, path):
    if root == token:
        print(root.text + '(' + root.dep_ + ')', end=' ')
        path.append(token)
    else:
        extractiom_root_token1(root, token.head, path)
        print('->  ' + '(' + token.dep_ + ')  ' + token.text, end=' ')
        path.append(token)


# extract the paths of dependency for each token
def extraction_paths(sentence):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)

    paths = []
    root = search_root(doc)
    for token in doc:
        path = []
        extractiom_root_token1(root, token, path)
        print(" ")
        paths.append(path)

    return paths


# extract subtree of a dependents given a token
def extraction_subtree(token):
    return list(token.subtree)


# extract the subtree for each token
def extraction_subtree_of_each_tokens(sentence):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)

    subtrees = []
    for token in doc:
        subtrees.append(extraction_subtree(token))

    return subtrees


# check if a given list of tokens (segment of a sentence) forms a subtree
def is_subtree_of_sentence(list_tokens, sentence):
    subtrees = extraction_subtree_of_each_tokens(sentence)

    for subtree in subtrees:
        if compare_two_list(list_tokens, subtree) is True:
            return True
    return False


# Compare two list element
def compare_two_list(l1, l2):
    l1.sort()
    l2.sort()

    if len(l1) != len(l2):
        return False
    else:
        for i in range(len(l1)):
            if l1[i].text != l2[i].text:
                return False
        return True


# identify head of a span, given its tokens
def head_span(span):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(span)

    return search_root(doc)


# extract sentence subject, direct object and indirect object spans
def extract_info_in_spans(sentence):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)

    dict_list = {}
    for token in doc:
        span_list = []
        if token.dep_ == 'nsubj' or token.dep_ == 'dobj' or token.dep_ == 'dative':
            for descendant in token.subtree:
                span_list.append(descendant.text)
            span_list = ' '.join(span_list)
            dict_list[token.dep_] = span_list

    return dict_list


# Prints the tree of a sentence
def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_


# Search the root in a doc
def search_root(doc):
    for token in doc:
        if token.dep_ == 'ROOT':
            root = token
    return root


def print_flag(flag, el):
    if flag is True:
        print(el, end=' ')
        print(True)
    else:
        print(el, end=' ')
        print(False)


if __name__ == '__main__':
    test_function()