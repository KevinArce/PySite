#We import
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#MySQL Connection. We added the parameters in orden to stablish a conecction with the DB.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'restaurante'

#We send it to MySQL (app contains all the information to "login" to the server)
mysql = MySQL(app)

#Now we initialize a Sesion
#Settings
app.secret_key = 'mysecretkey'

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('Index'))
    return render_template('login.html', error=error)

#We create a route to our index
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', cliente = data)

#Now we create a a route to our table and stablish a path to the browser so we can the page
@app.route('/add_cliente', methods=['POST'])
def add_client():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        direccion_cliente = request.form['direccion_cliente']
        telefono = request.form['telefono']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO restaurante.cliente(Nombre, direccion_cliente, telefono) VALUES ( %s, %s, %s)',
        (Nombre, direccion_cliente, telefono))
        mysql.connection.commit()
        flash('Client Added Successfully!')

        return redirect(url_for('Index'))

@app.route('/edit/<idCliente>')
def get_cliente(idCliente):
    cur = mysql.connect.cursor()
    cur.execute('SELECT * FROM cliente WHERE idCliente = %s',[idCliente])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-cliente.html',client = data[0])

@app.route('/update/<idCliente>', methods=['POST'])
def update_cliente(idCliente):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        direccion_cliente = request.form['direccion_cliente']
        telefono = request.form['telefono']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE cliente 
            SET Nombre = %s,
                direccion_cliente = %s,
                telefono = %s
                
            WHERE idCliente = %s
        """, (Nombre, direccion_cliente, telefono, idCliente))
        flash('Client Updated Successfully!')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:idCliente>', methods = ['POST','GET'])
def delete(idCliente):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cliente WHERE idCliente = {0}'.format(idCliente))
    mysql.connection.commit()
    flash('Client Removed Successfully')
    return redirect(url_for('Index'))

#We create a route to our index
@app.route('/entregapedidos')
def entrega():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM entregapedidos')
    data = cur.fetchall()
    print(data)
    return render_template('entregapedidos.html', entregapedidos = data)

#Now we create a a route to our table and stablish a path to the browser so we can the page
@app.route('/add_entregapedidos', methods=['POST'])
def add_entregapedidos():
    if request.method == 'POST':
        idempleado = request.form['idempleado']
        detallePedido = request.form['detallePedido']
        numero_mesa = request.form['numero_mesa']
        tiempoEntrega = request.form['tiempoEntrega']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO restaurante.entregapedidos(idempleado, detallePedido, numero_mesa, tiempoEntrega) VALUES (%s, %s, %s, %s)',
        (idempleado, detallePedido, numero_mesa, tiempoEntrega))
        mysql.connection.commit()
        flash('Pedido Added Successfully!')
        return redirect(url_for('entrega'))

@app.route('/editP/<idOrden>')
def get_entregapedidos(idOrden):
    cur = mysql.connect.cursor()
    cur.execute('SELECT * FROM entregapedidos WHERE idOrden = %s',[idOrden])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-entregapedido.html',entregapedido = data[0])

@app.route('/updateP/<idOrden>', methods=['POST'])
def update_entregapedidos(idOrden):
    if request.method == 'POST':
        idempleado = request.form['idempleado']
        detallepedido = request.form['detallepedido']
        tiempoEntrega = request.form['tiempoEntrega']
        numero_mesa = request.form['numero_mesa']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE entregapedidos 
            SET idempleado = %s,
                detallepedido = %s,
                tiempoEntrega = %s,
                numero_mesa = %s
            WHERE idOrden = %s
        """, (idempleado, detallepedido, tiempoEntrega, numero_mesa, idOrden))
        flash('Pedido Updated Successfully!')
        mysql.connection.commit()
        return redirect(url_for('entrega'))

@app.route('/deleteP/<string:idOrden>', methods = ['POST','GET'])
def deleteP(idOrden):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM entregapedidos WHERE idOrden = %s', [idOrden])
    mysql.connection.commit()
    flash('Pedido Removed Successfully')
    return redirect(url_for('entrega'))

if __name__ == '__main__':
  app.run(port = 3000, debug = True)
