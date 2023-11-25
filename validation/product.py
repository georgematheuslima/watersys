import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from exceptions.validations import FieldWithValueLessThanZero

LOGGER = logging.getLogger("sLogger")

class ProductValidation:
    def validate_product_model(self, product_data):
        LOGGER.info(f'Product model: {product_data}')
        required_fields = ["descricao", "unidade_idunidade", "valor_compra", "valor_venda", "quantidade"]
        missing_fields = [field for field in required_fields if field not in product_data]
        
        LOGGER.debug(f'Missing fields: {missing_fields}')
        
        if missing_fields:
            missing_fields_str = ", ".join(missing_fields)
            raise ValueError(f"Missing fields: {missing_fields_str}")
        
        def is_valid_non_negative_number(val):
            return isinstance(val, (int, float)) and val >= 0

        invalid_fields = [field for field in ["valor_compra", "valor_venda", "quantidade"] if not is_valid_non_negative_number(product_data.get(field, 0))]

        if invalid_fields:
            LOGGER.error(f"ProductModel has values less than 0 in fields: {', '.join(invalid_fields)}")
            raise FieldWithValueLessThanZero
    
