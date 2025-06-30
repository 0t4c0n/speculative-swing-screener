# 📁 Estructura Completa del Repositorio

## 🎯 Archivos Generados para "Speculative Swing Trading Screener"

### **Estructura del proyecto:**
```
speculative-swing-screener/
├── 📄 README.md                                    # Documentación completa
├── 📄 requirements.txt                             # Dependencias Python
├── 📄 .gitignore                                   # Archivos a ignorar
├── 🐍 speculative_screener_automated.py            # Script principal (CORE)
├── 🐍 create_speculative_dashboard.py              # Generador de dashboard
├── 🐍 test_screener_local.py                       # Script de testing local
├── .github/
│   └── workflows/
│       └── 📄 speculative-swing-analysis.yml       # Automatización GitHub Actions
└── docs/
    └── 🌐 index.html                               # Dashboard web especulativo
```

## 📋 Descripción de Archivos

### **🎯 Archivos Principales**

#### **1. `speculative_screener_automated.py`** ⭐ CORE
- **Función**: Motor principal del screener especulativo
- **Características**:
  - Pipeline optimizado con filtros en cascada (early-exit)
  - Obtención 100% dinámica de tickers (sin hardcode)
  - Análisis técnico completo con 12 filtros
  - Cálculo automático de stop loss y take profit
  - Procesa ~8,000+ acciones en 3-4 minutos
  - Sistema de scoring avanzado (0-200 puntos)

#### **2. `create_speculative_dashboard.py`**
- **Función**: Convierte resultados CSV en JSON para dashboard
- **Características**:
  - Procesa Top 10 candidatos
  - Calcula métricas de dashboard
  - Genera análisis de mercado
  - Manejo de errores robusto
  - Fallback data para casos sin resultados

#### **3. `docs/index.html`** 📱
- **Función**: Dashboard web especulativo responsive
- **Características**:
  - Diseño especulativo (colores rojos/naranjas)
  - Muestra stop loss y take profit exactos
  - Risk/reward ratios calculados
  - Métricas técnicas en tiempo real
  - Setup types y señales de entrada
  - Auto-refresh cada 10 minutos
  - Optimizado para móvil

### **⚙️ Archivos de Configuración**

#### **4. `.github/workflows/speculative-swing-analysis.yml`**
- **Función**: Automatización con GitHub Actions
- **Horarios**:
  - 4 horas después del cierre de mercado US
  - Horario estándar: 01:00 UTC (02:00 España)
  - Horario verano: 00:00 UTC (01:00 España)
- **Timeout**: 3 horas máximo
- **Deploy**: Automático a GitHub Pages

#### **5. `requirements.txt`**
- **Dependencias**:
  - `yfinance==0.2.60` (datos de mercado)
  - `pandas==2.2.3` (manipulación datos)
  - `requests==2.31.0` (APIs)
  - `numpy==1.24.3` (cálculos numéricos)

#### **6. `.gitignore`**
- **Ignora**:
  - Archivos Python temporales
  - CSVs generados por el screener
  - Archivos de IDE y OS
  - Logs y backups

### **🧪 Archivo de Testing**

#### **7. `test_screener_local.py`**
- **Función**: Probar screener localmente
- **Características**:
  - Test con muestra de acciones conocidas
  - Verificación de universe builder
  - Test de generación de dashboard
  - Debug y diagnóstico
  - No requiere toda la base de datos

#### **8. `README.md`** 📖
- **Contenido completo**:
  - Instrucciones de setup
  - Explicación de filtros técnicos
  - Sistema de scoring detallado
  - Ejemplos de setups
  - Troubleshooting
  - Disclaimers legales

## 🚀 Instrucciones de Instalación

### **Paso 1: Crear repositorio**
```bash
# En GitHub, crear repo público "speculative-swing-screener"
git clone https://github.com/[tu-usuario]/speculative-swing-screener.git
cd speculative-swing-screener
```

### **Paso 2: Copiar archivos**
Copiar todos los archivos generados en la estructura exacta mostrada arriba.

### **Paso 3: Activar GitHub Pages**
1. Ir a **Settings** > **Pages**
2. Source: **GitHub Actions**
3. Guardar

### **Paso 4: Primera ejecución**
```bash
# Test local (opcional)
pip install -r requirements.txt
python test_screener_local.py

# O esperar ejecución automática nocturna
# O ejecutar manualmente desde Actions
```

## 🎯 URLs Finales

- **Repositorio**: `https://github.com/[tu-usuario]/speculative-swing-screener`
- **Dashboard**: `https://[tu-usuario].github.io/speculative-swing-screener/`
- **Actions**: `https://github.com/[tu-usuario]/speculative-swing-screener/actions`

## ⚡ Diferencias vs Trading Bot Original

| Característica | Trading Bot Original | Speculative Screener |
|---|---|---|
| **Objetivo** | Acciones conservadoras filtradas | Swing trading especulativo |
| **Filtros** | 8 filtros conservadores | 12 filtros técnicos avanzados |
| **Risk Profile** | Bajo riesgo, dividendos | Alto riesgo/alta recompensa |
| **Timeframe** | Inversión largo plazo | Swing trading 1-2 semanas |
| **Stop Loss** | No calculado | Calculado automáticamente |
| **Take Profit** | No calculado | Calculado automáticamente |
| **Market Cap** | Cualquiera | $300M - $50B |
| **Sectores** | Todos | Especulativos/growth |
| **Dashboard** | Verde/azul conservador | Rojo/naranja especulativo |
| **Optimización** | Básica | Pipeline de cascada avanzado |

## 🔧 Personalización Fácil

### **Cambiar criterios de riesgo:**
En `speculative_screener_automated.py`:
```python
# Línea ~200 - Cambiar stop loss máximo
max_risk_stop = current_price * 0.88  # -12% en vez de -10%

# Línea ~150 - Cambiar RSI range
if 35 <= rsi_current <= 75:  # Más amplio que 40-70
```

### **Cambiar horario:**
En `.github/workflows/speculative-swing-analysis.yml`:
```yaml
- cron: '0 2 * * 2-6'   # 2 horas después en vez de 4
```

## 🎉 ¡Listo para usar!

El repositorio está **completamente funcional** con:
- ✅ Screener optimizado para 8,000+ acciones
- ✅ Dashboard especulativo responsive  
- ✅ Automatización nocturna
- ✅ Cálculo automático de stop/target
- ✅ Sistema de scoring avanzado
- ✅ Documentación completa
- ✅ Testing local incluido

**¡Solo copia los archivos y activa GitHub Pages!** 🚀