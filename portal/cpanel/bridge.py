"""One bounded WSGI request, launched by the account's PHP-FPM front controller."""
import base64
import io
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path('/home/philexcel/.config/philexcel-hub')
HOSTS = {f'{name}.philexcel.com' for name in ('ai', 'enroll', 'admin', 'axon')}

def rate_allowed(database, address, now=None):
    """Account-private, atomic shared limit across short-lived PHP/Python workers."""
    minute = int(time.time() if now is None else now) // 60
    with sqlite3.connect(database, timeout=5) as db:
        db.execute('CREATE TABLE IF NOT EXISTS requests (address TEXT, minute INTEGER, count INTEGER, PRIMARY KEY(address, minute))')
        db.execute('BEGIN IMMEDIATE')
        db.execute('DELETE FROM requests WHERE minute < ?', (minute - 2,))
        db.execute('INSERT INTO requests VALUES (?, ?, 1) ON CONFLICT(address,minute) DO UPDATE SET count=count+1', (address, minute))
        count = db.execute('SELECT count FROM requests WHERE address=? AND minute=?', (address, minute)).fetchone()[0]
    return count <= 60

def dispatch(application, payload):
    host = payload['host']
    if host not in HOSTS:
        raise ValueError('Untrusted host')
    body = base64.b64decode(payload['body'], validate=True)
    if len(body) > 16384:
        raise ValueError('Request too large')
    url = urlsplit(payload['uri'])
    environ = {
        'REQUEST_METHOD': payload['method'], 'SCRIPT_NAME': '',
        'PATH_INFO': unquote(url.path, encoding='latin-1'), 'QUERY_STRING': url.query,
        'SERVER_NAME': host, 'SERVER_PORT': '443', 'HTTP_HOST': host,
        'SERVER_PROTOCOL': 'HTTP/1.1', 'REMOTE_ADDR': payload['remote'],
        'CONTENT_LENGTH': str(len(body)), 'CONTENT_TYPE': payload.get('content_type', ''),
        'wsgi.version': (1, 0), 'wsgi.url_scheme': 'https', 'wsgi.input': io.BytesIO(body),
        'wsgi.errors': sys.stderr, 'wsgi.multithread': False,
        'wsgi.multiprocess': True, 'wsgi.run_once': True,
    }
    for key, target in [('cookie', 'HTTP_COOKIE'), ('csrf', 'HTTP_X_CSRF_TOKEN'), ('accept', 'HTTP_ACCEPT')]:
        environ[target] = payload.get(key, '')
    response = {}
    def start_response(status, headers, exc_info=None):
        if exc_info:
            raise exc_info[1].with_traceback(exc_info[2])
        response.update(status=int(status.split()[0]), headers=headers)
    chunks = application(environ, start_response)
    data = bytearray()
    try:
        for chunk in chunks:
            data.extend(chunk)
            if len(data) > 8 * 1024 * 1024:
                raise ValueError('Response too large')
    finally:
        if hasattr(chunks, 'close'):
            chunks.close()
    response['body'] = base64.b64encode(data).decode('ascii')
    return response

def main():
    os.umask(0o077)
    payload = json.loads(sys.stdin.buffer.read(100000))
    if payload['host'] not in HOSTS:
        raise ValueError('Untrusted host')
    config = json.loads((PRIVATE / 'environment.json').read_text())
    if not isinstance(config, dict) or any(not isinstance(v, str) for v in config.values()):
        raise ValueError('Invalid private configuration')
    os.environ.update(config)
    # Flask's in-memory limiter cannot persist across one-request workers.
    # The SQLite limiter below is shared across every portal worker instead.
    os.environ['CPANEL_PRIVATE_BRIDGE'] = '1'
    os.environ['RATE_LIMIT_STORAGE_URI'] = 'memory://'
    if not rate_allowed(PRIVATE / 'rate.sqlite', payload['remote']):
        result = {'status': 429, 'headers': [('Content-Type','text/plain'), ('Retry-After','60'), ('Cache-Control','no-store')], 'body': base64.b64encode(b'Too many requests. Please wait a minute.').decode()}
    else:
        sys.path.insert(0, str(ROOT))
        from app import app
        result = dispatch(app, payload)
    print(json.dumps(result))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        # Do not expose tokens, request bodies, paths or provider messages.
        print('Portal bridge failure: ' + type(error).__name__, file=sys.stderr)
        sys.exit(1)
