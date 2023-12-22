from flask import Flask, render_template

app = Flask(__name__)

# coustomers pages

@app.route("/login")
def login():
    return render_template('/login.html')

@app.route("/daftar")
def signIn():
    return render_template('/sign-in.html')

@app.route("/")
@app.route("/index")
def index():
    return render_template('/index.html')

@app.route("/products")
def product():
    return render_template('/product.html')



# admin pages

@app.route("/admin/login")
def adminLogin():
    return render_template('/admin/login.html')

@app.route("/admin/")
@app.route("/admin/dashboard")
def adminDashboard():
    return render_template('/admin/dashboard.html')

@app.route("/admin/products")
def adminProducts():
    return render_template('/admin/products.html')

@app.route("/admin/customers")
def adminCustomers():
    return render_template('/admin/customers.html')

@app.route("/admin/contacts")
def adminContacts():
    return render_template('/admin/contact.html')

if __name__ == "__main__":
    app.run(debug=True)