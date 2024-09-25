Aquí tienes las correcciones para los `README.md` de los tres proyectos:

---

### Procesamiento y Limpieza de Datos con Pandas

```markdown
# Procesamiento y Limpieza de Datos con Pandas

Este proyecto de Python proporciona un conjunto de funciones para procesar, limpiar y validar datos en un archivo CSV, generando un archivo limpio con los datos correctos y un archivo con los datos eliminados junto con la razón de su eliminación. Además, genera un archivo CSV con estadísticas agregadas basadas en los datos limpios.

## Funcionalidades

* **Lectura de archivos CSV:** `read_file(filename)` lee un archivo CSV y devuelve un DataFrame de Pandas en fragmentos para un procesamiento eficiente de archivos grandes.
* **Validación de datos:** `validate_data(df)` valida los tipos de datos en el DataFrame (ID, Fecha, Costo) y maneja las conversiones de tipo.
* **Normalización de datos:** `normalize_data(df)` normaliza los datos del DataFrame convirtiendo los nombres de los productos a mayúsculas.
* **Eliminación de duplicados:** `delete_duplicates(df)` elimina entradas duplicadas del DataFrame basándose en el ID, manteniendo la primera ocurrencia de cada ID.
* **Generación de razones para datos inválidos:** `generate_reason(row)` genera una cadena que describe la razón por la que una fila se considera inválida.
* **Guardado de datos eliminados:** `save_deleted_data(df)` guarda los datos eliminados durante la validación o la eliminación de duplicados en un archivo CSV separado `deleted_data.csv`.
* **Generación de un CSV con agregaciones:** `generate_csv_with_aggregations(input_csv, output_csv)` procesa el archivo CSV de entrada, realiza las operaciones de limpieza y genera un nuevo archivo CSV `data_clean.csv` con los datos limpios y otro archivo CSV `statistics.csv` con estadísticas agregadas (suma y promedio del costo) por nombre de producto.

## Estructura del proyecto

```
├── generate_data.py
├── unit_test.py
├── functions.py
└── main.py
```

* **`functions.py`:** Contiene las funciones para procesar, limpiar y validar los datos.
* **`generate_data.py`:** Script para generar un conjunto de datos de prueba (opcional).
* **`main.py`:** Script principal que ejecuta el proceso de limpieza y agregación de datos.
* **`unit_test.py`:** Contiene pruebas unitarias para las funciones de procesamiento de datos.
* **`data.csv`:** Archivo CSV de entrada con datos de ejemplo (reemplazar con tus propios datos).
* **`data_clean.csv`:** Archivo CSV de salida con los datos limpios.
* **`deleted_data.csv`:** Archivo CSV de salida con los datos eliminados y la razón de su eliminación.
* **`statistics.csv`:** Archivo CSV de salida con las estadísticas agregadas por nombre de producto.

## Cómo ejecutar el proyecto

1. Clona el repositorio.
2. Instala las bibliotecas necesarias: `pip install -r requirements.txt`.
3. (Opcional) Genera datos de prueba ejecutando: `python generate_data.py`.
4. Ejecuta el script principal: `python main.py`.

El script procesará el archivo `data.csv` (o el archivo generado por `generate_data.py`), limpiará los datos, los guardará en `data_clean.csv` y generará estadísticas en `statistics.csv`. Los datos eliminados durante el proceso se guardarán en `deleted_data.csv`.

## Pruebas Unitarias

Para ejecutar las pruebas unitarias, ejecuta el siguiente comando:

```bash
python unit_test.py
```

## Registro

El proyecto utiliza el módulo `logging` para registrar información sobre el proceso de limpieza de datos. Los mensajes de registro se guardan en el archivo `data_processing.log`.

## Memoria Utilizada

El proyecto utiliza `memory_profiler` para registrar la cantidad de memoria utilizada. Los resultados se imprimen en la consola al final de la ejecución del script.
```

---

### Subida de Archivos a S3 y Google Cloud Storage

```markdown
# Subida de Archivos a S3 y Google Cloud Storage

Este proyecto de Python te permite subir archivos a buckets de Amazon S3 y Google Cloud Storage (GCS). El código está organizado en dos archivos:

- **`functions.py`:** Contiene las funciones para crear buckets y subir archivos tanto a S3 como a GCS.
- **`main.py`:** Es el script principal que utiliza las funciones de `functions.py` para subir un archivo específico a ambos servicios.

## Requisitos

- Python 3.6 o superior.

Las siguientes bibliotecas de Python son necesarias:

- `boto3`
- `google-cloud-storage`
- `python-dotenv`

Puedes instalar las bibliotecas necesarias ejecutando:

```bash
pip install boto3 google-cloud-storage python-dotenv
```

## Configuración

### Credenciales de AWS:

1. Crea un archivo `.env` en la raíz del proyecto.
2. Define las siguientes variables de entorno en el archivo `.env`:

```
AWS_ACCESS_KEY_ID=<Tu ID de clave de acceso de AWS>
AWS_SECRET_ACCESS_KEY=<Tu clave de acceso secreta de AWS>
AWS_REGION=<La región de AWS donde quieres crear el bucket (por defecto us-east-1)>
```

### Credenciales de Google Cloud:

Sigue las instrucciones en la documentación de Google Cloud para configurar las credenciales de tu proyecto de Google Cloud.

## Uso

1. Modifica `main.py`:
   - Cambia `nombre_bucket_s3` y `nombre_bucket_gcs` por los nombres de buckets deseados.
   - Cambia `nombre_archivo` por el nombre del archivo que deseas subir.
   - Asegúrate de que `ruta_archivo` apunta a la ubicación correcta del archivo.

2. Ejecuta el script:

```bash
python main.py
```

El script intentará crear los buckets si no existen y luego subirá el archivo a ambos servicios. Los mensajes de registro se guardarán en `app.log`.

## Notas

- El script está configurado para subir un archivo específico. Puedes modificarlo para subir múltiples archivos o para iterar sobre una lista de archivos.
- El script crea buckets con nombres predeterminados. Puedes modificar esto para generar nombres de buckets dinámicos o para usar nombres de buckets existentes.
- Asegúrate de que tus credenciales de AWS y Google Cloud tengan los permisos necesarios para crear buckets y subir archivos.

## Resolución de Problemas

- Si encuentras errores relacionados con las credenciales de AWS, verifica que las variables de entorno en el archivo `.env` estén configuradas correctamente.
- Si encuentras errores relacionados con las credenciales de Google Cloud, verifica que las credenciales de tu proyecto estén configuradas correctamente según la documentación de Google Cloud.
- Los mensajes de error se registrarán en el archivo `app.log`, lo que puede ayudarte a identificar y solucionar problemas.
```

---

### CEX Chatbot para WhatsApp

```markdown
# CEX Chatbot para WhatsApp

Este proyecto implementa un chatbot básico para WhatsApp utilizando la API de WhatsApp Business y Flask. El chatbot puede responder a mensajes de texto, reaccionar a mensajes y enviar stickers.

## Funcionalidades

- **Saludo de bienvenida** y menú de opciones (botones).
- **Información sobre servicios** (lista).
- Opción de obtener más información sobre **embalaje especializado** (botones).
- **Despedida** y mensaje de ayuda si el usuario ingresa un texto no reconocido.
- **Reacciones a mensajes**.
- **Envío de stickers**.

## Configuración

### Credenciales de la API de WhatsApp Business:

1. Crea un archivo `.env` en la raíz del proyecto.
2. Define las siguientes variables de entorno en el archivo `.env`:

```
TOKEN=<Token de verificación del webhook>
WHATSAPP_TOKEN=<Token de acceso de la API de WhatsApp Business>
WHATSAPP_URL=<URL de la API de WhatsApp Business>
```

### Stickers:

Asegúrate de que los IDs de stickers en `config.py` sean válidos para tu cuenta de WhatsApp Business.

## Ejecución

1. Instala las dependencias:

```bash
pip install -r requirements.txt
```

2. Configura el webhook en la plataforma de Meta para desarrolladores. La URL del webhook debe apuntar a `/webhook` en tu servidor Flask.

3. Ejecuta el servidor Flask:

```bash
python main.py
```

## Uso

Una vez que el chatbot está en ejecución, los usuarios pueden enviar mensajes a tu número de WhatsApp Business para interactuar con él.

### Flujo de conversación

- El usuario envía "hola".
- El chatbot responde con un saludo de bienvenida y un menú de opciones:
  - Servicios
  - Seguimiento de envío
- Si el usuario selecciona "Servicios", el chatbot muestra una lista de servicios:
  - Envíos nacionales
  - Envíos internacionales
  - Embalaje especializado
- Si el usuario selecciona "Embalaje especializado", el chatbot pregunta si el usuario desea obtener más información.
- Si el usuario selecciona "Sí, quiero más información", el chatbot proporcionará más detalles sobre el embalaje especializado (esta parte aún no está implementada).
- Si el usuario selecciona "No, gracias" o ingresa un texto no reconocido, el chatbot se despedirá o ofrecerá ayuda con las opciones disponibles.

## Próximos Pasos

- Implementar la lógica para proporcionar información sobre embalaje especializado.
- Agregar más opciones al menú y ampliar la funcionalidad del chatbot.
- Integrar con un sistema de gestión de envíos para proporcionar información en tiempo real sobre el seguimiento de envíos
- Implementar un sistema de aprendizaje automático para mejorar la comprensión del lenguaje natural y las respuestas del chatbot.

## Notas

- El código actual es un ejemplo básico y se puede ampliar para crear un chatbot más completo.
- Asegúrate de seguir las políticas de WhatsApp Business al utilizar la API.
- El archivo `app.log` contendrá los logs del chatbot, que pueden ser útiles para depurar errores.
