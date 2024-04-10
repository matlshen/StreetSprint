from flask import Flask

app = Flask(__name__)

# Memebers API Route
@app.route("/members")
def members():
    return{"members": ["Memeber1", "Memeber2", "Memeber3"]}

if __name__ == "__main__":
    app.run(debug=True)