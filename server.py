import asyncio
import pickle

from aiohttp import web

app = web.Application()
docmap = None

def load_map():
    global docmap
    docmap = pickle.load(open('server.map', 'rb'))

def search_map(query):
    res = []
    query = query.lower()

    for entry in docmap:
        if query in entry['name'].lower():
            res.append((entry['name'], 1))

        if query in entry['data']:
            res.append((entry['name'], 0.5))

    s = sorted(res, key=lambda e: e[1], reverse=True)
    return s

async def index(request):
    return web.Response(text='This is an elixir-docsearch server!')

async def search(request):
    query = request.query.get('query')

    t = app.loop.run_in_executor(None, search_map, query)
    res = await t
    res = res[:15]

    return web.json_response(res)

def main():
    load_map()

    app.router.add_get('/', index)
    app.router.add_get('/search', search)

    web.run_app(app, host='127.0.0.1', port=8069)

if __name__ == '__main__':
    main()

