# Assets Directory

## Archivos Disponibles

### ✅ `plates_sample.dat` (28KB - Incluido en GitHub)
- **50 matrículas reales** de prueba
- Formato idéntico al archivo completo
- **Listo para Render deployment**
- Suficiente para demo y entrevista técnica

### ✅ `imgs_sample/` (1.5MB - 10 imágenes incluidas en GitHub)
- **10 imágenes reales** de matrículas
- Las más pequeñas del conjunto completo
- **Listas para visualización en Render**
- Suficiente para demo de OCR con imágenes

### ❌ `plates.dat` (115MB - Excluido de GitHub)
- Base de datos completa de matrículas españolas
- ~15,000 matrículas
- Solo disponible en desarrollo local

### ❌ `imgs/*.jpg` (~120MB - Excluidos de GitHub)
- ~300 imágenes completas de prueba
- Solo para desarrollo local
- Las 20 más pequeñas están en `imgs_sample/`

## Funcionamiento Automático

El código **detecta automáticamente** qué archivo usar:

1. Si existe `plates_sample.dat` → Lo usa (modo demo/producción)
2. Si existe `plates.dat` → Lo usa (modo desarrollo completo)
3. Si no existe ninguno → Error

**En Render:** Usará automáticamente `plates_sample.dat` ✅

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
