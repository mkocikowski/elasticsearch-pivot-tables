#!/usr/bin/env python

import sys
import json

data = json.loads(sys.stdin.read())

for item in data['aggregations']['items']['buckets']:
    print("%s %s" % (item['key'], [user['key'] for user in item['user']['buckets']]))

