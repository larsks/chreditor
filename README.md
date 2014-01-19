# Chreditor

This is a simple "server" for use with the [Edit with Emacs][1] extension
for [Google Chrome][2].  The script has been tested on both Linux and
OS X.

[1]: https://chrome.google.com/webstore/detail/edit-with-emacs/
[2]: https://www.google.com/intl/en/chrome/browser/

## Using on Linux

Run the `chreditor.py` script directory, or install it using `pip`:

    pip install .

Or install it using `easy_install`:

    easy_install .

And then run `chreditor`.

## Using on OS X

You can follow the Linux instructions if you'll be running Chreditor
form the command line.

The `build-osx-app` script will generate an OS X application
("Chreditor.app") using the [Platypus][3] command line tool.

[3]: http://sveinbjorn.org/platypus

## Configuration

Chreditor will read configuration information from
`$HOME/.config/chreditor.yml`, a [YAML][4] format configuration file.
All Chreditor configuration must be placed into a `chreditor`
dictionary:

    ---
    chreditor:
      editor: /usr/local/bin/gvim -f

Support configuration options:

- `editor` -- specify a complete editor command line. The filename
  will be appended to this command.

