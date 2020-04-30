import signal
import asyncio
from os import environ
from wsapi import readbcv, websockets
from utils import createLogger

def stop_handler(sig, loop, fatherlog):
    log = fatherlog.getChild('stop_handler')
    log.info(f'收到信号: {sig}, 正在关闭......')
    loop.stop()
    loop.remove_signal_handler(signal.SIGTERM)
    loop.add_signal_handler(signal.SIGINT, lambda: None)

loop = asyncio.get_event_loop()
fatherlog = createLogger('ReadBCV')

signal.signal(2, lambda: None)
loop.add_signal_handler(15, stop_handler, 15, loop, fatherlog)
loop.add_signal_handler(2, stop_handler, 2, loop, fatherlog)

addr = environ.get('APP_LISTEN', 'localhost')
port = int(environ.get('APP_PORT', '8765'))
path = environ.get('APP_PATH', '/')

start_server = websockets.serve(readbcv, addr, port)
loop.run_until_complete(start_server)
loop.run_forever()