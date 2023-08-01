#!/usr/bin/env python3
"""
Basic flask app for
Internalization and localization
"""
from flask import Flask, g,  request, render_template
from flask_babel import Babel, _
from typing import Dict, Union


# users details
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# configure app
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

# instantiate Babel instance
babel = Babel(app)


@babel.localeselector
def get_user() -> Union[Dict[int, Dict[str, Union[str, None]]], None]:
    """Get user with id"""
    req_user = request.args.get('login_as')
    if not req_user:
        return None
    # get user
    return users.get(int(req_user))


@app.before_request
def before_request() -> None:
    """Runs before every request"""
    g.user = get_user()


@babel.localeselector
def get_locale() -> Union[str, None]:
    """Select language translation based on locale"""
    # get language from url parameters
    req_lang = request.args.get('locale')

    if req_lang and req_lang in app.config['LANGUAGES']:
        return req_lang
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', methods=['GET'])
def simple_route() -> str:
    """A simple route"""
    home_title = 'Welcome to Holberton'
    home_header = 'Hello world!'
    return render_template(
        '5-index.html',
        home_title=home_title,
        home_header=home_header
    )


if __name__ == '__main__':
    app.run()
