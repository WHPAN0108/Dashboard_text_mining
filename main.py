# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Bio import Entrez
from nltk.tokenize import sent_tokenize

Entrez.email = "w.pan@silence-therapeutics.com"


def extract_xml_file(keywords):
    handle = Entrez.esearch(db="pubmed", term=keywords, retmax=200, sort='relevance')
    records = Entrez.read(handle)
    identifiers = records['IdList']
    handle = Entrez.efetch(db="pubmed", id=identifiers, retmax="200", rettype="fasta", retmode="xml")
    records = Entrez.read(handle)
    article = records['PubmedArticle']
    return article


def title_extraction(article_object):
    return article_object['MedlineCitation']['Article']['ArticleTitle']


def abstract_extraction(article_object):
    try:
        abstract_obj = article_object['MedlineCitation']['Article']['Abstract']['AbstractText']
        abstract_obj = ''.join(abstract_obj)
    except:
        abstract_obj = ''

    return abstract_obj


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    keyword = "PTEN AND liver"
    article = extract_xml_file(keyword)

    abstract_search = dict()
    for i,abstract_obj in enumerate(article):
        abstract_single = abstract_extraction(abstract_obj)
        token_text = sent_tokenize(abstract_single)
        keywords = keyword.split(" AND ")
        keyword_sentence = [k for k in token_text if all([key in k for key in keywords]) ]
        if len(keyword_sentence) != 0:
            abstract_search[title_extraction(abstract_obj)] = keyword_sentence

    key_example = list(abstract_search.keys())[0]
    print(key_example)
    print(*abstract_search[key_example], sep= "\n")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
