from flask import Flask, request, jsonify
import requests
import hashlib

app = Flask(__name__)

ACCESS_TOKEN = "sdgkhx"
ECOMMERCE_API_URL = "http://20.244.56.144/test/companies"
COMPANIES = ["AMZ", "FLP", "SNP", "MYN", "AZO"]
CATEGORIES = ["Phone", "Computer", "TV", "Earphone", "Tablet", "Charger", "Mouse", "Keyboard", "Pendrive", "Remote", "Speaker", "Headset", "Laptop", "PC"]

@app.route('/categories/<category>/products', methods=['GET'])
def get_top_products(category):
    if category not in CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    n = int(request.args.get('n', 10))
    if n > 10:
        n = 10
    page = int(request.args.get('page', 1))
    min_price = int(request.args.get('minPrice', 0))
    max_price = int(request.args.get('maxPrice', 100000))
    sort_by = request.args.get('sort_by', None)
    sort_order = request.args.get('sort_order', 'asc')

    products = fetch_and_aggregate_products(category, min_price, max_price, n)
    sorted_products = sort_products(products, sort_by, sort_order)
    paginated_products = paginate_products(sorted_products, n, page)

    return jsonify(paginated_products)

@app.route('/categories/<category>/products/<product_id>', methods=['GET'])
def get_product_details(category, product_id):
    product = get_product_by_id(category, product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

def fetch_and_aggregate_products(category, min_price, max_price, n):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    products = []
    for company in COMPANIES:
        url = f"{ECOMMERCE_API_URL}/{company}/categories/{category}/products?top={n}&minPrice={min_price}&maxPrice={max_price}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for product in response.json():
                product_id = hashlib.md5((product['productName'] + str(product['price'])).encode()).hexdigest()
                product['custom_id'] = product_id
                products.append(product)
    return products

def sort_products(products, sort_by, sort_order):
    if sort_by:
        reverse = (sort_order == 'desc')
        products.sort(key=lambda x: x.get(sort_by), reverse=reverse)
    return products

def paginate_products(products, n, page):
    start = (page - 1) * n
    end = start + n
    return products[start:end]

def get_product_by_id(category, product_id):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    for company in COMPANIES:
        url = f"{ECOMMERCE_API_URL}/{company}/categories/{category}/products"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for product in response.json():
                if product_id == hashlib.md5((product['productName'] + str(product['price'])).encode()).hexdigest():
                    return product
    return None

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Hardcoded data for testing
# PRODUCTS = {
#     "Laptop": [
#         {"productName": "Laptop 1", "price": 2236, "rating": 4.7, "discount": 63, "availability": "yes"},
#         {"productName": "Laptop 2", "price": 1244, "rating": 4.5, "discount": 45, "availability": "out-of-stock"},
#         {"productName": "Laptop 3", "price": 9102, "rating": 4.44, "discount": 98, "availability": "out-of-stock"},
#         {"productName": "Laptop 4", "price": 2652, "rating": 4.12, "discount": 70, "availability": "yes"},
#         {"productName": "Laptop 5", "price": 1258, "rating": 3.8, "discount": 33, "availability": "yes"}
#     ]
# }

# @app.route('/categories/<category>/products', methods=['GET'])
# def get_products(category):
#     n = int(request.args.get('n', 10))
#     if category not in PRODUCTS:
#         return jsonify({"error": "Invalid category"}), 400

#     products = PRODUCTS[category]
#     paginated_products = products[:n]
#     return jsonify(paginated_products)

# @app.route('/test', methods=['GET'])
# def test():
#     return jsonify({"status": "success", "data": "Test data"})

# if __name__ == '__main__':
#     app.run(debug=True)
