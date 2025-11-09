# Assets Directory

## Excluded Files

Los siguientes archivos fueron excluidos del repositorio de GitHub debido a su tamaño:

- **`imgs/*.jpg`** - Imágenes de prueba de matrículas (~120MB total)
- **`plates.dat`** - Base de datos de matrículas españolas (115MB)

Estos archivos están disponibles localmente para desarrollo y testing.

## Configuración para Producción

Para Render deployment, asegúrate de:

1. Subir el archivo `plates.dat` mediante variables de entorno o almacenamiento externo (S3, etc.)
2. Las imágenes de prueba NO son necesarias en producción
3. El OCR procesará imágenes cargadas por usuarios en tiempo real

## Estructura

```
backend/assets/
├── imgs/           # Imágenes de prueba (excluidas de Git)
│   └── *.jpg
└── plates.dat      # Base de datos OCR (excluida de Git)
```
