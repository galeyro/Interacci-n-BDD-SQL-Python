# Sistema CRUD de Alumnos con Store Procedures

Sistema de gestión de alumnos implementado en Python con conexión a SQL Server, utilizando Store Procedures para operaciones CRUD seguras y eficientes.

## 📋 Descripción del Proyecto

Este proyecto es un sistema orientado a objetos (OOP) desarrollado en Python que gestiona registros de alumnos en la base de datos CatequesisDB. Implementa todas las operaciones CRUD (Create, Read, Update, Delete) utilizando Store Procedures en SQL Server para garantizar seguridad contra inyecciones SQL y optimizar el rendimiento.

## 🎯 Características

- **Programación Orientada a Objetos**: Código modular, mantenible y escalable
- **Store Procedures**: Todas las operaciones usan SP para máxima seguridad
- **Configuración Segura**: Credenciales en archivo config.json (no hardcodeadas)
- **Interfaz Interactiva**: Menú CRUD completo y fácil de usar
- **Manejo de Errores**: Validación en 3 niveles (aplicación, BD, SQL)
- **Búsqueda Avanzada**: Buscar alumnos por nombre o apellido
- **Estadísticas**: Reporte estadístico de la tabla de alumnos

## 📦 Requisitos

- Python 3.7+
- SQL Server 2019+ con base de datos CatequesisDB
- pyodbc
- ODBC Driver for SQL Server

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone <url-repositorio>
cd "Tarea Python"
```

### 2. Instalar Dependencias Python

```powershell
pip install pyodbc
```

### 3. Configurar Base de Datos

#### Crear el archivo config.json

En la raíz del proyecto, crear `config.json` basándote en el archivo `config_sample.json` proporcionado:

```bash
cp config_sample.json config.json
```

Luego edita `config.json` con tus credenciales reales:

```json
{
  "name_server": "tu_servidor",
  "database": "CatequesisDB",
  "username": "tu_usuario",
  "password": "tu_contraseña",
  "controlador_odbc": "SQL Server"
}
```

**IMPORTANTE:** El archivo `config.json` NO debe subirse al repositorio. Está incluido en `.gitignore` por seguridad.

#### Otorgar Permisos al Usuario

Ejecutar el script `permisos_sql_server.sql` en SQL Server Management Studio (SSMS) como administrador:

```sql
USE master;
CREATE LOGIN [tu_usuario] WITH PASSWORD = '[tu_contraseña]';

USE CatequesisDB;
CREATE USER [tu_usuario] FOR LOGIN [tu_usuario];
ALTER ROLE db_datareader ADD MEMBER [tu_usuario];
ALTER ROLE db_datawriter ADD MEMBER [tu_usuario];
GRANT EXECUTE ON SCHEMA::dbo TO [tu_usuario];
```

#### Crear los Store Procedures

Ejecutar el script `store_procedures_alumno.sql` en SSMS con la base de datos CatequesisDB seleccionada.

### 4. Validar Estructura de Datos

Para verificar que la tabla Alumno tiene la estructura correcta:

```powershell
python validar_estructura_alumno.py
```

### 5. Verificar Conexión

Para probar que la conexión a SQL Server funciona correctamente:

```powershell
python prueba_conexion_PI.py
```

## 💾 Estructura de la Base de Datos

### Tabla: Alumno

| Columna          | Tipo          | Nullable | Descripción                       |
| ---------------- | ------------- | -------- | --------------------------------- |
| id_alumno        | INT           | NO       | Identificador único (Primary Key) |
| nombre           | NVARCHAR(100) | NO       | Nombre del alumno                 |
| apellido         | NVARCHAR(100) | NO       | Apellido del alumno               |
| fecha_nacimiento | DATE          | SI       | Fecha de nacimiento               |
| lugar_nacimiento | NVARCHAR(100) | SI       | Lugar de nacimiento               |
| direccion        | NVARCHAR(255) | SI       | Dirección del domicilio           |
| telefono_alumno  | NVARCHAR(20)  | SI       | Número de teléfono                |
| info_escolar     | NVARCHAR(255) | SI       | Información escolar               |
| info_salud       | NVARCHAR(500) | SI       | Información de salud              |

## 🔧 Store Procedures Disponibles

### 1. sp_InsertarAlumno

Inserta un nuevo alumno en la base de datos.

**Parámetros:**

- @Nombre (obligatorio)
- @Apellido (obligatorio)
- @FechaNacimiento (opcional)
- @LugarNacimiento (opcional)
- @Direccion (opcional)
- @TelefonoAlumno (opcional)
- @InfoEscolar (opcional)
- @InfoSalud (opcional)

### 2. sp_ObtenerAlumnos

Obtiene la lista completa de todos los alumnos registrados.

### 3. sp_ObtenerAlumnoPorID

Obtiene los datos de un alumno específico por su ID.

**Parámetros:**

- @IdAlumno (obligatorio)

### 4. sp_ActualizarAlumno

Actualiza los datos de un alumno existente.

**Parámetros:**

- @IdAlumno (obligatorio)
- Todos los demás parámetros son opcionales

### 5. sp_EliminarAlumno

Elimina un alumno de la base de datos con validación previa.

**Parámetros:**

- @IdAlumno (obligatorio)

### 6. sp_BuscarAlumnosPorNombre

Busca alumnos por nombre o apellido (búsqueda parcial).

**Parámetros:**

- @NombreBusqueda (obligatorio)

### 7. sp_EstadisticasAlumnos

Genera estadísticas de la tabla de alumnos.

## 🎮 Uso

Para ejecutar el sistema CRUD:

```powershell
python script_crud_sp.py
```

### Menú Principal

```
====================================================
	** SISTEMA CRUD DE ALUMNOS **
	** USANDO STORE PROCEDURES **
	** CATEQUESIS DB **
====================================================
	1. Crear nuevo alumno
	2. Consultar todos los alumnos
	3. Consultar alumno por ID
	4. Buscar alumnos por nombre
	5. Actualizar datos del alumno
	6. Eliminar alumno
	7. Ver estadísticas
	8. Salir
====================================================
```

### Ejemplos de Uso

#### Crear un nuevo alumno

```
Seleccione una opción (1-8): 1

--- CREAR NUEVO ALUMNO ---
Ingrese Nombre del Alumno: Javier
Ingrese Apellido del Alumno: Arias
Ingrese Fecha de Nacimiento (YYYY-MM-DD) o dejar en blanco: 1999-08-14
Ingrese Lugar de Nacimiento o dejar en blanco: Quito
Ingrese Dirección o dejar en blanco: Calle Principal 123
Ingrese Teléfono o dejar en blanco: 0987654321
Ingrese Información Escolar o dejar en blanco: Último año de secundaria
Ingrese Información de Salud o dejar en blanco: Sin alergias conocidas

✓ Alumno registrado exitosamente con ID: 2
```

#### Consultar todos los alumnos

```
Seleccione una opción (1-8): 2

--- LISTADO DE ALUMNOS ---
ID    Nombre          Apellido        F. Nac.      Teléfono        Lugar
----------------------------------------------------------------------------------------------------
1     Javier          Arias           1999-08-14   N/A             N/A

Total de alumnos: 1
```

#### Buscar por nombre

```
Seleccione una opción (1-8): 4

Ingrese nombre o apellido a buscar: Javier

--- RESULTADOS DE BÚSQUEDA: 'Javier' ---
ID    Nombre          Apellido        F. Nac.      Teléfono
------
1     Javier          Arias           1999-08-14   N/A

Total encontrado: 1
```

## 📁 Estructura del Proyecto

```
Tarea Python/
├── script_crud_sp.py                 # Script principal con menú CRUD
├── prueba_conexion_PI.py             # Script para verificar conexión
├── validar_estructura_alumno.py      # Script para validar estructura de BD
├── config_sample.json                # Plantilla de configuración (ejemplo)
├── config.json                       # Configuración con credenciales (NO en Git)
├── store_procedures_alumno.sql       # SQL para crear Store Procedures
├── permisos_sql_server.sql           # SQL para crear usuario y permisos
├── .gitignore                        # Excluir archivos sensibles de Git
└── README.md                         # Este archivo
```

## 🔒 Seguridad

### Prevención de Inyecciones SQL

Todos los queries utilizan parámetros nombrados a través de Store Procedures, evitando completamente la concatenación de strings SQL. Los valores se pasan como parámetros separados garantizando que nunca sean interpretados como código SQL.

### Gestión de Credenciales

- Las credenciales se almacenan en `config.json` que NO se sube al repositorio
- El archivo `config_sample.json` proporciona una plantilla segura como ejemplo
- Agregar `config.json` a `.gitignore` (ya está configurado)
- Cada desarrollador crea su propio `config.json` a partir de `config_sample.json`
- En producción, considerar usar variables de entorno del sistema operativo

**Configuración de .gitignore:**

```
config.json
*.pyc
__pycache__/
.DS_Store
```

### Validación de Datos

- Validación a nivel de aplicación Python
- Validación a nivel de Store Procedure SQL
- Validación de tipos de datos
- Validación de restricciones de integridad referencial

## ⚙️ Configuración

### Variables de Entorno (Alternativa Segura)

Para mayor seguridad en producción, usar variables de entorno:

```python
import os

config = {
    'name_server': os.getenv('DB_SERVER', 'localhost'),
    'database': os.getenv('DB_NAME', 'CatequesisDB'),
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
```

## 📊 Estadísticas

El sistema proporciona estadísticas incluyendo:

- Total de alumnos registrados
- Años de nacimiento diferentes
- Alumno más viejo y más joven
- Lugares de nacimiento diferentes
- Alumnos con información de teléfono, escolar y salud

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo config.json"

Asegúrate de que el archivo `config.json` exista en la raíz del proyecto con las credenciales correctas.

### Error: "Error de conexión a SQL Server"

Verifica:

1. SQL Server está corriendo
2. El nombre del servidor es correcto
3. El usuario tiene permisos en la base de datos
4. El ODBC Driver está instalado

Instalar ODBC Driver:

```powershell
# Descargar desde: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

### Error: "No se encontró alumno con ID..."

Verifica que el ID ingresado existe en la base de datos consultando primero la lista de alumnos.

## 📝 Notas de Desarrollo

- El proyecto usa pyodbc para conexión a SQL Server
- Los Store Procedures manejan transacciones automáticamente
- Cada operación retorna un status ('SUCCESS' o 'ERROR')
- Los campos opcionales pueden dejarse en blanco
- Las fechas deben estar en formato YYYY-MM-DD

## 📄 Licencia

Este proyecto es parte del curso de Análisis de Datos - Proyecto Integrador.

## ✍️ Autor

Desarrollo: Proyecto Integrador - Semestre 8
Base de Datos: CatequesisDB
Institución: Universidad de Las Américas (UDLA)

---

**Última actualización:** Noviembre 2025
