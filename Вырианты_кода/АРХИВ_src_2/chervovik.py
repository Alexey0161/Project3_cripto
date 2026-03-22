# import re

# pattern = r'.+^([^/.]+)'
# text = "пример.тест.слово"

# match = re.match(pattern, text)
# if match:
#     print(match.group(1))
# text = "пример.тест.слово.песня.симфония"

    text = text.split('.')
    text = text[0] + '.' + ''.join(text[1:])
# print(text)