import binascii

from threema.gateway import util, e2e
from threema.gateway.key import Key


def msg_decrypt(private_key, public_key, message, nonce):
    # Get key instances

    private_key = util.read_key_or_key_file(private_key, Key.Type.private)
    public_key = util.read_key_or_key_file(public_key, Key.Type.public)

    # Convert nonce to bytes
    nonce = binascii.unhexlify(nonce)

    # Read message from stdin and convert to bytes
    message = binascii.unhexlify(message)

    # Print text
    text_message = e2e.decrypt(private_key.sk, public_key.pk, nonce, message)
    return(text_message)

def main():
    print("This application is for library usage only")

if __name__ == '__main__':
    main()
