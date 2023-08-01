#!/usr/bin/env python3
"""
Basic flask app for
Internalization and localization
"""
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/', methods=['GET'])
def simple_route() -> str:
    """A simple route"""
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run()
