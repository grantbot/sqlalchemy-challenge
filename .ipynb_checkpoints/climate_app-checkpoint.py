from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hi. Available routes are as follows: /recipitation, /stations, /tobs"
    
    

if __name__ == "__main__":
    app.run(debug=True)
