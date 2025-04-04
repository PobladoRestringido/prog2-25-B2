from flask import Flask, request

app = Flask(__name__)

inmuebles = {}


@app.route('/')
def hola():
    return 'Bienvenido a la API de inmuebles'


@app.route('/inmuebles', methods=['GET'])
def get_inmuebles():
    return list(inmuebles.keys()), 200


@app.route('/inmuebles/<id>', methods=['GET'])
def get_inmueble_id(id):
    try:
        return inmuebles[id], 200
    except KeyError:
        return f'Inmueble {id} No encontrado', 404


@app.route('/inmuebles/<id>', methods=['POST'])
def añadir_inmuebles(id):
    if id not in inmuebles:
        inmuebles[id] = request.args.get('value', '')
        return f'Inmueble{id} añadido', 200
    else:
        return f'Inmueble {id} ya existe', 409


if __name__ == '__main__':
    app.run(debug=True)
