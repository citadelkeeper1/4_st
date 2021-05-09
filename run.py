from wsgiref.simple_server import make_server
from signal import signal, SIGINT, SIGTERM, raise_signal
from platform import system
from sys import exit
from keyboard import hook
from os import kill, getpid
from fw.main import Framework
from urls import front_controllers
from views import routes

main_process_id = getpid()


def keyboard_handler(kb_event):  # обработчик клавиатуры
    if kb_event.name == "esc":
        raise_signal(SIGTERM)


hook(keyboard_handler)

system_name = system()


def signal_handler(sig, frame=None):
    # обработчик сигналов выхода
    if system_name == 'Linux':
        print(f'\nExit signal received (u): {sig}. Server stopped.')
        exit(0)
    else:  # ctrl+break, ctrl+c, etc...
        print(f'\nExit signal received (w): {sig}. Server stopped.')
        kill(main_process_id, SIGTERM)


# привязываем signal_handler к сигналам нормального завершения
signal(SIGINT, signal_handler)  # перехват ctrl+c для linux
signal(SIGTERM, signal_handler)
if system_name == 'Windows':
    from win32api import SetConsoleCtrlHandler  # перехват ctrl+break

    SetConsoleCtrlHandler(signal_handler, True)

app = Framework(routes, front_controllers)

SERVER_PORT = 8080

with make_server('', SERVER_PORT, app) as web:
    print(f"Server: running. OS: {system_name}. Port: {SERVER_PORT}")
    try:
        web.serve_forever()
    except KeyboardInterrupt:
        pass
