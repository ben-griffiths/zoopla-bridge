import json

from flask.wrappers import Response


class PrefixMiddleware(object):
    def __init__(self, app, prefix=""):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"].startswith(self.prefix):
            environ["PATH_INFO"] = environ["PATH_INFO"][len(self.prefix) :]
            environ["SCRIPT_NAME"] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response("404", [("Content-Type", "text/plain")])
            return ["This url does not belong to the app.".encode()]


class JsonResponse(Response):
    def __init__(self, *args, **kwargs):
        kwargs["mimetype"] = "application/json"
        super().__init__(
            json.dumps(args[0], default=json_serializer), *args[1:], **kwargs
        )


def get(func):
    return [func, "GET"]


def put(func):
    return [func, "PUT"]


def post(func):
    return [func, "POST"]


def map_url_rules(app, rules):
    for url, view_funcs in rules.items():
        for view_func in view_funcs:
            func, method = view_func
            app.add_url_rule(url, view_func=func, methods=[method])


def json_serializer(obj):
    import datetime
    from uuid import UUID

    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, dict):
        return str(obj)
    raise TypeError("Not sure how to serialize %s" % (obj,))
