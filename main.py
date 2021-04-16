import spacy
from spacy import displacy
from nltk import Tree


def print_hi(name):

    nlp = spacy.load('en_core_web_sm')

    piano_text = 'Gus is learning piano with his teacher'
    extraction_paths(piano_text)
    """piano_doc = nlp(piano_text)

    for token in piano_doc:
        print(token.text, token.tag_, token.head.text, token.dep_)

    [to_nltk_tree(sent.root).pretty_print() for sent in piano_doc.sents]
    root = search_root(piano_doc)
    sub = extraction_subtree(piano_doc[3])
    for token in sub:
        print(token.text, token.tag_, token.head.text, token.dep_)

    # extractiom_root_token(root, piano_doc[6])
    # http://127.0.0.1:5000
    # displacy.serve(piano_doc, style='dep')"""


# extract a path of dependency relations from the ROOT to a token
def extractiom_root_token1(root, token, path):
    if root == token:
        print(root.text + '(' + root.dep_ + ')', end=' ')
        path.append(token)
    else:
        extractiom_root_token1(root, token.head, path)
        print('->  ' + '(' + token.dep_ + ')  ' + token.text, end=' ')
        path.append(token)


def extraction_paths(sentece):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentece)

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

# check if a given list of tokens (segment of a sentence) forms a subtree

# identify head of a span, given its tokens

# extract sentence subject, direct object and indirect object spans


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
