import flet as ft
from typing import Any
from app.views.nuevo_editar import formulario_nuevo_editar_producto
from app.services.transacciones_api_productos import create_product

async def products_view(page: ft.Page) -> ft.Control:
    
    def inicio_editar_producto(producto_existente):
        async def guardar_edicion(data_editada):
            try:
                print(f"Editando producto ID {data_editada.get('id')}")
                await actualizar_data()
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=ft.Colors.DANGER)

        dlg, open_, close = formulario_nuevo_editar_producto(
            page, 
            on_submit=guardar_edicion, 
            initial=producto_existente
        )
        open_()
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Ingreso")),
            ft.DataColumn(ft.Text("Min")),
            ft.DataColumn(ft.Text("Max")),
            ft.DataColumn(ft.Text("Acciones")), 
        ],
        rows=[]
    )
    def construir_filas(productos):
        filas = []
        for p in productos:
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.get("name", ""))),
                        ft.DataCell(ft.Text(str(p.get("quantity", 0)))),
                        ft.DataCell(ft.Text(p.get("ingreso_date", ""))),
                        ft.DataCell(ft.Text(str(p.get("min_stock", 0)))),
                        ft.DataCell(ft.Text(str(p.get("max_stock", 0)))),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color="blue",
                                on_click=lambda e, prod=p: inicio_editar_producto(prod)
                            )
                        ),
                    ]
                )
            )
        tabla.rows = filas
        page.update()
    async def actualizar_data():
        print("Actualizando tabla...")
        pass
    async def show_snackbar(page: ft.Page, title: str, message: str, bgcolor: str):
        page.snack_bar = ft.SnackBar(ft.Text(f"{title}: {message}"), bgcolor=bgcolor)
        page.snack_bar.open = True
        page.update()
    def inicio_new_producto(_e):
        async def crear_nuevo_producto(data: dict):
            try:
                await create_product(data)
                await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=ft.Colors.SUCCESS)
                await actualizar_data()
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=ft.Colors.DANGER)

        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto, initial=None)
        open_()
    btn_nuevo = ft.ElevatedButton("Nuevo producto", icon=ft.Icons.ADD, on_click=inicio_new_producto)
    total_text = ft.Text("Total de productos: 0", weight=ft.FontWeight.BOLD)
    return ft.Column(
        expand=True,
        controls=[
            btn_nuevo, 
            total_text, 
            ft.Container(content=tabla, padding=10)
        ]
    )