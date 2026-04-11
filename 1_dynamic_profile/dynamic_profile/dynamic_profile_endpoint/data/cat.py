import requests as req
from requests.exceptions import (
    ConnectionError, 
    ConnectTimeout,
    ContentDecodingError,
    JSONDecodeError,
    Timeout
)

CAT_QUOTE_URL = 'https://catfact.ninja/fact'

def get_cat_quote():
    try:
        cat_quote_obj = req.get(CAT_QUOTE_URL, timeout=3.5)
        cat_quote_obj = cat_quote_obj.json()
    except (Timeout, ConnectTimeout):
        cat_quote_obj = {
            'error': 'Connection to cat quote\'s server timed out',
            'status': 'fail',
        }
    except ConnectionError:
        cat_quote_obj = {
            'error': 'Error while connecting to cat quote\'s server',
            'status': 'fail',
        }
    except (ContentDecodingError, JSONDecodeError):
        cat_quote_obj = {
            'error': 'Malformed data cannot be converted to JSON',
            'status': 'fail'
        }

    return cat_quote_obj
