import flet as ft
from views import productos_list_view, producto_create_view, producto_edit_view

def main(page: ft.Page):
    page.title = "CRUD Productos"

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(productos_list_view(page))
        elif page.route == "/create":
            page.views.append(producto_create_view(page))
        elif page.route.startswith("/edit/"):
            # ruta: /edit/123
            try:
                id_str = page.route.split("/edit/")[1]
                prod_id = int(id_str)
            except Exception:
                page.snack_bar = ft.SnackBar(ft.Text("ID inválido en la URL"))
                page.snack_bar.open = True
                page.go("/")
                return
            page.views.append(producto_edit_view(page, prod_id))
        page.update()

    page.on_route_change = route_change
    # inicializar ruta (usa la ruta actual si existe, sino "/")
    page.go(page.route or "/")

if __name__ == "__main__":
    ft.app(target=main)
