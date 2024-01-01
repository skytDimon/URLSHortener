from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
import ctypes
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import validators

# Загрузка библиотеки C++
dll = ctypes.cdll.LoadLibrary("./ProjectShorter.dll")

app = FastAPI(
    title="ShortURL"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["Auth"],
)

router = APIRouter(
    tags=['Pages']
)


@router.get('/')
def get_base_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(router)


def url(longURl):
    # Определение типа возвращаемого значения для функции библиотеки C++ (const char*)
    dll.shorten_url.argtypes = [ctypes.c_char_p]
    dll.shorten_url.restype = ctypes.c_char_p

    # Вызов функции из библиотеки C++ и получение результата в Python
    short_url_bytes = dll.shorten_url(longURl.encode())
    short_url_str = short_url_bytes.decode("utf-8")

    return short_url_str


@app.post('/result', tags=["Results"])
def result(request: Request, value: str = Form(...)):
    if validators.url(value):
        processed_value = url(value)
    else:
        return templates.TemplateResponse("index.html", {"request": request,
                                                         "processed_value": "Пожалуйста, убедитесь, что ссылка "
                                                                            "корректна и введите ее еще раз"})

    return templates.TemplateResponse("index.html",
                                      {"request": request, "processed_value": processed_value, "user_value": value})


@app.get("/favicon.ico", tags=["Pages"])
async def favicon():
    return RedirectResponse(url="static/prjgpwejg.png")


@app.get('/{short_id}', tags=["Results"])
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
