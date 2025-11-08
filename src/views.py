import flet as ft
from db import fetch_all_productos, fetch_producto, insert_producto, update_producto, delete_producto
from models import Producto

def productos_list_view(page: ft.Page) -> ft.View:
    def cargar_productos():
        rows = []
        for row in fetch_all_productos():
            producto = Producto.from_row(row)
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(producto.id))),
                        ft.DataCell(ft.Text(producto.nombre)),
                        ft.DataCell(ft.Text(f"{producto.precio:.2f}")),
                        ft.DataCell(ft.Text(str(producto.cantidad))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, pid=producto.id: page.go(f"/edit/{pid}")),
                                ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, pid=producto.id: eliminar_producto(pid))
                            ], spacing=10)
                        )
                    ]
                )
            )
        productos_table.rows = rows
        page.update()

    def eliminar_producto(pid):
        try:
            delete_producto(pid)
            page.snack_bar = ft.SnackBar(ft.Text("Producto eliminado"))
            page.snack_bar.open = True
            cargar_productos()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
        page.update()

    productos_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )

    header = ft.Row([
        ft.Text("Productos", size=24),
        ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e: page.go("/create")),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    cargar_productos()

    return ft.View(
        "/",
        controls=[
            ft.Column([header, productos_table], tight=True)
        ]
    )

def producto_create_view(page: ft.Page) -> ft.View:
    nombre_field = ft.TextField(label="Nombre", width=400)
    precio_field = ft.TextField(label="Precio", width=200)
    cantidad_field = ft.TextField(label="Cantidad", width=200)

    def agregar_producto(e):
        try:
            nombre = nombre_field.value.strip()
            precio = float(precio_field.value)
            cantidad = int(cantidad_field.value)
            if not nombre:
                raise ValueError("El nombre no puede estar vacío")
            insert_producto(nombre, precio, cantidad)
            page.snack_bar = ft.SnackBar(ft.Text("Producto creado"))
            page.snack_bar.open = True
            page.go("/")  # volver a la lista
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
            page.update()

    form = ft.Column([
        ft.Text("Crear producto", size=20),
        nombre_field,
        precio_field,
        cantidad_field,
        ft.Row([
            ft.ElevatedButton("Crear", on_click=agregar_producto),
            ft.TextButton("Cancelar", on_click=lambda e: page.go("/"))
        ], spacing=10)
    ], spacing=10)

    return ft.View(
        "/create",
        controls=[form]
    )

def producto_edit_view(page: ft.Page, prod_id: int) -> ft.View:
    row = fetch_producto(prod_id)
    if not row:
        # si no existe el producto, mostrar mensaje y regresar a lista
        page.snack_bar = ft.SnackBar(ft.Text("Producto no encontrado"))
        page.snack_bar.open = True
        page.go("/")
        return ft.View("/edit", controls=[ft.Text("Redirigiendo...")])

    producto = Producto.from_row(row)

    nombre_field = ft.TextField(label="Nombre", value=producto.nombre, width=400)
    precio_field = ft.TextField(label="Precio", value=str(producto.precio), width=200)
    cantidad_field = ft.TextField(label="Cantidad", value=str(producto.cantidad), width=200)

    def guardar(e):
        try:
            nombre = nombre_field.value.strip()
            precio = float(precio_field.value)
            cantidad = int(cantidad_field.value)
            if not nombre:
                raise ValueError("El nombre no puede estar vacío")
            update_producto(prod_id, nombre, precio, cantidad)
            page.snack_bar = ft.SnackBar(ft.Text("Producto actualizado"))
            page.snack_bar.open = True
            page.go("/")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
            page.update()

    def eliminar(e):
        try:
            delete_producto(prod_id)
            page.snack_bar = ft.SnackBar(ft.Text("Producto eliminado"))
            page.snack_bar.open = True
            page.go("/")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
            page.update()

    form = ft.Column([
        ft.Text(f"Editar producto #{producto.id}", size=20),
        nombre_field,
        precio_field,
        cantidad_field,
        ft.Row([
            ft.ElevatedButton("Guardar cambios", on_click=guardar),
            ft.FilledTonalButton("Eliminar", on_click=eliminar),
            ft.TextButton("Cancelar", on_click=lambda e: page.go("/"))
        ], spacing=10)
    ], spacing=10)

    return ft.View(
        f"/edit/{prod_id}",
        controls=[form]
    )
