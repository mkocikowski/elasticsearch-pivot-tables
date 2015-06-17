I have:

```
item  | category  | user  | qty
------|-----------|-------|----
item1 | category1 | user1 | 2
item1 | category1 | user1 | 5
item1 | category1 | user1 | 1
item1 | category1 | user2 | 1
item2 | category1 | user3 | 2
item3 | category2 | user1 | 2
item3 | category2 | user1 | 3
item3 | category2 | user2 | 1
item3 | category2 | user2 | 2
```

I want:

```
user  | category1 | category2
------|-----------|-----------
user1 | 8         | 5
user2 | 1         | 3
user3 | 2         | 0

```

Load data into ES:

```
curl -s -XDELETE 'http://localhost:9200/pivot3'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item1", "category": "category1", "user": "user1", "qty": 2}'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item1", "category": "category1", "user": "user1", "qty": 5}'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item1", "category": "category1", "user": "user1", "qty": 1}'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item1", "category": "category1", "user": "user2", "qty": 1}'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item2", "category": "category1", "user": "user3", "qty": 2}'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item3", "category": "category2", "user": "user1", "qty": 2}'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item3", "category": "category2", "user": "user1", "qty": 3}'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item3", "category": "category2", "user": "user2", "qty": 1}'
curl -s -XPOST 'http://localhost:9200/pivot3/orders' -d '{"item": "item3", "category": "category2", "user": "user2", "qty": 2}'
```

Pivot query:

```
curl -s -XGET 'http://localhost:9200/pivot3/orders/_search?search_type=count' -d '
{
    "aggs": {
        "user": {
            "terms": {
                "field": "user"
            },
            "aggs": {
                "categories": {
                    "terms": {
                        "field": "category"
                    },
                    "aggs": {
                        "qty": {
                            "sum": {
                                "field": "qty"
                            }
                        }
                    }
                }
            }
        }
    }
}
' | ./pivot3.py
```

Parsed response:

```
user1 [(u'category1', 8.0), (u'category2', 5.0)]
user2 [(u'category2', 3.0), (u'category1', 1.0)]
user3 [(u'category1', 2.0)]
```



