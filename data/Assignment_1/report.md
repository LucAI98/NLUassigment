# Report

The functions implemented in this code are made with the help of spacy library.

## extraction_paths(sentence)
The function takes in input a sentence and prints the relations between each token in the sentence from the root to the token.
To do that, the sentence is first parsed and a doc object is obtained. Then save the path for each token through an auxiliar function.

```python
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
```

This auxiliar function saves and prints in a recorsive way the path from a token to the ROOT, thanks to `head` attribute.

```python
def extractiom_root_token1(root, token, path):
    if root == token:
        print(root.text + '(' + root.dep_ + ')', end=' ')
        path.append(token)
    else:
        extractiom_root_token1(root, token.head, path)
        print('->  ' + '(' + token.dep_ + ')  ' + token.text, end=' ')
        path.append(token)
```
## extraction_subtree_of_each_tokens(sentence)
The function takes as input a sentence and returns the subtree of words contained in the sentence.
Since: "A subtree of a tree T is a tree consisting of a node in T and all of its descendants in T." the function returns the subtree of the input word in sentence order, input word included.
It is possible to obtain the subtree through the `subtree` attribute.

```python
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
```

## is_subtree_of_sentence(list_tokens, sentence)
The function takes as input a sentence and a list of words. 
All the subtrees of the sentece are obtained exploiting `extraction_subtree_of_each_tokens()` and 
 each list is compared with list of tokens. The compare is a simple confront of the elements of the two list, if they are the same the function will return `True`, if not `False`.

```python
# check if a given list of tokens (segment of a sentence) forms a subtree
def is_subtree_of_sentence(list_tokens, sentence):
    subtrees = extraction_subtree_of_each_tokens(sentence)

    for subtree in subtrees:
        if compare_two_list(list_tokens, subtree) is True:
            return True
    return False

```

## head_span(span)
The function takes as input a sequence of words(not necessary a sentence) and returns the root of those words with an auxiliar function used before.


```python
# identify head of a span, given its tokens
def head_span(span):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(span)

    return search_root(doc)
```

## extract_info_in_spans(sentence)
The function takes as input a sentence and returns a dictionary containing as key the relation (`'nsubj'`, `'dobj'`, `'iobj'`) and as value a list containing the words related to the key.
After parsing the sentence it checks if the dependency relation is one of the key above, in a positive case a list containing the subtree of the token is populated. Then the list is joined in order to have one single string. 
Lastly it returns the dictionary list.

```python
# extract sentence subject, direct object and indirect object spans
def extract_info_in_spans(sentence):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)

    dict_list = {}
    for token in doc:
        span_list = []
        if token.dep_ == 'nsubj' or token.dep_ == 'dobj' or token.dep_ == 'iobj':
            for descendant in token.subtree:
                span_list.append(descendant.text)
            span_list = ' '.join(span_list)
            dict_list[token.dep_] = span_list

    return dict_list
```
# Output
When you start the program all these functions are tested with `Gus is learning piano with his teacher.` sentence:
```
 --- Paths for each tokens ---
learning(ROOT) ->  (nsubj)  Gus  
learning(ROOT) ->  (aux)  is  
learning(ROOT)  
learning(ROOT) ->  (dobj)  piano  
learning(ROOT) ->  (dobj)  piano ->  (prep)  with  
learning(ROOT) ->  (dobj)  piano ->  (prep)  with ->  (pobj)  teacher ->  (poss)  his  
learning(ROOT) ->  (dobj)  piano ->  (prep)  with ->  (pobj)  teacher  
learning(ROOT) ->  (punct)  .  

 --- Subtree for each tokens ---
[Gus]
[is]
[Gus, is, learning, piano, with, his, teacher, .]
[piano, with, his, teacher]
[with, his, teacher]
[his]
[his, teacher]
[.]

 --- Check if a list of token is a subtree ---
[with, his, teacher] True
[with, teacher] False

 --- Head of a span ---
piano with
piano

 --- Extracted info of the sentence ---
{'nsubj': 'Gus', 'dobj': 'piano with his teacher'}
```
