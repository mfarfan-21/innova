# ✅ LISTO PARA DEPLOYMENT EN RENDER

## 🎯 Estado Actual

**✅ TODO CONFIGURADO Y LISTO**

- ✅ Código subido a GitHub: https://github.com/mfarfan-21/innova.git
- ✅ `plates_sample.dat` incluido (50 matrículas reales, 28KB)
- ✅ Código auto-detecta sample vs full data
- ✅ Backend testeado localmente ✅
- ✅ Ready para Render deployment

---

## 🚀 Deployment en Render (15 minutos)

### Paso 1: Crear Web Service

1. Ve a https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Conecta GitHub si no lo has hecho
4. Selecciona: **`mfarfan-21/innova`**
5. Click **"Connect"**

### Paso 2: Configuración (Auto-detectada)

Render detectará automáticamente `backend/render.yaml`:

```yaml
✅ Name: innova-backend
✅ Environment: Python
✅ Region: Oregon (Free)
✅ Root Directory: /backend
✅ Build: pip install -r requirements.txt
✅ Start: uvicorn src.main:app --host 0.0.0.0 --port $PORT
✅ Health Check: /health
```

**Importante:** Asegúrate que "Root Directory" sea `/backend` o `backend`

### Paso 3: Variables de Entorno

Agrega en la sección **"Environment Variables"**:

```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_anon_key_de_supabase
PYTHON_VERSION=3.11.0
```

**Obtener credenciales:**
1. Ve a tu proyecto Supabase: https://supabase.com/dashboard
2. Settings → API
3. Copia:
   - Project URL → `SUPABASE_URL`
   - Project API keys → anon/public → `SUPABASE_KEY`

### Paso 4: Deploy

1. Click **"Create Web Service"**
2. Espera ~3-5 minutos (verás los logs en tiempo real)
3. Una vez completado: `✅ Live`
4. Tu URL: `https://innova-backend-xxxx.onrender.com`

### Paso 5: Verificación

```bash
# Health check
curl https://tu-url.onrender.com/health

# Debería responder:
{"status":"healthy"}
```

```bash
# Test OCR endpoint
curl https://tu-url.onrender.com/ocr/plates

# Debería listar ~50 matrículas
```

---

## 🌐 Frontend en Vercel (10 minutos)

### Paso 1: Crear Proyecto

1. Ve a https://vercel.com/dashboard
2. **"Add New..."** → **"Project"**
3. Importa: **`mfarfan-21/innova`**
4. Framework: **Vite** (auto-detectado)

### Paso 2: Configuración del Build

Vercel configurará automáticamente:

```
✅ Build Command: npm run build
✅ Output Directory: dist
✅ Install Command: npm install
```

### Paso 3: Variables de Entorno

Agrega estas variables:

```env
VITE_SUPABASE_URL=tu_url_de_supabase
VITE_SUPABASE_ANON_KEY=tu_anon_key_de_supabase
VITE_API_URL=https://tu-backend.onrender.com
```

**Importante:** `VITE_API_URL` debe ser la URL de Render (Paso anterior)

### Paso 4: Deploy

1. Click **"Deploy"**
2. Espera ~2-3 minutos
3. Tu URL: `https://innova-xxxx.vercel.app`

---

## 🔧 CORS Configuration

Si recibes errores de CORS, actualiza `backend/src/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://innova-xxxx.vercel.app"  # ← Agrega tu URL de Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Luego:
```bash
git add backend/src/main.py
git commit -m "fix: Add Vercel URL to CORS"
git push
```

Render se re-deployará automáticamente.

---

## ✅ Testing Post-Deployment

### 1. Backend Health
```bash
curl https://tu-backend.onrender.com/health
```

### 2. Backend OCR List
```bash
curl https://tu-backend.onrender.com/ocr/plates | head -20
```

### 3. Frontend
1. Navega a `https://innova-xxxx.vercel.app`
2. Login con tus credenciales Supabase
3. Prueba:
   - ✅ Home → Ver tarjetas
   - ✅ OCR → Procesar matrícula
   - ✅ Chatbot → Enviar mensaje

---

## 📊 Sample Data Info

El sistema está usando **`plates_sample.dat`** con:

- ✅ **50 matrículas reales** españolas
- ✅ Formato idéntico al archivo completo
- ✅ Suficiente para demo profesional
- ✅ Tamaño: 28KB (GitHub-friendly)

**Matrículas de ejemplo:**
- MD719JJ, MD558LJ, CS32WO, W0597WW
- Y 46 más...

---

## 🎤 Para la Entrevista

### Pregunta Esperada:
> "¿Por qué solo 50 matrículas?"

### Tu Respuesta:
> "Para la demo implementé un sample de 50 matrículas reales que permiten demostrar toda la funcionalidad sin comprometer el tamaño del repositorio. El sistema está diseñado con un patrón Repository que permite escalar fácilmente:
> 
> **Opciones de escalado:**
> 1. Migrar a AWS S3/Cloudflare R2 para almacenar millones de registros
> 2. Integrar con Google Cloud Vision o Tesseract Cloud para OCR en tiempo real
> 3. Implementar una base de datos PostgreSQL con indexación completa
> 
> El código ya soporta esto gracias a la arquitectura hexagonal - solo cambiaría la implementación del repositorio sin tocar la lógica de negocio."

---

## ⚠️ Limitaciones Free Tier

### Render Backend
- **Sleep después de 15 min** de inactividad
- Primera request tras sleep: ~30-60 segundos
- **Solución:** UptimeRobot para ping cada 10 min (gratis)

### Vercel Frontend
- ✅ Sin sleep, siempre activo
- ✅ 100 GB bandwidth/mes
- ✅ Despliegues automáticos en push

---

## 🐛 Troubleshooting

### "Module not found" en Render
✅ Verifica que Root Directory sea `/backend` o `backend`

### CORS errors en frontend
✅ Agrega tu URL de Vercel al CORS en `main.py`

### OCR endpoint returns 404
✅ Verifica que `plates_sample.dat` esté en el repositorio
✅ Check logs en Render Dashboard

### "No se encontró plates.dat"
✅ Verifica que `plates_sample.dat` esté incluido en GitHub
✅ Check `.gitignore` permite `!backend/assets/plates_sample.dat`

---

## 📞 Next Steps

1. ✅ **Deploy Backend** → Render (~15 min)
2. ✅ **Deploy Frontend** → Vercel (~10 min)
3. ✅ **Test End-to-End** → Login + OCR + Chatbot
4. ✅ **Preparar Demo** → Screenshots, bullet points
5. ✅ **¡Entrevista!** → Mostrar código + demo live

---

**🎉 ¡Todo listo! Siguiente paso: Deploy en Render**

Repository: https://github.com/mfarfan-21/innova.git
