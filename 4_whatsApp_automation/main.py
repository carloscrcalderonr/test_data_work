from flask import Flask, request
import config
import functions

app = Flask(__name__)

@app.route('/welcome', methods=['GET'])
def welcome_message():
    return 'Hola mundo cex, desde Flask'

@app.route('/webhook', methods=['GET'])
def validate_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == config.token and challenge is not None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as error:
        return str(error), 403

@app.route('/webhook', methods=['POST'])
def handle_messages():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        message_id = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtain_whatsapp_message(message)

        services.process_chatbot(text, number, message_id, name)
        return 'enviado'

    except Exception as error:
        return 'no enviado ' + str(error)

if __name__ == '__main__':
    app.run()
