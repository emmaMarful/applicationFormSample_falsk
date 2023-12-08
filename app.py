from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import backend as credentials
from flask_mail import Mail, Message


app = Flask(__name__)

# a dictionary that holds  data in the flask instance
app.config.update(
    SECRET_KEY=credentials.secret(),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.db',
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=credentials.username(),
    MAIL_PASSWORD=credentials.password()
)

db = SQLAlchemy(app)
mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        print(f"{first_name}, {last_name}, {email}, {date}, {occupation}")

        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)

        db.session.add(form)
        db.session.commit()

        message_body = f"Thank you for your submission, {first_name} \n" \
                       f"Here are your data: \n {first_name} \n {last_name}" \
                       f"\n {date} \n Thank you!"

        message = Message(subject="New fom submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)

        # send email with the MAIL instance .send
        mail.send(message)

        flash("Your form was submitted successfully!", "success ")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
