#!/usr/bin/env python
#
# This is an edit server for use with the "Edit in Emacs" extension
# for Chrome.
#
# http://github.com/larsks/chreditor

import os
import sys
import argparse
import tempfile
import urlparse
import shlex
import logging

import gevent
from gevent import monkey; monkey.patch_all()
from gevent import subprocess
import bottle
import yaml

default_config_file = os.path.join(
        os.environ['HOME'],
        '.config', 'chreditor.yml')

default_edit_command = 'gvim -f --servername WEB --remote-tab-wait-silent'

app = bottle.app()
log = None
config = {}


@app.route('/status')
def do_status():
    return 'active'

@app.route('/edit', method='post')
def do_edit():
    url = bottle.request.headers['x-url']
    host = urlparse.urlparse(url)[1].split(':')[0]
    cmd = config.get('editor', default_edit_command)

    log.info('received editor request from %s', url)

    with tempfile.NamedTemporaryFile(prefix='%s_' % host, delete=False) as fd:
        data_in = bottle.request.body.read()
        fd.write(data_in)

    try:
        cmd = shlex.split(cmd) + [fd.name]
        log.debug('running command: %s', ' '.join('"%s"' % x for x in cmd))
        retcode = subprocess.check_call(cmd)
        log.debug('command returned: %d', retcode)
    except OSError as detail:
        log.warn('failed to run editor: %s', detail)

    with open(fd.name) as fd:
        data_out = fd.read()
        yield data_out


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--port', '-p', default='45068')
    p.add_argument('--config', '-f',
            default=default_config_file)
    p.add_argument('--debug', action='store_true')
    return p.parse_args()


def load_config(config_file):
    global config
    log.debug('trying to load configuration from %s', config_file)

    try:
        with open(config_file) as fd:
            log.info('loading configuation from %s', config_file)
            config = yaml.load(fd)['chreditor']
    except (IOError, KeyError):
        pass


def main():
    global log

    args = parse_args()
    
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARN

    logging.basicConfig(
            level=loglevel,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(message)s')

    log = logging.getLogger('chreditor')
    load_config(args.config)

    sys.stderr.write('\n'.join([
    '======================================================================',
    'Creditor ("Edit with Emacs" edit server for Linux and OS X)',
    'by Lars Kellogg-Stedman <lars@oddbit.com>',
    'http://github.com/larsks/chreditor',
    '======================================================================',
    '',
    ]))

    app.run(server='gevent', port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()

