from .primitives import TextComponent


class MessagesInterface:
    start: TextComponent
    help: TextComponent

    def subscribe(self, group_name: str) -> TextComponent:
        raise NotImplementedError

    def unsubscribe(self, group_name: str) -> TextComponent:
        raise NotImplementedError

    def change_theme(self, theme: str) -> TextComponent:
        raise NotImplementedError
