#!/usr/bin/env python3
from flask import Flask, request


app = Flask('TestServer')


@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def catchall_get_endpoint(path: str):
    p = f"{path.replace('/', '.')}.{request.method.lower()}"

    if "resources/" not in path:
        if request.args.get('key') != 'test-key-ftw':
            return '{"status": false, "message": "Invalid API key"}\n', 403

    try:
        with app.open_resource(f'response/{p}') as f:
            return f.read()
    except FileNotFoundError:
        return '{"status": false, "message": "Test file not found"}\n', 404


if __name__ == "__main__":
    app.run(host='localhost', port=8000)
