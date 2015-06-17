#!/usr/bin/env python

import sys
import json

data = json.loads(sys.stdin.read())

for user in data['aggregations']['user']['buckets']:
    print("%s %s" % (user['key'], [(c['key'], c['qty']['value']) for c in user['categories']['buckets']]))

