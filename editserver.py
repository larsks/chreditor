#!/usr/bin/env python

import os
import sys
import argparse
import tempfile
import urlparse
from contextlib import contextmanager

import gevent
from gevent import monkey; monkey.patch_all()
from gevent import subprocess
import bottle

app = bottle.app()

@app.route('/status')
def do_status():
    return 'active'

@app.route('/edit', method='post')
def do_edit():
    url = bottle.request.headers['x-url']
    host = urlparse.urlparse(url)[1].split(':')[0]

    with tempfile.NamedTemporaryFile(prefix='%s_' % host) as fd:
        data_in = bottle.request.body.read()
        fd.write(data_in)
        fd.seek(0)
        subprocess.check_call(['gvim', '-f', '--servername', 'WEB',
                         '--remote-tab-wait-silent', fd.name])
        fd.seek(0)
        data_out = fd.read()
        yield data_out

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--port', '-p', default='45068')
    return p.parse_args()

def main():
    args = parse_args()
    app.run(server='gevent', port=args.port)

if __name__ == '__main__':
    main()

