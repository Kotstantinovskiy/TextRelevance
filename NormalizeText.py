import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import msgpack
import pickle

stopWords = set(stopwords.words("english")) |  set(stopwords.words("russian"))

from whoosh.analysis import RegexTokenizer
only_tokenizer = RegexTokenizer()
from whoosh.analysis import StandardAnalyzer
tokenizer = StandardAnalyzer(stoplist=stopWords)
from pymystem3 import Mystem
mystem = Mystem()
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def html2word_whoosh_text(d_text):
    title_list = []
    text = ''
    d_text['title_orig'] = []
    if d_text['title'] != None and d_text['title'] != []:
        for token in only_tokenizer(d_text['title']):
            d_text['title_orig'].append(token.text)

        d_text['title'] = d_text['title'].replace(u'—', '')
        d_text['title'] = d_text['title'].replace(u'–', '')
        d_text['title'] = d_text['title'].replace(u'−', '')
        d_text['title'] = d_text['title'].replace('-', '')
        for token in tokenizer(d_text['title']):
            text = mystem.lemmatize(token.text)[0]
            title_list.append(lemmatizer.lemmatize(text))
    d_text['title'] = title_list

    desc_list = []
    if d_text['description'] != None and d_text['description'] != [] and d_text['description'] != '' :
        for token in tokenizer(d_text['description']):
            text = mystem.lemmatize(token.text)[0]
            desc_list.append(lemmatizer.lemmatize(text))
    d_text['description'] = desc_list

    keyw_list = []
    if d_text['keywords'] != None and d_text['keywords'] != []:
        for token in tokenizer(d_text['keywords']):
            text = mystem.lemmatize(token.text)[0]
            keyw_list.append(lemmatizer.lemmatize(text))
    d_text['keywords'] = keyw_list

    h1_list = []
    if d_text['h1'] != None and d_text['h1'] != []:
        for token in tokenizer(d_text['h1']):
            text = mystem.lemmatize(token.text)[0]
            h1_list.append(lemmatizer.lemmatize(text))
    d_text['h1'] = h1_list

    h2_list = []
    if d_text['h2'] != None and d_text['h2'] != []:
        for token in tokenizer(d_text['h2']):
            text = mystem.lemmatize(token.text)[0]
            h2_list.append(lemmatizer.lemmatize(text))
    d_text['h2'] = h2_list

    h3_list = []
    if d_text['h3'] != None and d_text['h3'] != []:
        for token in tokenizer(d_text['h3']):
            text = mystem.lemmatize(token.text)[0]
            h3_list.append(lemmatizer.lemmatize(text))
    d_text['h3'] = h1_list

    h4_list = []
    if d_text['h4'] != None and d_text['h4'] != []:
        for token in tokenizer(d_text['h4']):
            text = mystem.lemmatize(token.text)[0]
            h4_list.append(lemmatizer.lemmatize(text))
    d_text['h4'] = h1_list

    h5_list = []
    if d_text['h5'] != None and d_text['h5'] != []:
        for token in tokenizer(d_text['h5']):
            text = mystem.lemmatize(token.text)[0]
            h5_list.append(lemmatizer.lemmatize(text))
    d_text['h5'] = h5_list

    strong_list = []
    if d_text['strong'] != None and d_text['strong'] != []:
        for token in tokenizer(d_text['strong']):
            text = mystem.lemmatize(token.text)[0]
            strong_list.append(lemmatizer.lemmatize(text))
    d_text['strong'] = strong_list

    ins_list = []
    if d_text['ins'] != None and d_text['ins'] != []:
        for token in tokenizer(d_text['ins']):
            text = mystem.lemmatize(token.text)[0]
            ins_list.append(lemmatizer.lemmatize(text))
    d_text['ins'] = ins_list

    s = []
    s_lemm = []
    s_position = []
    sentence_lemm = []
    sentence = []
    k = 0
    for senten in sent_tokenize(d_text['text']):
        senten = senten.replace(u'—', '')
        senten = senten.replace(u'–', '')
        senten = senten.replace(u'−', '')
        senten = senten.replace('-', '')
        for term in tokenizer(senten):
            if len(term.text) <= 25 and len(term.text) > 1:
                sentence.append(term.text)
                text = mystem.lemmatize(term.text)[0]
                sentence_lemm.append(lemmatizer.lemmatize(text))
                k += 1
        s_position.append(k)
    d_text['text_position'] = s_position
    d_text['orig_text'] = sentence
    d_text['text'] = sentence_lemm
    return

if __name__ == '__main__':
    start = 72001
    step = 1500
    for i in range(1):
        name = 'doc_dict_clear_text_' + str(start + i * step) + '_' + str(start + (i + 1) * step) + '.bin'
        print name
        with open("obrabotka/" + name, 'rb') as index_f:
            d = msgpack.load(index_f, encoding='utf-8')
        for dic in d:
            html2word_whoosh_text(dic)
        with open("obrabotka_sen/" + name, 'wb') as f_dict:
            msgpack.dump(d, f_dict, use_bin_type=True)
        print name
