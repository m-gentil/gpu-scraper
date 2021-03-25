DEFAULT_HEADERS = {
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
}

HTML_HEADERS = {**DEFAULT_HEADERS, "accept": "text/html"}

JSON_HEADERS = {**DEFAULT_HEADERS, "accept": "application/json"}

TIMEOUT_SECONDS = 10
