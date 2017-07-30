import asyncio
import pickle
import logging

from aiohttp import web

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

app = web.Application()
docmap = None

def load_map():
    global docmap
    docmap = pickle.load(open('server.map', 'rb'))

def search_map(query):
    res = []
    query = query.lower()

    for entry in docmap:
        score = 0

        data = entry['data']

        if query in data:
            count = data.count(query)
            score = count / 50

        if query in entry['name'].lower():
            score = 1

        score = min(score, 1)
        score = round(score, 2)
        if score > 0.05:
            res.append((entry['name'], score))

    s = sorted(res, key=lambda e: e[1], reverse=True)
    return s

async def index(request):
    return web.Response(text='This is an elixir-docsearch server!')

async def search(request):
    payload = await request.json()
    query = payload['query']
    limit = payload.get('limit', 15)

    if len(query) == 0:
        return web.Response(status=400, text='BAD REQUEST')

    log.info('Searching for %r', query)

    t = app.loop.run_in_executor(None, search_map, query)
    res = await t
    res = res[:limit]

    return web.json_response(res)

def main():
    load_map()

    app.router.add_get('/', index)
    app.router.add_get('/search', search)

    web.run_app(app, host='127.0.0.1', port=8069)

if __name__ == '__main__':
    main()

