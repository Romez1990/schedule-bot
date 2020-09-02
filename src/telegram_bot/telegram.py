from .telegram_dispatcher import TelegramDispatcher


class Telegram:
    def __init__(self, dispatcher: TelegramDispatcher):
        self.dispatcher = dispatcher

    def start(self) -> None:
        self.dispatcher.start()
