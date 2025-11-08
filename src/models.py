class Producto:
    def __init__(self, id, nombre, precio, cantidad):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    @staticmethod
    def from_row(row):
        return Producto(row[0], row[1], row[2], row[3])
