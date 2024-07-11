import requests

headers = {
    "Authorization": "sk_test_51Pb8vZRq60gSsgMSZx5eKNXImyF2PI88fBePn8QboDXm59knUj50lLyUa2DLyGxhUQ3brPp8AwFkTKeEYPOzWP71000WjLUtg6",
    "Content-Type": "application/x-www-form-urlencoded"
}


def create_product():
    url = "https://api.stripe.com/v1/products"

    data = {
        "name": "Course Product"
    }

    response = requests.post(url, headers=headers, data=data)
    product_id = response.json()["id"]
    return product_id


def create_price(product_id):
    url = "https://api.stripe.com/v1/prices"
    data = {
        "product": product_id,
        "unit_amount": 1000,
        "currency": "usd"
    }

    response = requests.post(url, headers=headers, data=data)
    price_id = response.json()["id"]
    return price_id


def create_checkout_session(price_id):
    url = "https://api.stripe.com/v1/checkout/sessions"
    data = {
        "payment_method_types": ["card"],
        "line_items": [
            {
                "price": price_id,
                "quantity": 1
            }
        ],
        "mode": "payment",
        "success_url": "https://localhost:8000/success",
        "cancel_url": "https://localhost:8000/cancel"
    }

    response = requests.post(url, headers=headers, data=data)
    checkout_session_url = response.json()["url"]
    return checkout_session_url
