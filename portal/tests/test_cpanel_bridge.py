import base64
import importlib.util
from pathlib import Path
import pytest
from flask import Flask, request

spec = importlib.util.spec_from_file_location('cpanel_bridge', Path(__file__).parents[1]/'cpanel/bridge.py')
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

def payload(**changes):
    result = dict(host='ai.philexcel.com', body='', uri='/', method='GET', remote='192.0.2.1')
    result.update(changes)
    return result

def test_bridge_preserves_headers_cookies_and_request():
    app = Flask(__name__)
    @app.post('/hello')
    def hello():
        response = app.response_class(request.get_data(), status=201)
        response.set_cookie('first','a',secure=True,httponly=True)
        response.set_cookie('second','b',secure=True)
        response.headers['Location'] = 'https://' + request.host + '/next'
        assert request.is_secure
        assert request.args['q'] == 'one'
        assert request.cookies['session'] == 'example'
        assert request.headers['X-CSRF-Token'] == 'token'
        return response
    result=bridge.dispatch(app,payload(uri='/hello?q=one', method='POST',body=base64.b64encode(b'hello').decode(),cookie='session=example',csrf='token'))
    assert result['status']==201
    assert base64.b64decode(result['body'])==b'hello'
    assert len([h for h in result['headers'] if h[0]=='Set-Cookie'])==2
    assert ('Location','https://ai.philexcel.com/next') in result['headers']

def test_bridge_rejects_host_and_large_request():
    with pytest.raises(ValueError): bridge.dispatch(None,payload(host='evil.example'))
    with pytest.raises(ValueError): bridge.dispatch(None,payload(body=base64.b64encode(b'x'*16385).decode()))

def test_rate_limit_persists_and_expires(tmp_path):
    db=tmp_path/'rate.sqlite'
    for _ in range(60): assert bridge.rate_allowed(db,'address',now=600)
    assert not bridge.rate_allowed(db,'address',now=600)
    assert bridge.rate_allowed(db,'other-address',now=600)
    assert bridge.rate_allowed(db,'address',now=660)
