from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

from app.models.product import Product

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def list_products():
    products = Product.select()
    return jsonify([model_to_dict(p) for p in products])


@products_bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.get_or_none(Product.id == id)
    if not product:
        return {"error": "Not found"}, 404
    return model_to_dict(product)


@products_bp.route("/products", methods=["POST"])
def create_product():
    data = request.json

    product = Product.create(
        name=data["name"],
        category=data["category"],
        price=data["price"],
        stock=data["stock"],
    )

    return model_to_dict(product), 201