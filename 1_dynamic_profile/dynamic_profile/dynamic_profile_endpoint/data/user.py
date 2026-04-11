from .time import get_today
from .cat import get_cat_quote

def get_user_object():

    user_object = {
        "status": "success",
        "user": {
        "email": "debaycisse@gmail.com",
        "name": "Azeez Adebayo",
        "stack": "Python/Django"
        },
        "timestamp": get_today(),
    }

    cat_quote = get_cat_quote()

    if cat_quote.get('error'):
        user_object['fact'] = cat_quote.get('error')
    else:
        user_object['fact'] = cat_quote.get('fact')

    return user_object
