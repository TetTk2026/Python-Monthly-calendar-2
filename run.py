from wsgiref.simple_server import make_server

from monthly_calendar.web import app


if __name__ == "__main__":
    host, port = "127.0.0.1", 8000
    print(f"Serving on http://{host}:{port}")
    with make_server(host, port, app) as server:
        server.serve_forever()
