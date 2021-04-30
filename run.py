from fw.main import Framework
from urls import routes, front_controllers
from wsgiref.simple_server import make_server
from signal import signal, SIGINT, SIGTERM
from platform import system
from sys import exit

system_name = system()


def signal_handler(sig, frame=None):
    # обработчик сигналов выхода
    print(f'\nExit signal received: {sig}. Server stopped.')
    if system_name == 'Linux':
        exit(0)


# привязываем signal_handler к сигналам нормального завершения в зависимости от типа ОС
if system_name == 'Linux':
    signal(SIGINT, signal_handler)  # перехват ctrl+c
    signal(SIGTERM, signal_handler)
elif system_name == 'Windows':
    # не нашёл способ установить pywin32 под linux, поэтому импортирую здесь
    from win32api import SetConsoleCtrlHandler  # перехват ctrl+break

    SetConsoleCtrlHandler(signal_handler, True)

app = Framework(routes, front_controllers)

SERVER_PORT = 8080

with make_server('', SERVER_PORT, app) as web:
    print(f"Server: running. OS: {system_name}. Port: {SERVER_PORT}")
    web.serve_forever()
