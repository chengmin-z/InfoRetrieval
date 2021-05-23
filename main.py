import logging
import signal

import retrieval
from crawler import Crawler
import dao

from sanic import Sanic
from sanic import response
from sanic import exceptions


app = Sanic('Remote')


@app.exception(exceptions.NotFound)
async def ignore_404(request, exception):
    return response.text('errorUrl', status=404)


@app.post('/query')
async def query(request):
    query_str: str = request.json.get('input')
    result = retrieval.retrieval_query(query_str)
    return response.json({'code': 200, 'msg': 'success', 'data': result}, status=200)


def main():
    need_get_file: bool = True
    if need_get_file:
        Crawler().process()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    _logFmt = logging.Formatter('%(ascTime)s %(levelName).1s %(lineno)-3d %(funcName)-20s %(message)s',
                                datefmt='%H:%M:%S')
    _consoleHandler = logging.StreamHandler()
    _consoleHandler.setLevel(logging.DEBUG)
    _consoleHandler.setFormatter(_logFmt)

    log = logging.getLogger(__file__)
    log.addHandler(_consoleHandler)
    log.setLevel(logging.DEBUG)

    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
