"""
Rutas (vistas) de la Tienda Virtual.

Aquí se define la lógica que conecta las URLs con los templates HTML,
usando el archivo productos.json como única fuente de datos (no hay
base de datos en este taller).
"""

import json
import os

from flask import Blueprint, render_template, abort

# Un Blueprint permite organizar las rutas de forma modular.
main = Blueprint("main", __name__)

# Ruta absoluta al archivo JSON de productos.
# os.path.dirname(__file__) apunta a la carpeta app/, por eso el JSON
# debe vivir en app/data/productos.json
RUTA_PRODUCTOS = os.path.join(os.path.dirname(__file__), "data", "productos.json")


def cargar_productos():
    """Lee productos.json y retorna la lista de productos (lista de dicts)."""
  
    with open(RUTA_PRODUCTOS,"r", encoding="utf-8") as archivo:
        productos = json.load(archivo)

    return productos

def buscar_producto_por_sku(sku):
    """Busca un producto por su SKU dentro de la lista de productos. """
    
productos = cargar_productos()

    for producto in productos:
        if producto["sku"] == sku:
            return producto

    return None


@main.route("/")
def index():
    """Página principal: muestra el catálogo completo de productos."""
    productos = cargar_productos()

    return render_template("index.html", productos=productos)


@main.route("/producto/<sku>")
def detalle(sku):
    """Página de detalle de un producto específico, buscado por SKU."""
    producto = buscar_producto_por_sku(sku)

    if producto is None:
        abort(404)

    return render_template("detalle.html", producto=producto)
