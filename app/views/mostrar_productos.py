import flet as ft
from typing import Any
from app.services.transacciones_api_productos import listar_productos
from app.styles.estilos import Colors, Textos, Cards, Buttons, Inputs

def products_view(page: ft.Page):
    rows_data:list[dict[str, Any]] = []
    total_items = 0
    total_text = ft.Text("Total de productos: (cargando...)", style=Textos.text)
    
    columnas=[
        ft.DataColumn(ft.Text("Nombre", style=Textos.text)),
        ft.DataColumn(ft.Text("Cantidad", style=Textos.text)),
        ft.DataColumn(ft.Text("Ingreso", style=Textos.text)),
        ft.DataColumn(ft.Text("Min", style=Textos.text)),
        ft.DataColumn(ft.Text("Max", style=Textos.text)),
    ]

    # Tabla inicial vacía
    tabla = ft.DataTable(
        columns=columnas,
        rows=[], 
        width=900,
        heading_row_height=60,
        heading_row_color=Colors.BG,
        data_row_max_height=60,
        data_row_min_height=48,
    )

    async def actualizar_data():
        nonlocal rows_data, total_items
        try:
            # Trae los registros reales de tu base de datos
            data = listar_productos(limit=500, offset=0)
            total_items = int(data.get("total", 0))
            total_text.value = f"Total de productos: {total_items}"
            rows_data = data.get("items", [])
            actualizar_filas()
        except Exception as e:
            print(f"Error al cargar DB: {e}")

    def actualizar_filas():
        nuevas_filas = []
        for p in rows_data:
            nuevas_filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(p.get("name", "")))),
                        ft.DataCell(ft.Text(str(p.get("quantity", "")))),
                        ft.DataCell(ft.Text(str(p.get("ingreso_date", "") or ""))),
                        ft.DataCell(ft.Text(str(p.get("min_stock", "")))),
                        ft.DataCell(ft.Text(str(p.get("max_stock", "")))),
                    ]
                )
            )
        tabla.rows = nuevas_filas
        page.update()

    page.run_task(actualizar_data)
    
    btn_nuevo = ft.ElevatedButton("Nuevo", bgcolor=Colors.BG, color="white")

    contenido = ft.Column(
        expand=True, 
        spacing=30,
        scroll=ft.ScrollMode.AUTO, 
        controls=[
            btn_nuevo,
            total_text,
            ft.Container(content=tabla) 
        ]
    )

    return contenido