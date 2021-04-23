
from fw.main import Framework
from urls import routes, front_controllers
from wsgiref.simple_server import make_server
from signal import signal, SIGINT, SIGTERM


def signal_handler(sig, frame):
    # обработчик сигналов выхода
    print(f'\nExit signal received: {sig}. Server stopped.')
    exit(0)


# привязываем signal_handler к сигналам нормального завершения
signal(SIGINT, signal_handler)
signal(SIGTERM, signal_handler)

app = Framework(routes, front_controllers)

SERVER_PORT = 8080

with make_server('', SERVER_PORT, app) as web:
    print(f"Server running on port: {SERVER_PORT}")
    web.serve_forever()
