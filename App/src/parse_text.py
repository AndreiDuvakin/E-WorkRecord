import re


def parser_text(text):
    data = {
        "title": {
            "serial": "",
            "number": "",
            "first_name": "",
            "last_name": "",
            "patronymic": "",
            "birthday": "",
            "issue_date": "",
            "profession": "",
            "education": ""
        }
    }

    serial_match = re.search(r'\w № (\d+) \w', text)
    if serial_match:
        data["title"]["number"] = serial_match.group(1)

    return data
