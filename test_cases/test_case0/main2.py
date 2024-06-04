from main import Product
from typing import List

class Products:
        
    products: List[Product]
    
    def add_product(self, product: Product):
        self.products.append(product)
    
    def remove_product(self, product: Product):
        self.products.remove(product)
    
    def get_product(self, product_id: int) -> Product:
        for product in self.products:
            if product.id == product_id:
                return product
        raise Exception("Product not found")
    
    def get_products(self) -> List[Product]:
        return self.products