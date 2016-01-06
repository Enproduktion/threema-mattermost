from flask import request, abort, jsonify

from threema_mm import app, settings, calculate_hmac, threema, data
from threema_mm.data import users

import threema_mm.threema.lookup
import threema_mm.threema.decrypt

import asyncio
import netaddr

public_keys = {}


def get_user_attribute(threema_id, requested_attribute):
    if threema_id in users.users:
        try:
            return(users.users[threema_id][requested_attribute])
        except:
            return(None)


def commit_webhook(text, threema_id):
    import requests

    if text == "None":
        return False

    dictToSend = {
        "text": text,
        "username": get_user_attribute(threema_id, "name") or threema_id,
        "icon_url": get_user_attribute(threema_id, "icon_url") or settings.icon_url
    }

    r = requests.post(settings.mattermost_hook_url, json=dictToSend)


def getpublickey (threema_id):

    loop = asyncio.get_event_loop()
    public_keys[threema_id] = loop.run_until_complete(threema.lookup.getpub(settings.threema_id, settings.threema_api_secret, threema_id))

    if threema_id in public_keys:
        return public_keys[threema_id]
    else:
        loop = asyncio.get_event_loop()
        public_keys[threema_id] = loop.run_until_complete(threema.lookup.getpub(settings.threema_id, settings.threema_api_secret, threema_id))
        return public_keys[threema_id]


@app.before_request
def limit_remote_addr():
    import netaddr
    if netaddr.IPAddress(request.remote_addr) not in netaddr.IPNetwork(settings.threema_servers):
        abort(403)


@app.route('/', methods=['POST'])
def send_json():
    message = {}

    if calculate_hmac.compare_hmac(calculate_hmac.calculate_hmac(settings.threema_api_secret,request.form['from'], request.form['to'], request.form['messageId'], request.form['date'], request.form['nonce'], request.form['box']), request.form['mac']): 
        message["from"] =  request.form['from']
        message["to"] =  request.form['to']
        message["messageId"] = request.form['messageId']
        message["date"] = request.form['date']
        message["nonce"] = request.form['nonce']
        message["box"] = request.form['box']
        message["mac"] = request.form['mac']
	
        message["public"] = getpublickey(message["from"])
        message["plain"] = str(threema.decrypt.msg_decrypt(settings.threema_private_key, message["public"], message["box"], message["nonce"]))

        commit_webhook(message["plain"], message["from"])

        return "OK"
    else:
        return "NOT OK"
