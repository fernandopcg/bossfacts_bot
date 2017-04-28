# -*- coding: utf-8 -*-
import json
import requests
import time
import urllib
import random

TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot_name = "@bossfacts_bot"	# Bot will only respond to messages containing this

RESPONSES = ['Eso es fácil no?',
            'Eso está hecho ya',
            'Eso es copy paste',
            'En un sprint está hecho, no?',
            'Los de Cloud Services lo tienen ya hecho, es adaptarlo',
            'Mira a ver si respira',
            'Dale un ping',
            'Pero se va dejando?',
            'Estamos en periodo friends and family',
            'En Openshit',
            'Posgret',
            'Son primos hermanos',
            'Al final, no deja de ser...',
            'Hay que publicar en yammer',
            'Nos tenemos que dejar ver',
            'Olvidate de eso, ahora estamos con otra cosa',
            'Nos ha salido un portalillo nuevo',
            'No parece muy complicado eso,¿no?',
            'Lo único cambiarle los colores',
            'Son cuatro líneas de código',
            'Lo ponemos en friends&family de momento',
            'Arturo que no, que eso no es así',
            'Hay que ir mirando esto: http://bit.ly/2qei3E6',
            'Un par de clicks']


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        print update
        if "text" in update["message"]:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_to=None):
    text = urllib.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&reply_to_message_id={}".format(text, chat_id, reply_to)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            #echo_all(updates)
            for update in updates["result"]:
                    print update
                    if "message" in update and "text" in update["message"] and bot_name in update["message"]["text"]:
                        original_message = update["message"]["message_id"]
                        text = update["message"]["text"]
                        text = random.choice(RESPONSES)
                        chat = update["message"]["chat"]["id"]
                        print "text:"
                        print text
                        print " chat:"
                        print chat
                        send_message(text, chat, original_message)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
