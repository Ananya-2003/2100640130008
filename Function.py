import hashlib

def fetch_and_aggregate_products(category):
    products = []
    for url in ECOMMERCE_API_URLS:
        response = requests.get(f"{url}/categories/{category}/products")
        if response.status_code == 200:
            for product in response.json():
                product_id = hashlib.md5((product['name'] + product['price']).encode()).hexdigest()
                product['custom_id'] = product_id
                products.append(product)
    return products
