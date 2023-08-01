#!/usr/bin/env python3
"""
Basic flask app for
Internalization and localization
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Configuration class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_LOCALE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

# instantiate Babel instance
babel = Babel(app)


@app.route('/', methods=['GET'])
def simple_route() -> str:
    """A simple route"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()
