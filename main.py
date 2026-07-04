from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🎓 Campus Buddy</h1>
    <h3>Website is running successfully 🚀</h3>
    <p>Created by Yuvaraj</p>
    """

if __name__ == "__main__":
    app.run(debug=True)