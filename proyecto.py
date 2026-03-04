import os
import hashlib
import getpass

# --- SISTEMA DE USUARIOS ---
class Usuario:
    def _init_(self, nombre_usuario, contrasena_encriptada):
        self.nombre_usuario = nombre_usuario
        self.contrasena_encriptada = contrasena_encriptada

    def a_csv(self):
        return f"{self.nombre_usuario},{self.contrasena_encriptada}\n"

class GestorUsuarios:
    def _init_(self, archivo="usuarios_pro.txt"):
        self.archivo = archivo
        self.usuarios = {}
        self._cargar_datos()

    def _encriptar_contrasena(self, contrasena):
        return hashlib.sha256(contrasena.encode()).hexdigest()

    def _cargar_datos(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as f:
                    for linea in f:
                        parts = linea.strip().split(",")
                        if len(parts) == 2:
                            usuario, contrasena = parts
                            self.usuarios[usuario] = Usuario(usuario, contrasena)
            except: pass

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            f.writelines(usuario.a_csv() for usuario in self.usuarios.values())

    def registrar(self, nombre_usuario, contrasena):
        if nombre_usuario in self.usuarios:
            print(f"El usuario '{nombre_usuario}' ya existe.")
            return False
        if not nombre_usuario.strip() or not contrasena.strip():
            print("Usuario y contraseña no pueden estar vacíos.")
            return False
            
        contrasena_encriptada = self._encriptar_contrasena(contrasena)
        self.usuarios[nombre_usuario] = Usuario(nombre_usuario, contrasena_encriptada)
        self.guardar()
        print(f"Usuario '{nombre_usuario}' registrado exitosamente.")
        return True

    def autenticar(self, nombre_usuario, contrasena):
        if nombre_usuario not in self.usuarios:
            print("Usuario no encontrado.")
            return False
            
        usuario = self.usuarios[nombre_usuario]
        if usuario.contrasena_encriptada == self._encriptar_contrasena(contrasena):
            return True
        else:
            print("Contraseña incorrecta.")
            return False

# --- CLASE BASE (Herencia) ---
class Item:
    def _init_(self, codigo, nombre):
        self.codigo = codigo 
        self.nombre = nombre.strip().title()

# --- CLASE DERIVADA ---
class Producto(Item):
    def _init_(self, codigo, nombre, precio, cantidad):
        super()._init_(codigo, nombre)
        self.precio = precio
        self.cantidad = cantidad

    @property
    def precio(self): return self._precio

    @precio.setter
    def precio(self, valor):
        if float(valor) < 0: raise ValueError("Precio negativo no permitido.")
        self._precio = float(valor)

    @property
    def cantidad(self): return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if int(valor) < 0: raise ValueError("Stock negativo no permitido.")
        self._cantidad = int(valor)

    def _str_(self):
        return f"ID: {self.codigo:<10} | {self.nombre:<15} | ${self.precio:>8.2f} | Stock: {self.cantidad:>4}"

    def a_csv(self):
        return f"{self.codigo},{self.nombre},{self.precio},{self.cantidad}\n"

# --- CAPTURA Y VALIDACIÓN ESTRICTA ---
def solicitar_solo_numeros(mensaje, permitir_decimal=False):
    while True:
        try:
            entrada = input(mensaje).strip()
            valor = float(entrada) if permitir_decimal else int(entrada)
            if valor >= 0:
                return entrada if not permitir_decimal else valor
            print("Error: No se permiten números negativos.")
        except ValueError:
            print("Error: Ingrese un número válido.")

# --- LÓGICA DE INVENTARIO ---
class Inventario:
    def _init_(self, nombre_archivo="inventario_pro.txt"):
        self.archivo = nombre_archivo
        self.productos = {}
        self._cargar_datos()

    def _cargar_datos(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as f:
                    for linea in f:
                        parts = linea.strip().split(",")
                        if len(parts) == 4:
                            codigo, nombre, precio, cantidad = parts
                            self.productos[codigo] = Producto(codigo, nombre, float(precio), int(cantidad))
            except: pass

    def agregar(self, codigo, nombre, precio, cantidad):
        if codigo in self.productos:
            print(f"❌ El código {codigo} ya existe para: {self.productos[codigo].nombre}")
            return
        self.productos[codigo] = Producto(codigo, nombre, precio, cantidad)
        print(f"✅ Registrado: {nombre}")

    def borrar(self, codigo):
        if self.productos.pop(codigo, None):
            print(f"🗑️ Producto {codigo} eliminado.")
        else:
            print("❌ Código no encontrado.")

    # --- NUEVA FUNCIÓN DE BÚSQUEDA ---
    def buscar(self, criterio):
        """Busca por código exacto o coincidencia parcial en el nombre."""
        encontrados = []
        criterio = criterio.lower().strip()
        
        for producto in self.productos.values():
            if criterio == producto.codigo or criterio in producto.nombre.lower():
                encontrados.append(producto)
        return encontrados

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            f.writelines(producto.a_csv() for producto in self.productos.values())

# --- SISTEMA DE AUTENTICACIÓN (NUEVO MENÚ) ---
def menu_auth():
    gestor = GestorUsuarios()
    
    while True:
        print(f"\n{'='*15} SISTEMA DE AUTENTICACIÓN {'='*15}")
        print("1. Iniciar Sesión | 2. Registrarse | 3. Salir")
        opc = input("Seleccione: ").strip()

        if opc == "1":
            print("\n--- INICIAR SESIÓN ---")
            usuario = input("Usuario: ").strip()
            contrasena = getpass.getpass("Contraseña: ").strip()
            
            if gestor.autenticar(usuario, contrasena):
                print(f"\n¡Bienvenido/a, {usuario}!")
                menu(usuario) # Pasar al menú principal de inventario
            
        elif opc == "2":
            print("\n--- REGISTRO DE USUARIO ---")
            nuevo_usuario = input("Nuevo usuario: ").strip()
            nueva_contrasena = getpass.getpass("Nueva contraseña: ").strip()
            contrasena_confirmacion = getpass.getpass("Confirmar contraseña: ").strip()
            
            if nueva_contrasena == contrasena_confirmacion:
                gestor.registrar(nuevo_usuario, nueva_contrasena)
            else:
                print("Las contraseñas no coinciden.")
                
        elif opc == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

# --- MENÚ PRINCIPAL ---
def menu(usuario_actual):
    inv = Inventario()
    
    while True:
        print(f"\n{'='*15} GESTIÓN NUMÉRICA - Usuario: {usuario_actual} {'='*15}")
        print("1. Agregar | 2. Ver Todo | 3. Buscar | 4. Borrar | 5. Salir")
        opc = input("Seleccione: ")

        if opc == "1":
            codigo = solicitar_solo_numeros("Código (solo números): ")
            nombre = input("Nombre del producto: ")
            precio = solicitar_solo_numeros("Precio: ", permitir_decimal=True)
            cantidad = solicitar_solo_numeros("Cantidad (Stock): ")
            inv.agregar(codigo, nombre, precio, cantidad)

        elif opc == "2":
            print("\n" + "="*50)
            if not inv.productos: 
                print("Inventario vacío.")
            else:
                for producto in inv.productos.values(): print(producto)
            print("="*50)

        elif opc == "3":
            busqueda = input("Ingrese el código o nombre a buscar: ")
            resultados = inv.buscar(busqueda)
            print("\n" + "-"*20 + " RESULTADOS " + "-"*20)
            if resultados:
                for resultado in resultados: print(resultado)
            else:
                print("No se encontraron coincidencias.")
            print("-"*52)

        elif opc == "4":
            codigo_borrar = solicitar_solo_numeros("Ingrese el código numérico a borrar: ")
            inv.borrar(codigo_borrar)

        elif opc == "5":
            inv.guardar()
            print("Cambios guardados. Saliendo...")
            break

if _name_ == "_main_":
    menu_auth()