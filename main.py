from flask import Flask, render_template, request

from dialogflow import detect_intent

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    user_text = request.args.get("msg")
    bot_response = detect_intent(user_text)
    return bot_response


if __name__ == "__main__":
    app.run()
