from base.repositories.repository import Repository
from base.models.product_model import ProductModel


class ProductsRepository(Repository):
    model = ProductModel
    table = "products"
