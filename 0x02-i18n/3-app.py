#!/usr/bin/env python3
"""
Basic flask app for
Internalization and localization
"""
from flask import Flask, request, render_template
from flask_babel import Babel, _
from typing import Union


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


@babel.localeselector
def get_locale() -> Union[str, None]:
    """Select language translation based on locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', methods=['GET'])
def simple_route() -> str:
    """A simple route"""
    home_title = 'Welcome to Holberton'
    home_header = 'Hello world!'
    return render_template(
        '3-index.html',
        home_title=home_title,
        home_header=home_header
    )


if __name__ == '__main__':
    app.run()
