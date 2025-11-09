# 🚀 Guía de Despliegue - INNOVA Platform

## ✅ Estado Actual

- ✅ Código subido a GitHub: https://github.com/mfarfan-21/innova.git
- ✅ Backend configurado con `render.yaml`
- ✅ Tests pasando: 24/24
- ⏳ Pending: Deploy en Render + Vercel

---

## 📦 Backend Deployment (Render)

### Paso 1: Conectar GitHub con Render

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu cuenta de GitHub si aún no lo has hecho
4. Selecciona el repositorio: **`mfarfan-21/innova`**
5. Click en **"Connect"**

### Paso 2: Configuración Automática

Render detectará automáticamente el archivo `backend/render.yaml` y configurará:

- ✅ **Name:** innova-backend
- ✅ **Environment:** Python
- ✅ **Region:** Oregon (Free tier)
- ✅ **Build Command:** `pip install -r requirements.txt`
- ✅ **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- ✅ **Root Directory:** `/backend`

### Paso 3: Variables de Entorno

Configura las siguientes variables en **Environment** tab:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-supabase-anon-key
PYTHON_VERSION=3.11.0
```

**Obtener las credenciales de Supabase:**
1. Ve a tu proyecto en [Supabase Dashboard](https://supabase.com/dashboard)
2. Settings → API
3. Copia `Project URL` → SUPABASE_URL
4. Copia `anon/public key` → SUPABASE_KEY

### Paso 4: Deploy

1. Click en **"Create Web Service"**
2. Espera a que el build termine (~3-5 minutos)
3. Una vez completado, verás la URL: `https://innova-backend.onrender.com`
4. Verifica que el endpoint `/health` responda correctamente

### Verificación del Backend

```bash
# Health check
curl https://innova-backend.onrender.com/health

# Respuesta esperada:
# {"status": "healthy"}
```

---

## 🌐 Frontend Deployment (Vercel - Recomendado)

### Paso 1: Conectar con Vercel

1. Ve a [Vercel Dashboard](https://vercel.com/dashboard)
2. Click en **"Add New..."** → **"Project"**
3. Importa el repositorio: **`mfarfan-21/innova`**
4. Vercel detectará automáticamente que es un proyecto Vite

### Paso 2: Configuración del Build

Vercel configurará automáticamente:

- ✅ **Framework Preset:** Vite
- ✅ **Build Command:** `npm run build`
- ✅ **Output Directory:** `dist`
- ✅ **Install Command:** `npm install`

### Paso 3: Variables de Entorno

Agrega las siguientes variables en **Environment Variables**:

```env
VITE_SUPABASE_URL=https://tu-proyecto.supabase.co
VITE_SUPABASE_ANON_KEY=tu-supabase-anon-key
VITE_API_URL=https://innova-backend.onrender.com
```

**Importante:** Usa la URL de Render del backend en `VITE_API_URL`

### Paso 4: Deploy

1. Click en **"Deploy"**
2. Espera ~2-3 minutos
3. Una vez completado, verás la URL: `https://innova-xxxx.vercel.app`
4. Accede y prueba el login, OCR y chatbot

---

## 🔧 Configuración CORS en Backend

Si recibes errores de CORS, asegúrate de que `src/main.py` incluya el dominio de Vercel:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://innova-xxxx.vercel.app"  # ← Agrega tu dominio de Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Después del cambio:
```bash
git add backend/src/main.py
git commit -m "fix: Add Vercel domain to CORS allowed origins"
git push
```

Render se actualizará automáticamente.

---

## ⚠️ Limitaciones del Free Tier

### Render (Backend)
- ⏱️ **Sleep after 15 min** de inactividad
- 🐌 Primera request tras sleep: ~30-60 segundos
- 📊 **750 horas/mes** gratuitas
- 💾 Memoria limitada

**Solución:** Usar un servicio de ping cada 10 minutos (UptimeRobot, etc.) o actualizar a plan pagado.

### Vercel (Frontend)
- ✅ Sin sleep, siempre activo
- ✅ 100 GB bandwidth/mes
- ✅ CDN global
- ✅ Despliegues automáticos en cada push

---

## 📝 Testing Post-Deployment

### 1. Backend Health Check
```bash
curl https://innova-backend.onrender.com/health
```

### 2. Login Test
```bash
curl -X POST https://innova-backend.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

### 3. Frontend
- Navega a `https://innova-xxxx.vercel.app`
- Inicia sesión con tus credenciales de Supabase
- Prueba el OCR subiendo una imagen
- Prueba el chatbot haciendo una pregunta

---

## 🐛 Troubleshooting

### Backend no responde
- ✅ Verifica que las variables `SUPABASE_URL` y `SUPABASE_KEY` están configuradas
- ✅ Revisa los logs en Render Dashboard → "Logs" tab
- ✅ Confirma que el health endpoint funciona: `/health`

### Frontend muestra errores de API
- ✅ Verifica que `VITE_API_URL` apunta a la URL correcta de Render
- ✅ Confirma que CORS está configurado correctamente en el backend
- ✅ Abre DevTools (F12) → Console para ver errores específicos

### OCR no funciona
- ✅ El archivo `plates.dat` NO está en el repositorio (115MB)
- ✅ Para producción, necesitas configurar un almacenamiento externo (S3, etc.)
- ✅ Alternativamente, sube el archivo manualmente en Render o usa una API de OCR externa

---

## 🎯 Next Steps

1. ✅ Deploy backend en Render
2. ✅ Deploy frontend en Vercel
3. ✅ Configurar variables de entorno
4. ✅ Verificar que todo funciona end-to-end
5. 📧 Opcional: Configurar dominio personalizado
6. 📊 Opcional: Configurar monitoring (Sentry, LogRocket)
7. 🔒 Opcional: Mejorar seguridad (rate limiting, API keys)

---

## 📞 Support

Si tienes problemas:
- 📖 Revisa los logs en Render/Vercel
- 🐛 Verifica errores en la consola del navegador (F12)
- 📧 Contacta al equipo de desarrollo

---

**¡Listo para la demo de tu entrevista técnica!** 🚀
