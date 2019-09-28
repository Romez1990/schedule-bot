import imgkit


def load_template() -> str:
    with open('template/index.html', encoding='utf8') as file:
        return file.read()


html = load_template()
main_css = 'template/main.css'
themes = {
    'light': 'template/themes/light.css',
    'dark': 'template/themes/dark.css',
}
imgkit.from_string(html, css=[themes['dark'], main_css],
                   output_path='schedule.jpg')
