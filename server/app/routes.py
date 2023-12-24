from app import app
from app.controller import product_brands
from app.controller import product_catalogs
from app.controller import users
from app.controller import todos
from app.controller import customers

@app.route('/')
@app.route('/index')
def home():
    return "Hello, world!"

@app.route('/login', methods=['POST'])
def login():
    return users.login()

@app.route('/refresh', methods=['POST'])
def refresh():
    return users.refresh()



################ users routes
@app.route('/users', methods=['GET'])
def getUsers():
    return users.getAllusers()

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    return users.getUserById(id)

@app.route('/users', methods=['POST'])
def addUser():
    return users.insertUser()

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    return users.updateUser(id)

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    return users.deleteUser(id)



################ todo routes
@app.route('/todo', methods=['GET'])
def getTodos():
    return todos.index()

@app.route('/todo/<id>', methods=['GET'])
def getTodo(id):
    return todos.getTodoById(id)

@app.route('/todo', methods=['POST'])
def addTodos():
    return todos.insertTodo()

@app.route('/todo/<id>', methods=['PUT'])
def updateTodo(id):
    return todos.updateTodo(id)

@app.route('/todo/<id>', methods=['DELETE'])
def deleteTodo(id):
    return todos.deleteTodo(id)



################ product-brands routes
@app.route('/product-brands', methods=['GET'])
def getProductBrands():
    return product_brands.getAllProductBrands()

@app.route('/product-brands/<id>', methods=['GET'])
def getProductBrand(id):
    return product_brands.getProductBrandById(id)

@app.route('/product-brands', methods=['POST'])
def addProductBrand():
    return product_brands.insertProductBrand()

@app.route('/product-brands/<id>', methods=['PUT'])
def updateProductBrand(id):
    return product_brands.updateProductBrand(id)

@app.route('/product-brands/<id>', methods=['DELETE'])
def deleteProductBrand(id):
    return product_brands.deleteProductBrand(id)



################ product-catalogs routes
@app.route('/product-catalogs', methods=['GET'])
def getProductcatalogs():
    return product_catalogs.getAllProductCatalogs()

@app.route('/admin/product-catalogs', methods=['GET'])
def getProductcatalogsAdmin():
    return product_catalogs.getAllProductCatalogsAdmin()

@app.route('/product-catalogs/<id>', methods=['GET'])
def getProductcatalog(id):
    return product_catalogs.getProductCatalogCatalogById(id)

@app.route('/product-catalogs', methods=['POST'])
def addProductcatalog():
    return product_catalogs.insertProductCatalog()

@app.route('/product-catalogs/<id>', methods=['PUT'])
def updateProductcatalog(id):
    return product_catalogs.updateProductCatalog(id)

@app.route('/product-catalogs/<id>', methods=['DELETE'])
def deleteProductcatalog(id):
    return product_catalogs.deleteProductCatalog(id)



################ customer routes
@app.route('/customers', methods=['GET'])
def getCustomers():
    return customers.getAllCustomers()

@app.route('/customers/<id>', methods=['GET'])
def getCustomer(id):
    return customers.getCustomerById(id)

@app.route('/customers', methods=['POST'])
def addCustomer():
    return customers.insertCustomer()

@app.route('/customers/<id>', methods=['PUT'])
def updateCustomer(id):
    return customers.updateCustomer(id)

@app.route('/customers/<id>', methods=['DELETE'])
def deleteCustomer(id):
    return customers.deleteCustomer(id)




if __name__ == '__main__':
    app.run()