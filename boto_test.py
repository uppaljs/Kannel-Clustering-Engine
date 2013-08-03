In [6]: from boto.sqs.connection import SQSConnection

In [7]: conn = SQSConnection('AKIAI6TGU5J3XBGFECKQ','J7JJ7yWyqRlpryny4ZDJQRCDSPOM6cU5NUhIxnHg')

In [8]: q = conn.create_queue('myqueue')
