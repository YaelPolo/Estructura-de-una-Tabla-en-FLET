import flet as ft
from app.views.mostrar_productos_httpx import products_view

def main(page: ft.Page):
    page.title = "Inventario de Productos"
    page.theme_mode = ft.ThemeMode.DARK
    page.add(products_view(page))
    
if __name__ == "__main__":
    ft.run(main)