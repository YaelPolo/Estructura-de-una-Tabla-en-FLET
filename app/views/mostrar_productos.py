import flet as ft
from typing import Any
from app.services.transacciones_api_productos import listar_productos, get_product, create_product, update_product, delete_product
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos, Cards

def products_view(page: ft.page) -> ft.control:
        rows_data: list[dict[str, Any]] = []
        total_items = 0
        total_text = ft.Text("Total de productos: (cargando...)", style = Textos.H4)
        #Encabezados

        columnas = [
                ft.DataColumn(label=ft.Text("Nombre", style=Textos.H4)),
                ft.DataColumn(label=ft.Text("Cantidad", style=Textos.H4)),
                ft.DataColumn(label=ft.Text("Ingreso", style=Textos.H4)),
                ft.DataColumn(label=ft.Text("Min", style=Textos.H4)),
                ft.DataColumn(label=ft.Text("Max", style=Textos.H4)),
        ]

        #Se definen las filas de la tabla
        #Cada data.append agrega

        data = []
        data.append(
                ft.DataRow(
                        cells = [
                                ft.DataCell(ft.Text("Nombre1...")),
                                ft.DataCell(ft.Text("Cantidad1...")),
                                ft.DataCell(ft.Text("Ingreso1...")),
                                ft.DataCell(ft.Text("Min1...")),
                                ft.DataCell(ft.Text("Max1...")),
                        ]
                )
            )
        #Se crea la tabla con los encabezados(columnas) y los datos de prueba(data)
        tabla = ft.DataTable(
                columns = columnas,
                rows = data,
                width = 900,
                heading_row_height = 60,
                heading_row_color = Colors.BG,
                data_row_max_height = 60,
                data_row_min_height = 48,
        )

        return tabla