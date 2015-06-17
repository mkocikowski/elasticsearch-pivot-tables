#!/usr/bin/env python

import sys
import json

data = json.loads(sys.stdin.read())

for user in data['aggregations']['user']['buckets']:
    for item in user['items']['buckets']:
        print("%s %s %d" % (user['key'], item['key'], item['qty']['value']))

