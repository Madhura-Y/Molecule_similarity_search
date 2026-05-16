from flask import Flask, render_template, request, jsonify
from search import search

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def molecule_search():

    data = request.get_json()

    query = data.get("query")

    try:
        results = search(query)

        return jsonify({
            "status": "success",
            "results": results
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)