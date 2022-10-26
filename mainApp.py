from flask import Flask, jsonify, request

app = Flask(__name__)

# Importamos la lista de productos para tener acceso a ella con nuestra REST API
from products import products

# La función de esta ruta es acceder a la lista de productos creada anteriormente y retornar un archivo json
@app.route('/products')
def getProducts():
    return jsonify(products)

# Cumple con la función de obtener la información de un solo producto, para mostrar en consola la información
# Es decir, consultar la información de un producto dentro de la lista
@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]

# La condición es para que el usuario al consultar un la información de un producto, si este existe dentro de la lista, lo retorna, si no, mostrará un mensaje
    if (len(productsFound) > 0):
        return jsonify({"product": productsFound[0]})
    return jsonify({"Message": "Product not found"}) 

# Si deseamos añadir un producto, creamos una ruta con el método post, lo debemos especificar, ya que de lo contrario, el lenguaje dejará por defecto el método get
@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    return jsonify({'message': "product added succesfully", "products":products})

# Ahora vamos a crear una ruta donde utilizaremos el método PUT, que nos permite actualizar algo dentro de la lista, en este caso, un producto
@app.route('/products/<string:product_name>', methods=['PUT'])
def updateProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message": "Product Updated",
            "product": productFound[0]
        })
    return jsonify({"message": "Product Not Found"})

# Creamos una ruta más pero utilizamos el método delete, que nos permite eliminar un producto en este caso
@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productsFound=[product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            "message": "Product deleted succesfully",
            "products": products
        })
    return jsonify({"message": "product not found"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)