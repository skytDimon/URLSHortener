import random
import string

import pyshorteners


def shorten_url(url):

    return pyshorteners.Shortener().clckru.short(url)
def shorten_url1(long_url):
    characters = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(characters) for _ in range(6))
    short_url = "https://shortURL/" + short_id

    # Сохранить пару "длинная ссылка - сокращенная ссылка" в базе данных

    return short_url


if __name__ == "__main__":
    print(shorten_url1(shorten_url("https://dzen.ru/list/gadgets/cokratit-tekct-python")))