from vkwave.bots import SimpleLongPollUserBot


class VkBot:
    def __init__(self):
        self.__bot = SimpleLongPollUserBot(tokens="QWERTY")

    @property
    def bot(self) -> SimpleLongPollUserBot:
        return self.__bot