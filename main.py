from flask import Flask, render_template, request
import requests
import smtplib

app = Flask(__name__)

api_link = "https://api.npoint.io/2acba0b9f7eb78dec5af"
all_posts = requests.get(api_link).json()

OWN_EMAIL = "email@gmail.com"
OWN_PASSWORD = "somepassword"


@app.route('/')
def hello():
    return render_template('index.html', posts=all_posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:index>')
def post(index):
    requested_post = None
    for some_post in all_posts:
        if some_post["id"] == index:
            requested_post = some_post
            print(requested_post)
    return render_template("post.html", post=requested_post)


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=True)
