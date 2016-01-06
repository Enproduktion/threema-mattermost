import asyncio

from threema.gateway import Connection, GatewayError, Key

@asyncio.coroutine
def getpub(threema_id, threema_api_secret, requested_id):
    connection = Connection(threema_id, threema_api_secret)
    try:
        with connection:
            key = (yield from connection.get_public_key(requested_id))
            return(Key.encode(key))
    except GatewayError as exc:
        return(False)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getpub())

if __name__ == '__main__':
    main()

