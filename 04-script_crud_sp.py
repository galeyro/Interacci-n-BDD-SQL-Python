"""
SISTEMA CRUD DE ALUMNOS - USANDO STORE PROCEDURES
Conexión a SQLServer con Python - CatequesisDB
Integración de Store Procedures con Menú Interactivo

@author Arias Javier, Andrade Eduardo, Guevara Galo
@date 2025

Descripción:
Clase GestorAlumnosConSP que encapsula todas las operaciones CRUD
utilizando Store Procedures en SQL Server - Base de datos CatequesisDB
"""

import pyodbc
import json
import sys
from datetime import datetime


class GestorAlumnosConSP:
    """
    Clase para gestionar operaciones CRUD con la tabla Alumno usando Store Procedures.
    Implementa encapsulamiento de la conexión y operaciones de base de datos.
    
    Atributos:
        conexion: Conexión activa a SQL Server
        connection_string: Cadena de conexión formada desde config.json
    """
    
    def __init__(self):
        """
        Inicializa la conexión desde el archivo config.json
        Carga las credenciales de SQL Server y establece la conexión
        """
        try:
            with open('config.json', 'r') as archivo_config:
                config = json.load(archivo_config)
            
            name_server = config['name_server']
            database = config['database']
            username = config['username']
            password = config['password']
            controlador_odbc = config['controlador_odbc']
            
            # Construir cadena de conexión
            self.connection_string = f'DRIVER={controlador_odbc};SERVER={name_server};DATABASE={database};UID={username};PWD={password}'
            
            # Establecer conexión
            self.conexion = pyodbc.connect(self.connection_string)
            print("\n✓ Conexión exitosa a SQL Server - CatequesisDB")
            
        except FileNotFoundError:
            print("✗ Error: No se encontró el archivo config.json")
            sys.exit(1)
        except pyodbc.DatabaseError as e:
            print(f"✗ Error de conexión a SQL Server: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error inesperado: {e}")
            sys.exit(1)
    
    # ==================== OPERACIÓN C (CREATE) ====================
    def insertar_alumno(self):
        """
        Inserta un nuevo alumno utilizando sp_InsertarAlumno.
        Solicita los datos al usuario a través de inputs.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                print("\n--- CREAR NUEVO ALUMNO ---")
                
                # Solicitar datos obligatorios
                nombre = input("Ingrese Nombre del Alumno: ").strip()
                apellido = input("Ingrese Apellido del Alumno: ").strip()
                
                # Validación básica
                if not nombre or not apellido:
                    print("✗ Error: Nombre y Apellido son obligatorios")
                    return
                
                # Solicitar datos opcionales
                fecha_nacimiento_str = input("Ingrese Fecha de Nacimiento (YYYY-MM-DD) o dejar en blanco: ").strip()
                fecha_nacimiento = None
                if fecha_nacimiento_str:
                    try:
                        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
                    except ValueError:
                        print("✗ Error: Formato de fecha inválido. Use YYYY-MM-DD")
                        return
                
                lugar_nacimiento = input("Ingrese Lugar de Nacimiento o dejar en blanco: ").strip() or None
                direccion = input("Ingrese Dirección o dejar en blanco: ").strip() or None
                telefono_alumno = input("Ingrese Teléfono o dejar en blanco: ").strip() or None
                info_escolar = input("Ingrese Información Escolar o dejar en blanco: ").strip() or None
                info_salud = input("Ingrese Información de Salud o dejar en blanco: ").strip() or None
                
                # Ejecutar Store Procedure
                SQL = """
                EXEC sp_InsertarAlumno 
                    @Nombre = ?,
                    @Apellido = ?,
                    @FechaNacimiento = ?,
                    @LugarNacimiento = ?,
                    @Direccion = ?,
                    @TelefonoAlumno = ?,
                    @InfoEscolar = ?,
                    @InfoSalud = ?
                """
                
                micursor.execute(SQL, 
                    (nombre, apellido, fecha_nacimiento, lugar_nacimiento, 
                     direccion, telefono_alumno, info_escolar, info_salud))
                
                resultado = micursor.fetchone()
                
                if resultado and resultado[0] == 'SUCCESS':
                    print(f"✓ Alumno registrado exitosamente con ID: {resultado[1]}")
                else:
                    print(f"✗ Error: {resultado[1] if resultado else 'Error desconocido'}")
                
        except Exception as e:
            print(f"✗ Error al insertar alumno: {e}")
    
    # ==================== OPERACIÓN R (READ) ====================
    def consultar_alumnos(self):
        """
        Consulta todos los alumnos utilizando sp_ObtenerAlumnos.
        Formatea la salida en columnas para mejor legibilidad.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                # Ejecutar Store Procedure
                micursor.execute("EXEC sp_ObtenerAlumnos")
                registros = micursor.fetchall()
                
                if not registros:
                    print("\n✗ No hay alumnos registrados en la base de datos")
                    return
                
                # Mostrar encabezados
                print("\n--- LISTADO DE ALUMNOS ---")
                print(f"{'ID':<5} {'Nombre':<15} {'Apellido':<15} {'F. Nac.':<12} {'Teléfono':<15} {'Lugar':<20}")
                print("-" * 100)
                
                # Mostrar registros
                for registro in registros:
                    id_alumno = registro[0]
                    nombre = registro[1]
                    apellido = registro[2]
                    fecha_nac = str(registro[3]) if registro[3] else "N/A"
                    telefono = registro[6] if registro[6] else "N/A"
                    lugar = registro[4] if registro[4] else "N/A"
                    
                    print(f"{id_alumno:<5} {nombre:<15} {apellido:<15} {fecha_nac:<12} {telefono:<15} {lugar:<20}")
                
                print(f"\nTotal de alumnos: {len(registros)}\n")
                
        except Exception as e:
            print(f"✗ Error al consultar alumnos: {e}")
    
    def consultar_alumno_por_id(self):
        """
        Consulta un alumno específico por ID utilizando sp_ObtenerAlumnoPorID.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                try:
                    id_alumno = int(input("\nIngrese ID del Alumno: "))
                except ValueError:
                    print("✗ Error: El ID debe ser un número")
                    return
                
                # Ejecutar Store Procedure
                micursor.execute("EXEC sp_ObtenerAlumnoPorID @IdAlumno = ?", (id_alumno,))
                registro = micursor.fetchone()
                
                if not registro:
                    print(f"✗ No se encontró alumno con ID {id_alumno}")
                    return
                
                # Mostrar datos del alumno
                print(f"\n--- DATOS DEL ALUMNO ---")
                print(f"ID:                    {registro[0]}")
                print(f"Nombre:                {registro[1]}")
                print(f"Apellido:              {registro[2]}")
                print(f"Fecha de Nacimiento:   {registro[3] if registro[3] else 'N/A'}")
                print(f"Lugar de Nacimiento:   {registro[4] if registro[4] else 'N/A'}")
                print(f"Dirección:             {registro[5] if registro[5] else 'N/A'}")
                print(f"Teléfono:              {registro[6] if registro[6] else 'N/A'}")
                print(f"Información Escolar:   {registro[7] if registro[7] else 'N/A'}")
                print(f"Información de Salud:  {registro[8] if registro[8] else 'N/A'}")
                print()
                
        except Exception as e:
            print(f"✗ Error al consultar alumno: {e}")
    
    def buscar_alumnos_por_nombre(self):
        """
        Busca alumnos por nombre utilizando sp_BuscarAlumnosPorNombre.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                nombre_busqueda = input("\nIngrese nombre o apellido a buscar: ").strip()
                
                if not nombre_busqueda:
                    print("✗ Error: Debe ingresar un término de búsqueda")
                    return
                
                # Ejecutar Store Procedure
                micursor.execute("EXEC sp_BuscarAlumnosPorNombre @NombreBusqueda = ?", (nombre_busqueda,))
                registros = micursor.fetchall()
                
                if not registros:
                    print(f"\n✗ No se encontraron alumnos con '{nombre_busqueda}'")
                    return
                
                # Mostrar resultados
                print(f"\n--- RESULTADOS DE BÚSQUEDA: '{nombre_busqueda}' ---")
                print(f"{'ID':<5} {'Nombre':<15} {'Apellido':<15} {'F. Nac.':<12} {'Teléfono':<15}")
                print("-" * 70)
                
                for registro in registros:
                    id_alumno = registro[0]
                    nombre = registro[1]
                    apellido = registro[2]
                    fecha_nac = str(registro[3]) if registro[3] else "N/A"
                    telefono = registro[6] if registro[6] else "N/A"
                    
                    print(f"{id_alumno:<5} {nombre:<15} {apellido:<15} {fecha_nac:<12} {telefono:<15}")
                
                print(f"\nTotal encontrado: {len(registros)}\n")
                
        except Exception as e:
            print(f"✗ Error al buscar alumnos: {e}")
    
    # ==================== OPERACIÓN U (UPDATE) ====================
    def actualizar_alumno(self):
        """
        Actualiza los datos de un alumno utilizando sp_ActualizarAlumno.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                print("\n--- ACTUALIZAR ALUMNO ---")
                
                try:
                    id_alumno = int(input("Ingrese ID del Alumno a actualizar: "))
                except ValueError:
                    print("✗ Error: El ID debe ser un número")
                    return
                
                # Verificar si el alumno existe
                micursor.execute("EXEC sp_ObtenerAlumnoPorID @IdAlumno = ?", (id_alumno,))
                alumno = micursor.fetchone()
                
                if not alumno:
                    print(f"✗ No se encontró alumno con ID {id_alumno}")
                    return
                
                print(f"\nAlumno encontrado: {alumno[1]} {alumno[2]}")
                print("\nIngrese los datos a actualizar (dejar en blanco para no cambiar):")
                
                # Solicitar datos
                nombre = input("Nuevo Nombre: ").strip() or None
                apellido = input("Nuevo Apellido: ").strip() or None
                
                fecha_nac_str = input("Nueva Fecha de Nacimiento (YYYY-MM-DD): ").strip()
                fecha_nac = None
                if fecha_nac_str:
                    try:
                        fecha_nac = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
                    except ValueError:
                        print("✗ Error: Formato de fecha inválido")
                        return
                
                lugar = input("Nuevo Lugar de Nacimiento: ").strip() or None
                direccion = input("Nueva Dirección: ").strip() or None
                telefono = input("Nuevo Teléfono: ").strip() or None
                info_escolar = input("Nueva Información Escolar: ").strip() or None
                info_salud = input("Nueva Información de Salud: ").strip() or None
                
                # Ejecutar Store Procedure
                SQL = """
                EXEC sp_ActualizarAlumno
                    @IdAlumno = ?,
                    @Nombre = ?,
                    @Apellido = ?,
                    @FechaNacimiento = ?,
                    @LugarNacimiento = ?,
                    @Direccion = ?,
                    @TelefonoAlumno = ?,
                    @InfoEscolar = ?,
                    @InfoSalud = ?
                """
                
                micursor.execute(SQL, 
                    (id_alumno, nombre, apellido, fecha_nac, lugar,
                     direccion, telefono, info_escolar, info_salud))
                
                resultado = micursor.fetchone()
                
                if resultado and resultado[0] == 'SUCCESS':
                    print(f"✓ {resultado[1]}")
                else:
                    print(f"✗ Error: {resultado[1] if resultado else 'Error desconocido'}")
                    
        except Exception as e:
            print(f"✗ Error al actualizar alumno: {e}")
    
    # ==================== OPERACIÓN D (DELETE) ====================
    def eliminar_alumno(self):
        """
        Elimina un alumno utilizando sp_EliminarAlumno.
        Solicita confirmación del usuario.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                print("\n--- ELIMINAR ALUMNO ---")
                
                try:
                    id_alumno = int(input("Ingrese ID del Alumno a eliminar: "))
                except ValueError:
                    print("✗ Error: El ID debe ser un número")
                    return
                
                # Verificar si el alumno existe
                micursor.execute("EXEC sp_ObtenerAlumnoPorID @IdAlumno = ?", (id_alumno,))
                alumno = micursor.fetchone()
                
                if not alumno:
                    print(f"✗ No se encontró alumno con ID {id_alumno}")
                    return
                
                # Confirmar eliminación
                confirmacion = input(f"¿Está seguro que desea eliminar a {alumno[1]} {alumno[2]}? (s/n): ").lower()
                
                if confirmacion != 's':
                    print("Operación cancelada")
                    return
                
                # Ejecutar Store Procedure
                micursor.execute("EXEC sp_EliminarAlumno @IdAlumno = ?", (id_alumno,))
                resultado = micursor.fetchone()
                
                if resultado and resultado[0] == 'SUCCESS':
                    print(f"✓ {resultado[1]}")
                else:
                    print(f"✗ Error: {resultado[1] if resultado else 'Error desconocido'}")
                    
        except Exception as e:
            print(f"✗ Error al eliminar alumno: {e}")
    
    # ==================== ESTADÍSTICAS ====================
    def mostrar_estadisticas(self):
        """
        Muestra estadísticas de la tabla Alumno utilizando sp_EstadisticasAlumnos.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                # Ejecutar Store Procedure
                micursor.execute("EXEC sp_EstadisticasAlumnos")
                stats = micursor.fetchone()
                
                if not stats:
                    print("\n✗ No hay datos para mostrar")
                    return
                
                # Mostrar estadísticas
                print("\n--- ESTADÍSTICAS DE ALUMNOS ---")
                print(f"Total de Alumnos:                  {stats[0]}")
                print(f"Años de Nacimiento Diferentes:     {stats[1]}")
                print(f"Alumno más Viejo:                  {stats[2] if stats[2] else 'N/A'}")
                print(f"Alumno más Joven:                  {stats[3] if stats[3] else 'N/A'}")
                print(f"Lugares de Nacimiento Diferentes:  {stats[4]}")
                print(f"Alumnos con Teléfono:              {stats[5]}")
                print(f"Alumnos con Información Escolar:   {stats[6]}")
                print(f"Alumnos con Información de Salud:  {stats[7]}\n")
                
        except Exception as e:
            print(f"✗ Error al obtener estadísticas: {e}")
    
    # ==================== MENÚ PRINCIPAL ====================
    def ejecutar_menu(self):
        """
        Menú interactivo CRUD que permite al usuario seleccionar operaciones.
        """
        while True:
            self._mostrar_menu_principal()
            
            try:
                opcion = input("Seleccione una opción (1-8): ").strip()
                
                if opcion == '1':
                    self.insertar_alumno()
                elif opcion == '2':
                    self.consultar_alumnos()
                elif opcion == '3':
                    self.consultar_alumno_por_id()
                elif opcion == '4':
                    self.buscar_alumnos_por_nombre()
                elif opcion == '5':
                    self.actualizar_alumno()
                elif opcion == '6':
                    self.eliminar_alumno()
                elif opcion == '7':
                    self.mostrar_estadisticas()
                elif opcion == '8':
                    self.cerrar_conexion()
                    print("Saliendo del programa...\n")
                    break
                else:
                    print("✗ Opción no válida. Ingrese un número entre 1 y 8")
                    
            except KeyboardInterrupt:
                print("\n\n✗ Programa interrumpido por el usuario")
                self.cerrar_conexion()
                break
            except Exception as e:
                print(f"✗ Error inesperado: {e}")
    
    @staticmethod
    def _mostrar_menu_principal():
        """
        Muestra el menú principal de opciones.
        """
        print("\n" + "=" * 60)
        print("\t** SISTEMA CRUD DE ALUMNOS **")
        print("\t** USANDO STORE PROCEDURES **")
        print("\t** CATEQUESIS DB **")
        print("=" * 60)
        print("\t1. Crear nuevo alumno")
        print("\t2. Consultar todos los alumnos")
        print("\t3. Consultar alumno por ID")
        print("\t4. Buscar alumnos por nombre")
        print("\t5. Actualizar datos del alumno")
        print("\t6. Eliminar alumno")
        print("\t7. Ver estadísticas")
        print("\t8. Salir")
        print("=" * 60)
    
    def cerrar_conexion(self):
        """
        Cierra la conexión con SQL Server.
        """
        try:
            self.conexion.close()
            print("✓ Conexión cerrada correctamente")
        except Exception as e:
            print(f"✗ Error al cerrar conexión: {e}")


# ==================== PROGRAMA PRINCIPAL ====================
if __name__ == "__main__":
    try:
        # Crear instancia del gestor
        gestor = GestorAlumnosConSP()
        
        # Ejecutar menú CRUD
        gestor.ejecutar_menu()
        
    except Exception as e:
        print(f"✗ Error en la aplicación: {e}")
