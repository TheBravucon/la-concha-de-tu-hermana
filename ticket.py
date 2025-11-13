import pandas as pd
import datetime

def crear_ticket(carrito):
    df = pd.DataFrame(carrito)
    df["subtotal"] = df["precio"] * df["cantidad"]
    total = df["subtotal"].sum()

    fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"ticket_{fecha}.csv"

    df.loc[len(df.index)] = ["", "", "", f"TOTAL: ${total:.2f}"]
    df.to_csv(nombre_archivo, index=False, encoding="utf-8-sig")

    print(f"Ticket generado: {nombre_archivo}")
    return nombre_archivo, total
