"""
SISTEMA CRUD DE ESTUDIANTES - DISEÑO ORIENTADO A OBJETOS
Conexión a SQLServer con Python
Ejemplo de CRUD evitando inyecciones SQL

@author Arias Javier, Andrade Eduardo, Guevara Galo
@date 2025

Descripción:
Clase GestorEstudiantes que encapsula todas las operaciones CRUD
para la tabla Estudiantes en SQL Server
"""

import pyodbc
import json
import sys


class GestorEstudiantes:
    """
    Clase para gestionar operaciones CRUD con la tabla Estudiantes.
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
            print("\n✓ Conexión exitosa a SQL Server")
            
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
    def insertar_estudiante(self):
        """
        Inserta un nuevo registro de estudiante en la tabla Estudiantes.
        Solicita los datos al usuario y utiliza parámetros para evitar inyecciones SQL.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                # Consulta SQL parametrizada para evitar inyecciones
                SQL_STATEMENT = """INSERT INTO Estudiantes
                (IDEstudiante, NombreEstudiante, ApellidoEstudiante, Email, Telefono)
                VALUES (?, ?, ?, ?, ?)"""
                
                # Solicitar datos al usuario
                print("\n--- CREAR NUEVO REGISTRO ---")
                l_IDEstudiante = int(input("Ingrese ID del Estudiante: "))
                l_NombreEstudiante = input("Ingrese Nombre del Estudiante: ")
                l_ApellidoEstudiante = input("Ingrese Apellido del Estudiante: ")
                l_Email = input("Ingrese Email del Estudiante: ")
                l_Telefono = input("Ingrese Teléfono del Estudiante: ")
                
                # Ejecutar inserción
                micursor.execute(SQL_STATEMENT, 
                                (l_IDEstudiante, l_NombreEstudiante, 
                                 l_ApellidoEstudiante, l_Email, l_Telefono))
                
                self.conexion.commit()
                print("✓ Registro insertado exitosamente")
                
        except ValueError:
            print("✗ Error: Ingrese valores válidos (ID debe ser número)")
            self.conexion.rollback()
        except pyodbc.IntegrityError as e:
            print(f"✗ Error de integridad: El ID ya existe o datos inválidos")
            self.conexion.rollback()
        except Exception as e:
            print(f"✗ Error al insertar registro: {e}")
            self.conexion.rollback()
    
    # ==================== OPERACIÓN R (READ) ====================
    def consultar_estudiantes(self):
        """
        Consulta y muestra todos los registros de la tabla Estudiantes.
        Formatea la salida en columnas para mejor legibilidad.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                # Consulta SQL
                SQL_QUERY = """
                SELECT IDEstudiante, NombreEstudiante, ApellidoEstudiante, Email, Telefono
                FROM Estudiantes
                ORDER BY IDEstudiante
                """
                
                micursor.execute(SQL_QUERY)
                records = micursor.fetchall()
                
                if not records:
                    print("✗ No hay registros en la tabla Estudiantes")
                    return
                
                # Mostrar encabezados
                print("\n--- LISTADO DE ESTUDIANTES ---")
                print(f"{'ID':<5} {'Nombre':<15} {'Apellido':<15} {'Email':<25} {'Teléfono':<12}")
                print("-" * 75)
                
                # Mostrar registros
                for registro in records:
                    print(f"{registro.IDEstudiante:<5} {registro.NombreEstudiante:<15} "
                          f"{registro.ApellidoEstudiante:<15} {registro.Email:<25} {registro.Telefono:<12}")
                
                print(f"\nTotal de registros: {len(records)}\n")
                
        except Exception as e:
            print(f"✗ Error al consultar registros: {e}")
    
    # ==================== OPERACIÓN U (UPDATE) ====================
    def actualizar_estudiante(self):
        """
        Actualiza el email de un estudiante existente.
        Solicita el ID del estudiante y el nuevo email.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                # Consulta SQL parametrizada
                SQL_STATEMENT = """UPDATE Estudiantes
                SET Email = ?
                WHERE IDEstudiante = ?"""
                
                print("\n--- ACTUALIZAR REGISTRO ---")
                l_IDEstudiante = int(input("Ingrese ID del Estudiante a actualizar: "))
                l_Email = input("Ingrese el nuevo Email del Estudiante: ")
                
                # Ejecutar actualización
                micursor.execute(SQL_STATEMENT, (l_Email, l_IDEstudiante))
                
                self.conexion.commit()
                
                if micursor.rowcount > 0:
                    print("✓ Registro actualizado exitosamente")
                else:
                    print("✗ No se encontró un estudiante con ese ID")
                    
        except ValueError:
            print("✗ Error: El ID debe ser un número")
            self.conexion.rollback()
        except Exception as e:
            print(f"✗ Error al actualizar registro: {e}")
            self.conexion.rollback()
    
    # ==================== OPERACIÓN D (DELETE) ====================
    def eliminar_estudiante(self):
        """
        Elimina un registro de estudiante de la tabla Estudiantes.
        Solicita confirmación del usuario antes de eliminar.
        """
        try:
            with self.conexion.cursor() as micursor:
                
                # Consulta SQL parametrizada
                SQL_STATEMENT = """DELETE FROM Estudiantes
                WHERE IDEstudiante = ?"""
                
                print("\n--- ELIMINAR REGISTRO ---")
                l_IDEstudiante = int(input("Ingrese ID del Estudiante a eliminar: "))
                
                # Confirmar eliminación
                confirmacion = input(f"¿Está seguro que desea eliminar al estudiante con ID {l_IDEstudiante}? (s/n): ")
                
                if confirmacion.lower() != 's':
                    print("Operación cancelada")
                    return
                
                # Ejecutar eliminación
                micursor.execute(SQL_STATEMENT, (l_IDEstudiante,))
                
                self.conexion.commit()
                
                if micursor.rowcount > 0:
                    print("✓ Registro eliminado exitosamente")
                else:
                    print("✗ No se encontró un estudiante con ese ID")
                    
        except ValueError:
            print("✗ Error: El ID debe ser un número")
            self.conexion.rollback()
        except Exception as e:
            print(f"✗ Error al eliminar registro: {e}")
            self.conexion.rollback()
    
    # ==================== MENÚ CRUD ====================
    def ejecutar_menu(self):
        """
        Menú interactivo CRUD que permite al usuario seleccionar operaciones.
        """
        while True:
            self._mostrar_opciones_crud()
            
            try:
                opcion = int(input("Seleccione una opción (1-5): "))
                
                if opcion == 1:
                    self.insertar_estudiante()
                elif opcion == 2:
                    self.consultar_estudiantes()
                elif opcion == 3:
                    self.actualizar_estudiante()
                elif opcion == 4:
                    self.eliminar_estudiante()
                elif opcion == 5:
                    self.cerrar_conexion()
                    print("Saliendo del programa...\n")
                    break
                else:
                    print("✗ Opción no válida. Ingrese un número entre 1 y 5")
                    
            except ValueError:
                print("✗ Error: Ingrese un número válido")
            except KeyboardInterrupt:
                print("\n\n✗ Programa interrumpido por el usuario")
                self.cerrar_conexion()
                break
            except Exception as e:
                print(f"✗ Error inesperado: {e}")
    
    @staticmethod
    def _mostrar_opciones_crud():
        """
        Muestra el menú de opciones CRUD.
        Método estático para mejor organización.
        """
        print("\n" + "=" * 50)
        print("\t** SISTEMA CRUD DE ESTUDIANTES **")
        print("=" * 50)
        print("\t1. Crear registro")
        print("\t2. Consultar registros")
        print("\t3. Actualizar registro")
        print("\t4. Eliminar registro")
        print("\t5. Salir")
        print("=" * 50)
    
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
        gestor = GestorEstudiantes()
        
        # Ejecutar menú CRUD
        gestor.ejecutar_menu()
        
    except Exception as e:
        print(f"✗ Error en la aplicación: {e}")