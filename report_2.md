# Report

# 0. Evaluate spaCy NER on CoNLL 2003

I loaded CoNLL 2003 through a function `read_corpus_conll()` provided by the script conll.py.
I made the output list leaner with an auxiliar function in which cut the document separators.
Then I apply spacy to process all the sentences and extract the entities to evaluate the total accuracy, precision, recall, f-measure.
Obtaining as results:
 ```
 --- Accuracy of the model ---
total: 0.784168785828197


--- chunk level performance ---
              p         r         f     s
LOC    0.481481  0.015606  0.030233  1666
MISC   0.078103  0.565527  0.137252   702
PER    0.761373  0.592547  0.666434  1610
ORG    0.443798  0.275904  0.340267  1660
total  0.247238  0.325470  0.281011  5638
 ```
# 1. Grouping of Entities.

Chunks from Doc.noun_chunks can contain multiple entities, so I wrote a function that extract the entities from the chunks, if there are different type of ent, I ll group them in a class.
I decided to consider the order and number of entities in a group as different classes for the count of the frequency.
 ```
--- best frequencies of group entities ---
_CARDINAL_ : 972
_GPE_ : 919
_PERSON_ : 777
_ORG_ : 699
_DATE_ : 665
_NORP_ : 192
_MONEY_ : 97
_ORDINAL_ : 77
_GPE_CARDINAL_ : 74
_CARDINAL_PERSON_ : 71
_TIME_ : 68
_PERCENT_ : 57
_CARDINAL_GPE_ : 48
_PERSON_GPE_ : 45
_CARDINAL_CARDINAL_ : 43
_QUANTITY_ : 40
_LOC_ : 36
_EVENT_ : 35
_PERSON_CARDINAL_ : 32
_GPE_GPE_ : 27
_GPE_DATE_ : 21
 ```
# 2. Fix segmentation errors

A possible post processing step would be to adjust the span of the entities. So I extended the entity span to cover the full noun-compounds
But after this change the performances are worse then before.
 ```
--- Accuracy of the model ---
total: 0.7766475582949011


--- chunk level performance ---
              p         r         f     s
LOC    0.373134  0.015006  0.028852  1666
MISC   0.078958  0.582621  0.139068   702
PER    0.602362  0.570186  0.585833  1610
ORG    0.322932  0.268072  0.292956  1660
total  0.220518  0.318730  0.260680  5638
 ```