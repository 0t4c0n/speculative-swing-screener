# 🎯 Speculative Swing Trading Screener

Sistema automatizado de **alto riesgo/alta recompensa** que analiza acciones especulativas de NYSE, NASDAQ y AMEX usando filtros técnicos avanzados para identificar oportunidades de swing trading especulativo.

## 📱 Acceso Móvil

**Tu dashboard estará disponible en:**
`https://[tu-usuario].github.io/[nombre-repo]/`

## ⚙️ Configuración Inicial

### 1. Crear repositorio en GitHub
```bash
# Crear nuevo repositorio público en GitHub llamado "speculative-swing-screener"
```

### 2. Estructura de archivos necesaria
```
speculative-swing-screener/
├── speculative_screener_automated.py   # Script principal optimizado
├── create_speculative_dashboard.py     # Generador de JSON para dashboard
├── requirements.txt                     # Dependencias Python
├── .github/
│   └── workflows/
│       └── speculative-swing-analysis.yml  # GitHub Action
└── docs/
    └── index.html                      # Dashboard especulativo
```

### 3. Activar GitHub Pages
1. Ve a **Settings** > **Pages** en tu repositorio
2. En **Source** selecciona **GitHub Actions**
3. Guarda los cambios

### 4. Configurar automatización
El screener se ejecutará automáticamente:
- **Horario estándar (Nov-Mar)**: 01:00 UTC = 4h después del cierre (21:00 UTC)
- **Horario de verano (Mar-Nov)**: 00:00 UTC = 4h después del cierre (20:00 UTC)  
- **Días**: Martes a Sábado UTC (equivale a Lunes-Viernes días de mercado US)
- **Duración**: 60-120 minutos (análisis completo de ~8,000+ acciones)
- **Ejecución manual**: Pestaña "Actions" > "Run workflow"

### Horarios de mercado US:
- **EST (Nov-Mar)**: 9:30 AM - 4:00 PM = 14:30 - 21:00 UTC
- **EDT (Mar-Nov)**: 9:30 AM - 4:00 PM = 13:30 - 20:00 UTC

### Hora en España:
- **Horario estándar**: 02:00 (2 AM) 
- **Horario de verano**: 01:00 (1 AM)

## 🎯 Filosofía del Screener: "Technical Momentum Swing"

### **Objetivo:**
Encontrar acciones especulativas con **momentum establecido** pero no sobrecalentadas, en **pullbacks controlados** que respetan soportes técnicos, con **potencial de breakout** y **risk/reward favorable** para stops al -10%.

### **Timeframe:**
- **Swing trading clásico**: 1-2 semanas de duración
- **Gestión de riesgo**: Stop loss máximo -10%
- **Análisis**: 100% técnico (sin fundamentales)

## 🔍 Filtros Técnicos Aplicados

El screener aplica **filtros en cascada optimizados** para procesar miles de acciones eficientemente:

### **STAGE 1: Filtros Ultra-Rápidos (sin datos históricos)**
1. **Market Cap**: $300M - $50B (liquidez suficiente, no mega caps)
2. **Precio**: $5 - $150 (evitar penny stocks)
3. **Sectores**: Excluir conservadores (utilities, REITs, staples)

### **STAGE 2: Filtros Técnicos Básicos**
4. **ATR**: <8% diario (volatilidad manejable para swing)
5. **Beta**: <3.0 (especulativo pero no extremo)
6. **Tendencia**: Precio > MA50, MA21 > MA50 (alcista)
7. **Volumen**: >500K promedio (liquidez mínima)

### **STAGE 3: Análisis Técnico Completo**
8. **Momentum RSI**: 40-70 (momentum sin sobrecompra)
9. **Pullback**: -12% a 0% desde máximo 20d (entrada controlada)
10. **Volumen Spike**: >120% vs promedio 20d (confirmación institucional)
11. **Risk/Reward**: Mínimo 1:1.5 (favorable para stop -10%)
12. **Relative Strength**: Outperform SPY últimos 5 días

## 📊 Sistema de Scoring (0-200 puntos)

### **MOMENTUM SCORE (0-80 pts):**
- **RSI óptimo** (45-65): 30 pts
- **Posición vs MA21** (-5% a +3%): 25 pts  
- **Tendencia MA21 vs MA50** (>2%): 25 pts

### **BREAKOUT SCORE (0-50 pts):**
- **Pullback ideal** (-8% a -2%): 30 pts
- **Consolidación tight** (<12% rango): 20 pts

### **VOLUME SCORE (0-30 pts):**
- **Volume spike >150%**: 30 pts
- **Volume spike >120%**: 20 pts

### **QUALITY SCORE (0-40 pts):**
- **Consistencia volumen**: 15 pts
- **Estabilidad precio** (menos gaps): 25 pts

## 🎯 Clasificación de Oportunidades

### **🔥 PRIME SETUPS (160-200 pts):**
- Momentum fuerte + pullback ideal
- Volume spike confirmatorio
- Risk/reward >1:2

### **✅ GOOD SETUPS (120-159 pts):**
- Momentum establecido
- Setup técnico sólido  
- Risk/reward >1:1.5

### **⏳ WATCH LIST (80-119 pts):**
- Momentum débil o setup incompleto
- Esperar mejor entrada

## 📱 Dashboard Especulativo

### **Características:**
- ✅ **Responsive** optimizado para móvil
- 🎯 **Top 10** acciones especulativas con scoring
- 🛑 **Stop Loss** exacto (precio y %)
- 🎯 **Take Profit** exacto (precio y %)
- 📊 **Risk/Reward ratio** calculado
- 📈 **Métricas técnicas** en tiempo real
- ⚡ **Setup types** (Momentum Pullback, Breakout, etc.)
- 🔄 **Auto-refresh** cada 10 minutos

### **Información mostrada por acción:**
- **Score total** y ranking
- **Stop Loss**: Precio exacto y % pérdida
- **Take Profit**: Precio exacto y % ganancia  
- **Risk:Reward ratio** (ej: 1:1.8)
- **Setup type** (Momentum Pullback, Breakout Anticipation, etc.)
- **Métricas técnicas**: RSI, pullback %, volume spike, ATR%
- **Relative Strength** vs SPY 5d
- **Señales de entrada** específicas

## 🚀 Proceso de Ejecución Optimizado

### **Pipeline de Filtros en Cascada:**
1. **Stage 1** (5ms/acción): ~8,000 acciones → ~1,600 survivors (80% eliminadas)
2. **Stage 2** (50ms/acción): 1,600 acciones → ~400 survivors (75% eliminadas)  
3. **Stage 3** (200ms/acción): 400 acciones → ~50-100 candidates (análisis completo)
4. **Top 10 selection**: Mejores scores para dashboard

**⏱️ Tiempo total estimado**: 3-4 minutos (vs 8+ horas sin optimización)

### **Automatización nocturna:**
```
21:00 EST → Cierre mercado US
01:00 EST → Inicio screener (4h después)  
01:04 EST → Screening completo
01:05 EST → Dashboard actualizado
07:00 CET → Disponible en España
```

## 🎯 Ejemplos de Setups Ideales

### **PERFECT MOMENTUM PULLBACK:**
- Stock sube +25% último mes
- Pullback -6% desde máximo  
- RSI 58 (momentum sin sobrecompra)
- Volume 150% en pullback
- Target: +18% (resistencia técnica)
- Stop: -9% (soporte técnico)
- **R:R = 1:2.0**

### **BREAKOUT ANTICIPATION:**
- Consolidación 2 semanas en rango 8%
- Volume decreciente durante consolidación
- Precio en parte alta del rango
- MA21 rising, precio > MA21 > MA50
- Target: +15% (breakout proyectado)
- Stop: -8% (soporte consolidación)
- **R:R = 1:1.9**

## ⚠️ Consideraciones Importantes

### **Gestión de Riesgo:**
- **Stop Loss obligatorio**: Calculado técnicamente
- **Máximo riesgo**: -10% por posición
- **Risk/Reward mínimo**: 1:1.5
- **No es asesoramiento financiero**: Solo análisis técnico

### **Características del Screening:**
- **Cobertura total**: ~8,000+ acciones (NYSE + NASDAQ + AMEX)
- **100% dinámico**: Sin tickers hardcodeados
- **Altamente selectivo**: Solo Top 10 mejores setups
- **Optimizado**: Pipeline de filtros en cascada
- **Delay datos**: 15-20 min (APIs gratuitas)

### **Perfil de Riesgo:**
- **Ultra especulativo**: Solo para traders experimentados
- **Alta volatilidad**: ATR hasta 8% diario
- **Quick moves**: Setups de 1-2 semanas típicamente
- **Gestión estricta**: Stops obligatorios

## 🔧 Personalización

### **Modificar filtros técnicos:**
Edita `speculative_screener_automated.py`:
```python
# Ejemplo: Cambiar RSI range
rsi_optimal_range = (45, 65)  # Por defecto (40, 70)

# Ejemplo: Cambiar pullback máximo  
max_pullback = -10.0  # Por defecto -12.0

# Ejemplo: Cambiar volume threshold
min_volume = 1000000  # Por defecto 500,000
```

### **Modificar scoring weights:**
```python
# En función _complete_analysis()
momentum_weight = 0.35  # Por defecto 0.30
breakout_weight = 0.30  # Por defecto 0.25
volume_weight = 0.20    # Por defecto 0.15
quality_weight = 0.15   # Por defecto 0.30
```

### **Cambiar horario de ejecución:**
Modifica el `cron` en `.github/workflows/speculative-swing-analysis.yml`

## 📞 Solución de Problemas

### **Error "No data found":**
- Verificar conexión a APIs de Yahoo Finance
- Comprobar que no sea fin de semana

### **Sin candidatos en dashboard:**
- Los filtros son muy selectivos (normal)
- Verificar que el mercado tuvo sesión
- Revisar logs en GitHub Actions

### **Error en GitHub Actions:**
- Revisar logs en pestaña "Actions"
- Verificar que GitHub Pages esté activado
- Timeout si el mercado está muy volátil (normal)

### **Dashboard no actualiza:**
- Forzar refresh del navegador (Ctrl+F5)
- Verificar que el Action se ejecutó correctamente
- Comprobar timestamp en footer

## 🎯 Próximos Pasos

1. **Copia** todos los archivos a tu repositorio
2. **Activa** GitHub Pages en Settings
3. **Espera** a la próxima ejecución nocturna
4. **Opcional**: Ejecuta manualmente desde Actions para probar

## ⚖️ Disclaimer Legal

- **No es asesoramiento financiero**: Solo análisis técnico automatizado
- **Alto riesgo**: Para traders experimentados únicamente  
- **Gestión de riesgo obligatoria**: Usar stops siempre
- **Datos con delay**: No para day trading
- **Backtesting recomendado**: Probar estrategia antes de capital real

---

**🎯 Desarrollado por 0t4c0n | Speculative Swing Trading Screener**