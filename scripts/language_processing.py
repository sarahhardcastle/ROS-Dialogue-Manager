# -*- coding: utf-8 -*-

import spacy
import inflect
import word_dict
import regex as re

nlp = spacy.load('en')

def process_sentence(sentence):
    global split_sentence
    processed_speech = [[], []]
    
   # sentence = ''
    split_sentence = sentence.split()
   # for index, word in enumerate(split_sentence):
   #     if re.match('(\d+)m' ,word):
   #         split_sentence[index] = word[0:-1]
   #         word = word[0:-1] + " meters"
   #     sentence += word + ' '

    doc = nlp(unicode(sentence))

    for word in doc:
        print (word.lemma_, word.tag_, [child for child in word.children])

    root = next((x for x in doc if x.dep_ == unicode('ROOT')), None)
    print(type(root))

    if doc[-1].text == '?':
        processed_speech[0].append('Question')

    elif root.lemma_ == 'be':
        processed_speech[0].append('Statement')

    elif root.tag_ in ['VB', 'VBD', 'VBP', 'VBZ', 'RB']:
        action(doc, root, processed_speech)
    
    print (root.tag_, processed_speech)

    return processed_speech

def action(doc, token, processed_speech):
    if (token.lemma_ in word_dict.MOVE):
        processed_speech[0].append('Action')
        processed_speech[1].append(token.lemma_)

    elif (token.text in word_dict.DIRECTION):
        processed_speech[0].append('Direction')
        processed_speech[1].append(token.text)

    elif (token.tag_ == 'RB'):
        processed_speech[0].append('Adverb')
        processed_speech[1].append(token.lemma_)    

    elif (token.tag_ == 'IN'):
        processed_speech[0].append('Preposition')
        processed_speech[1].append(token.lemma_)
        preposition(doc, token, processed_speech)

    elif (token.lemma_ in word_dict.UNIT):
        processed_speech[0].append('UNIT')
        processed_speech[1].append(token.lemma_)

    elif (token.tag_ == 'CD'):
        number = ''
        index = 0
        for j in doc:
            if j.text == token.text:
                while doc[index - 1].tag_ == 'CD' or doc[index - 1].text == 'and':
                    index -= 1
                number = re.match(r"(\d+)", split_sentence[index]).group(0)
                break
            index = index + 1
        processed_speech[0].append('Number')
        processed_speech[1].append(int(number))


    for child in token.children:        
        processed_speech = action(doc, child, processed_speech)
    
    return processed_speech

def preposition(doc, token, processed_speech):
    for child in token.children:
        if (child.tag_ == 'NN'):
            processed_speech[0].append('Noun')
            processed_speech[1].append(child.lemma_)
    return processed_speech

def distance(doc, token):
    global split_sentence
    for child in token.children:
        if (child.tag_ == 'CD'):
            number = ''
            index = 0
            for j in doc:
                if j.text == child.text:
                    while doc[index - 1].tag_ == 'CD' or doc[index - 1].text == 'and':
                        index -= 1
                    number += split_sentence[index]
                    break
                index = index + 1
            return ('Number', number)

process_sentence("Hello, this is a test")