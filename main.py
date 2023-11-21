# import secrets
#
# import uvicorn
# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from src.short_URL import url, dll
# import ctypes
# from fastapi import FastAPI, Depends, APIRouter
# from src.auth.base_config import auth_backend, fastapi_users
# from src.auth.schemas import UserRead, UserCreate
# from flask import redirect, request, render_template
#
# templates = Jinja2Templates(directory="templates")
#


#
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="",
#     tags=["Auth"],
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="",
#     tags=["Auth"],
# )
#
# @app.get("/shortURL", tags=["Generate"])
# def get_shortedURL(user: str):
#     return f"Ваша сокращенная ссылка -> {redirect_url(result(user))}"
#
#
# if __name__ == "__main__":
#     uvicorn.run("main:app --reload", port=5000, log_level="info")
import ctypes
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, HTMLResponse
from pages.router import router as router_pages

# Загрузка библиотеки C++
dll = ctypes.cdll.LoadLibrary("./ProjectShorter.dll")
app = FastAPI(
    title="ShortURL"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(router)


@app.get("/items/{short_id}", response_class=HTMLResponse)
def redirect_url(short_id: str):
    dll.getDataFromDatabase.argtypes = [ctypes.c_char_p]
    dll.getDataFromDatabase.restype = ctypes.c_char_p

    # Вызов функции из библиотеки C++ и получение результата в Python
    redirectable_url_bytes = dll.getDataFromDatabase(("http://127.0.0.1:8000/" + short_id).encode())
    redirectable_url_str = redirectable_url_bytes.decode("utf-8")

    return RedirectResponse(redirectable_url_str, status_code=302)


def url(longURl):
    # Определение типа возвращаемого значения для функции библиотеки C++ (const char*)
    dll.shorten_url.argtypes = [ctypes.c_char_p]
    dll.shorten_url.restype = ctypes.c_char_p

    # Вызов функции из библиотеки C++ и получение результата в Python
    short_url_bytes = dll.shorten_url(longURl.encode())
    short_url_str = short_url_bytes.decode("utf-8")

    return short_url_str


# @app.get('/')
# def index(request: Request):
#


@app.post('/result')
def result(request: Request, value: str = Form(...)):
    if len(value) > 1:
        processed_value = url(value)
    else:
        return templates.TemplateResponse("index.html", {"request": request, "processed_value": "Вы не указали ссылку"})

    return templates.TemplateResponse("index.html",
                                      {"request": request, "processed_value": processed_value, "user_value": value})


# @app.get('/favicon.ico')
# def favicon():
#     return app.send_static_file('prjgpwejg.png')


@app.get('/{short_id}')
def redirect_url(short_id: str):
    dll.getDataFromDatabase.argtypes = [ctypes.c_char_p]
    dll.getDataFromDatabase.restype = ctypes.c_char_p

    # Вызов функции из библиотеки C++ и получение результата в Python
    redirectable_url_bytes = dll.getDataFromDatabase(("http://127.0.0.1:8000/" + short_id).encode())
    redirectable_url_str = redirectable_url_bytes.decode("utf-8")

    return RedirectResponse(redirectable_url_str, status_code=302)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
