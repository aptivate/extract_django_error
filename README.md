# Django Error Extractor

Extracts details of errors from Django error emails


## Installation

If you don't use `pipsi`, you're missing out.
Here are [installation instructions](https://github.com/mitsuhiko/pipsi#readme).

Simply run:

    $ pipsi install .

Or if you want to use pip:

    $ sudo pip install -e git+https://github.com/aptivat/extract_django_error


## Usage

The way it was written was to give it a list of filenames, and each filename is
an email (as if you're using maildir).  I use notmuch so I can do:

    $ notmuch search --output=files --limit=10 \
        'subject:"django error external ip internal server error" AND from:root@myserver.com' | \
        xargs extract_django_error

Which would give us the one line exception description from each email.

You can also pipe an email directly into the command, eg:

    $ cat path/to/email | extract_django_error -

Note the `-` at the end of the error to make the command read the email from stdin.
Not so useful when just using `cat` but could be used to pipe in emails from procmail
or other scripts.

## Options

    -m, --max-len INTEGER  Maximum length of returned string (default: 80)
    -s, --server-name      Include the URL server name
    -p, --path             Include the URL path
    -q, --query            Include the URL query string
    --help                 Show this message and exit
