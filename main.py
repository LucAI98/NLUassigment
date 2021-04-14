import spacy
from spacy import displacy


def print_hi(name):

    print(f'Hi, {name}')

    nlp = spacy.load('en_core_web_sm')

    piano_text = 'Gus is learning piano with his teacher'
    piano_doc = nlp(piano_text)
    for token in piano_doc:
        print(token.text, token.tag_, token.head.text, token.dep_)

    # http://127.0.0.1:5000
    displacy.serve(piano_doc, style='dep')

# extract a path of dependency relations from the ROOT to a token
def extractiom_root_token():
    print('Boh')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
