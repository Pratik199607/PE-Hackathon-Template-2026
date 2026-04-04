import logging
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

from app.models.product import Product

logger = logging.getLogger(__name__)

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def list_products():
    logger.info("Fetching all products")

    products = Product.select()
    return jsonify([model_to_dict(p) for p in products])


@products_bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.get_or_none(Product.id == id)

    if not product:
        logger.warning(f"Product not found: {id}")
        return {"error": "Not found"}, 404

    return model_to_dict(product)


@products_bp.route("/products", methods=["POST"])
def create_product():
    data = request.json

    try:
        product = Product.create(
            name=data["name"],
            category=data["category"],
            price=data["price"],
            stock=data["stock"],
        )

        logger.info(f"Product created: {product.id}")
        return model_to_dict(product), 201

    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return {"error": "Internal Server Error"}, 500