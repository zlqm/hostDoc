import hashlib
from pathlib import Path
import re
from urllib.parse import unquote

from flask import Flask, Response, request, send_file
import requests
from docViewer.render import render_file

app = Flask(__name__)


def render_url(url):
    cache_root = Path('/tmp')

    try:
        resp = requests.get(url)
    except requests.HTTPError:
        return Response('failed to get resource', status=503)

    content_hash = hashlib.new('md5', resp.content).hexdigest
    source_filename = f'{content_hash}.rst'
    dest_filename = f'{content_hash}.html'
    source_path = cache_root.joinpath(source_filename)
    dest_path = cache_root.joinpath(dest_filename)

    if not dest_path.exists():
        if not source_path.parent.exists():
            source_path.parent.mkdir()
        with open(source_path, 'w') as f:
            f.write(resp.text)
        rendered_content = render_file(source_path)
        with open(dest_path, 'wb') as f:
            f.write(rendered_content)
    return send_file(dest_path)


@app.route('/render')
def render():
    file_url = request.args.get('url')
    if not file_url:
        return Response('argument url is required', status=400)
    file_url = unquote(file_url)
    if not file_url.endswith('.rst'):
        return Response('only rst format supported', status=400)
    if not re.match(r'https?://.+', file_url):
        return Response('please check url argument', status=400)
    if not file_url.endswith('.rst'):
        return Response('only rst3 supported!', status=400)
    return render_url(file_url)
