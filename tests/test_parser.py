from extract_django_error.cli import ErrorEmailParser

traceback_text = """Traceback (most recent call last):

  File "/var/django/idsapi/dev/django/idsapi/.ve/lib/python2.6/site-packages/django/core/handlers/base.py", line 109, in get_response
    response = callback(request, *callback_args, **callback_kwargs)

  File "/var/django/idsapi/dev/django/idsapi/.ve/lib/python2.6/site-packages/django/views/generic/base.py", line 48, in view
    return self.dispatch(request, *args, **kwargs)

  File "/var/django/idsapi/dev/django/idsapi/.ve/lib/python2.6/site-packages/django/views/decorators/csrf.py", line 77, in wrapped_view
    return view_func(*args, **kwargs)

  File "/var/django/idsapi/dev/django/idsapi/.ve/lib/python2.6/site-packages/djangorestframework/views.py", line 133, in dispatch
    response_obj = handler(request, *args, **kwargs)

  File "/var/django/idsapi/dev/django/idsapi/openapi/views.py", line 183, in get
    return {'results': self.build_response()[0]}

  File "/var/django/idsapi/dev/django/idsapi/openapi/views.py", line 104, in build_response
    self.search_response, self.solr_query = self.query.execute()

  File "/var/django/idsapi/dev/django/idsapi/openapi/search_builder.py", line 167, in execute
    return self.si_query.execute(), solr_query

  File "/var/django/idsapi/dev/django/idsapi/.ve/src/sunburnt/sunburnt/search.py", line 634, in execute
    result = self.interface.search(**self.options())

  File "/var/django/idsapi/dev/django/idsapi/.ve/src/sunburnt/sunburnt/sunburnt.py", line 211, in search
    return self.schema.parse_response(self.conn.select(params))

  File "/var/django/idsapi/dev/django/idsapi/.ve/src/sunburnt/sunburnt/schema.py", line 533, in parse_response
    return SolrResponse.from_json(self, msg)

  File "/var/django/idsapi/dev/django/idsapi/.ve/src/sunburnt/sunburnt/schema.py", line 747, in from_json
    doc = json.loads(jsonmsg)

  File "/usr/lib/python2.6/json/__init__.py", line 307, in loads
    return _default_decoder.decode(s)

  File "/usr/lib/python2.6/json/decoder.py", line 319, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())

  File "/usr/lib/python2.6/json/decoder.py", line 338, in raw_decode
    raise ValueError("No JSON object could be decoded")

ValueError: No JSON object could be decoded"""


def test_parser_parse_traceback():
    eep = ErrorEmailParser()
    eep.parse_traceback(traceback_text)
    assert eep.one_line_error == "ValueError: No JSON object could be decoded"
