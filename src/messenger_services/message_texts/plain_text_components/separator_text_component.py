from data.vector import List
from messenger_services.message_texts.components import TextComponent


class SeparatorTextComponent(TextComponent):
    def __init__(self, components: List[TextComponent], separator: str) -> None:
        self.__components = components
        self.__separator = separator

    def render(self) -> str:
        components = self.__components.map(self.__render_component)
        return self.__separator.join(components)

    def __render_component(self, component: TextComponent) -> str:
        return component.render()
