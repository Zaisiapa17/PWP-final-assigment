from app import app
from app.controller import users
from app.controller import todos
from app.controller import product_brands

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




if __name__ == '__main__':
    app.run()