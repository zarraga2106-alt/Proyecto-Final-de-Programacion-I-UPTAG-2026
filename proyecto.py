import os
import hashlib
import getpass

class Usuario:
    def __init__(self, nombre_usuario, contrasena_encriptada):
        self.nombre_usuario = nombre_usuario
        self.contrasena_encriptada = contrasena_encriptada

    def a_csv(self):
        return f"{self.nombre_usuario},{self.contrasena_encriptada}\n"

class GestorUsuarios:
    def __init__(self, archivo="usuarios_pro.txt"):
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

class Item:
    def __init__(self, codigo, nombre):
        self.codigo = codigo 
        self.nombre = nombre.strip().title()

class Producto(Item):
    def __init__(self, codigo, nombre, precio, cantidad):
        super().__init__(codigo, nombre)
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

    def __str__(self):
        return f"ID: {self.codigo:<10} | {self.nombre:<15} | ${self.precio:>8.2f} | Stock: {self.cantidad:>4}"

    def a_csv(self):
        return f"{self.codigo},{self.nombre},{self.precio},{self.cantidad}\n"

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

class Inventario:
    def __init__(self, nombre_archivo="inventario_pro.txt"):
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

    def buscar(self, criterio):
        encontrados = []
        criterio = criterio.lower().strip()
        for producto in self.productos.values():
            if criterio == producto.codigo or criterio in producto.nombre.lower():
                encontrados.append(producto)
        return encontrados

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            f.writelines(producto.a_csv() for producto in self.productos.values())

def menu_auth():
    gestor = GestorUsuarios()
    while True:
        print(f"\n{'='*15} SISTEMA DE ACCESO {'='*15}")
        print("1. Iniciar Sesión\n2. Registrarse\n3. Salir")
        opc = input("Seleccione: ").strip()

        if opc == "1":
            usuario = input("Usuario: ").strip()
            contrasena = getpass.getpass("Contraseña: ").strip()
            if gestor.autenticar(usuario, contrasena):
                print(f"\n¡Acceso concedido! Bienvenido, {usuario}.")
                menu_principal(usuario)
        elif opc == "2":
            nuevo_u = input("Nuevo usuario: ").strip()
            nueva_c = getpass.getpass("Nueva contraseña: ").strip()
            confirmar = getpass.getpass("Confirme contraseña: ").strip()
            if nueva_c == confirmar:
                gestor.registrar(nuevo_u, nueva_c)
            else:
                print("❌ Las contraseñas no coinciden.")
        elif opc == "3":
            print("Finalizando programa...")
            break

def menu_principal(usuario_actual):
    inv = Inventario()
    while True:
        print(f"\n{'#'*10} INVENTARIO - Sesión: {usuario_actual} {'#'*10}")
        print("1. Agregar Producto\n2. Ver Todo\n3. Buscar\n4. Borrar\n5. Cerrar Sesión y Guardar")
        opc = input("Seleccione: ")

        if opc == "1":
            cod = solicitar_solo_numeros("Código: ")
            nom = input("Nombre: ")
            pre = solicitar_solo_numeros("Precio: ", True)
            can = solicitar_solo_numeros("Cantidad: ")
            inv.agregar(cod, nom, pre, can)
        elif opc == "2":
            print("\n--- LISTA DE PRODUCTOS ---")
            for p in inv.productos.values(): print(p)
            if not inv.productos: print("No hay productos registrados.")
        elif opc == "3":
            crit = input("Buscar (Código o Nombre): ")
            resultados = inv.buscar(crit)
            for r in resultados: print(r)
            if not resultados: print("Sin coincidencias.")
        elif opc == "4":
            cod_b = solicitar_solo_numeros("Código a eliminar: ")
            inv.borrar(cod_b)
        elif opc == "5":
            inv.guardar()
            print("📦 Datos guardados. Volviendo al login...")
            break

if __name__ == "__main__":
    menu_auth()
