"""
SCRIPT DE PRUEBA DE CONEXIÓN A CatequesisDB
Verifica que el usuario pythonconsultor tiene acceso correcto
"""

import pyodbc
import json
import sys


def probar_conexion():
    """
    Prueba la conexión a SQL Server con las credenciales en config.json
    """
    try:
        # Cargar configuración
        with open('config.json', 'r') as archivo_config:
            config = json.load(archivo_config)
        
        print("=" * 70)
        print("PRUEBA DE CONEXIÓN A SQL SERVER")
        print("=" * 70)
        
        # Mostrar datos de conexión (sin contraseña)
        print(f"\n📋 Datos de conexión:")
        print(f"   Servidor: {config['name_server']}")
        print(f"   Base de datos: {config['database']}")
        print(f"   Usuario: {config['username']}")
        print(f"   Driver ODBC: {config['controlador_odbc']}")
        
        # Construir cadena de conexión
        connection_string = f"DRIVER={config['controlador_odbc']};SERVER={config['name_server']};DATABASE={config['database']};UID={config['username']};PWD={config['password']}"
        
        print(f"\n⏳ Intentando conectar...")
        
        # Intentar conexión
        conexion = pyodbc.connect(connection_string)
        
        print("✅ ¡Conexión exitosa!")
        
        # Prueba 1: Obtener versión de SQL Server
        print("\n" + "-" * 70)
        print("PRUEBA 1: Versión de SQL Server")
        print("-" * 70)
        
        cursor = conexion.cursor()
        cursor.execute('SELECT @@VERSION')
        version = cursor.fetchone()
        print(f"✓ {version[0][:80]}...")
        
        # Prueba 2: Listar tablas en la base de datos
        print("\n" + "-" * 70)
        print("PRUEBA 2: Tablas disponibles en CatequesisDB")
        print("-" * 70)
        
        cursor.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        tablas = cursor.fetchall()
        
        if tablas:
            print(f"✓ Se encontraron {len(tablas)} tabla(s):\n")
            for tabla in tablas:
                print(f"   • {tabla[0]}.{tabla[1]}")
        else:
            print("⚠ No hay tablas en la base de datos")
        
        # Prueba 3: Probar permisos SELECT
        print("\n" + "-" * 70)
        print("PRUEBA 3: Verificar permisos SELECT")
        print("-" * 70)
        
        if tablas:
            tabla_prueba = tablas[0]
            cursor.execute(f"""
                SELECT TOP 1 * FROM [{tabla_prueba[0]}].[{tabla_prueba[1]}]
            """)
            resultado = cursor.fetchone()
            print(f"✓ Permiso SELECT verificado en {tabla_prueba[0]}.{tabla_prueba[1]}")
        else:
            print("⚠ No hay tablas para probar SELECT")
        
        # Prueba 4: Probar Store Procedures
        print("\n" + "-" * 70)
        print("PRUEBA 4: Store Procedures disponibles")
        print("-" * 70)
        
        cursor.execute("""
            SELECT ROUTINE_SCHEMA, ROUTINE_NAME, ROUTINE_TYPE
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY ROUTINE_SCHEMA, ROUTINE_NAME
        """)
        
        procedures = cursor.fetchall()
        
        if procedures:
            print(f"✓ Se encontraron {len(procedures)} Store Procedure(s):\n")
            for proc in procedures:
                print(f"   • {proc[0]}.{proc[1]}")
        else:
            print("⚠ No hay Store Procedures en la base de datos")
        
        # Prueba 5: Información de la base de datos
        print("\n" + "-" * 70)
        print("PRUEBA 5: Información de la base de datos")
        print("-" * 70)
        
        cursor.execute("""
            SELECT 
                DB_NAME() AS [Base de Datos],
                USER_NAME() AS [Usuario Actual],
                GETDATE() AS [Fecha/Hora Servidor]
        """)
        
        info = cursor.fetchone()
        print(f"✓ Base de datos actual: {info[0]}")
        print(f"✓ Usuario actual: {info[1]}")
        print(f"✓ Fecha/Hora del servidor: {info[2]}")
        
        # Resumen final
        print("\n" + "=" * 70)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 70)
        print("\nLa conexión está lista para usar en script.py\n")
        
        # Cerrar conexión
        cursor.close()
        conexion.close()
        
        return True
        
    except pyodbc.DatabaseError as e:
        print(f"\n❌ Error de base de datos: {e}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Error: No se encontró config.json")
        return False
    except json.JSONDecodeError:
        print(f"\n❌ Error: config.json tiene formato inválido")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False


if __name__ == "__main__":
    exito = probar_conexion()
    sys.exit(0 if exito else 1)
