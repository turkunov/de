from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from python_app.utils.os_ops import load_json, load_html
from python_app.db import session
from python_app.crud import (
    get_users, insert_random_user
)
from bs4 import BeautifulSoup as BSHTML
import random


META = load_json('./fastapi_meta.json')
app = FastAPI(
    title=META['CLIENT_META']['title'],
    description=META['CLIENT_META']['description'],
    version=META['CLIENT_META']['version'],
    terms_of_service=None,
    contact=META['CLIENT_META']['contact'],
    license_info=None
)

# CORS for debug purpusoses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# middleware to accept only 
# GET /, /gen_user, /docs and /health
@app.middleware("http")
async def request_preprocesser(request: Request, call_next):
    endpoint, method = str(request.url).split('/')[-1], request.method.lower()
    if method == 'get':
        if endpoint in ['','health','docs','openapi.json'] or 'gen_user' in endpoint:
            response = await call_next(request)
            return response
    return Response(status_code=404)


@app.get('/')
async def get_records():
    res = list(map(vars, get_users(session)))

    # load html file with random user's profile card
    soup = BSHTML(load_html('./static/db_view.html'))
    if len(res) > 0:
        res = random.choice(res)
        image = soup.find('img', attrs={'id': 'profile_pic'})
        image['src'] = res['img']
        name = soup.find('h5', attrs={'id':'user_name'})
        name.string = f'{res["name"]} {res["surname"]}'

    return HTMLResponse(content=soup, status_code=200)


@app.get('/gen_user')
async def add_user(clear_cache: bool = False):
    random_person = insert_random_user(session, clear_cache=clear_cache)
    return JSONResponse(status_code=200, content=f'Inserted 1 new record | '
                        f'name : {random_person["name"]} | surname : {random_person["surname"]}')


@app.get('/health')
async def check_health():
    return JSONResponse(status_code=200, content={'status': 'OK'})