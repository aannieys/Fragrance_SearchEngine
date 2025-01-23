# ID: 6488120, Suphavadee Cheng
# ID: 6488176, Jidapa Moolkaew
# ID: 6488204, Pimmada Chompurat

from flask import Flask, request
from markupsafe import escape
from flask import render_template
from elasticsearch import Elasticsearch
import math
import re

ELASTIC_PASSWORD = "eltsforirclass"

es = Elasticsearch("https://localhost:9200",
                   http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    page_size = 10
    keyword = request.args.get('keyword')
    selected_filter = request.args.get('select')
    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    price_match1 = re.search(r'\b(\d+)\s*(price|baht|cheaper\s*than|cheap|lower\s*than|less\s*than)\s*', keyword, re.IGNORECASE)
    price_match2 = re.search(r'\s*(price|baht|cheaper\s*than|cheap|lower\s*than|less\s*than)\s*(\d+)?\b', keyword, re.IGNORECASE)
   
    desired_price = None
    if price_match1:
        desired_price = int(price_match1.group(1))
    elif price_match2:
        desired_price = int(price_match2.group(2)) if price_match2.group(2) is not None else None


    body = {
        'size': page_size,
        'from': page_size * (page_no - 1),
        'query': {
            'bool': {
                'should': [
                    {
                        'multi_match': {
                            'query': keyword,
                            'fields': [
                                'name^2', 'about^2', 'brand^3', 'categories^1', 'fragrance_family^1',
                                'gender^1', 'how_long^1', 'kind_of_scent^1', 'notes^1', 'occasion^1',
                                'scent_type^1', 'season^1', 'smell_like^1','volume^10'
                            ],
                            'fuzziness': 'AUTO',
                            'fuzzy_transpositions': True
                        }
                    }
                ],
                'filter': []
            }
        },
        'sort': [
            {'_score': {'order': 'desc'}},  
            {'name': {'order': 'asc'}} 
        ]
    }

    if desired_price:
        body['query']['bool']['filter'].append({'range': {'price': {'lte': desired_price, 'boost': 5}}})
        body['sort'] = [{'price': {'order': 'desc'}}]

    if selected_filter:
        if selected_filter == 'price':
            digit_match = re.search(r'\d+', keyword)
            if digit_match:
                extracted_digits = int(digit_match.group())
                body.pop('sort', None)
                body['query']['bool']['filter'] = [{
                    'range': {
                        selected_filter: {
                            'lte': extracted_digits,
                            'boost': 10
                        }
                    }
                }]
                body['sort'] = [{'_score': {'order': 'desc'}}]
        elif selected_filter in ['Women', 'Men', 'Unisex']:
            body['query']['bool']['filter'].append({
                'match': {
                    'gender': {
                        'query': selected_filter,
                        'boost': 10,
                        'fuzziness': 'AUTO',
                        'fuzzy_transpositions': True
                    }
                }
            })
        elif selected_filter in ['Cologne', 'Perfume']:
            body['query']['bool']['filter'].append({
                'match': {
                    'categories': {
                        'query': selected_filter,
                        'boost': 10,
                        'fuzziness': 'AUTO',
                        'fuzzy_transpositions': True
                    }
                }
            })

    res = es.search(index='fragrance_products', body=body)
    hits = [
        {
            'name': doc['_source']['name'],
            'brand': doc['_source']['brand'],
            'gender': doc['_source']['gender'],
            'categories': doc['_source']['categories'],
            'volume': doc['_source']['volume'],
            'price': str(doc['_source']['price']),
            'fragrance_family': doc['_source']['fragrance_family'],
            'about': doc['_source']['about'],
            'scent_type': doc['_source']['scent_type'],
            'notes': doc['_source']['notes'],
            'smell_like': doc['_source']['smell_like'],
            'kind_of_scent': doc['_source']['kind_of_scent'],
            'occasion': doc['_source']['occasion'],
            'season': doc['_source']['season'],
            'how_long': doc['_source']['how_long']
        }
        for doc in res['hits']['hits']
    ]
    page_total = math.ceil(res['hits']['total']['value']/page_size)


    return render_template('search.html', keyword=keyword, hits=hits, page_no=page_no, page_total=page_total, body=body,desired_price=desired_price, selected_filter=selected_filter)
