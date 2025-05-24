import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import json
import os
from datetime import datetime
import threading
import time
from collections import defaultdict

class TortilleriaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌽 Tortillería La Guadalupana - Sistema Integral 🌽")
        self.root.geometry("1300x900")  # Aumentar el tamaño inicial
        self.root.configure(bg="#2E8B57")  # Verde bosque
        self.root.resizable(True, True)
        
        # Configurar icono personalizado
        try:
            self.root.iconbitmap("tortilla_icon.ico")
        except:
            try:
                self.root.iconbitmap(default="tortilla_icon.ico")
            except:
                pass
        
        # Variables de estado
        self.usuario_actual = None
        self.tipo_usuario = None  # 'cliente', 'empleado', 'admin'
        self.modo_actual = None
        
        # Datos de usuarios del sistema
        self.usuarios_sistema = {
            "admin": {"password": "admin123", "role": "admin", "nombre": "Administrador"},
            "gerente": {"password": "gerente123", "role": "admin", "nombre": "Gerente General"},
            "empleado1": {"password": "emp123", "role": "empleado", "nombre": "Juan Pérez"},
            "empleado2": {"password": "emp456", "role": "empleado", "nombre": "María García"},
            "cajero": {"password": "caja123", "role": "empleado", "nombre": "Luis Rodríguez"}
        }
        
        # Inventario con más detalles
        self.inventario = {
            "tortillas_maiz": {
                "nombre": "Tortillas de Maíz",
                "stock": 50.0,
                "precio": 25.0,
                "unidad": "kg",
                "descripcion": "Tortillas de maíz tradicionales, hechas a mano",
                "categoria": "tortillas"
            },
            "tortillas_harina": {
                "nombre": "Tortillas de Harina",
                "stock": 35.0,
                "precio": 30.0,
                "unidad": "kg",
                "descripcion": "Tortillas de harina suaves y esponjosas",
                "categoria": "tortillas"
            },
            "masa_maiz": {
                "nombre": "Masa de Maíz",
                "stock": 40.0,
                "precio": 20.0,
                "unidad": "kg",
                "descripcion": "Masa fresca de maíz nixtamalizado",
                "categoria": "masa"
            },
            "masa_harina": {
                "nombre": "Masa de Harina",
                "stock": 25.0,
                "precio": 22.0,
                "unidad": "kg",
                "descripcion": "Masa de harina lista para tortillas",
                "categoria": "masa"
            }
        }
        
        # Carrito de compras mejorado
        self.carrito = {}
        
        # Historial de ventas
        self.historial_ventas = []
        
        # Configurar fuentes personalizadas
        self.fuente_titulo = font.Font(family="Helvetica", size=18, weight="bold")
        self.fuente_subtitulo = font.Font(family="Helvetica", size=14, weight="bold")
        self.fuente_normal = font.Font(family="Helvetica", size=12)
        self.fuente_precio = font.Font(family="Helvetica", size=13, weight="bold")
        
        # Estilos para ttk
        self.configurar_estilos()
        
        # Cargar datos
        self.cargar_datos()
        
        # Inicializar con pantalla de bienvenida
        self.crear_pantalla_bienvenida()
        
    def configurar_estilos(self):
        """Configura estilos personalizados para widgets ttk"""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Configurar estilo para botones
        style.configure('TButton', 
                      font=('Helvetica', 12),
                      padding=6,
                      relief='raised')
        
        style.map('TButton',
                 foreground=[('pressed', 'white'), ('active', 'white')],
                 background=[('pressed', '#1F4E37'), ('active', '#228B22')])
        
        # Estilo para botones principales
        style.configure('Primary.TButton',
                      foreground='white',
                      background='#228B22',
                      font=('Helvetica', 14, 'bold'),
                      padding=10)
        
        style.map('Primary.TButton',
                 background=[('pressed', '#1F4E37'), ('active', '#32CD32')])
        
        # Estilo para botones de peligro
        style.configure('Danger.TButton',
                      foreground='white',
                      background='#DC143C',
                      font=('Helvetica', 12, 'bold'))
        
        # Estilo para botones de éxito
        style.configure('Success.TButton',
                      foreground='white',
                      background='#32CD32',
                      font=('Helvetica', 12, 'bold'))
        
        # Estilo para botones de información
        style.configure('Info.TButton',
                      foreground='white',
                      background='#4169E1',
                      font=('Helvetica', 12, 'bold'))
        
        # Estilo para botones de advertencia
        style.configure('Warning.TButton',
                      foreground='white',
                      background='#FF8C00',
                      font=('Helvetica', 12, 'bold'))
        
        # Estilo para Treeview
        style.configure('Treeview',
                      font=('Helvetica', 10),
                      rowheight=25)
        
        style.configure('Treeview.Heading',
                      font=('Helvetica', 11, 'bold'))
        
    def cargar_datos(self):
        """Cargar datos desde archivos JSON"""
        try:
            if os.path.exists("inventario_tortilleria.json"):
                with open("inventario_tortilleria.json", "r", encoding="utf-8") as f:
                    self.inventario = json.load(f)
        except Exception as e:
            print(f"Error al cargar inventario: {e}")
            
        try:
            if os.path.exists("ventas_tortilleria.json"):
                with open("ventas_tortilleria.json", "r", encoding="utf-8") as f:
                    self.historial_ventas = json.load(f)
        except Exception as e:
            print(f"Error al cargar historial: {e}")
    
    def guardar_datos(self):
        """Guardar datos en archivos JSON"""
        try:
            with open("inventario_tortilleria.json", "w", encoding="utf-8") as f:
                json.dump(self.inventario, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el inventario: {str(e)}")
            
        try:
            with open("ventas_tortilleria.json", "w", encoding="utf-8") as f:
                json.dump(self.historial_ventas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el historial de ventas: {str(e)}")
    
    def limpiar_ventana(self):
        """Limpiar todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def crear_pantalla_bienvenida(self):
        """Crear pantalla de bienvenida principal"""
        self.limpiar_ventana()
        
        # Frame principal con gradiente simulado
        main_frame = tk.Frame(self.root, bg="#2E8B57")
        main_frame.pack(fill="both", expand=True)
        
        # Header con animación de bienvenida
        header_frame = tk.Frame(main_frame, bg="#228B22", height=150)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Logo y título
        logo_frame = tk.Frame(header_frame, bg="#228B22")
        logo_frame.pack(pady=10)
        
        # Título principal animado
        self.titulo_principal = tk.Label(logo_frame, 
                                       text="🌽 TORTILLERÍA LA GUADALUPANA 🌽",
                                       font=("Helvetica", 28, "bold"),
                                       bg="#228B22", fg="#FFD700")
        self.titulo_principal.pack(pady=5)
        
        subtitulo = tk.Label(logo_frame,
                           text="Sistema Integral de Ventas y Administración",
                           font=("Helvetica", 14, "italic"),
                           bg="#228B22", fg="white")
        subtitulo.pack()
        
        # Frame central para botones
        center_frame = tk.Frame(main_frame, bg="#2E8B57")
        center_frame.pack(expand=True, fill="both")
        
        # Container para los botones principales
        buttons_container = tk.Frame(center_frame, bg="#2E8B57")
        buttons_container.pack(expand=True)
        
        # Título de selección
        tk.Label(buttons_container,
                text="Seleccione su tipo de acceso:",
                font=("Helvetica", 18, "bold"),
                bg="#2E8B57", fg="white").pack(pady=30)
        
        # Frame para botones en fila
        buttons_frame = tk.Frame(buttons_container, bg="#2E8B57")
        buttons_frame.pack(pady=20)
        
        # Botón COMPRADOR/CLIENTE
        btn_cliente = ttk.Button(buttons_frame,
                               text="🛒\nSOY CLIENTE\n(Realizar Compra)",
                               style='Primary.TButton',
                               command=self.modo_cliente)
        btn_cliente.pack(side="left", padx=20, ipadx=20, ipady=20)
        
        # Botón EMPLEADO
        btn_empleado = ttk.Button(buttons_frame,
                                text="👨‍💼\nSOY EMPLEADO\n(Área de Trabajo)",
                                style='Primary.TButton',
                                command=self.login_empleado)
        btn_empleado.pack(side="left", padx=20, ipadx=20, ipady=20)
        
        # Botón SALIR
        btn_salir = ttk.Button(buttons_frame,
                             text="❌\nSALIR\n(Cerrar Sistema)",
                             style='Danger.TButton',
                             command=self.salir_aplicacion)
        btn_salir.pack(side="left", padx=20, ipadx=20, ipady=20)
        
        # Información del sistema en la parte inferior
        info_frame = tk.Frame(main_frame, bg="#1F4E37", height=100)
        info_frame.pack(fill="x", side="bottom")
        info_frame.pack_propagate(False)
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        tk.Label(info_frame,
                text=f"🕐 Fecha: {fecha_actual} | 📍 Sucursal: Centro | 📞 Tel: (555) 123-4567 | 👤 Usuarios registrados: {len(self.usuarios_sistema)}",
                font=("Helvetica", 11),
                bg="#1F4E37", fg="white").pack(pady=10)
        
        # Mostrar productos destacados
        productos_frame = tk.Frame(info_frame, bg="#1F4E37")
        productos_frame.pack()
        
        productos_texto = "🌟 Productos Destacados: Tortillas de Maíz y Harina | Masa Tradicional | ¡Hechas al Momento! 🌟"
        tk.Label(productos_frame,
                text=productos_texto,
                font=("Helvetica", 10, "italic"),
                bg="#1F4E37", fg="#FFD700").pack()
        
        # Mostrar estadísticas rápidas
        stats_frame = tk.Frame(info_frame, bg="#1F4E37")
        stats_frame.pack(pady=5)
        
        total_productos = len(self.inventario)
        total_ventas = len(self.historial_ventas)
        tk.Label(stats_frame,
                text=f"📊 Estadísticas: {total_productos} productos en inventario | {total_ventas} ventas registradas",
                font=("Helvetica", 9),
                bg="#1F4E37", fg="white").pack()
    
    def modo_cliente(self):
        """Activar modo cliente (compras sin login)"""
        self.tipo_usuario = "cliente"
        self.usuario_actual = "Cliente"
        self.modo_actual = "cliente"
        self.crear_interfaz_cliente()
    
    def login_empleado(self):
        """Mostrar pantalla de login para empleados"""
        self.crear_login_empleado()
    
    def salir_aplicacion(self):
        """Salir de la aplicación"""
        respuesta = messagebox.askyesno("Confirmar Salida", 
                                      "¿Está seguro que desea salir del sistema?",
                                      icon="question")
        if respuesta:
            self.guardar_datos()
            self.root.quit()
            self.root.destroy()
    
    def crear_login_empleado(self):
        """Crear pantalla de login para empleados/administradores"""
        self.limpiar_ventana()
        
        # Frame principal de login
        login_main = tk.Frame(self.root, bg="#2E8B57")
        login_main.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(login_main, bg="#228B22", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🔐 ACCESO DE EMPLEADOS Y ADMINISTRADORES",
                font=("Helvetica", 18, "bold"), bg="#228B22", fg="white").pack(pady=30)
        
        # Frame central para el formulario
        center_frame = tk.Frame(login_main, bg="#2E8B57")
        center_frame.pack(expand=True)
        
        # Container del login
        login_container = tk.Frame(center_frame, bg="#F0F8FF", relief="raised", bd=3)
        login_container.pack(expand=True, padx=100, pady=50)
        
        # Título del formulario
        tk.Label(login_container, text="Iniciar Sesión",
                font=("Helvetica", 20, "bold"), bg="#F0F8FF", fg="#2E8B57").pack(pady=20)
        
        # Campo Usuario
        tk.Label(login_container, text="👤 Usuario:",
                font=("Helvetica", 14, "bold"), bg="#F0F8FF", fg="black").pack(pady=(20,5))
        
        self.entry_usuario = ttk.Entry(login_container, font=("Helvetica", 12), width=25)
        self.entry_usuario.pack(pady=5)
        
        # Campo Contraseña
        tk.Label(login_container, text="🔑 Contraseña:",
                font=("Helvetica", 14, "bold"), bg="#F0F8FF", fg="black").pack(pady=(20,5))
        
        self.entry_password = ttk.Entry(login_container, font=("Helvetica", 12), width=25,
                                      show="*")
        self.entry_password.pack(pady=5)
        
        # Botones
        buttons_login_frame = tk.Frame(login_container, bg="#F0F8FF")
        buttons_login_frame.pack(pady=30)
        
        ttk.Button(buttons_login_frame, text="🚀 Iniciar Sesión",
                 style='Success.TButton',
                 command=self.validar_login_empleado).pack(side="left", padx=10)
        
        ttk.Button(buttons_login_frame, text="🔙 Volver",
                 style='Info.TButton',
                 command=self.crear_pantalla_bienvenida).pack(side="left", padx=10)
        
        # Información de usuarios de prueba
        info_frame = tk.Frame(login_container, bg="#E6F3FF", relief="sunken", bd=2)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(info_frame, text="👥 USUARIOS DE PRUEBA:",
                font=("Helvetica", 11, "bold"), bg="#E6F3FF", fg="#2E8B57").pack(pady=5)
        
        usuarios_info = """
Administradores:
• admin / admin123 (Administrador)
• gerente / gerente123 (Gerente General)

Empleados:
• empleado1 / emp123 (Juan Pérez)
• cajero / caja123 (Luis Rodríguez)
        """
        
        tk.Label(info_frame, text=usuarios_info,
                font=("Helvetica", 10), bg="#E6F3FF", fg="black", justify="left").pack(pady=5)
        
        # Bind Enter key
        self.entry_password.bind("<Return>", lambda e: self.validar_login_empleado())
        self.entry_usuario.focus()
    
    def validar_login_empleado(self):
        """Validar credenciales de empleado/administrador"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if usuario in self.usuarios_sistema and self.usuarios_sistema[usuario]["password"] == password:
            self.usuario_actual = usuario
            self.tipo_usuario = self.usuarios_sistema[usuario]["role"]
            self.modo_actual = "empleado"
            
            # Mostrar mensaje de bienvenida
            nombre = self.usuarios_sistema[usuario]["nombre"]
            messagebox.showinfo("Bienvenido", f"¡Bienvenido {nombre}!\nAcceso concedido al sistema.")
            
            if self.tipo_usuario == "admin":
                self.crear_interfaz_admin()
            else:
                self.crear_interfaz_empleado()
        else:
            messagebox.showerror("Error de Acceso", 
                               "Usuario o contraseña incorrectos.\nPor favor, verifique sus credenciales.")
            self.entry_password.delete(0, tk.END)
    
    def crear_interfaz_cliente(self):
        self.limpiar_ventana()
    
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=3)  # 75% para productos
        self.root.grid_columnconfigure(1, weight=1)  # 25% para carrito
        self.root.grid_rowconfigure(0, weight=1)
    
        # Frame de productos (izquierda)
        productos_frame = tk.Frame(self.root, bg="#F0F8FF")
        productos_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
        # Frame del carrito (derecha)
        carrito_frame = tk.Frame(self.root, bg="#E6F3FF", bd=2, relief="groove")
        carrito_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
        # Configurar scroll para productos
        canvas = tk.Canvas(productos_frame, bg="#F0F8FF")
        scrollbar = ttk.Scrollbar(productos_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F0F8FF")
    
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # Crear contenido
        self.crear_catalogo_productos_cliente(scrollable_frame)
        self.crear_panel_carrito_cliente(carrito_frame)
    
        # Botón volver abajo
        btn_volver = ttk.Button(self.root, text="🔙 Volver al Menú Principal",
                          style='Danger.TButton',
                          command=self.crear_pantalla_bienvenida)
        btn_volver.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    
    def crear_catalogo_productos_cliente(self, parent):
        """Crear catálogo de productos para clientes"""
        # Título del catálogo
        tk.Label(parent, text="🌟 NUESTROS PRODUCTOS FRESCOS 🌟",
                font=("Helvetica", 18, "bold"), bg="#F0F8FF", fg="#2E8B57").pack(pady=20)
        
        # Agrupar productos por categoría
        categorias = {}
        for key, producto in self.inventario.items():
            cat = producto.get("categoria", "otros")
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append((key, producto))
        
        # Mostrar cada categoría
        for categoria, productos in categorias.items():
            # Frame de la categoría
            cat_frame = tk.LabelFrame(parent, text=f"🌽 {categoria.upper()}",
                                     font=("Helvetica", 16, "bold"), bg="#F0F8FF", fg="#228B22",
                                     relief="groove", bd=3)
            cat_frame.pack(fill="x", padx=20, pady=10)
            
            # Grid de productos
            productos_grid = tk.Frame(cat_frame, bg="#F0F8FF")
            productos_grid.pack(fill="x", padx=10, pady=10)
            
            col = 0
            for key, producto in productos:
                if producto["stock"] > 0:  # Solo mostrar productos disponibles
                    self.crear_tarjeta_producto_cliente(productos_grid, key, producto, col)
                    col += 1
                    if col >= 2:  # 2 productos por fila
                        col = 0
    
    def crear_tarjeta_producto_cliente(self, parent, key, producto, column):
        """Crear tarjeta de producto para cliente"""
        # Frame de la tarjeta
        card_frame = tk.Frame(parent, bg="white", relief="raised", bd=2)
        card_frame.grid(row=column//2, column=column%2, padx=10, pady=10, sticky="ew")
        parent.grid_columnconfigure(column%2, weight=1)
        
        # Información del producto
        info_frame = tk.Frame(card_frame, bg="white")
        info_frame.pack(fill="x", padx=10, pady=10)
        
        # Nombre del producto
        tk.Label(info_frame, text=producto["nombre"],
                font=("Helvetica", 14, "bold"), bg="white", fg="#2E8B57").pack(anchor="w")
        
        # Descripción
        tk.Label(info_frame, text=producto["descripcion"],
                font=("Helvetica", 10), bg="white", fg="gray", wraplength=250).pack(anchor="w")
        
        # Precio y disponibilidad
        precio_frame = tk.Frame(info_frame, bg="white")
        precio_frame.pack(fill="x", pady=5)
        
        tk.Label(precio_frame, text=f"💰 ${producto['precio']:.2f}/{producto['unidad']}",
                font=("Helvetica", 12, "bold"), bg="white", fg="#228B22").pack(side="left")
        
        stock_color = "#228B22" if producto['stock'] > 5 else "#FF8C00" if producto['stock'] > 0 else "#DC143C"
        tk.Label(precio_frame, text=f"📦 {producto['stock']:.1f} {producto['unidad']} disponibles",
                font=("Helvetica", 10), bg="white", fg=stock_color).pack(side="right")
        
        # Controles de compra
        compra_frame = tk.Frame(card_frame, bg="white")
        compra_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(compra_frame, text="Cantidad:",
                font=("Helvetica", 10, "bold"), bg="white").pack(side="left")
        
        cantidad_entry = ttk.Entry(compra_frame, width=8, font=("Helvetica", 10))
        cantidad_entry.pack(side="left", padx=5)
        cantidad_entry.insert(0, "0.5")
        
        ttk.Button(compra_frame, text="🛒 Agregar",
                 style='Success.TButton',
                 command=lambda: self.agregar_producto_carrito_cliente(key, cantidad_entry)).pack(side="right")
    
    def crear_panel_carrito_cliente(self, parent):
        """Crear panel del carrito para clientes"""
        # Título del carrito
        tk.Label(parent, text="🛒 MI CARRITO DE COMPRAS",
                font=("Helvetica", 16, "bold"), bg="#E6F3FF", fg="#2E8B57").pack(pady=10)
        
        # Lista del carrito con scroll
        carrito_frame = tk.Frame(parent, bg="#E6F3FF")
        carrito_frame.pack(expand=True, fill="both", padx=10)
        
        # Canvas para scroll
        self.carrito_canvas = tk.Canvas(carrito_frame, bg="white", height=300)
        carrito_scrollbar = ttk.Scrollbar(carrito_frame, orient="vertical", command=self.carrito_canvas.yview)
        self.carrito_scroll_frame = tk.Frame(self.carrito_canvas, bg="white")
        
        self.carrito_scroll_frame.bind(
            "<Configure>",
            lambda e: self.carrito_canvas.configure(scrollregion=self.carrito_canvas.bbox("all")))
        
        self.carrito_canvas.create_window((0, 0), window=self.carrito_scroll_frame, anchor="nw")
        self.carrito_canvas.configure(yscrollcommand=carrito_scrollbar.set)
        
        self.carrito_canvas.pack(side="left", fill="both", expand=True)
        carrito_scrollbar.pack(side="right", fill="y")
        
        # Panel de totales
        totales_frame = tk.Frame(parent, bg="#FFD700", relief="raised", bd=2)
        totales_frame.pack(fill="x", padx=10, pady=5)
        
        self.label_subtotal = tk.Label(totales_frame, text="Subtotal: $0.00",
                                      font=("Helvetica", 12, "bold"), bg="#FFD700", fg="black")
        self.label_subtotal.pack(pady=2)
        
        self.label_total = tk.Label(totales_frame, text="TOTAL: $0.00",
                                   font=("Helvetica", 16, "bold"), bg="#FFD700", fg="#2E8B57")
        self.label_total.pack(pady=2)
        
        # Botones de acción
        acciones_frame = tk.Frame(parent, bg="#E6F3FF")
        acciones_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(acciones_frame, text="🗑️ Vaciar Carrito",
                 style='Danger.TButton',
                 command=self.vaciar_carrito_cliente).pack(fill="x", pady=2)
        
        ttk.Button(acciones_frame, text="💳 COMPRAR AHORA",
                 style='Success.TButton',
                 command=self.procesar_compra_cliente).pack(fill="x", pady=5)
        
        # Inicializar carrito vacío
        self.actualizar_carrito_cliente()
    
    def agregar_producto_carrito_cliente(self, key, entry_cantidad):
        """Agregar producto al carrito del cliente"""
        try:
            cantidad = float(entry_cantidad.get())
            if cantidad <= 0:
                messagebox.showwarning("Cantidad Inválida", "La cantidad debe ser mayor a 0")
                return
                
            if cantidad > self.inventario[key]["stock"]:
                messagebox.showerror("Stock Insuficiente", 
                                   f"Solo tenemos {self.inventario[key]['stock']:.1f} {self.inventario[key]['unidad']} disponibles")
                return
            
            # Agregar al carrito
            if key in self.carrito:
                self.carrito[key] += cantidad
            else:
                self.carrito[key] = cantidad
            
            # Verificar límite total
            if self.carrito[key] > self.inventario[key]["stock"]:
                self.carrito[key] = self.inventario[key]["stock"]
                messagebox.showwarning("Límite de Stock", 
                                     f"Se ajustó la cantidad al máximo disponible: {self.inventario[key]['stock']:.1f} kg")
            
            entry_cantidad.delete(0, tk.END)
            entry_cantidad.insert(0, "0.5")
            
            self.actualizar_carrito_cliente()
            messagebox.showinfo("Producto Agregado", 
                              f"✅ {self.inventario[key]['nombre']} agregado al carrito")
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida")
    
    def actualizar_carrito_cliente(self):
        """Actualizar visualización del carrito del cliente"""
        # Limpiar carrito actual
        for widget in self.carrito_scroll_frame.winfo_children():
            widget.destroy()
        
        total = 0
        
        if not self.carrito:
            tk.Label(self.carrito_scroll_frame, text="🛒 Tu carrito está vacío\n\n¡Agrega algunos productos deliciosos!",
                    font=("Helvetica", 11), bg="white", fg="gray", justify="center").pack(pady=50)
        else:
            for key, cantidad in self.carrito.items():
                producto = self.inventario[key]
                subtotal = cantidad * producto["precio"]
                total += subtotal
                
                # Frame del item
                item_frame = tk.Frame(self.carrito_scroll_frame, bg="#F8F8F8", relief="solid", bd=1)
                item_frame.pack(fill="x", padx=5, pady=2)
                
                # Info del producto
                info_text = f"{producto['nombre']}\n{cantidad:.1f} {producto['unidad']} × ${producto['precio']:.2f}"
                tk.Label(item_frame, text=info_text,
                        font=("Helvetica", 10), bg="#F8F8F8", fg="black", justify="left").pack(side="left", padx=5, pady=5)
                
                # Precio y botón eliminar
                right_frame = tk.Frame(item_frame, bg="#F8F8F8")
                right_frame.pack(side="right", padx=5, pady=5)
                
                tk.Label(right_frame, text=f"${subtotal:.2f}",
                        font=("Helvetica", 11, "bold"), bg="#F8F8F8", fg="#228B22").pack()
                
                ttk.Button(right_frame, text="❌", style='Danger.TButton',
                         command=lambda k=key: self.eliminar_producto_carrito(k)).pack()
        
        # Actualizar totales
        self.label_subtotal.config(text=f"Subtotal: ${total:.2f}")
        self.label_total.config(text=f"TOTAL: ${total:.2f}")
    
    def eliminar_producto_carrito(self, key):
        """Eliminar producto del carrito"""
        if key in self.carrito:
            del self.carrito[key]
            self.actualizar_carrito_cliente()
            messagebox.showinfo("Producto Eliminado", "Producto removido del carrito")
    
    def vaciar_carrito_cliente(self):
        """Vaciar todo el carrito"""
        if self.carrito:
            respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de vaciar todo el carrito?")
            if respuesta:
                self.carrito.clear()
                self.actualizar_carrito_cliente()
                messagebox.showinfo("Carrito Vaciado", "Se han eliminado todos los productos")
        else:
            messagebox.showinfo("Carrito Vacío", "El carrito ya está vacío")
    
    def procesar_compra_cliente(self):
        """Procesar la compra del cliente"""
        if not self.carrito:
            messagebox.showwarning("Carrito Vacío", "Agregue productos al carrito antes de comprar")
            return
    
        # Verificar stock antes de procesar
        for key, cantidad in self.carrito.items():
            if cantidad > self.inventario[key]["stock"]:
                messagebox.showerror("Error", 
                              f"No hay suficiente stock de {self.inventario[key]['nombre']}. Disponible: {self.inventario[key]['stock']:.1f} {self.inventario[key]['unidad']}")
                return
    
        # Calcular total
        total = sum(self.carrito[key] * self.inventario[key]["precio"] for key in self.carrito)
    
        # Mostrar resumen de compra
        resumen = "RESUMEN DE COMPRA:\n\n"
        for key, cantidad in self.carrito.items():
            producto = self.inventario[key]
            subtotal = cantidad * producto["precio"]
            resumen += f"• {producto['nombre']}: {cantidad:.1f} {producto['unidad']} - ${subtotal:.2f}\n"
    
        resumen += f"\nTOTAL A PAGAR: ${total:.2f}"
    
        respuesta = messagebox.askyesno("Confirmar Compra", f"{resumen}\n\n¿Confirma la compra?")
    
        if respuesta:
            # Actualizar inventario
            for key, cantidad in self.carrito.items():
                self.inventario[key]["stock"] -= cantidad
        
            # Registrar venta
            venta = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cliente": "Cliente Mostrador",
                "productos": dict(self.carrito),
                "total": total,
                "vendedor": "Cliente (Autoservicio)"
            }
            self.historial_ventas.append(venta)
        
        # Guardar datos
            self.guardar_datos()
        
            # Limpiar carrito
            self.carrito.clear()
            self.actualizar_carrito_cliente()
        
            messagebox.showinfo("Compra Exitosa", 
                          f"¡Gracias por su compra!\n\nTotal pagado: ${total:.2f}\n\n¡Que disfrute sus productos frescos!")
    
    def crear_interfaz_empleado(self):
        """Crear interfaz para empleados"""
        self.limpiar_ventana()
        
        # Header del empleado
        header = tk.Frame(self.root, bg="#32CD32", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        nombre = self.usuarios_sistema[self.usuario_actual]["nombre"]
        tk.Label(header, text=f"👨‍💼 PANEL EMPLEADO - {nombre}",
                font=("Helvetica", 20, "bold"), bg="#32CD32", fg="white").pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#F0F8FF")
        main_frame.pack(fill="both", expand=True)
        
        # Panel de información
        info_panel = tk.Frame(main_frame, bg="#E6F3FF", height=50)
        info_panel.pack(fill="x")
        info_panel.pack_propagate(False)
        
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        tk.Label(info_panel, text=f"📅 {fecha} | 🏪 Sistema de Empleados | 👨‍💼 {nombre}",
                font=("Helvetica", 11, "bold"), bg="#E6F3FF", fg="black").pack(pady=12)
        
        # Menú de opciones para empleados
        menu_frame = tk.Frame(main_frame, bg="#F0F8FF")
        menu_frame.pack(expand=True)
        
        tk.Label(menu_frame, text="MENÚ DE OPCIONES",
                font=("Helvetica", 18, "bold"), bg="#F0F8FF", fg="#2E8B57").pack(pady=30)
        
        # Botones de opciones
        opciones_frame = tk.Frame(menu_frame, bg="#F0F8FF")
        opciones_frame.pack()
        
        # Primera fila de botones
        fila1 = tk.Frame(opciones_frame, bg="#F0F8FF")
        fila1.pack(pady=10)
        
        ttk.Button(fila1, text="📦\nVER INVENTARIO\nConsultar Stock",
                 style='Info.TButton',
                 width=20, command=self.ver_inventario_empleado).pack(side="left", padx=10)
        
        ttk.Button(fila1, text="🛒\nVENDER PRODUCTOS\nProcesar Venta",
                 style='Success.TButton',
                 width=20, command=self.vender_productos_empleado).pack(side="left", padx=10)
        
        ttk.Button(fila1, text="📊\nVER VENTAS\nHistorial del Día",
                 style='Warning.TButton',
                 width=20, command=self.ver_ventas_empleado).pack(side="left", padx=10)
        
        # Segunda fila de botones
        fila2 = tk.Frame(opciones_frame, bg="#F0F8FF")
        fila2.pack(pady=10)
        
        ttk.Button(fila2, text="🔄\nCERRAR SESIÓN\nSalir del Sistema",
                 style='Danger.TButton',
                 width=20, command=self.cerrar_sesion).pack(side="left", padx=10)
        
        ttk.Button(fila2, text="🏠\nMENÚ PRINCIPAL\nPantalla Inicial",
                 style='Primary.TButton',
                 width=20, command=self.crear_pantalla_bienvenida).pack(side="left", padx=10)
    
    def crear_interfaz_admin(self):
        """Crear interfaz para administradores"""
        self.limpiar_ventana()
        
        # Header del admin
        header = tk.Frame(self.root, bg="#B22222", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        nombre = self.usuarios_sistema[self.usuario_actual]["nombre"]
        tk.Label(header, text=f"👑 PANEL ADMINISTRADOR - {nombre}",
                font=("Helvetica", 20, "bold"), bg="#B22222", fg="#FFD700").pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#F0F8FF")
        main_frame.pack(fill="both", expand=True)
        
        # Panel de información
        info_panel = tk.Frame(main_frame, bg="#FFE4E1", height=50)
        info_panel.pack(fill="x")
        info_panel.pack_propagate(False)
        
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        tk.Label(info_panel, text=f"📅 {fecha} | 🏪 Sistema Administrativo | 👑 {nombre}",
                font=("Helvetica", 11, "bold"), bg="#FFE4E1", fg="black").pack(pady=12)
        
        # Menú de opciones para administradores
        menu_frame = tk.Frame(main_frame, bg="#F0F8FF")
        menu_frame.pack(expand=True)
        
        tk.Label(menu_frame, text="PANEL DE CONTROL ADMINISTRATIVO",
                font=("Helvetica", 18, "bold"), bg="#F0F8FF", fg="#B22222").pack(pady=30)
        
        # Botones de opciones administrativas
        opciones_frame = tk.Frame(menu_frame, bg="#F0F8FF")
        opciones_frame.pack()
        
        # Primera fila
        fila1 = tk.Frame(opciones_frame, bg="#F0F8FF")
        fila1.pack(pady=10)
        
        ttk.Button(fila1, text="📦\nGESTIÓN INVENTARIO\nAgregar/Editar Stock",
                 style='Info.TButton',
                 width=20, command=self.gestion_inventario_admin).pack(side="left", padx=10)
        
        ttk.Button(fila1, text="📊\nREPORTES VENTAS\nEstadísticas Completas",
                 style='Success.TButton',
                 width=20, command=self.reportes_ventas_admin).pack(side="left", padx=10)
        
        ttk.Button(fila1, text="👥\nGESTIÓN USUARIOS\nEmpleados y Accesos",
                 style='Warning.TButton',
                 width=20, command=self.gestion_usuarios_admin).pack(side="left", padx=10)
        
        # Segunda fila
        fila2 = tk.Frame(opciones_frame, bg="#F0F8FF")
        fila2.pack(pady=10)
        
        ttk.Button(fila2, text="🛒\nVENDER PRODUCTOS\nProcesar Venta",
                 style='Success.TButton',
                 width=20, command=self.vender_productos_empleado).pack(side="left", padx=10)
        
        ttk.Button(fila2, text="💾\nRESPALDO DATOS\nExportar/Importar",
                 style='Info.TButton',
                 width=20, command=self.respaldo_datos_admin).pack(side="left", padx=10)
        
        # Tercera fila
        fila3 = tk.Frame(opciones_frame, bg="#F0F8FF")
        fila3.pack(pady=20)
        
        ttk.Button(fila3, text="🔄\nCERRAR SESIÓN\nSalir del Sistema",
                 style='Danger.TButton',
                 width=20, command=self.cerrar_sesion).pack(side="left", padx=10)
        
        ttk.Button(fila3, text="🏠\nMENÚ PRINCIPAL\nPantalla Inicial",
                 style='Primary.TButton',
                 width=20, command=self.crear_pantalla_bienvenida).pack(side="left", padx=10)
    
    def ver_inventario_empleado(self):
        """Ver inventario para empleados"""
        ventana_inventario = tk.Toplevel(self.root)
        ventana_inventario.title("📦 Consulta de Inventario")
        ventana_inventario.geometry("900x650")
        ventana_inventario.configure(bg="#F0F8FF")
        
        # Header
        header = tk.Frame(ventana_inventario, bg="#4169E1", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="📦 INVENTARIO ACTUAL",
                font=("Helvetica", 18, "bold"), bg="#4169E1", fg="white").pack(pady=15)
        
        # Crear tabla de inventario
        tabla_frame = tk.Frame(ventana_inventario, bg="#F0F8FF")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Usar Treeview para mejor visualización
        tree = ttk.Treeview(tabla_frame, columns=("Producto", "Stock", "Precio", "Unidad", "Estado"), show="headings")
        
        # Configurar columnas
        tree.heading("Producto", text="Producto")
        tree.heading("Stock", text="Stock")
        tree.heading("Precio", text="Precio")
        tree.heading("Unidad", text="Unidad")
        tree.heading("Estado", text="Estado")
        
        tree.column("Producto", width=250, anchor="w")
        tree.column("Stock", width=100, anchor="center")
        tree.column("Precio", width=100, anchor="center")
        tree.column("Unidad", width=80, anchor="center")
        tree.column("Estado", width=120, anchor="center")
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insertar datos
        for key, producto in self.inventario.items():
            estado = "✅ Disponible" if producto["stock"] > 5 else "⚠️ Poco Stock" if producto["stock"] > 0 else "❌ Agotado"
            color_estado = "#90EE90" if producto["stock"] > 5 else "#FFD700" if producto["stock"] > 0 else "#FFB6C1"
            
            tree.insert("", "end", values=(
                producto["nombre"],
                f"{producto['stock']:.1f}",
                f"${producto['precio']:.2f}",
                producto["unidad"],
                estado
            ))
        
        # Aplicar estilos a las filas
        for i, item in enumerate(tree.get_children()):
            values = tree.item(item, 'values')
            estado = values[4]
            if estado == "⚠️ Poco Stock":
                tree.tag_configure('warning', background='#FFFACD')
                tree.item(item, tags=('warning',))
            elif estado == "❌ Agotado":
                tree.tag_configure('danger', background='#FFE4E1')
                tree.item(item, tags=('danger',))
            else:
                tree.tag_configure('success', background='#F0FFF0')
                tree.item(item, tags=('success',))
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Estadísticas rápidas
        stats_frame = tk.Frame(ventana_inventario, bg="#FFD700", height=40)
        stats_frame.pack(fill="x", pady=10)
        
        total_productos = len(self.inventario)
        productos_agotados = sum(1 for p in self.inventario.values() if p["stock"] == 0)
        productos_poco_stock = sum(1 for p in self.inventario.values() if 0 < p["stock"] <= 5)
        
        tk.Label(stats_frame, 
                text=f"📊 Total Productos: {total_productos} | ⚠️ Poco Stock: {productos_poco_stock} | ❌ Agotados: {productos_agotados}",
                font=("Helvetica", 11, "bold"), bg="#FFD700", fg="black").pack(pady=5)
        
        # Botón cerrar
        ttk.Button(ventana_inventario, text="Cerrar", style='Danger.TButton',
                 command=ventana_inventario.destroy).pack(pady=10)
    
    def vender_productos_empleado(self):
        """Interfaz de venta para empleados"""
        ventana_venta = tk.Toplevel(self.root)
        ventana_venta.title("🛒 Procesar Venta")
        ventana_venta.geometry("1100x750")
        ventana_venta.configure(bg="#F0F8FF")
        
        # Variables locales para la venta
        carrito_venta = {}
        
        # Header
        header = tk.Frame(ventana_venta, bg="#228B22", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🛒 PROCESANDO VENTA",
                font=("Helvetica", 18, "bold"), bg="#228B22", fg="white").pack(pady=15)
        
        # Frame principal dividido
        main_frame = tk.Frame(ventana_venta, bg="#F0F8FF")
        main_frame.pack(fill="both", expand=True)
        
        # Panel izquierdo - Productos
        productos_frame = tk.LabelFrame(main_frame, text="Productos Disponibles", 
                                      font=("Helvetica", 14, "bold"), bg="#F0F8FF")
        productos_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Canvas para scroll de productos
        canvas_productos = tk.Canvas(productos_frame, bg="#F0F8FF")
        scrollbar_productos = ttk.Scrollbar(productos_frame, orient="vertical", command=canvas_productos.yview)
        scrollable_productos = tk.Frame(canvas_productos, bg="#F0F8FF")
        
        scrollable_productos.bind(
            "<Configure>",
            lambda e: canvas_productos.configure(scrollregion=canvas_productos.bbox("all")))
        
        canvas_productos.create_window((0, 0), window=scrollable_productos, anchor="nw")
        canvas_productos.configure(yscrollcommand=scrollbar_productos.set)
        
        # Lista de productos
        for key, producto in self.inventario.items():
            if producto["stock"] > 0:
                prod_frame = tk.Frame(scrollable_productos, bg="white", relief="solid", bd=1)
                prod_frame.pack(fill="x", padx=5, pady=2)
                
                info_frame = tk.Frame(prod_frame, bg="white")
                info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)
                
                tk.Label(info_frame, text=producto["nombre"], font=("Helvetica", 11, "bold"),
                        bg="white", fg="black").pack(anchor="w")
                tk.Label(info_frame, text=f"${producto['precio']:.2f}/{producto['unidad']} - Stock: {producto['stock']:.1f}",
                        font=("Helvetica", 10), bg="white", fg="gray").pack(anchor="w")
                
                # Controles de venta
                control_frame = tk.Frame(prod_frame, bg="white")
                control_frame.pack(side="right", padx=5, pady=5)
                
                cantidad_entry = ttk.Entry(control_frame, width=8, font=("Helvetica", 10))
                cantidad_entry.pack(side="left", padx=2)
                cantidad_entry.insert(0, "1.0")
                
                ttk.Button(control_frame, text="Agregar", style='Success.TButton',
                         command=lambda k=key, e=cantidad_entry: self.agregar_a_venta(k, e, carrito_venta, carrito_label, total_label)).pack(side="left", padx=2)
        
        canvas_productos.pack(side="left", fill="both", expand=True)
        scrollbar_productos.pack(side="right", fill="y")
        
        # Panel derecho - Carrito de venta
        carrito_frame = tk.LabelFrame(main_frame, text="Carrito de Venta", 
                                    font=("Helvetica", 14, "bold"), bg="#F0F8FF", width=400)
        carrito_frame.pack(side="right", fill="y", padx=10, pady=10)
        carrito_frame.pack_propagate(False)
        
        # Área del carrito
        carrito_scroll = tk.Text(carrito_frame, height=20, width=45, font=("Helvetica", 10))
        carrito_scroll.pack(padx=5, pady=5)
        
        carrito_label = carrito_scroll  # Referencia para actualizar
        
        # Total
        total_frame = tk.Frame(carrito_frame, bg="#FFD700", relief="raised", bd=2)
        total_frame.pack(fill="x", padx=5, pady=5)
        
        total_label = tk.Label(total_frame, text="TOTAL: $0.00", font=("Helvetica", 16, "bold"),
                             bg="#FFD700", fg="black")
        total_label.pack(pady=5)
        
        # Botones de acción
        botones_frame = tk.Frame(carrito_frame, bg="#F0F8FF")
        botones_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(botones_frame, text="Limpiar", style='Danger.TButton',
                 command=lambda: self.limpiar_venta(carrito_venta, carrito_label, total_label)).pack(fill="x", pady=2)
        
        ttk.Button(botones_frame, text="PROCESAR VENTA", style='Success.TButton',
                 command=lambda: self.finalizar_venta(carrito_venta, ventana_venta)).pack(fill="x", pady=5)
        
        ttk.Button(botones_frame, text="Cancelar", style='Info.TButton',
                 command=ventana_venta.destroy).pack(fill="x", pady=2)
        
        # Referencias para las funciones
        ventana_venta.carrito_venta = carrito_venta
        ventana_venta.carrito_label = carrito_label
        ventana_venta.total_label = total_label
    
    def agregar_a_venta(self, key, entry, carrito_venta, carrito_label, total_label):
        """Agregar producto a la venta"""
        try:
            cantidad = float(entry.get())
            if cantidad <= 0:
                messagebox.showwarning("Error", "La cantidad debe ser mayor a 0")
                return
            
            if cantidad > self.inventario[key]["stock"]:
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {self.inventario[key]['stock']:.1f}")
                return
            
            if key in carrito_venta:
                carrito_venta[key] += cantidad
            else:
                carrito_venta[key] = cantidad
            
            # Verificar límite total
            if carrito_venta[key] > self.inventario[key]["stock"]:
                carrito_venta[key] = self.inventario[key]["stock"]
            
            self.actualizar_carrito_venta(carrito_venta, carrito_label, total_label)
            entry.delete(0, tk.END)
            entry.insert(0, "1.0")
            
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
    
    def actualizar_carrito_venta(self, carrito_venta, carrito_label, total_label):
        """Actualizar visualización del carrito de venta"""
        carrito_label.delete(1.0, tk.END)
        total = 0
        
        if not carrito_venta:
            carrito_label.insert(tk.END, "Carrito vacío...")
        else:
            for key, cantidad in carrito_venta.items():
                producto = self.inventario[key]
                subtotal = cantidad * producto["precio"]
                total += subtotal
                
                linea = f"{producto['nombre']}\n{cantidad:.1f} {producto['unidad']} × ${producto['precio']:.2f} = ${subtotal:.2f}\n\n"
                carrito_label.insert(tk.END, linea)
        
        total_label.config(text=f"TOTAL: ${total:.2f}")
    
    def limpiar_venta(self, carrito_venta, carrito_label, total_label):
        """Limpiar carrito de venta"""
        carrito_venta.clear()
        self.actualizar_carrito_venta(carrito_venta, carrito_label, total_label)
    
    def finalizar_venta(self, carrito_venta, ventana):
        """Finalizar la venta"""
        if not carrito_venta:
            messagebox.showwarning("Error", "El carrito está vacío")
            return
        
        total = sum(carrito_venta[key] * self.inventario[key]["precio"] for key in carrito_venta)
        
        # Confirmar venta
        respuesta = messagebox.askyesno("Confirmar Venta", f"Total: ${total:.2f}\n¿Procesar venta?")
        
        if respuesta:
            # Actualizar inventario
            for key, cantidad in carrito_venta.items():
                self.inventario[key]["stock"] -= cantidad
            
            # Registrar venta
            venta = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cliente": "Cliente Mostrador",
                "productos": dict(carrito_venta),
                "total": total,
                "vendedor": self.usuarios_sistema[self.usuario_actual]["nombre"]
            }
            self.historial_ventas.append(venta)
            
            # Guardar datos
            self.guardar_datos()
            
            messagebox.showinfo("Venta Exitosa", f"Venta procesada exitosamente\nTotal: ${total:.2f}")
            ventana.destroy()
    
    def ver_ventas_empleado(self):
        """Ver ventas del día para empleados"""
        ventana_ventas = tk.Toplevel(self.root)
        ventana_ventas.title("📊 Ventas del Día")
        ventana_ventas.geometry("1000x700")
        ventana_ventas.configure(bg="#F0F8FF")
        
        # Header
        header = tk.Frame(ventana_ventas, bg="#FF8C00", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="📊 VENTAS DEL DÍA",
                font=("Helvetica", 18, "bold"), bg="#FF8C00", fg="white").pack(pady=15)
        
        # Frame para la lista de ventas
        ventas_frame = tk.Frame(ventana_ventas, bg="#F0F8FF")
        ventas_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Filtrar ventas del día
        hoy = datetime.now().strftime("%Y-%m-%d")
        ventas_hoy = [v for v in self.historial_ventas if v["fecha"].startswith(hoy)]
        
        if not ventas_hoy:
            tk.Label(ventas_frame, text="No hay ventas registradas hoy",
                    font=("Helvetica", 14), bg="#F0F8FF", fg="gray").pack(pady=50)
        else:
            # Estadísticas del día
            stats_frame = tk.Frame(ventana_ventas, bg="#FFD700", height=40)
            stats_frame.pack(fill="x", pady=10)
            
            total_ventas = len(ventas_hoy)
            total_monto = sum(v["total"] for v in ventas_hoy)
            promedio = total_monto / total_ventas if total_ventas > 0 else 0
            
            tk.Label(stats_frame, 
                    text=f"📅 Resumen del día: {total_ventas} ventas | Total: ${total_monto:.2f} | Promedio: ${promedio:.2f}",
                    font=("Helvetica", 12, "bold"), bg="#FFD700", fg="black").pack(pady=5)
            
            # Crear lista de ventas con Treeview
            tree_frame = tk.Frame(ventas_frame, bg="#F0F8FF")
            tree_frame.pack(fill="both", expand=True)
            
            tree = ttk.Treeview(tree_frame, columns=("ID", "Fecha", "Vendedor", "Total"), show="headings")
            
            # Configurar columnas
            tree.heading("ID", text="ID")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Vendedor", text="Vendedor")
            tree.heading("Total", text="Total")
            
            tree.column("ID", width=50, anchor="center")
            tree.column("Fecha", width=150, anchor="center")
            tree.column("Vendedor", width=200, anchor="w")
            tree.column("Total", width=100, anchor="e")
            
            # Insertar datos
            for i, venta in enumerate(ventas_hoy):
                tree.insert("", "end", values=(
                    i+1,
                    venta["fecha"][11:19],  # Solo la hora
                    venta["vendedor"],
                    f"${venta['total']:.2f}"
                ))
            
            # Agregar scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Función para ver detalles de la venta seleccionada
            def ver_detalle_venta(event):
                item = tree.focus()
                if item:
                    valores = tree.item(item, 'values')
                    indice = int(valores[0]) - 1
                    if 0 <= indice < len(ventas_hoy):
                        self.mostrar_detalle_venta(ventas_hoy[indice])
            
            tree.bind("<Double-1>", ver_detalle_venta)
        
        # Botón cerrar
        ttk.Button(ventana_ventas, text="Cerrar", style='Danger.TButton',
                 command=ventana_ventas.destroy).pack(pady=10)
    
    def mostrar_detalle_venta(self, venta):
        """Mostrar detalles de una venta específica"""
        ventana_detalle = tk.Toplevel(self.root)
        ventana_detalle.title(f"Detalle de Venta - {venta['fecha']}")
        ventana_detalle.geometry("600x500")
        ventana_detalle.configure(bg="#F0F8FF")
        
        # Header
        header = tk.Frame(ventana_detalle, bg="#4169E1", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"📋 DETALLE DE VENTA - {venta['fecha'][:10]}",
                font=("Helvetica", 16, "bold"), bg="#4169E1", fg="white").pack(pady=15)
        
        # Frame principal
        main_frame = tk.Frame(ventana_detalle, bg="#F0F8FF")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Información general
        info_frame = tk.Frame(main_frame, bg="#E6F3FF", relief="solid", bd=1)
        info_frame.pack(fill="x", pady=10)
        
        tk.Label(info_frame, 
                text=f"📅 Fecha: {venta['fecha']}\n👤 Cliente: {venta['cliente']}\n👨‍💼 Vendedor: {venta['vendedor']}\n💰 Total: ${venta['total']:.2f}",
                font=("Helvetica", 12), bg="#E6F3FF", fg="black", justify="left").pack(padx=10, pady=10, anchor="w")
        
        # Productos vendidos
        tk.Label(main_frame, text="📦 Productos Vendidos:",
                font=("Helvetica", 14, "bold"), bg="#F0F8FF", fg="#2E8B57").pack(pady=10, anchor="w")
        
        # Treeview para productos
        tree_frame = tk.Frame(main_frame, bg="#F0F8FF")
        tree_frame.pack(fill="both", expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=("Producto", "Cantidad", "Precio", "Subtotal"), show="headings")
        
        # Configurar columnas
        tree.heading("Producto", text="Producto")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("Precio", text="Precio Unitario")
        tree.heading("Subtotal", text="Subtotal")
        
        tree.column("Producto", width=200, anchor="w")
        tree.column("Cantidad", width=80, anchor="center")
        tree.column("Precio", width=100, anchor="e")
        tree.column("Subtotal", width=100, anchor="e")
        
        # Insertar productos
        for key, cantidad in venta["productos"].items():
            if key in self.inventario:
                producto = self.inventario[key]
                subtotal = cantidad * producto["precio"]
                tree.insert("", "end", values=(
                    producto["nombre"],
                    f"{cantidad:.1f} {producto['unidad']}",
                    f"${producto['precio']:.2f}",
                    f"${subtotal:.2f}"
                ))
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        ttk.Button(ventana_detalle, text="Cerrar", style='Danger.TButton',
                 command=ventana_detalle.destroy).pack(pady=10)
    
    def gestion_inventario_admin(self):
        """Gestión de inventario para administradores"""
        ventana_inventario = tk.Toplevel(self.root)
        ventana_inventario.title("📦 Gestión de Inventario")
        ventana_inventario.geometry("1100x750")
        ventana_inventario.configure(bg="#F0F8FF")
        
        # Header
        header = tk.Frame(ventana_inventario, bg="#4169E1", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="📦 GESTIÓN DE INVENTARIO",
                font=("Helvetica", 18, "bold"), bg="#4169E1", fg="white").pack(pady=15)
        
        # Frame principal
        main_frame = tk.Frame(ventana_inventario, bg="#F0F8FF")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Panel de productos existentes
        productos_frame = tk.LabelFrame(main_frame, text="Productos Actuales", 
                                      font=("Helvetica", 14, "bold"), bg="#F0F8FF")
        productos_frame.pack(fill="both", expand=True)
        
        # Crear tabla editable con Treeview
        tree_frame = tk.Frame(productos_frame, bg="#F0F8FF")
        tree_frame.pack(fill="both", expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Stock", "Precio", "Unidad", "Estado"), show="headings")
        
        # Configurar columnas
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Stock", text="Stock")
        tree.heading("Precio", text="Precio")
        tree.heading("Unidad", text="Unidad")
        tree.heading("Estado", text="Estado")
        
        tree.column("ID", width=50, anchor="center")
        tree.column("Nombre", width=250, anchor="w")
        tree.column("Stock", width=100, anchor="center")
        tree.column("Precio", width=100, anchor="center")
        tree.column("Unidad", width=80, anchor="center")
        tree.column("Estado", width=120, anchor="center")
        
        # Insertar datos
        for i, (key, producto) in enumerate(self.inventario.items()):
            estado = "✅ Disponible" if producto["stock"] > 5 else "⚠️ Poco Stock" if producto["stock"] > 0 else "❌ Agotado"
            
            tree.insert("", "end", values=(
                i+1,
                producto["nombre"],
                f"{producto['stock']:.1f}",
                f"${producto['precio']:.2f}",
                producto["unidad"],
                estado
            ), tags=(key,))
        
        # Aplicar estilos a las filas
        for item in tree.get_children():
            values = tree.item(item, 'values')
            estado = values[5]
            if estado == "⚠️ Poco Stock":
                tree.tag_configure('warning', background='#FFFACD')
                tree.item(item, tags=('warning',))
            elif estado == "❌ Agotado":
                tree.tag_configure('danger', background='#FFE4E1')
                tree.item(item, tags=('danger',))
            else:
                tree.tag_configure('success', background='#F0FFF0')
                tree.item(item, tags=('success',))
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Panel de controles
        controles_frame = tk.Frame(main_frame, bg="#F0F8FF")
        controles_frame.pack(fill="x", pady=10)
        
        # Botón para editar producto seleccionado
        def editar_producto():
            item = tree.focus()
            if item:
                key = tree.item(item, 'tags')[0]
                self.editar_producto_admin(key, ventana_inventario)
        
        ttk.Button(controles_frame, text="✏️ Editar Producto Seleccionado",
                 style='Warning.TButton',
                 command=editar_producto).pack(side="left", padx=5)
        
        ttk.Button(controles_frame, text="➕ Agregar Nuevo Producto",
                 style='Success.TButton',
                 command=self.agregar_producto_admin).pack(side="left", padx=5)
        
        ttk.Button(controles_frame, text="Actualizar Vista",
                 style='Info.TButton',
                 command=lambda: self.actualizar_vista_inventario(tree, ventana_inventario)).pack(side="right", padx=5)
        
        ttk.Button(controles_frame, text="Cerrar",
                 style='Danger.TButton',
                 command=ventana_inventario.destroy).pack(side="right", padx=5)
    
    def actualizar_vista_inventario(self, tree, ventana):
        """Actualizar la vista del inventario"""
        for item in tree.get_children():
            tree.delete(item)
        
        for i, (key, producto) in enumerate(self.inventario.items()):
            estado = "✅ Disponible" if producto["stock"] > 5 else "⚠️ Poco Stock" if producto["stock"] > 0 else "❌ Agotado"
            
            tree.insert("", "end", values=(
                i+1,
                producto["nombre"],
                f"{producto['stock']:.1f}",
                f"${producto['precio']:.2f}",
                producto["unidad"],
                estado
            ), tags=(key,))
        
        # Reaplicar estilos
        for item in tree.get_children():
            values = tree.item(item, 'values')
            estado = values[5]
            if estado == "⚠️ Poco Stock":
                tree.item(item, tags=('warning',))
            elif estado == "❌ Agotado":
                tree.item(item, tags=('danger',))
            else:
                tree.item(item, tags=('success',))
    
    def editar_producto_admin(self, key, ventana_padre):
        """Editar producto existente"""
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title(f"Editar Producto: {self.inventario[key]['nombre']}")
        ventana_editar.geometry("500x400")
        ventana_editar.configure(bg="#F0F8FF")
        
        producto = self.inventario[key]
        
        # Header
        tk.Label(ventana_editar, text=f"✏️ EDITAR PRODUCTO: {producto['nombre']}",
                font=("Helvetica", 16, "bold"), bg="#F0F8FF", fg="#2E8B57").pack(pady=20)
        
        # Formulario
        form_frame = tk.Frame(ventana_editar, bg="#F0F8FF")
        form_frame.pack(padx=30, pady=20)
        
        # Nombre
        tk.Label(form_frame, text="Nombre del Producto:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        nombre_entry = ttk.Entry(form_frame, font=("Helvetica", 11), width=40)
        nombre_entry.pack(fill="x", pady=5)
        nombre_entry.insert(0, producto["nombre"])
        
        # Descripción
        tk.Label(form_frame, text="Descripción:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        desc_entry = ttk.Entry(form_frame, font=("Helvetica", 11), width=40)
        desc_entry.pack(fill="x", pady=5)
        desc_entry.insert(0, producto["descripcion"])
        
        # Stock y Precio
        stock_precio_frame = tk.Frame(form_frame, bg="#F0F8FF")
        stock_precio_frame.pack(fill="x", pady=5)
        
        tk.Label(stock_precio_frame, text="Stock:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(side="left", padx=5)
        stock_entry = ttk.Entry(stock_precio_frame, font=("Helvetica", 11), width=10)
        stock_entry.pack(side="left", padx=5)
        stock_entry.insert(0, str(producto["stock"]))
        
        tk.Label(stock_precio_frame, text="Precio:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(side="left", padx=5)
        precio_entry = ttk.Entry(stock_precio_frame, font=("Helvetica", 11), width=10)
        precio_entry.pack(side="left", padx=5)
        precio_entry.insert(0, str(producto["precio"]))
        
        # Unidad y Categoría
        unidad_cat_frame = tk.Frame(form_frame, bg="#F0F8FF")
        unidad_cat_frame.pack(fill="x", pady=5)
        
        tk.Label(unidad_cat_frame, text="Unidad:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(side="left", padx=5)
        unidad_entry = ttk.Entry(unidad_cat_frame, font=("Helvetica", 11), width=10)
        unidad_entry.pack(side="left", padx=5)
        unidad_entry.insert(0, producto["unidad"])
        
        tk.Label(unidad_cat_frame, text="Categoría:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(side="left", padx=5)
        categoria_entry = ttk.Entry(unidad_cat_frame, font=("Helvetica", 11), width=15)
        categoria_entry.pack(side="left", padx=5)
        categoria_entry.insert(0, producto.get("categoria", "otros"))
        
        # Botones
        botones_frame = tk.Frame(ventana_editar, bg="#F0F8FF")
        botones_frame.pack(pady=20)
        
        ttk.Button(botones_frame, text="Guardar Cambios", style='Success.TButton',
                 command=lambda: self.guardar_cambios_producto(
                     key, nombre_entry, desc_entry, stock_entry, 
                     precio_entry, unidad_entry, categoria_entry, 
                     ventana_editar, ventana_padre)).pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="Cancelar", style='Danger.TButton',
                 command=ventana_editar.destroy).pack(side="left", padx=10)
    
    def guardar_cambios_producto(self, key, nombre_entry, desc_entry, stock_entry, 
                               precio_entry, unidad_entry, categoria_entry, 
                               ventana_editar, ventana_padre):
        """Guardar cambios en el producto"""
        try:
            nombre = nombre_entry.get().strip()
            descripcion = desc_entry.get().strip()
            stock = float(stock_entry.get())
            precio = float(precio_entry.get())
            unidad = unidad_entry.get().strip()
            categoria = categoria_entry.get().strip()
            
            if not nombre or not descripcion:
                messagebox.showerror("Error", "Nombre y descripción son obligatorios")
                return
            
            if stock < 0 or precio <= 0:
                messagebox.showerror("Error", "Stock no puede ser negativo y precio debe ser mayor a 0")
                return
            
            # Actualizar producto
            self.inventario[key]["nombre"] = nombre
            self.inventario[key]["descripcion"] = descripcion
            self.inventario[key]["stock"] = stock
            self.inventario[key]["precio"] = precio
            self.inventario[key]["unidad"] = unidad
            self.inventario[key]["categoria"] = categoria
            
            self.guardar_datos()
            messagebox.showinfo("Producto Actualizado", "Los cambios se han guardado exitosamente")
            ventana_editar.destroy()
            
            # Actualizar la ventana principal de inventario
            if ventana_padre:
                self.actualizar_vista_inventario(ventana_padre.children['!labelframe'].children['!frame'].children['!treeview'], ventana_padre)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def agregar_producto_admin(self):
        """Agregar nuevo producto al inventario"""
        ventana_nuevo = tk.Toplevel(self.root)
        ventana_nuevo.title("Agregar Nuevo Producto")
        ventana_nuevo.geometry("500x400")
        ventana_nuevo.configure(bg="#F0F8FF")
        
        # Header
        tk.Label(ventana_nuevo, text="AGREGAR NUEVO PRODUCTO", font=("Helvetica", 16, "bold"),
                bg="#F0F8FF", fg="#2E8B57").pack(pady=20)
        
        # Formulario
        form_frame = tk.Frame(ventana_nuevo, bg="#F0F8FF")
        form_frame.pack(padx=50, pady=20)
        
        # Campos del formulario
        tk.Label(form_frame, text="Nombre del Producto:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        nombre_entry = ttk.Entry(form_frame, font=("Helvetica", 11), width=40)
        nombre_entry.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Descripción:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        desc_entry = ttk.Entry(form_frame, font=("Helvetica", 11), width=40)
        desc_entry.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Precio por Unidad:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        precio_entry = ttk.Entry(form_frame, font=("Helvetica", 11), width=40)
        precio_entry.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Stock Inicial:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        stock_entry = ttk.Entry(form_frame, font=("Helvetica", 11), width=40)
        stock_entry.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Unidad de Medida:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        unidad_entry = ttk.Entry(form_frame, font=("Helvetica", 11), width=40)
        unidad_entry.pack(fill="x", pady=5)
        unidad_entry.insert(0, "kg")
        
        tk.Label(form_frame, text="Categoría:", font=("Helvetica", 11, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        categoria_entry = ttk.Entry(form_frame, font=("Helvetica", 11), width=40)
        categoria_entry.pack(fill="x", pady=5)
        categoria_entry.insert(0, "otros")
        
        # Botones
        botones_frame = tk.Frame(ventana_nuevo, bg="#F0F8FF")
        botones_frame.pack(pady=30)
        
        ttk.Button(botones_frame, text="Agregar Producto", style='Success.TButton',
                 command=lambda: self.guardar_nuevo_producto(
                     nombre_entry, desc_entry, precio_entry, 
                     stock_entry, unidad_entry, categoria_entry, ventana_nuevo)).pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="Cancelar", style='Danger.TButton',
                 command=ventana_nuevo.destroy).pack(side="left", padx=10)
    
    def guardar_nuevo_producto(self, nombre_entry, desc_entry, precio_entry, 
                             stock_entry, unidad_entry, categoria_entry, ventana):
        """Guardar nuevo producto en el inventario"""
        try:
            nombre = nombre_entry.get().strip()
            descripcion = desc_entry.get().strip()
            precio = float(precio_entry.get())
            stock = float(stock_entry.get())
            unidad = unidad_entry.get().strip()
            categoria = categoria_entry.get().strip()
            
            if not nombre or not descripcion:
                messagebox.showerror("Error", "Nombre y descripción son obligatorios")
                return
            
            if precio <= 0 or stock < 0:
                messagebox.showerror("Error", "Precio debe ser mayor a 0 y stock no puede ser negativo")
                return
            
            # Crear clave única para el producto
            key = nombre.lower().replace(" ", "_").replace("ñ", "n")
            contador = 1
            key_original = key
            while key in self.inventario:
                key = f"{key_original}_{contador}"
                contador += 1
            
            # Agregar producto
            self.inventario[key] = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
                "unidad": unidad,
                "categoria": categoria
            }
            
            self.guardar_datos()
            messagebox.showinfo("Producto Agregado", f"El producto '{nombre}' ha sido agregado exitosamente")
            ventana.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Valores numéricos inválidos")
    
    def reportes_ventas_admin(self):
        """Reportes de ventas para administradores"""
        ventana_reportes = tk.Toplevel(self.root)
        ventana_reportes.title("📊 Reportes de Ventas")
        ventana_reportes.geometry("1100x750")
        ventana_reportes.configure(bg="#F0F8FF")
        
        # Header
        header = tk.Frame(ventana_reportes, bg="#228B22", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="📊 REPORTES DE VENTAS",
                font=("Helvetica", 18, "bold"), bg="#228B22", fg="white").pack(pady=15)
        
        # Notebook para diferentes reportes
        notebook = ttk.Notebook(ventana_reportes)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Reporte del día
        dia_frame = tk.Frame(notebook, bg="#F0F8FF")
        notebook.add(dia_frame, text="Ventas del Día")
        
        self.crear_reporte_dia(dia_frame)
        
        # Reporte semanal
        semana_frame = tk.Frame(notebook, bg="#F0F8FF")
        notebook.add(semana_frame, text="Resumen Semanal")
        
        self.crear_reporte_resumen(semana_frame)
        
        # Productos más vendidos
        productos_frame = tk.Frame(notebook, bg="#F0F8FF")
        notebook.add(productos_frame, text="Productos Populares")
        
        self.crear_reporte_productos(productos_frame)
        
        # Botón cerrar
        ttk.Button(ventana_reportes, text="Cerrar", style='Danger.TButton',
                 command=ventana_reportes.destroy).pack(pady=10)
    
    def crear_reporte_dia(self, parent):
        """Crear reporte del día"""
        hoy = datetime.now().strftime("%Y-%m-%d")
        ventas_hoy = [v for v in self.historial_ventas if v["fecha"].startswith(hoy)]
        
        # Estadísticas generales
        stats_frame = tk.Frame(parent, bg="#FFD700", relief="raised", bd=2)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        if ventas_hoy:
            total_ventas = len(ventas_hoy)
            total_monto = sum(v["total"] for v in ventas_hoy)
            promedio = total_monto / total_ventas
            
            stats_text = f"📅 RESUMEN DEL DÍA ({datetime.now().strftime('%d/%m/%Y')})\n"
            stats_text += f"Total de Ventas: {total_ventas} | Monto Total: ${total_monto:.2f} | Promedio por Venta: ${promedio:.2f}"
        else:
            stats_text = "No hay ventas registradas para el día de hoy"
        
        tk.Label(stats_frame, text=stats_text, font=("Helvetica", 12, "bold"),
                bg="#FFD700", fg="black", justify="center").pack(pady=10)
        
        # Lista detallada de ventas
        if ventas_hoy:
            ventas_scroll_frame = tk.Frame(parent, bg="#F0F8FF")
            ventas_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            # Usar Treeview para mejor visualización
            tree = ttk.Treeview(ventas_scroll_frame, columns=("ID", "Hora", "Vendedor", "Total"), show="headings")
            
            # Configurar columnas
            tree.heading("ID", text="ID")
            tree.heading("Hora", text="Hora")
            tree.heading("Vendedor", text="Vendedor")
            tree.heading("Total", text="Total")
            
            tree.column("ID", width=50, anchor="center")
            tree.column("Hora", width=100, anchor="center")
            tree.column("Vendedor", width=200, anchor="w")
            tree.column("Total", width=100, anchor="e")
            
            # Insertar datos
            for i, venta in enumerate(ventas_hoy):
                tree.insert("", "end", values=(
                    i+1,
                    venta["fecha"][11:19],  # Solo la hora
                    venta["vendedor"],
                    f"${venta['total']:.2f}"
                ))
            
            # Agregar scrollbar
            scrollbar = ttk.Scrollbar(ventas_scroll_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Función para ver detalles de la venta seleccionada
            def ver_detalle_venta(event):
                item = tree.focus()
                if item:
                    valores = tree.item(item, 'values')
                    indice = int(valores[0]) - 1
                    if 0 <= indice < len(ventas_hoy):
                        self.mostrar_detalle_venta(ventas_hoy[indice])
            
            tree.bind("<Double-1>", ver_detalle_venta)
    
    def crear_reporte_resumen(self, parent):
        """Crear reporte resumen"""
        # Cálculos de estadísticas
        if not self.historial_ventas:
            tk.Label(parent, text="No hay datos de ventas disponibles",
                    font=("Helvetica", 14), bg="#F0F8FF", fg="gray").pack(pady=50)
            return
        
        # Estadísticas generales
        total_ventas = len(self.historial_ventas)
        total_monto = sum(v["total"] for v in self.historial_ventas)
        promedio_venta = total_monto / total_ventas if total_ventas > 0 else 0
        
        # Ventas por día (últimos 7 días)
        ventas_por_dia = defaultdict(lambda: {"count": 0, "total": 0})
        
        for venta in self.historial_ventas:
            fecha = venta["fecha"][:10]  # Solo la fecha, sin hora
            ventas_por_dia[fecha]["count"] += 1
            ventas_por_dia[fecha]["total"] += venta["total"]
        
        # Frame de estadísticas
        stats_frame = tk.LabelFrame(parent, text="Estadísticas Generales", 
                                  font=("Helvetica", 14, "bold"), bg="#F0F8FF")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        stats_text = f"""
📊 RESUMEN GENERAL DE VENTAS

Total de Ventas Registradas: {total_ventas}
Monto Total Vendido: ${total_monto:.2f}
Promedio por Venta: ${promedio_venta:.2f}
Días con Ventas: {len(ventas_por_dia)}
        """
        
        tk.Label(stats_frame, text=stats_text, font=("Helvetica", 12),
                bg="#F0F8FF", fg="black", justify="left").pack(padx=20, pady=10)
        
        # Ventas por día
        dias_frame = tk.LabelFrame(parent, text="Ventas por Día", 
                                 font=("Helvetica", 14, "bold"), bg="#F0F8FF")
        dias_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if ventas_por_dia:
            # Usar Treeview para mejor visualización
            tree = ttk.Treeview(dias_frame, columns=("Fecha", "Ventas", "Monto Total"), show="headings")
            
            # Configurar columnas
            tree.heading("Fecha", text="Fecha")
            tree.heading("Ventas", text="N° Ventas")
            tree.heading("Monto Total", text="Monto Total")
            
            tree.column("Fecha", width=150, anchor="center")
            tree.column("Ventas", width=100, anchor="center")
            tree.column("Monto Total", width=150, anchor="e")
            
            # Insertar datos ordenados por fecha (más reciente primero)
            for fecha, datos in sorted(ventas_por_dia.items(), reverse=True):
                fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
                tree.insert("", "end", values=(
                    fecha_formateada,
                    datos["count"],
                    f"${datos['total']:.2f}"
                ))
            
            # Agregar scrollbar
            scrollbar = ttk.Scrollbar(dias_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
    
    def crear_reporte_productos(self, parent):
        """Crear reporte de productos más vendidos"""
        if not self.historial_ventas:
            tk.Label(parent, text="No hay datos de ventas disponibles",
                    font=("Helvetica", 14), bg="#F0F8FF", fg="gray").pack(pady=50)
            return
        
        # Contar productos vendidos
        productos_vendidos = defaultdict(lambda: {"cantidad": 0, "total": 0, "veces": 0})
        
        for venta in self.historial_ventas:
            for prod_key, cantidad in venta["productos"].items():
                if prod_key in self.inventario:
                    producto = self.inventario[prod_key]
                    productos_vendidos[prod_key]["cantidad"] += cantidad
                    productos_vendidos[prod_key]["total"] += cantidad * producto["precio"]
                    productos_vendidos[prod_key]["veces"] += 1
        
        # Ordenar por cantidad vendida
        productos_ordenados = sorted(productos_vendidos.items(), 
                                   key=lambda x: x[1]["cantidad"], reverse=True)
        
        # Frame de productos populares
        populares_frame = tk.LabelFrame(parent, text="Productos Más Vendidos", 
                                      font=("Helvetica", 14, "bold"), bg="#F0F8FF")
        populares_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if productos_ordenados:
            # Usar Treeview para mejor visualización
            tree = ttk.Treeview(populares_frame, columns=("Producto", "Cantidad", "Monto", "Veces"), show="headings")
            
            # Configurar columnas
            tree.heading("Producto", text="Producto")
            tree.heading("Cantidad", text="Cantidad Vendida")
            tree.heading("Monto", text="Monto Total")
            tree.heading("Veces", text="Veces Vendido")
            
            tree.column("Producto", width=250, anchor="w")
            tree.column("Cantidad", width=150, anchor="center")
            tree.column("Monto", width=150, anchor="e")
            tree.column("Veces", width=100, anchor="center")
            
            # Insertar datos
            for prod_key, datos in productos_ordenados:
                if prod_key in self.inventario:
                    producto = self.inventario[prod_key]
                    tree.insert("", "end", values=(
                        producto["nombre"],
                        f"{datos['cantidad']:.1f} {producto['unidad']}",
                        f"${datos['total']:.2f}",
                        datos["veces"]
                    ))
            
            # Agregar scrollbar
            scrollbar = ttk.Scrollbar(populares_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
    
    def gestion_usuarios_admin(self):
        """Gestión de usuarios para administradores"""
        ventana_usuarios = tk.Toplevel(self.root)
        ventana_usuarios.title("👥 Gestión de Usuarios")
        ventana_usuarios.geometry("900x650")
        ventana_usuarios.configure(bg="#F0F8FF")
        
        # Header
        header = tk.Frame(ventana_usuarios, bg="#FF8C00", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="👥 GESTIÓN DE USUARIOS",
                font=("Helvetica", 18, "bold"), bg="#FF8C00", fg="white").pack(pady=15)
        
        # Frame principal
        main_frame = tk.Frame(ventana_usuarios, bg="#F0F8FF")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Lista de usuarios actuales
        usuarios_frame = tk.LabelFrame(main_frame, text="Usuarios del Sistema", 
                                     font=("Helvetica", 14, "bold"), bg="#F0F8FF")
        usuarios_frame.pack(fill="both", expand=True)
        
        # Usar Treeview para mejor visualización
        tree = ttk.Treeview(usuarios_frame, columns=("Usuario", "Nombre", "Rol"), show="headings")
        
        # Configurar columnas
        tree.heading("Usuario", text="Usuario")
        tree.heading("Nombre", text="Nombre Completo")
        tree.heading("Rol", text="Rol")
        
        tree.column("Usuario", width=150, anchor="w")
        tree.column("Nombre", width=250, anchor="w")
        tree.column("Rol", width=100, anchor="center")
        
        # Insertar datos
        for usuario, datos in self.usuarios_sistema.items():
            tree.insert("", "end", values=(
                usuario,
                datos["nombre"],
                datos["role"]
            ), tags=(usuario,))
        
        # Aplicar estilos a las filas
        for item in tree.get_children():
            values = tree.item(item, 'values')
            rol = values[2]
            if rol == "admin":
                tree.tag_configure('admin', background='#E6F3FF')
                tree.item(item, tags=('admin',))
            else:
                tree.tag_configure('empleado', background='#FFFFFF')
                tree.item(item, tags=('empleado',))
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(usuarios_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Panel de controles
        controles_frame = tk.Frame(main_frame, bg="#F0F8FF")
        controles_frame.pack(fill="x", pady=10)
        
        # Función para editar usuario seleccionado
        def editar_usuario():
            item = tree.focus()
            if item:
                usuario = tree.item(item, 'tags')[0]
                self.editar_usuario_admin(usuario, ventana_usuarios)
        
        ttk.Button(controles_frame, text="✏️ Editar Usuario Seleccionado",
                 style='Warning.TButton',
                 command=editar_usuario).pack(side="left", padx=5)
        
        ttk.Button(controles_frame, text="➕ Agregar Nuevo Usuario",
                 style='Success.TButton',
                 command=self.agregar_usuario_admin).pack(side="left", padx=5)
        
        # Función para eliminar usuario seleccionado
        def eliminar_usuario():
            item = tree.focus()
            if item:
                usuario = tree.item(item, 'tags')[0]
                if usuario != self.usuario_actual:  # No permitir eliminar el usuario actual
                    self.eliminar_usuario_admin(usuario, ventana_usuarios)
                else:
                    messagebox.showwarning("Error", "No puede eliminar su propio usuario mientras está conectado")
        
        ttk.Button(controles_frame, text="🗑️ Eliminar Usuario",
                 style='Danger.TButton',
                 command=eliminar_usuario).pack(side="left", padx=5)
        
        ttk.Button(controles_frame, text="Actualizar Vista",
                 style='Info.TButton',
                 command=lambda: self.actualizar_vista_usuarios(tree)).pack(side="right", padx=5)
        
        ttk.Button(controles_frame, text="Cerrar",
                 style='Danger.TButton',
                 command=ventana_usuarios.destroy).pack(side="right", padx=5)
    
    def actualizar_vista_usuarios(self, tree):
        """Actualizar la vista de usuarios"""
        for item in tree.get_children():
            tree.delete(item)
        
        for usuario, datos in self.usuarios_sistema.items():
            tree.insert("", "end", values=(
                usuario,
                datos["nombre"],
                datos["role"]
            ), tags=(usuario,))
        
        # Reaplicar estilos
        for item in tree.get_children():
            values = tree.item(item, 'values')
            rol = values[2]
            if rol == "admin":
                tree.item(item, tags=('admin',))
            else:
                tree.item(item, tags=('empleado',))
    
    def editar_usuario_admin(self, usuario, ventana_padre=None):
        """Editar usuario existente"""
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title(f"Editar Usuario: {usuario}")
        ventana_editar.geometry("500x400")
        ventana_editar.configure(bg="#F0F8FF")
        
        # Datos actuales del usuario
        datos_usuario = self.usuarios_sistema[usuario]
        
        # Formulario
        tk.Label(ventana_editar, text=f"EDITAR USUARIO: {usuario}", font=("Helvetica", 16, "bold"),
                bg="#F0F8FF", fg="#2E8B57").pack(pady=20)
        
        form_frame = tk.Frame(ventana_editar, bg="#F0F8FF")
        form_frame.pack(padx=30, pady=20)
        
        tk.Label(form_frame, text="Nombre Completo:", font=("Helvetica", 12, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        nombre_entry = ttk.Entry(form_frame, font=("Helvetica", 12), width=30)
        nombre_entry.pack(fill="x", pady=5)
        nombre_entry.insert(0, datos_usuario["nombre"])
        
        tk.Label(form_frame, text="Contraseña:", font=("Helvetica", 12, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        password_entry = ttk.Entry(form_frame, font=("Helvetica", 12), width=30, show="*")
        password_entry.pack(fill="x", pady=5)
        password_entry.insert(0, datos_usuario["password"])
        
        tk.Label(form_frame, text="Rol:", font=("Helvetica", 12, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        
        role_var = tk.StringVar(value=datos_usuario["role"])
        ttk.Radiobutton(form_frame, text="Empleado", variable=role_var, value="empleado",
                       style='Toolbutton').pack(anchor="w")
        ttk.Radiobutton(form_frame, text="Administrador", variable=role_var, value="admin",
                       style='Toolbutton').pack(anchor="w")
        
        # Botones
        botones_frame = tk.Frame(ventana_editar, bg="#F0F8FF")
        botones_frame.pack(pady=20)
        
        ttk.Button(botones_frame, text="Guardar Cambios", style='Success.TButton',
                 command=lambda: self.guardar_edicion_usuario(
                     usuario, nombre_entry, password_entry, 
                     role_var, ventana_editar, ventana_padre)).pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="Cancelar", style='Danger.TButton',
                 command=ventana_editar.destroy).pack(side="left", padx=10)
    
    def guardar_edicion_usuario(self, usuario, nombre_entry, password_entry, role_var, ventana_editar, ventana_padre=None):
        """Guardar cambios en usuario"""
        try:  
            nombre = nombre_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get()
            
            if not nombre or not password:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Actualizar usuario
            self.usuarios_sistema[usuario] = {
                "nombre": nombre,
                "password": password,
                "role": role
            }
            
            self.guardar_datos()
            messagebox.showinfo("Usuario Actualizado", f"Usuario '{usuario}' actualizado exitosamente")
            ventana_editar.destroy()
            
            # Actualizar la ventana principal de usuarios si existe
            if ventana_padre:
                tree = ventana_padre.children['!labelframe'].children['!treeview']
                self.actualizar_vista_usuarios(tree)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar usuario: {str(e)}")
    
    def eliminar_usuario_admin(self, usuario, ventana_padre):
        """Eliminar usuario del sistema"""
        respuesta = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de eliminar el usuario '{usuario}'?\n\nEsta acción no se puede deshacer.")
        
        if respuesta:
            del self.usuarios_sistema[usuario]
            self.guardar_datos()
            messagebox.showinfo("Usuario Eliminado", f"Usuario '{usuario}' eliminado exitosamente")
            ventana_padre.destroy()
            self.gestion_usuarios_admin()  # Refrescar ventana
    
    def agregar_usuario_admin(self):
        """Agregar nuevo usuario al sistema"""
        ventana_nuevo = tk.Toplevel(self.root)
        ventana_nuevo.title("Agregar Nuevo Usuario")
        ventana_nuevo.geometry("500x400")
        ventana_nuevo.configure(bg="#F0F8FF")
        
        # Header
        tk.Label(ventana_nuevo, text="AGREGAR NUEVO USUARIO", font=("Helvetica", 16, "bold"),
                bg="#F0F8FF", fg="#2E8B57").pack(pady=20)
        
        # Formulario
        form_frame = tk.Frame(ventana_nuevo, bg="#F0F8FF")
        form_frame.pack(padx=30, pady=20)
        
        tk.Label(form_frame, text="Nombre de Usuario:", font=("Helvetica", 12, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        usuario_entry = ttk.Entry(form_frame, font=("Helvetica", 12), width=30)
        usuario_entry.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Nombre Completo:", font=("Helvetica", 12, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        nombre_entry = ttk.Entry(form_frame, font=("Helvetica", 12), width=30)
        nombre_entry.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Contraseña:", font=("Helvetica", 12, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        password_entry = ttk.Entry(form_frame, font=("Helvetica", 12), width=30, show="*")
        password_entry.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Rol:", font=("Helvetica", 12, "bold"),
                bg="#F0F8FF").pack(anchor="w", pady=5)
        
        role_var = tk.StringVar(value="empleado")
        ttk.Radiobutton(form_frame, text="Empleado", variable=role_var, value="empleado",
                       style='Toolbutton').pack(anchor="w")
        ttk.Radiobutton(form_frame, text="Administrador", variable=role_var, value="admin",
                       style='Toolbutton').pack(anchor="w")
        
        # Botones
        botones_frame = tk.Frame(ventana_nuevo, bg="#F0F8FF")
        botones_frame.pack(pady=20)
        
        ttk.Button(botones_frame, text="Crear Usuario", style='Success.TButton',
                 command=lambda: self.guardar_nuevo_usuario(
                     usuario_entry, nombre_entry, password_entry, 
                     role_var, ventana_nuevo)).pack(side="left", padx=10)
        
        ttk.Button(botones_frame, text="Cancelar", style='Danger.TButton',
                 command=ventana_nuevo.destroy).pack(side="left", padx=10)
    
    def guardar_nuevo_usuario(self, usuario_entry, nombre_entry, password_entry, role_var, ventana):
        """Guardar nuevo usuario en el sistema"""
        try:
            usuario = usuario_entry.get().strip().lower()
            nombre = nombre_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get()
            
            if not usuario or not nombre or not password:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if usuario in self.usuarios_sistema:
                messagebox.showerror("Error", "El nombre de usuario ya existe")
                return
            
            # Crear nuevo usuario
            self.usuarios_sistema[usuario] = {
                "nombre": nombre,
                "password": password,
                "role": role
            }
            
            self.guardar_datos()
            messagebox.showinfo("Usuario Creado", f"Usuario '{usuario}' creado exitosamente")
            ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {str(e)}")
    
    def respaldo_datos_admin(self):
        """Opciones de respaldo de datos"""
        ventana_respaldo = tk.Toplevel(self.root)
        ventana_respaldo.title("💾 Respaldo de Datos")
        ventana_respaldo.geometry("700x500")
        ventana_respaldo.configure(bg="#F0F8FF")
        
        # Header
        header = tk.Frame(ventana_respaldo, bg="#800080", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="💾 RESPALDO DE DATOS",
                font=("Helvetica", 18, "bold"), bg="#800080", fg="white").pack(pady=15)
        
        # Opciones de respaldo
        opciones_frame = tk.Frame(ventana_respaldo, bg="#F0F8FF")
        opciones_frame.pack(expand=True)
        
        tk.Label(opciones_frame, text="OPCIONES DE RESPALDO", font=("Helvetica", 16, "bold"),
                bg="#F0F8FF", fg="#800080").pack(pady=30)
        
        # Botones de opciones
        ttk.Button(opciones_frame, text="📤\nEXPORTAR DATOS\nGuardar copia de seguridad",
                 style='Success.TButton',
                 width=25, command=self.exportar_datos).pack(pady=15)
        
        ttk.Button(opciones_frame, text="📥\nIMPORTAR DATOS\nCargar desde archivo",
                 style='Info.TButton',
                 width=25, command=self.importar_datos).pack(pady=15)
        
        ttk.Button(opciones_frame, text="🗄️\nVER ESTADÍSTICAS\nInformación del sistema",
                 style='Warning.TButton',
                 width=25, command=self.ver_estadisticas_sistema).pack(pady=15)
        
        ttk.Button(opciones_frame, text="❌\nCERRAR\nVolver al menú",
                 style='Danger.TButton',
                 width=25, command=ventana_respaldo.destroy).pack(pady=15)
    
    def exportar_datos(self):
        """Exportar datos del sistema"""
        try:
            from datetime import datetime
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            datos_completos = {
                "inventario": self.inventario,
                "historial_ventas": self.historial_ventas,
                "usuarios_sistema": self.usuarios_sistema,
                "fecha_respaldo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0"
            }
            
            # Preguntar dónde guardar el archivo
            archivo = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
                initialfile=f"respaldo_tortilleria_{fecha}.json"
            )
            
            if not archivo:  # Usuario canceló
                return
            
            # Guardar como JSON
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_completos, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Exportación Exitosa", 
                              f"Datos exportados exitosamente en:\n{archivo}")
            
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Error al exportar datos: {str(e)}")
    
    def importar_datos(self):
        """Importar datos al sistema"""
        try:
            archivo = filedialog.askopenfilename(
                title="Seleccionar archivo de respaldo",
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
            )
            
            if not archivo:
                return
            
            # Confirmar importación
            respuesta = messagebox.askyesno("Confirmar Importación", 
                                          "¿Está seguro de importar los datos?\n\nEsto sobrescribirá todos los datos actuales.")
            
            if not respuesta:
                return
            
            # Cargar datos
            with open(archivo, 'r', encoding='utf-8') as f:
                datos_importados = json.load(f)
            
            # Validar estructura
            if not all(key in datos_importados for key in ["inventario", "historial_ventas", "usuarios_sistema"]):
                messagebox.showerror("Error", "Archivo de respaldo inválido")
                return
            
            # Importar datos
            self.inventario = datos_importados["inventario"]
            self.historial_ventas = datos_importados["historial_ventas"]
            self.usuarios_sistema = datos_importados["usuarios_sistema"]
            
            # Guardar datos importados
            self.guardar_datos()
            
            messagebox.showinfo("Importación Exitosa", 
                              f"Datos importados exitosamente desde:\n{archivo}")
            
        except Exception as e:
            messagebox.showerror("Error de Importación", f"Error al importar datos: {str(e)}")
    
    def ver_estadisticas_sistema(self):
        """Ver estadísticas del sistema"""
        ventana_stats = tk.Toplevel(self.root)
        ventana_stats.title("🗄️ Estadísticas del Sistema")
        ventana_stats.geometry("800x600")
        ventana_stats.configure(bg="#F0F8FF")
        
        # Header
        header = tk.Frame(ventana_stats, bg="#FF8C00", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🗄️ ESTADÍSTICAS DEL SISTEMA",
                font=("Helvetica", 18, "bold"), bg="#FF8C00", fg="white").pack(pady=15)
        
        # Calcular estadísticas
        total_productos = len(self.inventario)
        total_usuarios = len(self.usuarios_sistema)
        total_ventas = len(self.historial_ventas)
        
        productos_agotados = sum(1 for p in self.inventario.values() if p["stock"] == 0)
        productos_poco_stock = sum(1 for p in self.inventario.values() if 0 < p["stock"] <= 5)
        
        valor_inventario = sum(p["stock"] * p["precio"] for p in self.inventario.values())
        monto_total_ventas = sum(v["total"] for v in self.historial_ventas)
        
        # Mostrar estadísticas en un Treeview
        tree_frame = tk.Frame(ventana_stats, bg="#F0F8FF")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tree = ttk.Treeview(tree_frame, columns=("Categoría", "Valor"), show="headings")
        
        # Configurar columnas
        tree.heading("Categoría", text="Categoría")
        tree.heading("Valor", text="Valor")
        
        tree.column("Categoría", width=300, anchor="w")
        tree.column("Valor", width=200, anchor="w")
        
        # Insertar datos
        tree.insert("", "end", values=("🏪 INVENTARIO", ""))
        tree.insert("", "end", values=("   • Total de Productos", total_productos))
        tree.insert("", "end", values=("   • Productos Agotados", productos_agotados))
        tree.insert("", "end", values=("   • Productos con Poco Stock (≤5)", productos_poco_stock))
        tree.insert("", "end", values=("   • Valor Total del Inventario", f"${valor_inventario:.2f}"))
        
        tree.insert("", "end", values=("👥 USUARIOS", ""))
        tree.insert("", "end", values=("   • Total de Usuarios", total_usuarios))
        tree.insert("", "end", values=("   • Administradores", sum(1 for u in self.usuarios_sistema.values() if u['role'] == 'admin')))
        tree.insert("", "end", values=("   • Empleados", sum(1 for u in self.usuarios_sistema.values() if u['role'] == 'empleado')))
        
        tree.insert("", "end", values=("💰 VENTAS", ""))
        tree.insert("", "end", values=("   • Total de Ventas Registradas", total_ventas))
        tree.insert("", "end", values=("   • Monto Total Vendido", f"${monto_total_ventas:.2f}"))
        tree.insert("", "end", values=("   • Promedio por Venta", f"${(monto_total_ventas/total_ventas):.2f if total_ventas > 0 else 0}"))
        
        tree.insert("", "end", values=("📅 SISTEMA", ""))
        tree.insert("", "end", values=("   • Fecha Actual", datetime.now().strftime("%d/%m/%Y %H:%M")))
        tree.insert("", "end", values=("   • Usuario Actual", f"{self.usuario_actual} ({self.usuarios_sistema[self.usuario_actual]['role']})"))
        tree.insert("", "end", values=("   • Versión del Sistema", "2.0"))
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        ttk.Button(ventana_stats, text="Cerrar", style='Danger.TButton',
                 command=ventana_stats.destroy).pack(pady=10)
    
    def cerrar_sesion(self):
        """Cerrar sesión actual"""
        respuesta = messagebox.askyesno("Cerrar Sesión", "¿Está seguro de cerrar la sesión actual?")
        if respuesta:
            self.usuario_actual = None
            self.crear_pantalla_bienvenida()
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()


# Ejecutar la aplicación
if __name__ == "__main__":
    app = TortilleriaApp()
    app.ejecutar ()