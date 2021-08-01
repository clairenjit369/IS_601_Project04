"""Route declaration."""
from flask import Flask
from flask import current_app as app
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home():
    """Landing page."""
    nav = [
        {'name': 'Home', 'url': 'https://example.com/1'},
        {'name': 'About', 'url': 'https://example.com/2'},
        {'name': 'Pics', 'url': 'https://example.com/3'}
    ]
    return render_template(
        'home.html',
        nav=nav,
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja.",
        status={'active': True}
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
