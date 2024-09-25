import requests
import config
import json
import time


def get_whatsapp_message(message):
    if 'type' not in message:
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'

    return text


def send_whatsapp_message(data):
    try:
        whatsapp_token = config.whatsapp_token
        whatsapp_url = config.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url,
                                 headers=headers,
                                 data=data)

        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e, 403


def text_message(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data


def button_reply_message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i + 1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data


def list_reply_message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i + 1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data


def document_message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data


def sticker_message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data


def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = config.stickers.get(media_name, None)

    return media_id


def reply_reaction_message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data


def reply_text_message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {"message_id": messageId},
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data


def mark_read_message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": messageId
        }
    )
    return data


def chatbot(text, number, messageId, name):
    text = text.lower()  # mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ", text)

    markRead = mark_read_message(messageId)
    list.append(markRead)
    time.sleep(2)

    if "hola" in text:
        body = "¡Hola! 👋 Bienvenido a CEX. ¿Cómo podemos ayudarte hoy?"
        footer = "Equipo CEX"
        options = ["✅ servicios", "📦 seguimiento de envío"]

        reply_button = button_reply_message(number, options, body, footer, "sed1", messageId)
        replyReaction = reply_reaction_message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(reply_button)
    elif "servicios" in text:
        body = "Ofrecemos una variedad de servicios de envío. ¿Cuál de estos servicios te gustaría explorar?"
        footer = "Equipo CEX"
        options = ["Envíos nacionales", "Envíos internacionales", "Embalaje especializado"]

        list_reply = list_reply_message(number, options, body, footer, "sed2", messageId)
        sticker = sticker_message(number, get_media_id("perro_traje", "sticker"))

        list.append(list_reply)
        list.append(sticker)
    elif "embalaje especializado" in text:
        body = "¡Perfecto! ¿Te gustaría recibir más información sobre nuestras opciones de embalaje?"
        footer = "Equipo CEX"
        options = ["✅ Sí, quiero más información", "⛔ No, gracias"]

        reply_button = button_reply_message(number, options, body, footer, "sed3", messageId)
        list.append(reply_button)

    elif "no, gracias." in text:
        text_message_var = text_message(number,
                                   "Perfecto! No dudes en contactarnos si tienes más preguntas. ¡Hasta luego! 😊")
        list.append(text_message_var)
    else:
        data = text_message(number,
                            "Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)

    for item in list:
        send_whatsapp_message(item)




