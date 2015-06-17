I have:

```
user  | items
------|-------------
user1 | item1, item2
user2 | item3,
user3 | item1, item3
```

I want:

```
item  | users
------|-------------
item1 | user1, user3
item2 | user1
item3 | user2, user3
```

Load data into ES:

```
curl -s -XDELETE 'http://localhost:9200/pivot1'
curl -s -XPOST 'http://localhost:9200/pivot1/users' -d '{"user": "user1", "items": ["item1", "item2"]}'
curl -s -XPOST 'http://localhost:9200/pivot1/users' -d '{"user": "user2", "items": ["item3"]}'
curl -s -XPOST 'http://localhost:9200/pivot1/users' -d '{"user": "user3", "items": ["item1", "item3"]}'
```

Pivot query:

```
curl -s -XGET 'http://localhost:9200/pivot1/users/_search?search_type=count' -d '
{
    "aggs": {
        "items": {
            "terms": {
                "field": "items"
            },
            "aggs": {
                "user": {
                    "terms": {
                        "field": "user"
                    }
                }
            }
        }
    }
}
' | ./pivot1.py
```

Parsed response:

```
item1 [u'user1', u'user3']
item3 [u'user2', u'user3']
item2 [u'user1']
```
