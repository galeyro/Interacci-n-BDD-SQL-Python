"""
SCRIPT PARA VALIDAR LA ESTRUCTURA DE LA TABLA ALUMNO
Verifica los campos reales en CatequesisDB
"""

import pyodbc
import json


def validar_estructura_tabla():
    """
    Obtiene la estructura real de la tabla Alumno
    """
    try:
        # Cargar configuración
        with open('config.json', 'r') as archivo_config:
            config = json.load(archivo_config)
        
        # Construir cadena de conexión
        connection_string = f"DRIVER={config['controlador_odbc']};SERVER={config['name_server']};DATABASE={config['database']};UID={config['username']};PWD={config['password']}"
        
        conexion = pyodbc.connect(connection_string)
        cursor = conexion.cursor()
        
        print("=" * 80)
        print("VALIDACIÓN DE ESTRUCTURA - TABLA ALUMNO")
        print("=" * 80)
        
        # Obtener información de columnas
        query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE,
            COLUMNPROPERTY(OBJECT_ID('dbo.Alumno'), COLUMN_NAME, 'IsIdentity') AS IsIdentity,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'Alumno' AND TABLE_SCHEMA = 'dbo'
        ORDER BY ORDINAL_POSITION
        """
        
        cursor.execute(query)
        columnas = cursor.fetchall()
        
        if not columnas:
            print("\n✗ La tabla Alumno no existe o no tiene columnas")
            return False
        
        print("\n📋 ESTRUCTURA DE LA TABLA ALUMNO:\n")
        print(f"{'Columna':<20} {'Tipo':<20} {'Tamaño':<10} {'Nullable':<10} {'Identity':<10} {'Default':<20}")
        print("-" * 100)
        
        for col in columnas:
            columna_nombre = col[0]
            tipo_dato = col[1]
            tamaño = str(col[2]) if col[2] else "N/A"
            es_nullable = "SI" if col[3] == "YES" else "NO"
            es_identity = "SI" if col[4] == 1 else "NO"
            default = col[5] if col[5] else "N/A"
            
            print(f"{columna_nombre:<20} {tipo_dato:<20} {tamaño:<10} {es_nullable:<10} {es_identity:<10} {default:<20}")
        
        # Obtener restricciones
        print("\n" + "-" * 80)
        print("🔑 RESTRICCIONES Y CLAVES:\n")
        
        pk_query = """
        SELECT CONSTRAINT_NAME, COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_NAME = 'Alumno' AND TABLE_SCHEMA = 'dbo'
        """
        
        cursor.execute(pk_query)
        restricciones = cursor.fetchall()
        
        if restricciones:
            for constraint in restricciones:
                print(f"✓ {constraint[0]}: {constraint[1]}")
        else:
            print("Sin restricciones definidas")
        
        # Obtener índices
        print("\n" + "-" * 80)
        print("📑 ÍNDICES:\n")
        
        index_query = """
        SELECT 
            i.name AS IndexName,
            STUFF((SELECT ', ' + c.name
                   FROM sys.index_columns ic
                   JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                   WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id
                   FOR XML PATH('')), 1, 2, '') AS Columnas,
            CASE WHEN i.is_primary_key = 1 THEN 'Primary Key'
                 WHEN i.is_unique = 1 THEN 'Unique'
                 ELSE 'Index' END AS Tipo
        FROM sys.indexes i
        WHERE i.object_id = OBJECT_ID('dbo.Alumno')
        AND i.index_id > 0
        """
        
        cursor.execute(index_query)
        indices = cursor.fetchall()
        
        if indices:
            for idx in indices:
                print(f"✓ {idx[0]}: {idx[2]} en columnas ({idx[1]})")
        else:
            print("Sin índices definidos")
        
        # Obtener cantidad de registros
        print("\n" + "-" * 80)
        print("📊 INFORMACIÓN ADICIONAL:\n")
        
        cursor.execute("SELECT COUNT(*) FROM dbo.Alumno")
        count = cursor.fetchone()[0]
        print(f"Total de registros: {count}")
        
        # Obtener primeros registros como ejemplo
        print("\n" + "-" * 80)
        print("📝 EJEMPLO DE REGISTROS:\n")
        
        cursor.execute("SELECT TOP 3 * FROM dbo.Alumno")
        ejemplos = cursor.fetchall()
        
        if ejemplos:
            # Mostrar encabezados
            for desc in cursor.description:
                print(f"  {desc[0]}", end=" | ")
            print("\n" + "-" * 100)
            
            # Mostrar datos
            for row in ejemplos:
                for value in row:
                    print(f"  {str(value)[:30]}", end=" | ")
                print()
        else:
            print("No hay registros para mostrar")
        
        print("\n" + "=" * 80)
        print("✅ VALIDACIÓN COMPLETADA")
        print("=" * 80)
        
        # Mostrar resumen
        print("\n📌 RESUMEN:")
        print(f"   Tabla: dbo.Alumno")
        print(f"   Columnas: {len(columnas)}")
        print(f"   Registros: {count}")
        
        conexion.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    validar_estructura_tabla()
