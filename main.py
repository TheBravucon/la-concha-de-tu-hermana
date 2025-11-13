import tkinter
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import productos
import usuarios
from productos import actualizar_stock
from ticket import crear_ticket

# Crear tablas necesarias
productos.crear_tabla()
usuarios.crear_tabla_usuarios()


# ==========================
# 🔐 Ventana de Login / Registro
# ==========================
def mostrar_login(root):
    login = ttk.Toplevel(master=root)
    login.title("Sistema de Ventas")
    login.geometry("400x500")
    login.protocol("WM_DELETE_WINDOW", root.destroy)

    frame = ttk.Frame(login, padding=30)
    frame.pack(expand=True)

    modo = ttk.StringVar(value="registro")

    def ocultar_mostrar_campos():
        widgets = [nombre_label, nombre_entry, rol_label, rol_combo]
        for widget in widgets:
            if widget.winfo_viewable():
                widget.grid_remove()
            else:
                widget.grid()

    def cambiar_modo():
        if modo.get() == "login":
            modo.set("registro")
            titulo.config(text="Crear Cuenta")
            boton_login.config(text="Registrarse")
            boton_cambio.config(text='Cambiar a login')
            ocultar_mostrar_campos()
        else:
            modo.set("login")
            titulo.config(text="Iniciar Sesión")
            boton_login.config(text="Iniciar Sesión")
            boton_cambio.config(text='Cambiar a registro')
            ocultar_mostrar_campos()

    titulo = ttk.Label(frame, text="Iniciar Sesión", font=("Segoe UI", 20, "bold"))
    titulo.grid(row=0, column=0, pady=15)

    ttk.Label(frame, text="Email:").grid(row=1, column=0)
    email_var = ttk.StringVar()
    ttk.Entry(frame, textvariable=email_var, width=30).grid(row=2, column=0, pady=5)

    ttk.Label(frame, text="Contraseña:").grid(row=3, column=0)
    pass_var = ttk.StringVar()
    ttk.Entry(frame, textvariable=pass_var, width=30, show="*").grid(row=4, column=0, pady=5)

    nombre_label = ttk.Label(frame, text="Nombre:")
    nombre_label.grid(row=5, column=0)
    nombre_var = ttk.StringVar()
    nombre_entry = ttk.Entry(frame, textvariable=nombre_var, width=30)
    nombre_entry.grid(row=6, column=0, pady=5)

    rol_label = ttk.Label(frame, text="Rol:")
    rol_label.grid(row=7, column=0)
    rol_combo = ttk.Combobox(frame, values=["cliente", "proveedor"], width=27, state="readonly")
    rol_combo.set("cliente")
    rol_combo.grid(row=8, column=0, pady=5)

    def procesar():
        email = email_var.get().strip()
        password = pass_var.get().strip()

        if modo.get() == "login":
            ok, usuario = usuarios.verificar_login(email, password)
            if ok:
                rol_user = usuario['rol']
                messagebox.showinfo("Bienvenido", f"Hola {usuario['nombre']} ({rol_user})")
                login.destroy()
                rol: usuarios.Rol = getattr(usuarios.Rol, rol_user)
                if rol == usuarios.Rol.cliente:
                    mostrar_carrito(root, usuario)
                else:
                    mostrar_inventario(root, usuario)
            else:
                messagebox.showerror("Error", usuario)
        else:
            nombre = nombre_var.get().strip()
            rol = rol_combo.get().strip()
            if not all([nombre, email, password, rol]):
                messagebox.showerror("Error", "Complete todos los campos")
                return
            ok, msg = usuarios.registrar_usuario(nombre, email, password, rol)
            if ok:
                messagebox.showinfo("Éxito", msg)
                cambiar_modo()
            else:
                messagebox.showerror("Error", msg)

    boton_login = ttk.Button(frame, text="Registrarse", bootstyle=PRIMARY, command=procesar)
    boton_login.grid(row=9, column=0, pady=10)

    boton_cambio = ttk.Button(frame, text='Cambiar a Login', bootstyle=SECONDARY, command=cambiar_modo)
    boton_cambio.grid(row=10, column=0)


# ==========================
# 🧾 Ventana principal (ya tienes esta parte)
# ==========================
def mostrar_carrito(root, usuario):
    app = ttk.Toplevel(master=root)
    app.title("Sistema de Ventas")
    app.state('zoomed')
    app.protocol("WM_DELETE_WINDOW", root.destroy)

    carrito = []

    nombre_var = ttk.StringVar()
    precio_var = ttk.DoubleVar()
    cantidad_var = ttk.IntVar()

    header = ttk.Label(app, text=f"🛍️ Bienvenido {usuario['nombre']} ({usuario['rol']})",
                       font=("Segoe UI", 20, "bold"), bootstyle=PRIMARY)
    header.pack(pady=20)

    def deslogear():
        app.destroy()
        mostrar_login(root)

    boton_deslogeo = ttk.Button(app, text="Deslogear", bootstyle=PRIMARY, command=deslogear)
    boton_deslogeo.pack(pady=20)

    def actualizar_productos(*_):
        termino = nombre_var.get()
        productos_encontrados.clear()
        if not termino:
            combo.config(values=[])
            combo.set('')
            return

        resultados = productos.buscar_productos(termino)
        nombres = []
        for id_, nombre, precio, cantidad in resultados:
            nombres.append(nombre)
            productos_encontrados[nombre] = {'id': id_, 'precio': precio, 'cantidad': cantidad}

        combo.config(values=nombres)
        if resultados:
            combo.set(resultados[0][1])
            combo.event_generate("<<ComboboxSelected>>")

    def seleccionar_producto(event):
        nonlocal producto_seleccionado
        producto = combo.get()
        producto_seleccionado = productos_encontrados[producto]
        producto_seleccionado['nombre'] = producto
        if producto_seleccionado and producto_seleccionado['precio']:
            precio_var.set(producto_seleccionado['precio'])

    productos_encontrados = {}
    producto_seleccionado = {}

    # --- Frame formulario de carrito ---
    frame_form = ttk.Labelframe(app, text="Agregar producto al carrito", padding=20)
    frame_form.pack(padx=20, pady=10, fill=X)

    ttk.Label(frame_form, text="Buscar por id o nombre").grid(row=0, column=0, sticky=W)
    buscador = ttk.Entry(frame_form, textvariable=nombre_var, width=40)
    buscador.grid(row=0, column=1)

    buscador.bind('<KeyRelease>', actualizar_productos)

    def validar_numeros(valor, widget_name):
        isdigit = valor == '' or valor.replace('.', '', 1).isdigit()
        if not isdigit:
            entry = app.nametowidget(widget_name)
            entry.after(1, lambda: entry.delete(0, tkinter.END))
            entry.after(1, lambda: entry.insert(0, "0"))
            return False

        return True

    vcmd = (app.register(validar_numeros), '%P', '%W')

    combo = ttk.Combobox(frame_form, state='readonly')
    combo.grid(row=1, column=1)
    combo.bind('<<ComboboxSelected>>', seleccionar_producto)

    ttk.Label(frame_form, text="Precio ($):").grid(row=2, column=0, sticky=W)
    precio_entry = ttk.Entry(frame_form, textvariable=precio_var, width=20)
    precio_entry.grid(row=2, column=1, sticky=W)
    precio_entry.config(state='disabled')

    ttk.Label(frame_form, text="Cantidad:").grid(row=3, column=0, sticky=W)
    ttk.Entry(frame_form, textvariable=cantidad_var, width=20, validate='key', validatecommand=vcmd).grid(row=3,
                                                                                                          column=1,
                                                                                                          sticky=W)

    def limpiar_campos():
        nombre_var.set("")
        precio_var.set(0)
        cantidad_var.set(0)
        combo.set('')
        combo.config(values=[])

    def agregar_o_actualizar():
        nonlocal producto_seleccionado
        id_ = producto_seleccionado['id']
        nombre = producto_seleccionado['nombre']
        precio = producto_seleccionado['precio']
        stock = producto_seleccionado['cantidad']
        cantidad = cantidad_var.get()

        if stock < cantidad:
            messagebox.showerror('Sin stock', 'No hay stock para cubrir la cantidad requerida')
        else:
            carrito.append({"id": id_, "nombre": nombre, "precio": precio, "cantidad": cantidad})
            actualizar_tabla()

        limpiar_campos()

    ttk.Button(frame_form, text="Agregar", bootstyle=SUCCESS, command=agregar_o_actualizar) \
        .grid(row=4, column=0, columnspan=2, pady=10)

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
                                                          f"${item['precio']:.2f}", item["cantidad"],
                                                          f"${subtotal:.2f}",
                                                          "❌ Borrar"))
        total_label.config(text=f"Total: ${total:.2f}")

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
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            borrar_producto(item_id)

    tabla.bind("<Button-1>", on_tabla_click)

    def generar_ticket():
        if not carrito:
            messagebox.showerror("Error", "El carrito está vacío")
            return
        archivo, total = crear_ticket(carrito)
        for producto in carrito:
            id_ = producto['id']
            cantidad = producto['cantidad']
            actualizar_stock(id_, cantidad)

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

    ttk.Button(app, text="👥 Gestionar Clientes / Proveedores", bootstyle=INFO, command=abrir_crud_usuarios).pack(
        pady=10)


def mostrar_inventario(root, usuario):
    app = ttk.Toplevel(master=root)
    app.title("Inventario")
    app.state('zoomed')
    app.protocol("WM_DELETE_WINDOW", root.destroy)

    header = ttk.Label(app, text=f"🛍️ Bienvenido {usuario['nombre']} ({usuario['rol']})",
                       font=("Segoe UI", 20, "bold"), bootstyle=PRIMARY)
    header.pack(pady=20)

    def deslogear():
        app.destroy()
        mostrar_login(root)

    boton_deslogeo = ttk.Button(app, text="Deslogear", bootstyle=PRIMARY, command=deslogear)
    boton_deslogeo.pack(pady=20)

    editando_id = None

    nombre_var = ttk.StringVar()
    precio_var = ttk.DoubleVar()
    cantidad_var = ttk.IntVar()

    def validar_numeros(valor, widget_name):
        isdigit = valor == '' or valor.replace('.', '', 1).isdigit()
        if not isdigit:
            entry = app.nametowidget(widget_name)
            entry.after(1, lambda: entry.delete(0, tkinter.END))
            entry.after(1, lambda: entry.insert(0, "0"))
            return False

        return True

    vcmd = (app.register(validar_numeros), '%P', '%W')

    frame_form = ttk.Labelframe(app, text='Crear producto', padding=20)
    frame_form.pack(padx=20, pady=10, fill=X)

    ttk.Label(frame_form, text="Nombre del producto:").grid(row=0, column=0, sticky=W)
    ttk.Entry(frame_form, textvariable=nombre_var, width=40).grid(row=0, column=1)

    ttk.Label(frame_form, text="Precio ($):").grid(row=1, column=0, sticky=W)
    ttk.Entry(frame_form, textvariable=precio_var, width=20, validate='key', validatecommand=vcmd).grid(row=1, column=1,
                                                                                                        sticky=W)

    ttk.Label(frame_form, text="Cantidad:").grid(row=2, column=0, sticky=W)
    ttk.Entry(frame_form, textvariable=cantidad_var, width=20, validate='key', validatecommand=vcmd).grid(row=2,
                                                                                                          column=1,
                                                                                                          sticky=W)

    def limpiar_campos():
        nonlocal editando_id
        nombre_var.set("")
        precio_var.set(0)
        cantidad_var.set(0)
        editando_id = None
        frame_form.config(text='Crear producto')
        form_button.config(text='Crear')
        app.update_idletasks()

    def agregar_o_actualizar():
        nonlocal editando_id
        nombre = nombre_var.get().strip()
        precio = precio_var.get()
        cantidad = cantidad_var.get()
        if not nombre or precio <= 0 or cantidad <= 0:
            messagebox.showerror("Error", "Complete todos los campos correctamente")
            return
        if editando_id is None:
            rows_affected = productos.guardar_producto(nombre, precio, cantidad)
            if rows_affected > 0:
                messagebox.showinfo('Creado', 'Producto creado con éxito')
            else:
                messagebox.showerror('Error', 'El producto no fue creado')
        else:
            rows_affected = productos.guardar_producto(nombre, precio, cantidad, True, editando_id)
            if rows_affected > 0:
                messagebox.showinfo('Editado', 'Producto editado con éxito')
            else:
                messagebox.showerror('Error', 'El producto no fue editado')

        actualizar_tabla()
        limpiar_campos()
        frame_form.config(text='Crear producto')
        app.update_idletasks()

    form_button = ttk.Button(frame_form, text='Crear', bootstyle=SUCCESS, command=agregar_o_actualizar)
    form_button.grid(row=3, column=0, columnspan=2, pady=10)

    reset_button = ttk.Button(frame_form, text='Reiniciar formulario', bootstyle=SUCCESS, command=limpiar_campos)
    reset_button.grid(row=3, column=3, columnspan=2, pady=10)

    frame_tabla = ttk.Labelframe(app, text="Inventario", padding=10)
    frame_tabla.pack(fill=BOTH, expand=True, padx=20, pady=10)

    columnas = ("ID", "Producto", "Precio", "Cantidad", "Acciones")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", bootstyle=INFO)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor=CENTER, width=150)
    tabla.column("Acciones", width=200)
    tabla.pack(fill=BOTH, expand=True)

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())

        productos_db = productos.obtener_productos()

        for item in productos_db:
            tabla.insert("", END, iid=item[0], values=(item[0], item[1],
                                                       f"${item[2]:.2f}", item[3], "🖊️ Editar   ❌ Borrar"))

    def editar_producto(item_id):
        nonlocal editando_id
        form_button.config(text='Actualizar')
        frame_form.config(text='Actualizar producto')
        editando_id = item_id
        producto_a_editar = productos.obtener_producto_by_id(item_id)
        nombre_var.set(producto_a_editar[1])
        precio_var.set(producto_a_editar[2])
        cantidad_var.set(producto_a_editar[3])
        editando_id = item_id
        app.update_idletasks()

    def borrar_producto(item_id):
        rows_affected = productos.borrar_producto(item_id)
        if rows_affected > 0:
            messagebox.showinfo('Borrado con éxito', 'El producto fue borrado con éxito')
        else:
            messagebox.showerror('Error', 'El producto no fue borrado')

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

    actualizar_tabla()


# --- Inicio del programa ---
if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    root.withdraw()  # ocultar la raíz (no se ve)
    mostrar_login(root)
    root.mainloop()
