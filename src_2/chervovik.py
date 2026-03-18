import re

pattern = r'^([^/\s]+)'
text = "пример /тест слово"

match = re.match(pattern, text)
if match:
    print(match.group(1))