import pandas as pd
from bs4 import BeautifulSoup
import os
import pickle

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

from whoosh.analysis import RegexTokenizer
from whoosh.analysis import StandardAnalyzer
from pymystem3 import Mystem
from nltk.stem import WordNetLemmatizer

stopWords = set(stopwords.words("english")) | set(stopwords.words("russian"))
only_tokenizer = RegexTokenizer()
tokenizer = StandardAnalyzer(stoplist=stopWords)
mystem = Mystem()
lemmatizer = WordNetLemmatizer()


def html2text_bs_visible(url_id, raw_html):
    parse_text = {}
    soup = BeautifulSoup(raw_html, "html.parser")

    parse_text['url_id'] = url_id

    if soup.title is not None:
        parse_text['title'] = soup.title.string.replace('ё', 'е')
    else:
        parse_text['title'] = []

    meta = soup.find_all('meta')
    if meta:
        for tag in meta:
            if tag.get("name", None) == "keywords":
                parse_text['keywords'] = tag.get("content", None).replace('ё', 'е')
            else:
                parse_text['keywords'] = []

            if tag.get("name", None) == "description":
                parse_text['description'] = tag.get("content", None).replace('ё', 'е')
            else:
                parse_text['description'] = []

    if soup.strong is not None:
        parse_text['strong'] = soup.strong.string.replace('ё', 'е')
    else:
        parse_text['strong'] = []

    if soup.h1 is not None:
        parse_text['h1'] = soup.h1.string.replace('ё', 'е')
    else:
        parse_text['h1'] = []

    if soup.h2 is not None:
        parse_text['h2'] = soup.h2.string.replace('ё', 'е')
    else:
        parse_text['h2'] = []

    if soup.h3 is not None:
        parse_text['h3'] = soup.h3.string.replace('ё', 'е')
    else:
        parse_text['h3'] = []

    if soup.h4 is not None:
        parse_text['h4'] = soup.h4.string.replace('ё', 'е')
    else:
        parse_text['h4'] = []

    if soup.h5 is not None:
        parse_text['h5'] = soup.h5.string.replace('ё', 'е')
    else:
        parse_text['h5'] = []

    if soup.ins is not None:
        parse_text['ins'] = soup.ins.string.replace('ё', 'е')
    else:
        parse_text['ins'] = []

    parse_text['text'] = soup.get_text().replace('ё', 'е')

    return parse_text


def parse_text(url_id):
    file = open("content/20190128/" + file_url_id.loc[file_url_id['url_id'] == url_id]['file'][0])
    url = file.readline()
    parse_text = html2text_bs_visible(url_id, file.read())
    return parse_text


def html2word_whoosh_text(tmp_text):
    tmp_text['title_orig'] = []

    title_list = []
    if tmp_text['title']:
        for token in only_tokenizer(tmp_text['title']):
            tmp_text['title_orig'].append(token.text)

        for token in tokenizer(tmp_text['title']):
            text = mystem.lemmatize(token.text)[0]
            title_list.append(lemmatizer.lemmatize(text))
    tmp_text['title'] = title_list

    desc_list = []
    if tmp_text['description'] != [] and tmp_text['description'] != '':
        for token in tokenizer(tmp_text['description']):
            text = mystem.lemmatize(token.text)[0]
            desc_list.append(lemmatizer.lemmatize(text))
    tmp_text['description'] = desc_list

    keyw_list = []
    if tmp_text['keywords']:
        for token in tokenizer(tmp_text['keywords']):
            text = mystem.lemmatize(token.text)[0]
            keyw_list.append(lemmatizer.lemmatize(text))
    tmp_text['keywords'] = keyw_list

    h1_list = []
    if tmp_text['h1']:
        for token in tokenizer(tmp_text['h1']):
            text = mystem.lemmatize(token.text)[0]
            h1_list.append(lemmatizer.lemmatize(text))
    tmp_text['h1'] = h1_list

    h2_list = []
    if tmp_text['h2']:
        for token in tokenizer(tmp_text['h2']):
            text = mystem.lemmatize(token.text)[0]
            h2_list.append(lemmatizer.lemmatize(text))
    tmp_text['h2'] = h2_list

    h3_list = []
    if tmp_text['h3']:
        for token in tokenizer(tmp_text['h3']):
            text = mystem.lemmatize(token.text)[0]
            h3_list.append(lemmatizer.lemmatize(text))
    tmp_text['h3'] = h1_list

    h4_list = []
    if tmp_text['h4']:
        for token in tokenizer(tmp_text['h4']):
            text = mystem.lemmatize(token.text)[0]
            h4_list.append(lemmatizer.lemmatize(text))
    tmp_text['h4'] = h1_list

    h5_list = []
    if tmp_text['h5']:
        for token in tokenizer(tmp_text['h5']):
            text = mystem.lemmatize(token.text)[0]
            h5_list.append(lemmatizer.lemmatize(text))
    tmp_text['h5'] = h5_list

    strong_list = []
    if tmp_text['strong']:
        for token in tokenizer(tmp_text['strong']):
            text = mystem.lemmatize(token.text)[0]
            strong_list.append(lemmatizer.lemmatize(text))
    tmp_text['strong'] = strong_list

    ins_list = []
    if tmp_text['ins']:
        for token in tokenizer(tmp_text['ins']):
            text = mystem.lemmatize(token.text)[0]
            ins_list.append(lemmatizer.lemmatize(text))
    tmp_text['ins'] = ins_list

    s_position = []
    sentence_lemm = []
    sentence = []
    k = 0
    for senten in sent_tokenize(tmp_text['text']):
        senten = senten.replace('—', '')
        senten = senten.replace('–', '')
        senten = senten.replace('−', '')
        senten = senten.replace('-', '')
        for term in tokenizer(senten):
            if 25 >= len(term.text) > 1:
                sentence.append(term.text)
                text = mystem.lemmatize(term.text)[0]
                sentence_lemm.append(lemmatizer.lemmatize(text))
                k += 1
        s_position.append(k)
    tmp_text['text_position'] = s_position
    tmp_text['orig_text'] = sentence
    tmp_text['text'] = sentence_lemm

    return tmp_text


urls_1 = pd.read_table("urls.numerate.txt", header=None)

urls_1 = urls_1.rename(columns={
    0: "url_id",
    1: "url"
})

result = []
for doc in os.listdir("content/20190128/"):
    f = open("content/20190128/" + str(doc))
    url_doc = [f.readline()[:-1], str(doc)]
    result.append(url_doc)

urls_2 = pd.DataFrame(result)
urls_2 = urls_2.rename(columns={
    0: "url",
    1: "file"
})

file_url_id = urls_2.set_index("url").join(urls_1.set_index("url")).reset_index()[['file', 'url_id']]

for url_id in range(74242):
    with open("data/" + str(url_id) + ".pickle", 'wb') as f:
        pickle.dump(html2word_whoosh_text(parse_text(url_id)), f)
