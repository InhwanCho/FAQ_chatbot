import os
import csv
import openai
import numpy as np
from pprint import pprint
import json
from numpy.linalg import norm

# slack.py가 아닌 vectordb.py를 테스트 시 필요
openai.api_key = "sk-..."


def load(filepath):
    faq_db = []
    with open(filepath, 'r', encoding='utf-8') as fp:
        cr = csv.reader(fp)
        next(cr)

        for row in cr:
            # row: id,question,answer
            text = "Question: " + row[1] + "\nAnswer: " + row[2] + "\n"
            vector = get_embedding(text)
            doc = {'id': row[0], 'vector': vector,
                   'question': row[1], 'answer': row[2]}
            faq_db.append(doc)

    return faq_db

def json_load(filepath):
    with open('faq.json', 'r') as f:
        
        faq_db_ = json.load(f)
        faq_db = faq_db_['FAQ']
        for faq in faq_db:
            faq['vector'] = get_embedding(faq['question']+faq['answer'])


    return faq_db


def get_embedding(content, model='text-embedding-ada-002'):
    response = openai.Embedding.create(input=content, model=model)
    vector = response['data'][0]['embedding']
    return vector



#코사인유사도
def similarity(v1, v2):  # return dot product of two vectors
    return np.dot(v1, v2)/(norm(v1)*norm(v2))


def search(vector, db):
    results = []

    for doc in db:
        score = similarity(vector, doc['vector'])
        results.append(
            {'id': doc['id'], 'score': score, 'question': doc['question'], 'answer': doc['answer']})

    results = sorted(results, key=lambda e: e['score'], reverse=True)

    return results


if __name__ == '__main__':

    # faq_db = load('prompt-faq.csv')
    # print(faq_db)
    faq_db = json_load('faq.json')
    

    question = "아이디가 생각 안나요"
    vector = get_embedding(question)

    result = search(vector, faq_db)
    pprint(result)
