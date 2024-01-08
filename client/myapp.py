from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'ape lu suuu'

# coustomers pages

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        api_url = 'http://127.0.0.1:3000/customers-login'
        api_data = {'email': email, 'password': password}
        response = requests.post(api_url, data=api_data)

        if response.status_code == 200:
            # Assuming the API returns a JSON response
            api_response = response.json()

            # Continue with the rest of your logic
            session['customer_is_logged_in'] = True
            session['customer_id'] = api_response['values']['data']['id']
            session['customer_name'] = api_response['values']['data']['name']
            session['customer_phone'] = api_response['values']['data']['phone']
            session['customer_email'] = api_response['values']['data']['email']
            return redirect(url_for('index'))

    if session.get('customer_is_logged_in'):
        return redirect(url_for('index'))

    return render_template('/login.html')

@app.route("/daftar", methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('kontact_name_add')
        email = request.form.get('kontact_email_add')
        phone = request.form.get('kontact_phone_add')
        password = request.form.get('kontact_password_add')
        
        api_url = 'http://127.0.0.1:3000/customers-signIn'
        api_data = {'kontact_name_add': name, 'kontact_email_add': email,'kontact_phone_add': phone , 'kontact_password_add': password}
        response = requests.post(api_url, data=api_data)
        if response.status_code == 200:
            return redirect(url_for('login'))

    return render_template('/sign-in.html')

@app.route("/")
@app.route("/index")
def index():
    return render_template('/index.html')

@app.route("/products")
def product():
    return render_template('/product.html')



# admin pages

@app.route("/admin/login", methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST' and 'login_name' in request.form and 'login_password' in request.form:
        name = request.form['login_name']
        password = request.form['login_password']

        api_url = 'http://127.0.0.1:3000/login'
        api_data = {'name': name, 'password': password}
        response = requests.post(api_url, data=api_data)

        if response.status_code == 200:
            # Assuming the API returns a JSON response
            api_response = response.json()
            session['token_access'] = api_response['values']['token_access']
            session['token_refresh'] = api_response['values']['token_refresh']

            # Continue with the rest of your logic
            session['is_logged_in'] = True
            session['username'] = api_response['values']['data']['name']
            return redirect(url_for('adminDashboard'))

    if session.get('is_logged_in'):
        return redirect(url_for('adminDashboard'))


    return render_template('/admin/login.html')

@app.route('/admin/logout')
def adminLogout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    session.pop('token_access', None)
    session.pop('token_refresh', None)

    return redirect(url_for('adminLogin'))

@app.route("/admin/")
@app.route("/admin/dashboard")
def adminDashboard():
    if 'is_logged_in' in session:
        return render_template('/admin/dashboard.html')
    else:
        return redirect(url_for('adminLogin'))

@app.route("/admin/products")
def adminProducts():
    if 'is_logged_in' in session:
        return render_template('/admin/products.html')
    else:
        return redirect(url_for('adminLogin'))

@app.route("/admin/customers")
def adminCustomers():
    if 'is_logged_in' in session:
        return render_template('/admin/customers.html')
    else:
        return redirect(url_for('adminLogin'))

@app.route("/admin/contacts")
def adminContacts():
    if 'is_logged_in' in session:
        return render_template('/admin/contact.html')
    else:
        return redirect(url_for('adminLogin'))

if __name__ == "__main__":
    app.run(debug=True)