# import pyshorteners
#
#
# def shorten_url(url):
#     return pyshorteners.Shortener().clckru.short(url)
import ctypes

# Загрузка библиотеки C++
dll = ctypes.cdll.LoadLibrary("./ProjectShorter.dll")


def url(longURl):
    # Определение типа возвращаемого значения для функции библиотеки C++ (const char*)
    dll.shorten_url.argtypes = [ctypes.c_char_p]
    dll.shorten_url.restype = ctypes.c_char_p

    # Вызов функции из библиотеки C++ и получение результата в Python
    short_url_bytes = dll.shorten_url(longURl.encode())
    short_url_str = short_url_bytes.decode("utf-8")

    return short_url_str
