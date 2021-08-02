from flask import Flask

# Using a development configuration
app = Flask(__name__)
app.config.from_object('config.DevConfig')


@app.route("/")
def home():
    message = 'Configurations:' + \
              ' SECRET_KEY: ' + str(app.config.get('SECRET_KEY')) + \
              ' SESSION_COOKIE_NAME: ' + str(app.config.get('SESSION_COOKIE_NAME'))
    return message


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
