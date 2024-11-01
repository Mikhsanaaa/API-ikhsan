from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data produk contoh
products = [
    {"id": 1, "name": "Bibit Jagung", "description": "Bibit jagung berkualitas tinggi", "price": 10000, "stock": 50, "category": "Benih", "weight": "500g", "expiry_date": "2024-12-01"},
    {"id": 2, "name": "Pupuk Organik", "description": "Pupuk organik ramah lingkungan", "price": 20000, "stock": 30, "category": "Pupuk", "weight": "1kg", "expiry_date": "2025-06-01"},
    {"id": 3, "name": "Alat Semprot", "description": "Alat semprot serbaguna untuk pupuk cair", "price": 150000, "stock": 10, "category": "Alat", "weight": "2kg", "expiry_date": "N/A"},
    {"id": 4, "name": "Benih Tomat", "description": "Benih tomat unggul", "price": 12000, "stock": 45, "category": "Benih", "weight": "300g", "expiry_date": "2024-10-10"},
    {"id": 5, "name": "Pestisida Cair", "description": "Pestisida untuk melindungi tanaman dari hama", "price": 50000, "stock": 25, "category": "Pestisida", "weight": "500ml", "expiry_date": "2024-11-15"},
    {"id": 6, "name": "Pupuk Kompos", "description": "Pupuk kompos dari bahan alami", "price": 25000, "stock": 60, "category": "Pupuk", "weight": "1kg", "expiry_date": "2025-01-20"},
    {"id": 7, "name": "Benih Cabai", "description": "Benih cabai dengan pertumbuhan cepat", "price": 10000, "stock": 40, "category": "Benih", "weight": "200g", "expiry_date": "2024-09-01"},
    {"id": 8, "name": "Polybag", "description": "Polybag untuk menanam sayuran di rumah", "price": 5000, "stock": 100, "category": "Alat", "weight": "50g", "expiry_date": "N/A"},
    {"id": 9, "name": "Bibit Kentang", "description": "Bibit kentang siap tanam", "price": 15000, "stock": 30, "category": "Benih", "weight": "400g", "expiry_date": "2025-02-12"},
    {"id": 10, "name": "Benih Mentimun", "description": "Benih mentimun yang mudah tumbuh", "price": 13000, "stock": 35, "category": "Benih", "weight": "250g", "expiry_date": "2024-11-22"},
    {"id": 11, "name": "Alat Cangkul", "description": "Cangkul untuk persiapan lahan", "price": 80000, "stock": 15, "category": "Alat", "weight": "1.5kg", "expiry_date": "N/A"},
    {"id": 12, "name": "Pupuk NPK", "description": "Pupuk NPK untuk meningkatkan hasil panen", "price": 35000, "stock": 50, "category": "Pupuk", "weight": "1kg", "expiry_date": "2024-10-01"},
    {"id": 13, "name": "Benih Bawang Merah", "description": "Benih bawang merah unggul", "price": 14000, "stock": 25, "category": "Benih", "weight": "300g", "expiry_date": "2025-03-10"},
    {"id": 14, "name": "Fungisida", "description": "Fungisida untuk mencegah jamur pada tanaman", "price": 60000, "stock": 20, "category": "Pestisida", "weight": "500ml", "expiry_date": "2024-12-15"},
    {"id": 15, "name": "Alat Pengukur pH Tanah", "description": "Alat untuk mengukur pH tanah", "price": 90000, "stock": 12, "category": "Alat", "weight": "250g", "expiry_date": "N/A"}
]

class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(products),
            "products": products
        }

    def post(self):
        data = request.get_json()
        new_product = {
            "id": len(products) + 1,
            "name": data["name"],
            "description": data["description"],
            "price": data["price"],
            "stock": data["stock"],
            "category": data["category"],
            "weight": data["weight"],
            "expiry_date": data["expiry_date"]
        }
        products.append(new_product)
        return {"error": False, "message": "Product added", "product": new_product}, 201

class ProductDetail(Resource):
    def get(self, product_id):
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            return {"error": False, "message": "success", "product": product}
        return {"error": True, "message": "Product not found"}, 404

    def put(self, product_id):
        data = request.get_json()
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            product.update({
                "name": data["name"],
                "description": data["description"],
                "price": data["price"],
                "stock": data["stock"],
                "category": data["category"],
                "weight": data["weight"],
                "expiry_date": data["expiry_date"]
            })
            return {"error": False, "message": "Product updated", "product": product}
        return {"error": True, "message": "Product not found"}, 404

    def delete(self, product_id):
        global products
        products = [p for p in products if p["id"] != product_id]
        return {"error": False, "message": "Product deleted"}

class ProductSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [p for p in products if query in p['name'].lower() or query in p['description'].lower()]
        return {"error": False, "founded": len(result), "products": result}

api.add_resource(ProductList, '/products')
api.add_resource(ProductDetail, '/products/<int:product_id>')
api.add_resource(ProductSearch, '/products/search')

if __name__ == '__main__':
    app.run(debug=True)
