import datetime
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

    serial_match = re.search(r'№\s*(\d+)', text)
    if serial_match:
        data["title"]["number"] = serial_match.group(1)

    last_name_match = re.search(r'\bфамилия[:\s]+([А-ЯЁа-яё]+)', text, re.IGNORECASE)
    text_rows = text.split('\n')
    number_index = list(filter(lambda x: '№' in x, text_rows))
    if not number_index:
        next_index = 3
    else:
        next_index = text_rows.index(number_index[0])
    if last_name_match:
        data["title"]["last_name"] = last_name_match.group(1)
    else:
        if number_index:
            number_index = next_index
            for i in range(1, 4):
                row = text_rows[number_index + i].split()
                row_copy = row.copy()
                if len(row) < 2:
                    continue
                row.sort(key=lambda x: (row_copy.index(x), len(x)))
                row = list(filter(lambda x: len(x) > 3, row))
                if row:
                    if len(row[-1]) > 3:
                        data["title"]["last_name"] = row[-1]
                        next_index = number_index + i
                        break

    first_name_match = re.search(r'\bимя[:\s]+([А-ЯЁа-яё]+)', text, re.IGNORECASE)
    if first_name_match:
        data["title"]["first_name"] = first_name_match.group(1)
    else:
        if number_index:
            number_index = next_index
            for i in range(1, 4):
                row = text_rows[number_index + i].split()
                row_copy = row.copy()
                if len(row) < 2:
                    continue
                row.sort(key=lambda x: (row_copy.index(x), len(x)))
                row = list(filter(lambda x: len(x) > 3, row))
                if row:
                    if len(row[-1]) > 3:
                        data["title"]["first_name"] = row[-1]
                        next_index = number_index + i
                        break

    patronymic_match = re.search(r'\bотчество[:\s]+([А-ЯЁа-яё]+)', text, re.IGNORECASE)
    if patronymic_match:
        data["title"]["patronymic"] = patronymic_match.group(1)
    else:
        if number_index:
            number_index = next_index
            for i in range(1, 4):
                row = text_rows[number_index + i].split()
                row_copy = row.copy()
                if len(row) < 2:
                    continue
                row.sort(key=lambda x: (row_copy.index(x), len(x)))
                row = list(filter(lambda x: len(x) > 3, row))
                if row:
                    if len(row[-1]) > 3:
                        data["title"]["patronymic"] = row[-1]
                        next_index = number_index + i
                        break

    patronymic_match = re.search(r'\bние[:\s]+([А-ЯЁа-яё]+)', text, re.IGNORECASE)
    if patronymic_match:
        data["title"]["education"] = patronymic_match.group(1)
    else:
        if number_index:
            number_index = next_index
            for i in range(1, 4):
                row = text_rows[number_index + i].split()
                row_copy = row.copy()
                if len(row) < 2:
                    continue
                row.sort(key=lambda x: (row_copy.index(x), len(x)))
                row = list(filter(lambda x: len(x) > 3, row))
                if row:
                    if len(row[-1]) > 3:
                        data["title"]["education"] = row[-1]
                        next_index = number_index + i
                        break

    patronymic_match = re.search(r'\bость[:\s]+([А-ЯЁа-яё]+)', text, re.IGNORECASE)
    if patronymic_match:
        data["title"]["profession"] = patronymic_match.group(1)
    else:
        if number_index:
            number_index = next_index
            for i in range(1, 4):
                row = text_rows[number_index + i].split()
                row_copy = row.copy()
                if len(row) < 2:
                    continue
                row.sort(key=lambda x: (row_copy.index(x), len(x)))
                row = list(filter(lambda x: len(x) > 3, row))
                if row:
                    if len(row[-1]) > 3:
                        data["title"]["profession"] = row[-1]
                        next_index = number_index + i
                        break

    birthday_match = re.search(r'\bния[:\s]+([0-3]?[0-9] [а-яё]+ \d{4})', text, re.IGNORECASE)
    if birthday_match is None:
        birthday_match = re.search(r'(\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4})', text, re.IGNORECASE)
    if birthday_match:
        try:
            data["title"]["birthday"] = datetime.datetime.strptime(birthday_match.group(1), '%d %B %Y').strftime(
                '%Y-%m-%d')
        except ValueError:
            pass

    all_word = []
    for word_row in [words.split() for words in text_rows]:
        for word in word_row:
            if len(word) > 3:
                all_word.append(word)

    return data, all_word
