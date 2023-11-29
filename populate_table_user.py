import logging
from random import randint
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.user_model import UserModel
from models.address_model import AddressModel
from models.products_model import ProductModel
from models.client_model import ClientModel
from models.sales_model import SaleModel

# DB_URL = 'postgresql+asyncpg://postgres:123@localhost:5432/watersys'
DB_URL = 'postgresql+asyncpg://postgres:123@postgres:5432/watersys'
engine = create_async_engine(DB_URL, echo=True)
LOGGER = logging.getLogger('sLogger')

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def populate_users(session):
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


async def populate_address(session):
    async with async_session() as session:
        addresses_data = [
            {
                "address": "Rua das Palmeiras, 789",
                "type": "Residencial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Renascença",
                                "reference_point": "Próximo ao Parque do Rangedor"
            },
            {
                "address": "Avenida dos Ipês, 101",
                "type": "Comercial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Turu",
                                "reference_point": "Ao lado do supermercado"
            },
            {
                "address": "Rua das Orquídeas, 234",
                "type": "Residencial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Calhau",
                                "reference_point": "Próximo à praia"
            },
            {
                "address": "Avenida das Mangueiras, 567",
                "type": "Comercial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Olho d'Água",
                                "reference_point": "Perto do centro empresarial"
            },
            {
                "address": "Rua dos Cajueiros, 890",
                "type": "Residencial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Jaracaty",
                                "reference_point": "Ao lado do colégio"
            },
            {
                "address": "Avenida das Acácias, 1234",
                "type": "Comercial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Cohajap",
                                "reference_point": "Próximo ao terminal de ônibus"
            },
            {
                "address": "Rua dos Lírios, 456",
                "type": "Residencial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Vinhais",
                                "reference_point": "Perto do parque"
            },
            {
                "address": "Avenida das Palmas, 7890",
                "type": "Comercial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Cohama",
                                "reference_point": "Ao lado do centro comercial"
            },
            {
                "address": "Rua das Bromélias, 321",
                "type": "Residencial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Centro",
                                "reference_point": "Próximo à praça principal"
            },
            {
                "address": "Avenida das Rosas, 654",
                "type": "Comercial",
                "state": "Maranhão",
                "abbreviation": "MA",
                                "city": "São Luís",
                                "neighborhood": "Araçagi",
                                "reference_point": "Perto do centro de convenções"
            }]

        for address_data in addresses_data:
            address = AddressModel(**address_data)
            session.add(address)

        await session.commit()


async def populate_products(session):
    async with async_session() as session:
        products_data = [
            {
                "descricao": "Água mineral 20L São Braz",
                "unidade_idunidade": 1,
                "valor_compra": 2.5,
                "valor_venda": 5.0,
                "quantidade": 100
            },
            {
                "descricao": "Água mineral 20L Indaiá",
                "unidade_idunidade": 2,
                "valor_compra": 2.0,
                "valor_venda": 4.5,
                "quantidade": 150
            },
            {
                "descricao": "Água mineral 20L Lençóis",
                "unidade_idunidade": 2,
                "valor_compra": 4.0,
                "valor_venda": 6.0,
                "quantidade": 150
            }
        ]

        for product_data in products_data:
            product = ProductModel(**product_data)
            session.add(product)

        await session.commit()


async def populate_clients(session):
    async with async_session() as session:
        clients_data = [
            {
                "client_first_name": "João",
                "client_last_name": "Oliveira",
                "cpf": "13579246801",
                "address_id": 3,
                "phone_number": "11987654321",
                "email": "joao@example.com"
            },
            {
                "client_first_name": "Maria",
                "client_last_name": "Souza",
                "cpf": "98765432109",
                "address_id": 4,
                "phone_number": "21123456789",
                "email": "maria@example.com"
            },
            {
                "client_first_name": "Pedro",
                "client_last_name": "Fernandes",
                "cpf": "24681357901",
                "address_id": 5,
                "phone_number": "11987654321",
                "email": "pedro@example.com"
            },
            {
                "client_first_name": "Mariana",
                "client_last_name": "Lima",
                "cpf": "98765413209",
                "address_id": 6,
                "phone_number": "21123456789",
                "email": "mariana@example.com"
            },
            {
                "client_first_name": "Lucas",
                "client_last_name": "Pereira",
                "cpf": "36925814701",
                "address_id": 7,
                "phone_number": "11987654321",
                "email": "lucas@example.com"
            },
            {
                "client_first_name": "Julia",
                "client_last_name": "Gomes",
                "cpf": "98765432091",
                "address_id": 8,
                "phone_number": "21123456789",
                "email": "julia@example.com"
            },
            {
                "client_first_name": "Gabriel",
                "client_last_name": "Santana",
                "cpf": "15926374801",
                "address_id": 9,
                "phone_number": "11987654321",
                "email": "gabriel@example.com"
            },
            {
                "client_first_name": "Larissa",
                "client_last_name": "Rodrigues",
                "cpf": "98765430192",
                "address_id": 10,
                "phone_number": "21123456789",
                "email": "larissa@example.com"
            },
            {
                "client_first_name": "Rafael",
                "client_last_name": "Martins",
                "cpf": "12345678999",
                "address_id": 1,
                "phone_number": "11987654321",
                "email": "rafael@example.com"
            },
            {
                "client_first_name": "Carolina",
                "client_last_name": "Cunha",
                "cpf": "99999999999",
                "address_id": 2,
                "phone_number": "21123456789",
                "email": "carolina@example.com"
            }
        ]

        for client_data in clients_data:
            client = ClientModel(**client_data)
            session.add(client)

        await session.commit()


async def generate_sales_data(session):
    sales_data_list = []
    last_purchase_dates = {}
    initial_purchase_date = datetime.strptime("2023-01-01", "%Y-%m-%d")

    LOGGER.info('Populating sales data')
    start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-10-31", "%Y-%m-%d")
    current_date = start_date

    clients_cpf = [
        "13579246801", "98765432109", "24681357901", "98765413209", "36925814701",
        "98765432091", "15926374801", "98765430192", "12345678999", "99999999999"
    ]
    purchase_dates = {cpf: initial_purchase_date for cpf in clients_cpf}
    base_intervals = {1: randint(7, 10), 2: randint(14, 20), 3: 21}

    generated_sales = 0
    while generated_sales < 190:
        for cpf in clients_cpf:
            quantity = randint(1, 3)
            interval = base_intervals[quantity]

            if purchase_dates[cpf] <= end_date:
                purchase_dates[cpf] += timedelta(days=interval)
                if purchase_dates[cpf] > end_date:
                    purchase_dates[cpf] = end_date

                date = purchase_dates[cpf].strftime("%Y-%m-%d")
                sales_record = {
                    "quantity": quantity,
                    "total_amount": quantity * 16,
                    "purchase_date": datetime.strptime(date, '%Y-%m-%d').date(),
                    "returnable": bool(randint(0, 1)),
                    "product_id": randint(1, 3),
                    "cpf": cpf
                }

            sales_data_list.append(sales_record)
            generated_sales += 1

    async with session.begin():
        products = await session.execute(select(ProductModel))
        products = products.scalars().all()

        for sales_record in sales_data_list:
            product_id = sales_record["product_id"]
            quantity = sales_record["quantity"]

            product = next(p for p in products if p.id == product_id)
            sales_record["total_amount"] = quantity * product.valor_venda

            sale = SaleModel(**sales_record)
            session.add(sale)

        await session.commit()

async def main():
    async with async_session() as session:
        await populate_address(session)
        await populate_products(session)
        await populate_clients(session)
        await populate_users(session)
        await generate_sales_data(session)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
