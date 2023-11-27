from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.user_model import UserModel
from models.address_model import AddressModel
from models.products_model import ProductModel
from models.client_model import ClientModel

DB_URL = 'postgresql+asyncpg://postgres:123@postgres:5432/watersys'
engine = create_async_engine(DB_URL, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def populate_users():
    async with async_session() as session:
        users_data = [
            {
                "name": "João",
                "last_name": "Silva",
                "email": "joao@example.com",
                "phone_number": "123456789",
                "location": "São Paulo",
                "is_admin": True,
                "is_deleted": False,
                "passwd": "senha123"
            },
            {
                "name": "Maria",
                "last_name": "Santos",
                "email": "maria@example.com",
                "phone_number": "987654321",
                "location": "Rio de Janeiro",
                "is_admin": False,
                "is_deleted": False,
                "passwd": "senha456"
            }
        ]

        for user_data in users_data:
            user = UserModel(**user_data)
            session.add(user)

        await session.commit()

async def populate_address():
    async with async_session() as session:
        addresses_data = [
            {
                "address": "Rua Principal, 123",
                "type": "Residencial",
                "state": "Maranhão",
                "abbreviation": "MA",
                "city": "São Luís",
                "neighborhood": "Centro",
                "reference_point": "Próximo ao mercado central"
            },
            {
                "address": "Avenida Central, 456",
                "type": "Comercial",
                "state": "Maranhão",
                "abbreviation": "MA",
                "city": "São Luís",
                "neighborhood": "Cohama",
                "reference_point": "Perto do shopping"
            }
        ]

        for address_data in addresses_data:
            address = AddressModel(**address_data)
            session.add(address)

        await session.commit()

async def populate_products():
    async with async_session() as session:
        products_data = [
            {
                "descricao": "Água mineral 20L São Braz",
                "unidade_idunidade": 1,
                "valor_compra": 10.0,
                "valor_venda": 15.0,
                "quantidade": 100
            },
            {
                "descricao": "Água mineral 20L Indaiá",
                "unidade_idunidade": 2,
                "valor_compra": 11.0,
                "valor_venda": 16.0,
                "quantidade": 150
            },
            {
                "descricao": "Água mineral 20L Lençóis",
                "unidade_idunidade": 2,
                "valor_compra": 11.0,
                "valor_venda": 16.0,
                "quantidade": 150
            }
        ]

        for product_data in products_data:
            product = ProductModel(**product_data)
            session.add(product)

        await session.commit()

async def populate_clients():
    async with async_session() as session:
        clients_data = [
            {
                "client_first_name": "Carlos",
                "client_last_name": "Silva",
                "cpf": "12345678901",
                "address_id": 1,
                "phone_number": "11987654321",
                "email": "carlos@example.com"
            },
            {
                "client_first_name": "Ana",
                "client_last_name": "Santos",
                "cpf": "98765432109",
                "address_id": 2,
                "phone_number": "21123456789",
                "email": "ana@example.com"
            }
        ]

        for client_data in clients_data:
            client = ClientModel(**client_data)
            session.add(client)

        await session.commit()

async def main():
    await populate_users()
    await populate_address()
    await populate_products()
    await populate_clients()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
