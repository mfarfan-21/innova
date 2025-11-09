# 🗄️ Opciones de Almacenamiento para Render

## ✅ SOLUCIÓN IMPLEMENTADA: Sample Data

**Estado:** ✅ LISTO PARA DEPLOY

### Qué se hizo:

1. ✅ Creado `plates_sample.dat` con 50 matrículas reales (28KB)
2. ✅ Código modificado para detectar automáticamente el archivo
3. ✅ `.gitignore` actualizado para incluir el sample
4. ✅ Funcional en Render sin configuración extra

### Cómo funciona:

```python
# El código detecta automáticamente:
if sample_path.exists():  # En Render/producción
    usar plates_sample.dat  # ✅ 50 matrículas
else:
    usar plates.dat  # 📍 Desarrollo local (~15,000 matrículas)
```

### Para tu entrevista:

**Puedes decir:**
> "Para la demo implementé un sample de 50 matrículas reales. En producción real migraría a S3/Cloudflare R2 para escalar a millones de registros, o integraría con una API OCR cloud como Google Vision para procesamiento en tiempo real sin gestión de archivos."

---

## ⚠️ Problema Original
Los archivos `plates.dat` (115MB) e imágenes de prueba (~120MB) no están en GitHub y son necesarios para el OCR.

---

## ✅ Solución 1: Variables de Entorno con Base64 (RÁPIDO - Para Demo)

**Ideal para:** Entrevista técnica, demo rápida
**Limitación:** Solo funciona con archivos pequeños (<1MB)

### Para plates.dat (115MB) - NO VIABLE
❌ Demasiado grande para variables de entorno

### Para archivo pequeño de prueba
Puedes crear un `plates_sample.dat` con solo 100 matrículas para demo:

```bash
# En tu máquina local
head -n 100 backend/assets/plates.dat > backend/assets/plates_sample.dat

# Convertir a base64
base64 backend/assets/plates_sample.dat > plates_sample_base64.txt

# Copiar contenido y añadir como variable PLATES_DATA_BASE64 en Render
```

Modificar `plates_dat_repository.py`:
```python
import os
import base64

def load_plates():
    # Intentar cargar desde variable de entorno
    plates_base64 = os.getenv('PLATES_DATA_BASE64')
    if plates_base64:
        plates_data = base64.b64decode(plates_base64).decode('utf-8')
        return parse_plates(plates_data)
    
    # Fallback a archivo local
    with open('assets/plates.dat', 'r') as f:
        return parse_plates(f.read())
```

**Pros:** Rápido, sin dependencias externas
**Contras:** Solo para archivos pequeños, limitado a ~100 matrículas

---

## ✅ Solución 2: AWS S3 / Cloudflare R2 (PRODUCCIÓN)

**Ideal para:** Producción real, escalabilidad
**Costo:** S3 Free Tier (5GB gratis), R2 (10GB gratis)

### Paso 1: Subir archivos a S3

```bash
# Instalar AWS CLI
brew install awscli  # macOS
# o
pip install awscli

# Configurar credenciales
aws configure

# Subir archivos
aws s3 cp backend/assets/plates.dat s3://innova-ocr-data/plates.dat
aws s3 sync backend/assets/imgs/ s3://innova-ocr-data/imgs/
```

### Paso 2: Modificar código para descargar en startup

Actualizar `backend/src/main.py`:

```python
import boto3
import os
from pathlib import Path

@app.on_event("startup")
async def download_assets():
    """Descargar assets de S3 al iniciar"""
    s3 = boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    # Descargar plates.dat
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    s3.download_file(
        'innova-ocr-data', 
        'plates.dat', 
        str(assets_dir / 'plates.dat')
    )
    
    print("✅ Assets descargados de S3")
```

### Paso 3: Variables en Render

```env
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=us-east-1
```

**Pros:** Profesional, escalable, producción-ready
**Contras:** Requiere configurar AWS, más complejo

---

## ✅ Solución 3: GitHub LFS (Large File Storage)

**Ideal para:** Mantener todo en GitHub
**Costo:** 1GB gratis, luego $5/mes por 50GB

### Configuración

```bash
# Instalar Git LFS
brew install git-lfs  # macOS
git lfs install

# Trackear archivos grandes
git lfs track "backend/assets/plates.dat"
git lfs track "backend/assets/imgs/*.jpg"

# Commit y push
git add .gitattributes backend/assets/
git commit -m "chore: Add LFS tracking for large assets"
git push
```

Render descargará automáticamente los archivos LFS.

**Pros:** Simple, todo en un lugar
**Contras:** Límite de 1GB free tier, costos adicionales

---

## ✅ Solución 4: API Externa para OCR (SIN ARCHIVOS LOCALES)

**Ideal para:** Producción moderna, sin gestión de archivos
**Costo:** Varios servicios gratuitos disponibles

### Servicios OCR Gratuitos

1. **Tesseract Cloud API** (gratis)
2. **OCR.space** (25,000 requests/mes gratis)
3. **Google Cloud Vision** ($300 crédito gratis)

### Implementación

```python
# backend/src/application/services/ocr_service.py
import requests

class OCRService:
    def __init__(self):
        self.api_key = os.getenv('OCR_API_KEY')
        
    async def recognize_plate(self, image_data: bytes):
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'file': image_data},
            data={'apikey': self.api_key, 'language': 'spa'}
        )
        return self.parse_ocr_response(response.json())
```

**Pros:** Sin gestión de archivos, moderna, escalable
**Contras:** Dependencia externa, puede tener latencia

---

## 🎯 Recomendación para tu Entrevista

### Opción Rápida (30 minutos):

**Usar mock data en el código**

Modificar `backend/src/infrastructure/adapters/outbound/file/plates_dat_repository.py`:

```python
class PlatesDatRepository:
    def __init__(self):
        # Mock data para demo - 10 matrículas de ejemplo
        self.mock_plates = [
            {"plate": "ABC1234", "confidence": 0.95, "coords": [...]},
            {"plate": "XYZ5678", "confidence": 0.92, "coords": [...]},
            {"plate": "MNO9012", "confidence": 0.89, "coords": [...]},
            {"plate": "DEF3456", "confidence": 0.91, "coords": [...]},
            {"plate": "GHI7890", "confidence": 0.94, "coords": [...]},
            # ... más ejemplos
        ]
    
    def get_all_plates(self):
        """Retorna mock data para demo"""
        return self.mock_plates
    
    def find_plate(self, plate_number: str):
        """Busca en mock data"""
        return next((p for p in self.mock_plates if p['plate'] == plate_number), None)
```

**Para imágenes:** Usar URLs de imágenes públicas temporales:

```python
DEMO_IMAGES = [
    "https://via.placeholder.com/600x400/009ece/ffffff?text=Plate+ABC1234",
    "https://via.placeholder.com/600x400/1c3967/ffffff?text=Plate+XYZ5678",
    # ...
]
```

**Pros:** 
- ✅ Cero configuración extra
- ✅ Deploy en 5 minutos
- ✅ Funciona para demo de entrevista
- ✅ No requiere servicios externos

**Contras:**
- ❌ No es producción real
- ❌ Datos limitados

---

## 📝 Plan de Acción Recomendado

### Para la Entrevista (HOY):
1. ✅ Usar **mock data** en el código
2. ✅ Deploy en Render con datos de ejemplo
3. ✅ Funcional en 30 minutos
4. ✅ Mencionar en la entrevista: "En producción usaría S3/R2 para almacenamiento"

### Post-Entrevista (Si consigues el trabajo):
1. Migrar a **AWS S3** o **Cloudflare R2**
2. Implementar caché en Redis para consultas frecuentes
3. O migrar a **OCR API externa** (Google Vision, Tesseract)

---

## 🚀 Implementación Inmediata

¿Quieres que implemente la **solución de mock data** ahora mismo para que puedas hacer el deploy en Render sin problemas?

Esto te permitirá:
- ✅ Deploy funcional en 15 minutos
- ✅ OCR funcionando con datos de ejemplo
- ✅ Demo lista para entrevista
- ✅ Código limpio y profesional

**Siguiente paso:** ¿Implemento el mock data o prefieres otra solución?
