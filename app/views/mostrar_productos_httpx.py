import flet as ft
from app.services.transacciones_api_productos import (
    create_product,
    listar_productos,
    update_product,
    delete_product
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
            ft.DataColumn(ft.Text("Min")),
            ft.DataColumn(ft.Text("Max")),
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
                        ft.DataCell(ft.Text(p.get("ingreso_date", "") or "")),
                        ft.DataCell(ft.Text(str(p.get("min_stock", "")))),
                        ft.DataCell(ft.Text(str(p.get("max_stock", "")))),
                        #### Se agrega para editar producto ###
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, p=p: inicio_editar_producto(p)),
                                    ft.IconButton(icon=ft.Icons.DELETE, tooltip="Borrar", on_click=lambda e, p=p: inicio_borrar_producto(p))
                                ]
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

    def inicio_editar_producto(p: dict):
        async def editar_producto(data: dict):
            try:
                data_sin_id = data.copy()
                if "id" in data_sin_id:
                    del data_sin_id["id"]
                update_product(p["id"], data_sin_id)
                close_()
                await show_snackbar(page, "Éxito", "Producto actualizado", bgcolor=ft.Colors.GREEN)
                await actualizar_data()
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=ft.Colors.RED)
                
        dlg, open_, close_ = formulario_nuevo_editar_producto(page, on_submit=editar_producto, initial=p)
        open_()

    ############# Borrar producto #############
    async def borrar_producto(p: dict):
        try:
            delete_product(p["id"])
            await show_snackbar(page, "Éxito", "Producto borrado", bgcolor=ft.Colors.GREEN)
            await actualizar_data()
        except Exception as ex:
            await show_snackbar(page, "Error", str(ex), bgcolor=ft.Colors.RED)

    def inicio_borrar_producto(p: dict):
        async def tarea():
            await borrar_producto(p)
        page.run_task(tarea)

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
            ft.Column(
                controls=[ft.Container(content=tabla, padding=10)],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        ]
    )