-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body   = '{"token": "PLACE_YOUR_TOKEN_HERE"}'
