-- =====================================================
-- STORE PROCEDURES PARA LA TABLA ALUMNO
-- Base de Datos: CatequesisDB
-- Estructura: id_alumno, nombre, apellido, fecha_nacimiento, lugar_nacimiento, 
--             direccion, telefono_alumno, info_escolar, info_salud
-- =====================================================

-- 1. SP PARA INSERTAR ALUMNO
-- =====================================================
IF EXISTS (SELECT *
FROM sys.objects
WHERE type = 'P' AND name = 'sp_InsertarAlumno')
    DROP PROCEDURE dbo.sp_InsertarAlumno;
GO

CREATE PROCEDURE dbo.sp_InsertarAlumno
    @Nombre NVARCHAR(100),
    @Apellido NVARCHAR(100),
    @FechaNacimiento DATE = NULL,
    @LugarNacimiento NVARCHAR(100) = NULL,
    @Direccion NVARCHAR(255) = NULL,
    @TelefonoAlumno NVARCHAR(20) = NULL,
    @InfoEscolar NVARCHAR(255) = NULL,
    @InfoSalud NVARCHAR(500) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        INSERT INTO dbo.Alumno
        (nombre, apellido, fecha_nacimiento, lugar_nacimiento, direccion,
        telefono_alumno, info_escolar, info_salud)
    VALUES
        (@Nombre, @Apellido, @FechaNacimiento, @LugarNacimiento, @Direccion,
            @TelefonoAlumno, @InfoEscolar, @InfoSalud);
        
        SELECT 'SUCCESS' AS Mensaje, SCOPE_IDENTITY() AS id_alumno;
    END TRY
    BEGIN CATCH
        SELECT 'ERROR' AS Mensaje, ERROR_MESSAGE() AS DetalleError;
    END CATCH
END
GO

-- 2. SP PARA CONSULTAR TODOS LOS ALUMNOS
-- =====================================================
IF EXISTS (SELECT *
FROM sys.objects
WHERE type = 'P' AND name = 'sp_ObtenerAlumnos')
    DROP PROCEDURE dbo.sp_ObtenerAlumnos;
GO

CREATE PROCEDURE dbo.sp_ObtenerAlumnos
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        id_alumno,
        nombre,
        apellido,
        fecha_nacimiento,
        lugar_nacimiento,
        direccion,
        telefono_alumno,
        info_escolar,
        info_salud
    FROM dbo.Alumno
    ORDER BY id_alumno;
END
GO

-- 3. SP PARA CONSULTAR UN ALUMNO POR ID
-- =====================================================
IF EXISTS (SELECT *
FROM sys.objects
WHERE type = 'P' AND name = 'sp_ObtenerAlumnoPorID')
    DROP PROCEDURE dbo.sp_ObtenerAlumnoPorID;
GO

CREATE PROCEDURE dbo.sp_ObtenerAlumnoPorID
    @IdAlumno INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        id_alumno,
        nombre,
        apellido,
        fecha_nacimiento,
        lugar_nacimiento,
        direccion,
        telefono_alumno,
        info_escolar,
        info_salud
    FROM dbo.Alumno
    WHERE id_alumno = @IdAlumno;
END
GO

-- 4. SP PARA ACTUALIZAR ALUMNO
-- =====================================================
IF EXISTS (SELECT *
FROM sys.objects
WHERE type = 'P' AND name = 'sp_ActualizarAlumno')
    DROP PROCEDURE dbo.sp_ActualizarAlumno;
GO

CREATE PROCEDURE dbo.sp_ActualizarAlumno
    @IdAlumno INT,
    @Nombre NVARCHAR(100) = NULL,
    @Apellido NVARCHAR(100) = NULL,
    @FechaNacimiento DATE = NULL,
    @LugarNacimiento NVARCHAR(100) = NULL,
    @Direccion NVARCHAR(255) = NULL,
    @TelefonoAlumno NVARCHAR(20) = NULL,
    @InfoEscolar NVARCHAR(255) = NULL,
    @InfoSalud NVARCHAR(500) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        UPDATE dbo.Alumno
        SET 
            nombre = ISNULL(@Nombre, nombre),
            apellido = ISNULL(@Apellido, apellido),
            fecha_nacimiento = ISNULL(@FechaNacimiento, fecha_nacimiento),
            lugar_nacimiento = ISNULL(@LugarNacimiento, lugar_nacimiento),
            direccion = ISNULL(@Direccion, direccion),
            telefono_alumno = ISNULL(@TelefonoAlumno, telefono_alumno),
            info_escolar = ISNULL(@InfoEscolar, info_escolar),
            info_salud = ISNULL(@InfoSalud, info_salud)
        WHERE id_alumno = @IdAlumno;
        
        IF @@ROWCOUNT > 0
            SELECT 'SUCCESS' AS Mensaje, 'Alumno actualizado correctamente' AS Detalle;
        ELSE
            SELECT 'ERROR' AS Mensaje, 'No se encontró alumno con ese ID' AS Detalle;
    END TRY
    BEGIN CATCH
        SELECT 'ERROR' AS Mensaje, ERROR_MESSAGE() AS DetalleError;
    END CATCH
END
GO

-- 5. SP PARA ELIMINAR ALUMNO
-- =====================================================
IF EXISTS (SELECT *
FROM sys.objects
WHERE type = 'P' AND name = 'sp_EliminarAlumno')
    DROP PROCEDURE dbo.sp_EliminarAlumno;
GO

CREATE PROCEDURE dbo.sp_EliminarAlumno
    @IdAlumno INT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- Verificar si el alumno existe
        IF NOT EXISTS (SELECT 1
    FROM dbo.Alumno
    WHERE id_alumno = @IdAlumno)
        BEGIN
        SELECT 'ERROR' AS Mensaje, 'No se encontró alumno con ese ID' AS Detalle;
        RETURN;
    END
        
        DELETE FROM dbo.Alumno
        WHERE id_alumno = @IdAlumno;
        
        SELECT 'SUCCESS' AS Mensaje, 'Alumno eliminado correctamente' AS Detalle;
    END TRY
    BEGIN CATCH
        SELECT 'ERROR' AS Mensaje, ERROR_MESSAGE() AS DetalleError;
    END CATCH
END
GO

-- 6. SP PARA BUSCAR ALUMNOS POR NOMBRE
-- =====================================================
IF EXISTS (SELECT *
FROM sys.objects
WHERE type = 'P' AND name = 'sp_BuscarAlumnosPorNombre')
    DROP PROCEDURE dbo.sp_BuscarAlumnosPorNombre;
GO

CREATE PROCEDURE dbo.sp_BuscarAlumnosPorNombre
    @NombreBusqueda NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        id_alumno,
        nombre,
        apellido,
        fecha_nacimiento,
        lugar_nacimiento,
        direccion,
        telefono_alumno,
        info_escolar,
        info_salud
    FROM dbo.Alumno
    WHERE nombre LIKE '%' + @NombreBusqueda + '%'
        OR apellido LIKE '%' + @NombreBusqueda + '%'
    ORDER BY nombre, apellido;
END
GO

-- 7. SP PARA OBTENER ESTADÍSTICAS DE ALUMNOS
-- =====================================================
IF EXISTS (SELECT *
FROM sys.objects
WHERE type = 'P' AND name = 'sp_EstadisticasAlumnos')
    DROP PROCEDURE dbo.sp_EstadisticasAlumnos;
GO

CREATE PROCEDURE dbo.sp_EstadisticasAlumnos
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        COUNT(*) AS TotalAlumnos,
        COUNT(DISTINCT YEAR(fecha_nacimiento)) AS AniosNacimientoDiferentes,
        MIN(fecha_nacimiento) AS AlumnoMasViejo,
        MAX(fecha_nacimiento) AS AlumnoMasJoven,
        COUNT(DISTINCT lugar_nacimiento) AS LugaresNacimientoDiferentes,
        COUNT(telefono_alumno) AS AlumnosConTelefono,
        COUNT(info_escolar) AS AlumnosConInfoEscolar,
        COUNT(info_salud) AS AlumnosConInfoSalud
    FROM dbo.Alumno;
END
GO

-- =====================================================
-- VERIFICAR QUE LOS STORE PROCEDURES FUERON CREADOS
-- =====================================================

PRINT '=== STORE PROCEDURES CREADOS EXITOSAMENTE ==='
PRINT ''
PRINT 'Los siguientes procedimientos están disponibles:'

SELECT
    SCHEMA_NAME(schema_id) AS Esquema,
    name AS NombreProcedimiento,
    type_desc AS Tipo,
    create_date AS FechaCreacion
FROM sys.objects
WHERE type = 'P'
    AND name LIKE 'sp_%Alumno%'
ORDER BY name;

PRINT ''
PRINT '=== USO DE LOS STORE PROCEDURES ==='
PRINT ''
PRINT '1. sp_InsertarAlumno'
PRINT '   EXEC sp_InsertarAlumno @Nombre, @Apellido, @FechaNacimiento, @LugarNacimiento, @Direccion, @TelefonoAlumno, @InfoEscolar, @InfoSalud'
PRINT ''
PRINT '2. sp_ObtenerAlumnos'
PRINT '   EXEC sp_ObtenerAlumnos'
PRINT ''
PRINT '3. sp_ObtenerAlumnoPorID'
PRINT '   EXEC sp_ObtenerAlumnoPorID @IdAlumno'
PRINT ''
PRINT '4. sp_ActualizarAlumno'
PRINT '   EXEC sp_ActualizarAlumno @IdAlumno, @Nombre, @Apellido, @FechaNacimiento, @LugarNacimiento, @Direccion, @TelefonoAlumno, @InfoEscolar, @InfoSalud'
PRINT ''
PRINT '5. sp_EliminarAlumno'
PRINT '   EXEC sp_EliminarAlumno @IdAlumno'
PRINT ''
PRINT '6. sp_BuscarAlumnosPorNombre'
PRINT '   EXEC sp_BuscarAlumnosPorNombre @NombreBusqueda'
PRINT ''
PRINT '7. sp_EstadisticasAlumnos'
PRINT '   EXEC sp_EstadisticasAlumnos'
