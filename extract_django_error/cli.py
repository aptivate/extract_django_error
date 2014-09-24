from __future__ import absolute_import, unicode_literals

import ast
import click
import re
from email.parser import Parser

# the file line is
# File "/var/django/idsapi/dev/django/idsapi/.ve/lib/python2.6/site-packages/httplib2/__init__.py", line 890, in connect
file_line_re = re.compile(r'''\ \ File              # start of line
                          \ "(?P<path>[^"]+)",      # the file path
                          \ line\ (?P<line_no>\d+), # the line number
                          \ in\ (?P<function>\w+)   # function/method name''',
                          re.VERBOSE)


def find_line_matching(lines, re_string, start_line=0):
    line_re = re.compile(re_string)
    for i, line in enumerate(lines):
        if i < start_line:
            continue
        if line_re.search(line):
            return i
    return None


class ErrorParser(object):

    def __init__(self, msg_file):
        self.msg_file = msg_file
        self.parse_email()

    def parse_email(self):
        self.parsed_email = Parser().parse(self.msg_file)
        email_parts = [p for p in self.parsed_email.walk()]
        if len(email_parts) > 1:
            raise Exception("unexpected parts to email %s" % self.msg_file)
        self.body = email_parts[0].get_payload()
        traceback, request = self.body.split("\n\n\n", 1)
        self.parse_traceback(traceback)
        self.parse_request(request)

    def parse_traceback(self, traceback):
        tb_lines = traceback.split("\n")
        self.one_line_error = tb_lines[-1]
        matches = file_line_re.match(tb_lines[-4])
        self.tb_final_path = matches.group("path")
        self.tb_final_line_no = matches.group("line_no")
        self.tb_final_function = matches.group("function")

    def parse_request(self, request):
        request_lines = request.split("\n")
        self.extract_meta(request_lines)

    def extract_meta(self, request_lines):
        meta_start = find_line_matching(request_lines, r'^META')
        meta_end = find_line_matching(request_lines, r'\}>$') + 1
        meta_lines = [l for l in request_lines[meta_start:meta_end] if not l.endswith(">,")]
        meta_text = "\n".join(meta_lines)[5:-1]
        self.meta = ast.literal_eval(meta_text)

    def assemble_output(self, max_len, server_name, path, query):
        bits = []
        if server_name:
            bits.append(self.meta["SERVER_NAME"])
        if path:
            bits.append(self.meta["PATH_INFO"])
        if query:
            bits.append(self.meta["QUERY_STRING"])
        bits.append(self.one_line_error)
        out = " ".join(bits)
        if max_len > 0:
            out = out[:max_len]
        return out

"""    --max-len=LEN     Maximum length of returned string [default: 80]
    -s --server-name  Include the URL server name
    -p --path         Include the URL path
    -q --query        Include the URL query string"""


@click.command()
@click.option('--max-len', '-m', default=80, help='Maximum length of returned string')
@click.option('--server-name', '-s', is_flag=True, help='Include the URL server name')
@click.option('--path', '-p', is_flag=True, help='Include the URL path')
@click.option('--query', '-q', is_flag=True, help='Include the URL query string')
@click.argument('files', nargs=-1, type=click.File(mode="rb"))
def main(files, max_len, server_name, path, query):
    """Extracts details of errors from Django error emails"""
    for msg_file in files:
        parser = ErrorParser(msg_file)
        click.echo(parser.assemble_output(max_len, server_name, path, query))
