from flask import (
    Flask,
    url_for,
    render_template,
    redirect
)
from forms import ContactForm, SignupForm


app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Standard `contact` form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "contact.jinja2",
        form=form,
        template="form-template",
        title="Contact Form"
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """User sign-up form for account creation."""
    form = SignupForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "signup.jinja2",
        form=form,
        template="form-template",
        title="Signup Form"
    )


@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        template="home-template",
        title="Flask-WTF tutorial"
    )


@app.route("/success", methods=["GET", "POST"])
def success():
    """Generic success page upon form submission."""
    return render_template(
        "success.jinja2",
        template="success-template"
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)