import datetime

import pandas as pd

EXCEL_COLUMNS = ['Id', 'Nombre de producto', 'Precio', 'Cantidad', 'Subtotal']


def crear_ticket(carrito):
    data = []
    total = 0.0
    for producto in carrito:
        id = producto['id']
        nombre = producto['nombre']
        precio = producto['precio']
        cantidad = producto['cantidad']
        subtotal = precio * cantidad
        total += subtotal
        data.append((id, nombre, f'$ {precio:.2f}', cantidad, f'$ {subtotal:.2f}'))

    df = pd.DataFrame(data, columns=EXCEL_COLUMNS)

    fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"ticket_{fecha}.xlsx"

    df.loc[len(carrito), 'Total'] = f"$ {total:.2f}"
    df.to_excel(nombre_archivo, index=False, sheet_name='Sheet1')

    print(f"Ticket generado: {nombre_archivo}")
    return nombre_archivo, total
