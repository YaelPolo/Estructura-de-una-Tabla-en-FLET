import flet as ft
from app.services.transacciones_api_productos import (
    create_product,
    listar_productos,
    update_product
)
from app.views.nuevo_editar import formulario_nuevo_editar_producto
from app.components.popup import show_popup
from app.components.error import show_snackbar

def products_view(page: ft.Page) -> ft.Control:
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Ingreso")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )
    async def actualizar_data():
        try:
            data = listar_productos(limit=500, offset=0)
            items = data.get("items", [])
            nuevas_filas = []
            for p in items:
                print("PRODUCTO:", p)  
                nuevas_filas.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(p.get("name", ""))),
                        ft.DataCell(ft.Text(str(p.get("quantity", "")))),
                        ft.DataCell(ft.Text(p.get("ingreso_date", ""))),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                on_click=lambda e, prod=p: abrir_formulario(prod)
                            )
                        ),
                    ])
                )
            tabla.rows = nuevas_filas
            page.update()
        except Exception as e:
            print("Error cargando tabla:", e)
    def abrir_formulario(producto_existente=None):
        print("ABRIENDO FORMULARIO CON:", producto_existente)
        async def procesar_datos(data_capturada: dict):
            try:
                print("DATOS RECIBIDOS:", data_capturada)
                if "id" in data_capturada:
                    print("EDITANDO PRODUCTO")
                    product_id = data_capturada["id"]
                    data_sin_id = data_capturada.copy()
                    del data_sin_id["id"]
                    update_product(product_id, data_sin_id)
                    await show_snackbar(page, "Éxito", "Producto actualizado.", bgcolor=ft.Colors.GREEN)
                else:
                    print("CREANDO PRODUCTO")
                    create_product(data_capturada)
                    await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=ft.Colors.GREEN)
                await actualizar_data()
            except Exception as ex:
                print("ERROR:", ex)
                await show_popup(page, "Error", str(ex))
        dlg, open_form, _ = formulario_nuevo_editar_producto(
            page,
            on_submit=procesar_datos,
            initial=producto_existente
        )
        open_form()
    btn_nuevo = ft.FilledButton(
        "Nuevo producto",
        icon=ft.Icons.ADD,
        on_click=lambda e: abrir_formulario()
    )
    page.run_task(actualizar_data)
    return ft.Column(
        expand=True,
        controls=[
            ft.Row(
                [
                    ft.Text("Inventario", size=25, weight="bold"),
                    btn_nuevo
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(),
            ft.Container(content=tabla, padding=10)
        ]
    )