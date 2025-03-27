# Gestión de Bases de Datos en SSMS

Este proyecto está diseñado para automatizar el proceso de integración de datos semanales en formato CSV a una base de datos de SQL Server, asegurando que no se almacenen registros duplicados y que se mantengan registros de cada ejecución.

Para ello utilizaremos SSMS (SQL Server Management Studio 19).

![image](https://github.com/user-attachments/assets/bba72dcc-8114-4e99-ac64-7b66ac74ca9c)

## Tabla de Contenidos

1. [Instalación](#instalación)
2. [Uso](#uso)
3. [Resumen del Proceso](#resumen-del-proceso)
4. [Automatización de Scripts](#automatización-de-scripts)
5. [Registro y Programación](#registro-y-programación)
6. [Solución de Problemas](#solución-de-problemas)
7. [Fin](#fin)

---

## Instalación

### Paso 1: Restaurar la Copia de Seguridad de la Base de Datos

Puedes restaurar la base de datos utilizando archivos `.bak` o `.bacpac`.

- **Para archivo .bak:**
    - Usa SQL Server Management Studio (SSMS) para restaurar la base de datos.
    ![image](https://github.com/user-attachments/assets/53925e66-416b-447b-b897-4b2eeb0d95e0)

- **Para archivo .bacpac:**
    - Usa SSMS para importar el archivo `.bacpac`.
    ![image](https://github.com/user-attachments/assets/a3e40dc3-8e13-4022-8e61-d89d365482ad)

### Paso 2: Configurar el Entorno

Asegúrate de configurar el archivo `.env` con las variables correctas:

```env
CSV_URL=https://example.com/data.csv
SAVE_DIRECTORY=./data/CSV_Files
DB_SERVER=localhost
DB_DATABASE=Testing_ETL
DB_USERNAME=sa
DB_PASSWORD=tu_contraseña
```

---

## Uso

### Paso 1: Descargar el Archivo CSV Semanal

Ejecuta el script `weekly_extract.py` para descargar el archivo CSV semanal.

![image](https://github.com/user-attachments/assets/694906a5-6ebd-41fe-ad56-f46f216a5993)

### Paso 2: Insertar Datos en la Tabla "Unificado"

Ejecuta el script `insert_to_table.py` para insertar los datos del CSV en la base de datos.

![image](https://github.com/user-attachments/assets/6a3df976-e3c7-4fad-9945-2774c2b4b1f7)

---

## Resumen del Proceso

1. **Descargar archivo CSV**: El script `weekly_extract.py` descarga el archivo CSV.
2. **Insertar datos en la tabla**: El script `insert_to_table.py` inserta las filas del CSV en la tabla "Unificado" y añade una marca de tiempo para cada fila en el campo `FECHA_COPIA`.
3. **Eliminar duplicados**: Una consulta asegura que no queden registros duplicados en la base de datos.

```markdown
+--------------+
| IDE | Script | (weekly_extract.py)
+--------------+
|
v
+-------------------+       +----------------+
|  Solicitud GET URL  | ----> | Obtener un archivo CSV |
+-------------------+       +----------------+
|
v
+--------------+
| IDE | Script | (insert_to_table.py)
+--------------+
|
v
+-----------------------------------------------------------+
| Extraer Datos del Archivo CSV, Transformarlos y Cargarlos en SSMS |
+-----------------------------------------------------------+
|
v
+------------------+
| SSMS | Consulta SQL | ----> (Eliminar duplicados y almacenar registros de ejecución)
+------------------+
```

---

## Automatización de Scripts

Uso Windows 10 Home, así que lo mostraré usando este sistema operativo.

Para asegurar que los scripts se ejecuten sin intervención manual, la ejecución de `weekly_extract.py` e `insert_to_table.py` se automatiza utilizando el Programador de Tareas de Windows. Esto permite la descarga del archivo CSV y la inserción de datos en la base de datos en el momento programado.

* La configuración de la automatización incluye:

1. Crear tareas programadas que apunten al ejecutable de Python y las rutas de los scripts respectivos.

![image](https://github.com/user-attachments/assets/97be939d-6885-45eb-a0c7-0d39e529e322)

2. Establecer el horario para que se ejecute todos los lunes a las 🕟 4:30 AM, asegurando que los datos se actualicen semanalmente.

![image](https://github.com/user-attachments/assets/5b3055a5-9b59-4c10-a5bf-3598e86028a0)

---

## Registro y Programación

**Registros**: Cada ejecución registra detalles importantes como el número de filas afectadas, la instancia del servidor y la fecha.
![image](https://github.com/user-attachments/assets/ab0c2644-d1b2-40ff-b1cc-b44786fd5e04)

**Programación**: Para esto utilizamos el Agente de SQL Server 🛠️

1. Crear un nuevo trabajo:
   ![image](https://github.com/user-attachments/assets/415a3628-a6bb-444f-bbb1-e10388825ccf)

2. Introducir la consulta para eliminar duplicados y almacenar registros:
   ![image](https://github.com/user-attachments/assets/15c44f21-a76a-4633-b8d2-4eec7a733abd)

3. Configurar el proceso para que se ejecute automáticamente todos los lunes a las 🕔 5:00 AM:
   ![image](https://github.com/user-attachments/assets/a340e6d9-668b-4601-8895-ec6666ae9375)

---

## Solución de Problemas

- Asegúrate de que el archivo `.env` contenga las credenciales correctas de la base de datos. 🙌🏻✅
  
- Asegúrate de que tu computadora esté encendida y no en modo suspensión durante el horario programado. ❌🖥️💤
  
- Puedes revisar el historial de tareas en el Programador de Tareas para ver si se ejecutó correctamente. 🔎🧾

---

## Fin

- ¿Es posible hacer esto en servicios en la nube como GCP o AWS? ¡Por supuesto! Esto es solo para mostrar los conceptos básicos en un entorno local... 😎

---
