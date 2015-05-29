# -*- coding: cp1251 -*-
import codecs
import re
import os
import csv
from tkFileDialog import askopenfilename



name = ''

def load():
    filename = askopenfilename()
    global name
    name = os.path.basename(filename)
    with codecs.open(filename, 'r', 'utf-8') as infile:
        text = infile.read()
    return text

def load_dict(filename):
    with codecs.open(filename, 'r', 'utf-8') as infile:
        text = infile.read()
    return text

def tokenize(text):
    chunks = text.split()
    tokens = []
    for chunk in chunks:
        token = chunk.strip(u" ")
        if token != u"":
            tokens.append(token)
    return tokens

def write_sent(list, filename):
    
    with codecs.open(filename, 'wb', 'utf-8') as file_sent:
        number = 0
        for sent in list:
            number += 1
            line = str(number) + '*' + sent
            file_sent.write(line + "\r\n")


def reading2(name_token):
    therms = []
    with codecs.open(name_token, 'r', 'utf-8') as intokens:
        tokens_typed = intokens.read()
        tokens_typed = tokens_typed.split('\r\n')
        for tt in tokens_typed:
            if tt != u'':
                tt = tt.split(' ')
                therms.append(tt)
        
    return therms

def endings(therms):
    
    num = 0
    max = len(therms)
    #print max

    for therm in therms:

        if therm[1] == u'.' and int(therm[0]) != max:
            
            n = int(therm[0])
            
            if therms[num + 1][1] == u'--':
                therm[2] = 'end'

        
        if therm[2] == 'other':
            
            
            if num == max - 1:
                a = 1
                
            if therms[num+1][2] != 'lower':

                therm[2] = 'end'

        if num != max-2:
                num = num + 1
    return therms 
            
def hyphens(therms):
    hyp = load_dict('hyphens.txt')
    hyphens = hyp.split('\r\n')
       
    
    for therm in therms:
        
        if therm[1] in hyphens:
            
            th = therm[1].split('-')
            the = unicode(th[0])
            
            if the.istitle():
                therm[2] = 'title'
            else:
                therm[2] = 'lower'
    
    return therms
    

def token_type(token2):
    token = unicode(token2)
   
    if token.islower() and token.isalpha():
        return "lower"
    elif token.istitle() and token.isalpha():
        return "title"
    elif token.isupper()and token.isalpha():
        return "upper"
    elif token.isalpha():
        return "mixed"
    elif token.isdigit():
        return "digit"
    elif token.isalnum():
        return "alnum"
    elif token.isspace():
        return "space"
    else:
        return "other"

def write_tokens(tokens, name_token):

    with codecs.open(name_token, 'wb', 'utf-8') as file_token:
        number_of_token = 0
        for token in tokens:

            number_of_token += 1
            parts = [str(number_of_token), token, token_type(token)]
            line = " ".join(parts)
            file_token.write(line + "\r\n")

def write_therms(tokens, name_token):

    with codecs.open(name_token, 'wb', 'utf-8') as file_token:
        number_of_token = 0
        for token in tokens:

            number_of_token += 1

            line = " ".join(token)
            file_token.write(line + "\r\n")

def clear(text):
    clear_text = text.strip()
    clear_text = re.sub('[,.?!:;]{1,3}', r' \g<0>', clear_text)
    clear_text = re.sub('["]', r'\g<0> ', clear_text)
    clear_text = re.sub('<[^>]+>', '', clear_text)
    
    clear_text = re.sub('([А-Я]) -- ([а-я]{1,3})', '\1-\2', clear_text)
    return clear_text

def error_end(therms):
    for therm in therms:
        if therm[1] == ',':
            therm[2] = 'other'
        if therm[2] == 'end':
            num = int(therm[0]) - 2
            if therms[num][2] == 'end':
                therms[num][2] = 'other'
                therm[2] = 'other'
        if therm[2] == 'other':
            num = int(therm[0]) - 2
            if therms[num][2] == 'end':
                therms[num][2] = 'other'
                therm[2] = 'other'
        if therm[1] == '(':
            num = int(therm[0]) - 2
            if therms[num][2] != 'end':
                therm[2] = 'other'

    return therms

def name_type(therms):
    n = 1
    name = 'name_' + str(n)
    for therm in therms:
       
        if therm[2] == 'title' and len(therm[1]) < 2:
            
            num = int(therm[0])
            if therms[num][2] == 'end':
               
                therms[num][2] = name
                therm[2] = name
               
                therms[num][2] = name
                therm[2] = name

        elif therm[2] == name:
           
            num = int(therm[0])
            if therms[num][2] == 'title':
                therms[num][2] = name
            if therms[num][2] == 'end':
                therms[num][2] = name

        else:
            n = n + 1
            name = 'name_' + str(n)        
               
    return therms

def date_type(therms):
    n = 1
    name = 'date_' + str(n)

    for therm in therms:

        if therm[2] == 'digit':
            num = int(therm[0])
            if num < len(therms):        
                if therms[num][2] == 'other':
                    
                    if therms[num + 1][2] == 'other':
                        

                        therm[2] = name
                        therms[num][2] = name
                        therms[num + 1][2] = name

                        n = n + 1
                        name = 'date_' + str(n)

        if therm[2] == 'other':
            dat = therm[1]
            if re.search(r'[1-9][1-9][-/][1-9][1-9][-/][1-9][1-9]*', dat):
                therm[2] = name
                n = n + 1
                name = 'date_' + str(n)

                          

    return therms
                    
def time_type(therms):
    n = 1
    name = 'time_' + str(n)

    for therm in therms:

        if therm[2] == 'digit':
            num = int(therm[0])
            if num < len(therms):
                if therms[num][2] == 'end':
                    tim = therms[num][1]

                    if re.search(r'\:[1-9]*', tim):
                        therm[2] = name
                        therms[num][2] = name
                        n = n + 1
                        name = 'time_' + str(n)

    return therms

def sentenc(therms):
    head = 0
    tail = 0
    sentences = []
    words = []
    max_len = len(therms)
    
    for therm in therms:
        words.append(therm[1])
    
    for therm in therms:
        
        if int(therm[0]) == max_len:
            
            tail = max_len - 1
            sent = ' '.join(words[head:])
            
            clear_sent = re.sub(' [,:;?!.]', r'\g<0>', sent)
            clear_sent = clear_sent.strip()
            sentences.append(clear_sent)
            
        if therm[2] == 'end':
            tail = int(therm[0])
            sent = ' '.join(words[head:tail-1])
            end = ''.join(words[tail-1:tail])
            sent = sent + end
            head = tail
            clear_sent = re.sub(' [,:;?!.]', r'\g<0>', sent)
            clear_sent = clear_sent.strip()
            sentences.append(clear_sent)
            
    return sentences

def go():
    text = load()

    name_clear = os.path.splitext(name)
    name_token = name_clear[0] + '_tokens.txt'
    name_sent = name_clear[0] + '_sentences.txt'
    

    clear_text = clear(text)
    
    tokenized_text = tokenize(clear_text)
    
    write_tokens(tokenized_text, name_token)

    therms = reading2(name_token)

    therms = hyphens(therms)

    therms = endings(therms)

    therms = name_type(therms)

    

    therms = error_end(therms)

    therms = time_type(therms)

    therms = date_type(therms)

    

    write_therms(therms, name_token)

    sentences = sentenc(therms)

    write_sent(sentences, name_sent)

    # ms.go_mystem(name_token)

def go_tokenize():
    text = load()
    name_clear = os.path.splitext(name)
    name_token = name_clear[0] + '_tokens.txt'

    clear_text = clear(text)  
    tokenized_text = tokenize(clear_text)

    write_tokens(tokenized_text, name_token)

    therms = reading2(name_token)
    therms = hyphens(therms)
    therms = endings(therms)
    therms = name_type(therms)
    therms = error_end(therms)
    therms = time_type(therms)
    therms = date_type(therms)

    write_therms(therms, name_token)

def go_sent():
    text = load()

    name_clear = os.path.splitext(name)
    name_token = name_clear[0] + '_tokens.txt'
    name_sent = name_clear[0] + '_sentences.txt'

    clear_text = clear(text)
    
    tokenized_text = tokenize(clear_text)
    
    write_tokens(tokenized_text, name_token)

    therms = reading2(name_token)

    therms = hyphens(therms)

    therms = endings(therms)

    therms = name_type(therms)

    

    therms = error_end(therms)

    therms = time_type(therms)

    therms = date_type(therms)

    

    write_therms(therms, name_token)

    sentences = sentenc(therms)

    write_sent(sentences, name_sent)


def wordcount(text):
    """
    Given a str, return the number of tokens
    """
    text = tokenize(clear(text))
    number_of_token = 0
    for token in text:
        if token_type(token) != 'other':
            number_of_token += 1
    return number_of_token

if __name__ == '__main__':

    go()

    print 'done'

    




