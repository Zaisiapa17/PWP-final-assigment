from flask import Flask, render_template

app = Flask(__name__)

@app.route("/login")
def login():
    return render_template('/login.html')

@app.route("/")
@app.route("/index")
def index():
    return render_template('/index.html')

@app.route("/products")
def product():
    return render_template('/product.html')

if __name__ == "__main__":
    app.run(debug=True)