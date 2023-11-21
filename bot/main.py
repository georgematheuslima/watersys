from telebot import types, TeleBot
from calcular_distancia import encontrar_coordenada_proxima
from typing import List, Tuple

# API_KEY =

# Lista de coordenadas dos depósitos
COORDENADAS: List[Tuple[float, float]] = [
    (-2.577497, -44.1676215),
    (-2.5710628, -44.1696658),
    (-2.542826, -44.1935365),
    (-2.5689437, -44.2687578),
]

bot = TeleBot(API_KEY)

# Crie um teclado inline
keyboard = types.InlineKeyboardMarkup(row_width=2)

# Adicione botões inline
buttons = [
    ("Pedir galão de água", "fazer_pedido"),
    ("Encontrar depósito", "encontrar_deposito"),
    ("Histórico de compra", "historico_de_compra"),
    ("Estimar galão", "estimar_galao"),
    ("Média de galão", "media_galao"),
]

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
        bot.send_message(chat_id, "Você selecionou 'Pedir galão de água'")
    elif callback_data == "encontrar_deposito":
        find_location(call.message)
    elif callback_data == "historico_de_compra":
        bot.send_message(chat_id, "Você selecionou 'Histórico de compra'")
    elif callback_data == "estimar_galao":
        bot.send_message(chat_id, "Você selecionou 'Estimar galão'")
    elif callback_data == "media_galao":
        bot.send_message(chat_id, "Você selecionou 'Média de galão'")
    else:
        bot.send_message(chat_id, "Opção não reconhecida")


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


if __name__ == "__main__":
    bot.polling()
