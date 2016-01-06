import hashlib
import hmac
import base64


def calculate_hmac(api_secret, msg_from, msg_to, msg_id, msg_date, msg_nonce, msg_box):
    
    secret = bytearray(api_secret,'utf-8')

    digest_maker = hmac.new(secret,digestmod=hashlib.sha256)

    digest_maker.update(bytearray(msg_from, "ascii")) # from
    digest_maker.update(bytearray(msg_to, "ascii")) # to
    digest_maker.update(bytearray(msg_id, "ascii")) # messageId (hex)
    digest_maker.update(bytearray(msg_date, "ascii")) # date (UNIX Timestamp)
    digest_maker.update(bytearray(msg_nonce, "ascii"))  # nonce (hex)
    digest_maker.update(bytearray(msg_box, "ascii"))  # box (hex)

    return(digest_maker.hexdigest())

def compare_hmac(calculated_hmac, received_hmac):
    if calculated_hmac == received_hmac:
        return True
    else:
        return False

