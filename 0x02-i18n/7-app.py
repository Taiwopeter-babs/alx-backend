#!/usr/bin/env python3
"""
Basic flask app for
Internalization and localization
"""
from flask import Flask, g, make_response, request, render_template
from flask_babel import Babel, _
import pytz
from typing import Any, Dict, Union


# users details
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def parse_language_header(header_str: str) -> str:
    """Processes the Accept-Language header"""
    first_split = header_str.split(',')

    # check if first preferred language needs parsing
    if '-' not in first_split[0]:
        return first_split[0]

    # get all languages
    languages = [lang for lang in first_split if ';' in lang]

    # choose the first language
    preferred_lang = languages[0].rsplit(';')[0]
    return preferred_lang


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
    user_locale = g.user.get('locale')

    # get language header
    req_lang_header = request.headers.get('Accept-Language')

    if req_lang and req_lang in app.config['LANGUAGES']:
        return req_lang

    # get locale from user settings
    if user_locale and user_locale in app.config['LANGUAGES']:
        return user_locale

    # get locale from header
    if req_lang_header:
        return parse_language_header(req_lang_header)

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> Union[str, None]:
    """Get timezone of user"""
    timezone_to_process: Union[str, None]

    # get timezone from url params
    req_timezone = request.args.get('timezone')
    # get timezone from user settings
    user_timezone = g.user.get('timezone')

    # verify timezone
    if req_timezone or user_timezone:
        if req_timezone:
            timezone_to_process = req_timezone
        else:
            timezone_to_process = user_timezone
    else:
        timezone_to_process = app.config['BABEL_DEFAULT_TIMEZONE']

    try:
        return_timezone = pytz.timezone(timezone_to_process)
    except pytz.exceptions.UnknownTimeZoneError:
        return None
    else:
        return return_timezone.zone


@app.route('/', methods=['GET'])
def simple_route() -> str:
    """A simple route"""
    home_title = 'Welcome to Holberton'
    home_header = 'Hello world!'
    return render_template(
        '7-index.html',
        home_title=home_title,
        home_header=home_header
    )


if __name__ == '__main__':
    app.run()
