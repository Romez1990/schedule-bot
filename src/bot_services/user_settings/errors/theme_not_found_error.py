class ThemeNotFoundError(Exception):
    def __init__(self, theme_name: str) -> None:
        super().__init__(f'theme {theme_name} not found')
