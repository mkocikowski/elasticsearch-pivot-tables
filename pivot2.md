I have:

```
item  | user  | qty
------|-------|-----
item1 | user1 | 2
item1 | user1 | 5
item1 | user1 | 1
item1 | user2 | 1
item2 | user3 | 2
item3 | user1 | 2
item3 | user1 | 3
item3 | user2 | 1
item3 | user2 | 2
```

I want:

```
user  | item  | qty
------|-------|-----
user1 | item1 | 8
user1 | item3 | 5
user2 | item1 | 1
user2 | item3 | 3
user3 | item2 | 2
```

Load data into ES:

```
curl -s -XDELETE 'http://localhost:9200/pivot2'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item1", "user": "user1", "qty": 2}'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item1", "user": "user1", "qty": 5}'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item1", "user": "user1", "qty": 1}'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item1", "user": "user2", "qty": 1}'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item2", "user": "user3", "qty": 2}'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item3", "user": "user1", "qty": 2}'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item3", "user": "user1", "qty": 3}'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item3", "user": "user2", "qty": 1}'
curl -s -XPOST 'http://localhost:9200/pivot2/items' -d '{"item": "item3", "user": "user2", "qty": 2}'
```

Pivot query:

```
curl -s -XGET 'http://localhost:9200/pivot2/items/_search?search_type=count' -d '
{
    "aggs": {
        "user": {
            "terms": {
                "field": "user"
            },
            "aggs": {
                "items": {
                    "terms": {
                        "field": "item"
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
' | ./pivot2.py
```

Parsed response:

```
user1 item1 8
user1 item3 5
user2 item3 3
user2 item1 1
user3 item2 2
```
