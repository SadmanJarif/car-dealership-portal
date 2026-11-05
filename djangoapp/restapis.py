import requests
from django.conf import settings

def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={"Content-Type": "application/json"}, params=kwargs, timeout=10)
        return response.json()
    except Exception as e:
        print("Network exception in get_request:", e)
        return None

def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs, timeout=10)
        return response.json()
    except Exception as e:
        print("Network exception in post_request:", e)
        return None

def get_dealers_from_cf(url):
    # Proxy to an external dealers back-end (Node/Mongo) when configured.
    result = get_request(url)
    if result:
        return result
    return None

def get_dealer_reviews_from_cf(url, dealer_id):
    result = get_request(url, dealerId=dealer_id)
    if result:
        return result
    return None

def get_dealers():
    # Local fallback: external URL unset in local dev, so callers use the DB.
    if settings.DEALERS_API_URL:
        dealers = get_dealers_from_cf(settings.DEALERS_API_URL)
        if dealers is not None:
            return dealers
    return None

def get_dealer_reviews(dealer_id):
    if settings.REVIEWS_API_URL:
        reviews = get_dealer_reviews_from_cf(settings.REVIEWS_API_URL, dealer_id)
        if reviews is not None:
            return reviews
    return None
