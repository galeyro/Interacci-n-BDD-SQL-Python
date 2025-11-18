-- =====================================================
-- SCRIPT PARA OTORGAR PERMISOS A pythonconsultor
-- Base de Datos: CatequesisDB
-- =====================================================

-- 1. CREAR LOGIN DEL USUARIO (Si no existe)
-- Ejecutar en: master
-- Nota: Si el usuario ya existe en SQL Server, saltarse este paso

IF NOT EXISTS (SELECT *
FROM sys.server_principals
WHERE name = 'pythonconsultor')
BEGIN
    CREATE LOGIN pythonconsultor WITH PASSWORD = '#############';
    PRINT 'Login pythonconsultor creado correctamente';
END
ELSE
BEGIN
    PRINT 'El login pythonconsultor ya existe';
END
GO

-- 2. CREAR USUARIO DE BASE DE DATOS
-- Ejecutar en: CatequesisDB
USE CatequesisDB;
GO

IF NOT EXISTS (SELECT *
FROM sys.database_principals
WHERE name = 'pythonconsultor')
BEGIN
    CREATE USER pythonconsultor FOR LOGIN pythonconsultor;
    PRINT 'Usuario pythonconsultor creado en CatequesisDB';
END
ELSE
BEGIN
    PRINT 'El usuario pythonconsultor ya existe en CatequesisDB';
END
GO

-- 3. OTORGAR PERMISOS BASICOS (SELECT, INSERT, UPDATE, DELETE)
-- Ejecutar en: CatequesisDB
USE CatequesisDB;
GO

GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO pythonconsultor;
PRINT 'Permisos CRUD (SELECT, INSERT, UPDATE, DELETE) otorgados en esquema dbo';
GO

-- 4. OTORGAR PERMISOS PARA EJECUTAR STORE PROCEDURES (Opcional pero recomendado)
-- Ejecutar en: CatequesisDB
USE CatequesisDB;
GO

GRANT EXECUTE ON SCHEMA::dbo TO pythonconsultor;
PRINT 'Permisos para EXECUTE en Store Procedures otorgados';
GO

-- 5. OTORGAR PERMISO PARA VER DEFINICIONES (Opcional)
-- Ejecutar en: CatequesisDB
USE CatequesisDB;
GO

GRANT VIEW DEFINITION ON SCHEMA::dbo TO pythonconsultor;
PRINT 'Permisos para VIEW DEFINITION otorgados';
GO

-- 6. OTORGAR PERMISO db_datareader Y db_datawriter (Alternativa más simple)
-- Ejecutar en: CatequesisDB
-- Descomenta estas líneas si prefieres usar roles de base de datos predefinidos
/*
USE CatequesisDB;
GO

ALTER ROLE db_datareader ADD MEMBER pythonconsultor;
ALTER ROLE db_datawriter ADD MEMBER pythonconsultor;
PRINT 'Usuario agregado a roles db_datareader y db_datawriter';
GO
*/

-- =====================================================
-- VERIFICAR PERMISOS OTORGADOS
-- =====================================================

-- Ver todos los permisos del usuario
USE CatequesisDB;
GO

SELECT
    pr.principal_id,
    pr.name AS [Usuario],
    pr.type_desc AS [Tipo],
    pe.class_desc AS [Clase],
    pe.permission_name AS [Permiso],
    pe.state_desc AS [Estado]
FROM sys.database_principals pr
    INNER JOIN sys.database_permissions pe ON pr.principal_id = pe.grantee_principal_id
WHERE pr.name = 'pythonconsultor'
ORDER BY pe.permission_name;
GO

-- =====================================================
-- NOTAS IMPORTANTES
-- =====================================================

/*
PASO A PASO PARA EJECUTAR ESTE SCRIPT:

1. Abre SQL Server Management Studio (SSMS)
2. Conecta como administrador (sa)

3. PRIMERA PARTE - Crear Login (en master):
   - Selecciona "master" en el dropdown de bases de datos
   - Ejecuta hasta la línea 14 (CREATE LOGIN)

4. SEGUNDA PARTE - Crear Usuario y Permisos (en CatequesisDB):
   - Selecciona "CatequesisDB" en el dropdown de bases de datos
   - Ejecuta desde la línea 18 hasta el final

ALTERNATIVA MÁS RÁPIDA:
Ejecuta TODO DE UNA VEZ si copias el script completo y lo ejecutas con SSMS

PERMISOS OTORGADOS:
✓ SELECT     - Leer datos
✓ INSERT     - Crear registros
✓ UPDATE     - Actualizar registros
✓ DELETE     - Eliminar registros
✓ EXECUTE    - Ejecutar Store Procedures
✓ VIEW DEF   - Ver definiciones de objetos

VERIFICACIÓN:
Después de ejecutar, verás una tabla con todos los permisos otorgados a pythonconsultor
*/
