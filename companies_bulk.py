#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
import json

next_page_id = ''
while True:
    data = {
        'form_data': {'must': {'hq_locations': ['Prague']}},
        'fields': 'id,name,industries',
        'next_page_id': next_page_id,
        'limit': 100,
        }

    headers = {'Content-Type': 'application/json'}

    r = \
        requests.post(url='https://api.dealroom.co/api/v1/companies/bulk'
                      , data=json.dumps(data), headers=headers,
                      auth=HTTPBasicAuth('api-key', ''))

    res = json.loads(r.text)
    print(res)

    next_page_id = res['next_page_id']
    if next_page_id == None:
        break