class TextMessagesInterface:
    start: str
    help: str

    def subscribe(self, group_name: str) -> str:
        raise NotImplementedError

    def unsubscribe(self, group_name: str) -> str:
        raise NotImplementedError

    def change_theme(self, theme: str) -> str:
        raise NotImplementedError
