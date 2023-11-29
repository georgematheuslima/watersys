from telebot import types, TeleBot
from calcular_distancia import encontrar_coordenada_proxima
from typing import List, Tuple
from dotenv import load_dotenv
import requests
import os
import json
from datetime import datetime


load_dotenv()
base_url = 'http://localhost:8000/api/v1/'
client_api = f'{base_url}client/client'
get_cliente_api = f'{base_url}client/telegram/'
sales_api = f'{base_url}sales/sales'
sales_history_api = f'{base_url}sales/telegram/'
user_data = {}


# Lista de coordenadas dos depósitos
COORDENADAS: List[Tuple[float, float]] = [
    (-2.577497, -44.1676215),
    (-2.5710628, -44.1696658),
    (-2.542826, -44.1935365),
    (-2.5689437, -44.2687578),
]

bot = TeleBot(os.getenv('TELEGRAM_API_KEY'))

# Crie um teclado inline
keyboard = types.InlineKeyboardMarkup(row_width=2)

# Adicione botões inline
buttons = [
    ("Pedir galão de água", "fazer_pedido"),
    ("Encontrar depósito", "encontrar_deposito"),
    ("Histórico de compra", "historico_de_compra"),
    ("Meus dados", "client_data"),
    ("Estimativa de pedido", "estimativa_pedido"),
    ("Se cadastrar", "signup"),
]


def calcular_media_dias_diferenca(lista_compras):
    # Verifica se há pelo menos 3 itens na lista
    if len(lista_compras) < 3:
        return "Dados insuficientes"

    # Obtém as datas de compra dos três primeiros itens
    datas_compra = [item["purchase_date"] for item in lista_compras[:3]]

    # Converte as datas para objetos datetime
    datas_datetime = [datetime.strptime(
        data, "%Y-%m-%d") for data in datas_compra]

    # Calcula a diferença em dias entre as datas
    diferenca_dias = [(datas_datetime[i+1] - datas_datetime[i]
                       ).days for i in range(len(datas_datetime)-1)]

    # Calcula a média das diferenças
    media_dias = sum(diferenca_dias) / len(diferenca_dias)

    return media_dias


keyboard.add(
    *[
        types.InlineKeyboardButton(text, callback_data=callback)
        for text, callback in buttons
    ]
)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Escolha uma opção em nosso menu de funcionalidades:",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    callback_data = call.data

    if callback_data == "fazer_pedido":
        client_cpf = get_client_data(chat_id).json()['cpf']
        formatted_data = {
            "quantity": 1,
            "returnable": True,
            "product_id": 1,
            "cpf": client_cpf
        }
        r = requests.post(sales_api, json=formatted_data)
        bot.send_message(chat_id, "Pedido realizado com sucesso!")
    elif callback_data == "encontrar_deposito":
        find_location(call.message)

    elif callback_data == "historico_de_compra":
        client_cpf = get_client_data(chat_id).json()['cpf']
        r = requests.get(sales_history_api + client_cpf)

        if r.status_code == 200:
            sales_history = r.json()

            # Create a fancy string with emojis
            formatted_sales_history = "\n".join([
                f"📅 Data de compra: {sale['purchase_date']}\n"
                f"🛍 ID do Produto: {sale['product_id']}\n"
                f"💰 Montante total: R$ {sale['total_amount']}\n"
                f"🔄 Retornável: {'Sim' if sale['returnable'] else 'Não'}\n"
                f"🔢 Quantidade: {sale['quantity']}\n"
                f"🆔 ID: {sale['id']}\n"
                f"-----------------------------"
                for sale in sales_history
            ])

            bot.send_message(chat_id, formatted_sales_history)
        else:
            bot.send_message(chat_id, "Failed to retrieve purchase history")

    elif callback_data == "client_data":
        client_data = get_client_data(chat_id)
        if client_data.status_code == 200:
            bot.send_message(
                chat_id, json.dumps(
                    client_data.json(), indent=2, ensure_ascii=False).replace('"', '')
                .replace('{', '============================\n')
                .replace('}', '\n============================')
                .replace(',', '\n')
                .replace(':', ' ➔'))

        else:
            bot.send_message(chat_id, 'Usuario não cadastrado')

    elif callback_data == "estimativa_pedido":
        client_cpf = get_client_data(chat_id)
        if client_cpf.status_code == 200:
            r = requests.get(sales_history_api + client_cpf.json()['cpf'])
            print(r)
            estimativa = calcular_media_dias_diferenca(r.json())

            if estimativa == "Dados insuficientes":
                bot.send_message(
                    chat_id, "Número de pedidos insuficientes para uma estimativa")
            bot.send_message(
                chat_id, f'Média de dias entre os pedidos: {estimativa} Dias')
        else:
            bot.send_message(chat_id, 'Usuario não cadastrado')

    elif callback_data == "signup":
        user_data[chat_id] = {}
        inform_name(call.message)
    else:
        bot.send_message(chat_id, "Opção não reconhecida")


def get_client_data(chat_id):
    return requests.get(get_cliente_api + str(chat_id))


def find_location(msg):
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    location_button = types.KeyboardButton(
        "Compartilhar Localização", request_location=True
    )
    markup.add(location_button)

    bot.send_message(
        msg.chat.id,
        "Clique no botão abaixo para compartilhar sua localização atual:",
        reply_markup=markup,
    )


# Define uma função para criar o botão com o link do mapa
def create_map_button(partida, destino):
    maps_link = f"https://www.google.com/maps/dir/?api=1&origin={partida}&destination={destino}&travelmode=driving"
    button = types.InlineKeyboardButton("Abrir Mapa", url=maps_link)
    return button


@bot.message_handler(content_types=["location"])
def handle_location(msg):
    user_coord: Tuple[float, float] = (
        msg.location.latitude, msg.location.longitude)

    # Encontra a coordenada mais próxima
    coord_proxima, _ = encontrar_coordenada_proxima(user_coord, COORDENADAS)

    # Cria uma mensagem descritiva
    message_text = (
        "Aqui está o link para as direções até o depósito mais"
        f" próximo:\n\n{coord_proxima}"
    )

    # Cria o botão com o link do mapa
    map_button = create_map_button(user_coord, coord_proxima)

    # Cria um teclado inline com o botão
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(map_button)

    # Envia a mensagem com o botão
    bot.send_message(msg.chat.id, message_text, reply_markup=keyboard)


def inform_name(msg):
    bot.send_message(msg.chat.id, "Por favor, seu nome:")
    bot.register_next_step_handler(msg, process_name)


def process_name(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['client_first_name'] = msg.text
    inform_last_name(msg)


def inform_last_name(msg):
    bot.send_message(msg.chat.id, "Por favor, seu sobrenome:")
    bot.register_next_step_handler(msg, process_last_name)


def process_last_name(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['client_last_name'] = msg.text
    inform_number(msg)


def inform_number(msg):
    bot.send_message(msg.chat.id, "Por favor, informe o número:")
    bot.register_next_step_handler(msg, process_number)


def process_number(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['phone_number'] = msg.text
    inform_cpf(msg)


def inform_cpf(msg):
    bot.send_message(msg.chat.id, "Por favor, informe o CPF:")
    bot.register_next_step_handler(msg, process_cpf)


def process_cpf(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['cpf'] = msg.text
    inform_address(msg)


def inform_address(msg):
    bot.send_message(msg.chat.id, "Por favor, informe o endereço:")
    bot.register_next_step_handler(msg, process_address)


def process_address(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['address'] = {"address": msg.text}
    inform_address_details(msg)


def inform_address_details(msg):
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton("Casa"), types.KeyboardButton("Trabalho"))
    bot.send_message(
        msg.chat.id, "Selecione o tipo de endereço:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_address_details)


def process_address_details(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['address']['type'] = msg.text
    inform_state(msg)


def inform_state(msg):
    bot.send_message(msg.chat.id, "Por favor, informe o estado:")
    bot.register_next_step_handler(msg, process_state)


def process_state(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['address']['state'] = msg.text
    user_data[chat_id]['address']['abbreviation'] = msg.text[:2]
    inform_abbreviation(msg)


def inform_abbreviation(msg):
    bot.send_message(msg.chat.id, "Por favor, informe a cidade:")
    bot.register_next_step_handler(msg, process_city)


def process_city(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['address']['city'] = msg.text
    inform_neighborhood(msg)


def inform_neighborhood(msg):
    bot.send_message(msg.chat.id, "Por favor, informe o bairro:")
    bot.register_next_step_handler(msg, process_neighborhood)


def process_neighborhood(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['address']['neighborhood'] = msg.text
    inform_reference_point(msg)


def inform_reference_point(msg):
    bot.send_message(msg.chat.id, "Por favor, informe um ponto de referência:")
    bot.register_next_step_handler(msg, process_reference_point)


def process_reference_point(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['address']['reference_point'] = msg.text
    user_data[chat_id]['address']['id'] = 0
    inform_email(msg)


def inform_email(msg):
    bot.send_message(msg.chat.id, "Por favor, informe o e-mail:")
    bot.register_next_step_handler(msg, process_email)


def process_email(msg):
    chat_id = msg.chat.id
    user_data[chat_id]['email'] = msg.text

    formatted_data = {
        "id": 0,
        "client_first_name": user_data[chat_id].get('client_first_name', ''),
        "client_last_name": user_data[chat_id].get('client_last_name', ''),
        "cpf": user_data[chat_id].get('cpf', ''),
        "address": user_data[chat_id].get('address', {}),
        "phone_number": user_data[chat_id].get('phone_number', ''),
        "email": user_data[chat_id].get('email', ''),
        "telegram_id": str(chat_id)
    }
    r = requests.post(client_api, json=formatted_data)
    if r.status_code == 201:
        bot.send_message(
            chat_id, f"Seu cadastro foi concluído!\n\n{formatted_data}")
    else:
        print(r.content)
        bot.send_message(chat_id, "Falha ao criar usuario.")
    # Reset user data for the next registration
    user_data[chat_id] = {}

    # Send the formatted data back


if __name__ == "__main__":
    bot.polling()
