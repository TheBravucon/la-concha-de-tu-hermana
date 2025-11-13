import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import productos
from ticket import crear_ticket
import usuarios

# Crear tablas necesarias
productos.crear_tabla()
usuarios.crear_tabla_usuarios()

# ==========================
# 🔐 Ventana de Login / Registro
# ==========================
def mostrar_login():
    login = ttk.Window("Login - Sistema de Ventas", "superhero")
    login.geometry("400x500")

    frame = ttk.Frame(login, padding=30)
    frame.pack(expand=True)

    modo = ttk.StringVar(value="login")

    def cambiar_modo():
        if modo.get() == "login":
            modo.set("registro")
            titulo.config(text="Crear Cuenta")
            boton_login.config(text="Registrarse")
        else:
            modo.set("login")
            titulo.config(text="Iniciar Sesión")
            boton_login.config(text="Iniciar Sesión")

    titulo = ttk.Label(frame, text="Iniciar Sesión", font=("Segoe UI", 20, "bold"))
    titulo.pack(pady=15)

    ttk.Label(frame, text="Email:").pack(anchor=W)
    email_var = ttk.StringVar()
    ttk.Entry(frame, textvariable=email_var, width=30).pack(pady=5)

    ttk.Label(frame, text="Contraseña:").pack(anchor=W)
    pass_var = ttk.StringVar()
    ttk.Entry(frame, textvariable=pass_var, width=30, show="*").pack(pady=5)

    ttk.Label(frame, text="Nombre:").pack(anchor=W)
    nombre_var = ttk.StringVar()
    ttk.Entry(frame, textvariable=nombre_var, width=30).pack(pady=5)

    ttk.Label(frame, text="Rol:").pack(anchor=W)
    rol_var = ttk.Combobox(frame, values=["cliente", "proveedor"], width=27, state="readonly")
    rol_var.set("cliente")
    rol_var.pack(pady=5)

    def procesar():
        email = email_var.get().strip()
        password = pass_var.get().strip()

        if modo.get() == "login":
            ok, data = usuarios.verificar_login(email, password)
            if ok:
                messagebox.showinfo("Bienvenido", f"Hola {data['nombre']} ({data['rol']})")
                login.destroy()
                mostrar_main(data)
            else:
                messagebox.showerror("Error", data)
        else:
            nombre = nombre_var.get().strip()
            rol = rol_var.get().strip()
            if not all([nombre, email, password, rol]):
                messagebox.showerror("Error", "Complete todos los campos")
                return
            ok, msg = usuarios.registrar_usuario(nombre, email, password, rol)
            if ok:
                messagebox.showinfo("Éxito", msg)
                cambiar_modo()
            else:
                messagebox.showerror("Error", msg)

    boton_login = ttk.Button(frame, text="Iniciar Sesión", bootstyle=PRIMARY, command=procesar)
    boton_login.pack(pady=10)

    ttk.Button(frame, text="Cambiar a Registro / Login", bootstyle=SECONDARY, command=cambiar_modo).pack()

    login.mainloop()

# ==========================
# 🧾 Ventana principal (ya tienes esta parte)
# ==========================
def mostrar_main(usuario):
    app = ttk.Window("Sistema de Ventas", "superhero")
    app.geometry("1100x700")

    carrito = []
    editando_id = None

    nombre_var = ttk.StringVar()
    precio_var = ttk.DoubleVar()
    cantidad_var = ttk.IntVar()

    header = ttk.Label(app, text=f"🛍️ Bienvenido {usuario['nombre']} ({usuario['rol']})",
                       font=("Segoe UI", 20, "bold"), bootstyle=PRIMARY)
    header.pack(pady=20)

    # --- Frame formulario de carrito ---
    frame_form = ttk.Labelframe(app, text="Agregar producto al carrito", padding=20)
    frame_form.pack(padx=20, pady=10, fill=X)

    ttk.Label(frame_form, text="Nombre del producto:").grid(row=0, column=0, sticky=W)
    ttk.Entry(frame_form, textvariable=nombre_var, width=40).grid(row=0, column=1)

    ttk.Label(frame_form, text="Precio ($):").grid(row=1, column=0, sticky=W)
    ttk.Entry(frame_form, textvariable=precio_var, width=20).grid(row=1, column=1, sticky=W)

    ttk.Label(frame_form, text="Cantidad:").grid(row=2, column=0, sticky=W)
    ttk.Entry(frame_form, textvariable=cantidad_var, width=20).grid(row=2, column=1, sticky=W)

    def limpiar_campos():
        nonlocal editando_id
        nombre_var.set("")
        precio_var.set(0)
        cantidad_var.set(0)
        editando_id = None

    def agregar_o_actualizar():
        nonlocal editando_id
        nombre = nombre_var.get().strip()
        precio = precio_var.get()
        cantidad = cantidad_var.get()
        if not nombre or precio <= 0 or cantidad <= 0:
            messagebox.showerror("Error", "Complete todos los campos correctamente")
            return
        if editando_id is None:
            prod_id = len(carrito) + 1 if carrito else 1
            carrito.append({"id": prod_id, "nombre": nombre, "precio": precio, "cantidad": cantidad})
        else:
            for item in carrito:
                if item["id"] == editando_id:
                    item["nombre"], item["precio"], item["cantidad"] = nombre, precio, cantidad
                    break
            editando_id = None
        actualizar_tabla()
        limpiar_campos()

    ttk.Button(frame_form, text="Agregar / Actualizar", bootstyle=SUCCESS, command=agregar_o_actualizar)\
        .grid(row=3, column=0, columnspan=2, pady=10)

    # --- Tabla carrito ---
    frame_tabla = ttk.Labelframe(app, text="Carrito actual", padding=10)
    frame_tabla.pack(fill=BOTH, expand=True, padx=20, pady=10)

    columnas = ("ID", "Producto", "Precio", "Cantidad", "Subtotal", "Acciones")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", bootstyle=INFO)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor=CENTER, width=150)
    tabla.column("Acciones", width=200)
    tabla.pack(fill=BOTH, expand=True)

    total_label = ttk.Label(app, text="Total: $0.00", font=("Segoe UI", 14, "bold"))
    total_label.pack(pady=10)

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        total = 0
        for item in carrito:
            subtotal = item["precio"] * item["cantidad"]
            total += subtotal
            tabla.insert("", END, iid=item["id"], values=(item["id"], item["nombre"],
                        f"${item['precio']:.2f}", item["cantidad"], f"${subtotal:.2f}",
                        "🖊️ Editar   ❌ Borrar"))
        total_label.config(text=f"Total: ${total:.2f}")

    def editar_producto(item_id):
        nonlocal editando_id
        for item in carrito:
            if item["id"] == item_id:
                nombre_var.set(item["nombre"])
                precio_var.set(item["precio"])
                cantidad_var.set(item["cantidad"])
                editando_id = item_id
                break

    def borrar_producto(item_id):
        nonlocal carrito
        carrito = [p for p in carrito if p["id"] != item_id]
        actualizar_tabla()

    def on_tabla_click(event):
        selected = tabla.identify_row(event.y)
        if not selected:
            return
        col = tabla.identify_column(event.x)
        col_index = int(col.replace('#', '')) - 1
        if columnas[col_index] != "Acciones":
            return
        try:
            item_id = int(selected)
        except ValueError:
            return
        bbox = tabla.bbox(selected, column=col)
        if not bbox:
            return
        x, _, width, _ = bbox
        rel_x = event.x - x
        if rel_x <= width / 2:
            editar_producto(item_id)
        else:
            if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
                borrar_producto(item_id)

    tabla.bind("<Button-1>", on_tabla_click)

    def generar_ticket():
        if not carrito:
            messagebox.showerror("Error", "El carrito está vacío")
            return
        archivo, total = crear_ticket(carrito)
        messagebox.showinfo("Ticket generado", f"Archivo: {archivo}\nTotal: ${total:.2f}")
        carrito.clear()
        actualizar_tabla()

    ttk.Button(app, text="💾 Generar Ticket", bootstyle=PRIMARY, command=generar_ticket).pack(pady=20)

    # --- CRUD Usuarios ---
    def abrir_crud_usuarios():
        crud = ttk.Toplevel(app)
        crud.title("Gestión de Usuarios")
        crud.geometry("700x500")

        tabla_u = ttk.Treeview(crud, columns=("ID", "Nombre", "Email", "Rol"), show="headings")
        for col in ("ID", "Nombre", "Email", "Rol"):
            tabla_u.heading(col, text=col)
            tabla_u.column(col, anchor=CENTER)
        tabla_u.pack(fill=BOTH, expand=True, pady=10, padx=10)

        def actualizar_u():
            tabla_u.delete(*tabla_u.get_children())
            for u in usuarios.obtener_usuarios():
                tabla_u.insert("", END, values=u)

        def eliminar_u():
            sel = tabla_u.selection()
            if not sel:
                return
            item = tabla_u.item(sel)
            user_id = item["values"][0]
            if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
                usuarios.eliminar_usuario(user_id)
                actualizar_u()

        ttk.Button(crud, text="Eliminar Usuario", bootstyle=DANGER, command=eliminar_u).pack(pady=5)
        actualizar_u()

    ttk.Button(app, text="👥 Gestionar Clientes / Proveedores", bootstyle=INFO, command=abrir_crud_usuarios).pack(pady=10)
    app.mainloop()

# --- Inicio del programa ---
if __name__ == "__main__":
    mostrar_login()
