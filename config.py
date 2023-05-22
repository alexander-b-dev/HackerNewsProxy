import secrets

key = secrets.token_urlsafe(40)
debug = True
originURL = "https://news.ycombinator.com/"
reqTimeout = 2  # timeout for origin page request
