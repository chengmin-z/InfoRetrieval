import logging
import signal

from crawler import Crawler
import search

from sanic import Sanic
from sanic import response
from sanic import exceptions
import time


app = Sanic('Remote')


@app.exception(exceptions.NotFound)
async def ignore_404():
    return response.text('errorUrl', status=404)


@app.post('/getPic')
async def get_pic(request):
    f = request.files.get("img")
    with open('./temp/' + str(int(time.time())) + '.jpg', 'wb') as fileUp:  # 这里必须为读写二进制模式的 wb
        fileUp.write(f.body)
        fileUp.close()
    return response.json({'code': 200, 'msg': 'success'}, status=200)


@app.post('/query')
async def query(request):
    query_str: str = request.json.get('input')
    result = search.retrieval_query(query_str)
    return response.json({'code': 200, 'msg': 'success', 'data': result}, status=200)


def main():
    print('[INFO] Welcome to use the backend of retrieval system')
    update_file = input('[INFO] Do you want to update the datafiles and construct inverted index? (yes/on): ')
    if update_file == 'yes':
        Crawler().process()
        print('[INFO] progress: Creating inverse index txt_file')
        search.create_inverse_txt()
        print('[INFO] progress: Created inverse index txt_file done')
    else:
        update_reverse_index = input('[INFO] Do you want to construct inverted index? (yes/on): ')
        if update_reverse_index == 'yes':
            print('[INFO] progress: Creating inverse index txt_file')
            search.create_inverse_txt()
            print('[INFO] progress: Created inverse index txt_file done')

    print('[INFO] Backend running')

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
