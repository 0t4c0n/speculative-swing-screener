# 🚀 Maximum Profit Swing Trading Screener

Sistema automatizado de **máximas ganancias rápidas** que analiza acciones especulativas con filtros estrictos para identificar las mejores oportunidades de swing trading con stop loss ≤ -10% y risk:reward ≥ 2:1.

## 📱 Acceso Móvil

**Tu dashboard estará disponible en:**
`https://[tu-usuario].github.io/[nombre-repo]/`

## ⚡ Características Principales

### 🔥 Optimizado para Máximas Ganancias
- **Profit Potential Score**: Nuevo sistema de scoring que prioriza magnitud y velocidad de ganancia
- **Stop Loss Estricto**: Máximo -10% (más conservador que versión anterior)
- **Risk:Reward Mínimo**: 2:1 (solo oportunidades de alto retorno)
- **Targets Optimizados**: Prioriza resistencias más altas para maximizar ganancias

### 📊 Métricas Exclusivas
- **Profit Score**: 0-100 puntos basado en potencial de ganancia
- **Días Estimados al Target**: Predicción de velocidad del movimiento
- **Eficiencia de Ganancia**: %/día esperado
- **Target Promedio**: +15-25% típicamente

## ⚙️ Configuración Inicial

### 1. Crear repositorio en GitHub
```bash
# Crear nuevo repositorio público en GitHub llamado "speculative-swing-screener"
```

### 2. Estructura de archivos necesaria
```
speculative-swing-screener/
├── speculative_screener_automated.py   # Script principal OPTIMIZADO
├── create_speculative_dashboard.py     # Generador con profit metrics
├── requirements.txt                     # Dependencias Python
├── .github/
│   └── workflows/
│       └── speculative-swing-analysis.yml  # GitHub Action
└── docs/
    └── index.html                      # Dashboard con profit metrics
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

## 🎯 Filosofía del Screener: "Maximum Profit Optimization"

### **Objetivo:**
Encontrar las 10 mejores acciones para obtener **máximas ganancias en el menor tiempo posible** con riesgo controlado (stop ≤ -10%).

### **Criterios Clave:**
- **Alta probabilidad de movimiento rápido**: Momentum + aceleración + proximidad breakout
- **Targets ambiciosos pero realistas**: +15-25% basados en resistencias técnicas
- **Risk management estricto**: Stop loss máximo -10% sin excepciones
- **Eficiencia temporal**: Prioriza setups que pueden alcanzar target en 3-15 días

## 🔍 Sistema de Filtros Optimizado

### **STAGE 1: Filtros Ultra-Rápidos**
1. **Market Cap**: $100M - $200B (ajustado para más liquidez)
2. **Precio**: $5 - $150 (evitar penny stocks)
3. **Sectores**: Excluir conservadores (utilities, REITs, staples)

### **STAGE 2: Filtros Técnicos Básicos**
4. **ATR**: <8% diario (volatilidad manejable)
5. **Beta**: <3.0 (especulativo pero no extremo)
6. **Tendencia**: Precio > MA50, MA21 > MA50 (alcista)
7. **Volumen**: >500K promedio (liquidez mínima)

### **STAGE 3: Análisis Avanzado + Profit Optimization**
8. **Stop Loss**: ≤ -10% calculado técnicamente (FILTRO ESTRICTO)
9. **Risk/Reward**: ≥ 2:1 (FILTRO ESTRICTO)
10. **Profit Potential Score**: Combina target %, velocidad esperada y probabilidad
11. **Relative Strength**: Debe superar a SPY
12. **Entry Signals**: Múltiples confirmaciones técnicas

## 📊 Sistema de Scoring Reoptimizado (0-200 puntos)

### **🔥 PROFIT POTENTIAL SCORE (60 pts - 30% del total):**
- **Target percentage** (40% del profit score)
  - ≥20%: 100 pts
  - ≥15%: 85 pts
  - ≥12%: 70 pts
  - ≥10%: 55 pts
- **Risk/Reward ratio** (30% del profit score)
  - ≥3.0: 100 pts
  - ≥2.5: 85 pts
  - ≥2.0: 70 pts
- **Velocidad esperada** (30% del profit score)
  - Basado en momentum, aceleración y volumen

### **MOMENTUM SCORE (40 pts - 20%):**
- RSI óptimo (45-65)
- Posición vs MA21
- Tendencia MA21 vs MA50

### **RELATIVE STRENGTH (30 pts - 15%):**
- Outperformance vs SPY últimos 5 días

### **VOLUME SCORE (30 pts - 15%):**
- Volume spike confirmatorio

### **OTROS COMPONENTES (40 pts - 20%):**
- Setup Type Score (10%)
- Breakout Proximity (5%)
- Acceleration Score (3%)
- Quality Score (2%)

## 🎯 Ejemplos de Setups Ideales

### **🔥 MAXIMUM PROFIT SETUP:**
```
Ejemplo: COIN
- Precio: $75
- Stop Loss: $68 (-9.3%) - Soporte en MA21
- Take Profit: $94 (+25.3%) - Resistencia técnica
- Risk:Reward: 1:2.7
- Profit Score: 95/100
- Días estimados: 8 días
- Eficiencia: 3.2%/día
- Setup: Breakout Anticipation
- Señales: Volume +180%, RSI 62, Beat SPY +4.5%
```

### **⚡ QUICK GAIN SETUP:**
```
Ejemplo: PLTR
- Precio: $28
- Stop Loss: $25.50 (-8.9%) - Soporte técnico
- Take Profit: $33 (+17.9%) - Resistencia 20d
- Risk:Reward: 1:2.0
- Profit Score: 82/100
- Días estimados: 5 días
- Eficiencia: 3.6%/día
- Setup: Momentum Pullback
- Señales: Pullback saludable -5%, Volume spike
```

## 📱 Dashboard Mejorado

### **🔥 Nueva Sección: Profit Potential**
- **Profit Score**: Indicador visual 0-100
- **Días al Target**: Estimación de velocidad
- **Eficiencia**: Ganancia esperada por día
- **Visual destacado**: Sección naranja/dorada para métricas de profit

### **Información por Acción:**
- Todas las métricas anteriores PLUS:
- **Profit metrics destacadas** en sección especial
- **Stop loss verificado** ≤ -10%
- **R:R verificado** ≥ 2:1
- **Ranking optimizado** por potencial de ganancia

## ⚠️ Mejoras vs Versión Anterior

| Característica | Versión Anterior | Versión Optimizada |
|---|---|---|
| **Stop Loss Max** | -12% | **-10%** (más estricto) |
| **R:R Mínimo** | 1.5:1 | **2:1** (más exigente) |
| **Scoring Principal** | Total Score genérico | **Profit Potential Score** |
| **Ordenamiento Top 10** | Por score total | **Por potencial de ganancia** |
| **Take Profit** | Conservador | **Optimizado para máximo** |
| **Métricas Nuevas** | No | **Días al target, %/día** |
| **Filtros Eliminación** | Básicos | **Elimina si stop > -10%** |

## 🚀 Proceso de Ejecución

### **Pipeline Optimizado:**
1. ~8,000 acciones iniciales
2. Stage 1: ~1,600 pasan filtros rápidos (80% eliminadas)
3. Stage 2: ~400 pasan técnicos básicos (75% eliminadas)
4. Stage 3: ~50-100 análisis completo
5. **Filtro Stop ≤ -10%**: ~20-40 candidatos
6. **Filtro R:R ≥ 2:1**: ~10-20 candidatos
7. **Top 10**: Ordenados por Profit Potential Score

**⏱️ Tiempo total**: 3-4 minutos

## 🔧 Personalización Avanzada

### **Ajustar agresividad de targets:**
```python
# En _calculate_stop_loss_take_profit_silent()
atr_target_multiplier = 4.0  # Default 3.5 (más agresivo)
max_target = current_price * 1.50  # Default 1.40 (targets más altos)
```

### **Modificar velocidad esperada:**
```python
# En _estimate_days_to_target()
base_days = 7  # Default 10 (espera movimientos más rápidos)
```

### **Cambiar pesos del Profit Score:**
```python
# En _calculate_profit_potential_score()
weights = {
    'target_percentage': 0.50,  # Default 0.40 (priorizar magnitud)
    'risk_reward': 0.25,        # Default 0.30
    'speed': 0.25               # Default 0.30
}
```

## ⚡ Rendimiento Esperado

### **Escenario Optimista (Bull Market):**
- 8-10 candidatos por día
- Target promedio: +20-25%
- Tiempo promedio al target: 5-8 días
- Success rate esperado: 40-50%

### **Escenario Normal:**
- 3-7 candidatos por día
- Target promedio: +15-20%
- Tiempo promedio al target: 8-12 días
- Success rate esperado: 30-40%

### **Escenario Pesimista (Bear Market):**
- 0-3 candidatos por día
- Target promedio: +12-15%
- Tiempo promedio al target: 10-15 días
- Success rate esperado: 20-30%

## 📞 Solución de Problemas

### **"Sin candidatos en dashboard":**
- Normal en mercados laterales/bajistas
- Filtros muy estrictos garantizan calidad
- Stop ≤ -10% elimina muchas opciones
- R:R ≥ 2:1 es muy selectivo

### **"Profit Score = 0":**
- Ejecutar versión actualizada del screener
- Verificar que los CSV tienen campos nuevos
- Revisar logs de error en create_dashboard.py

### **"Targets parecen muy altos":**
- Es intencional - optimizado para máximas ganancias
- Basados en resistencias técnicas reales
- Use stops siempre para proteger capital

## ⚖️ Disclaimer Legal IMPORTANTE

- **ALTO RIESGO**: Sistema diseñado para traders agresivos
- **NO es asesoramiento financiero**: Solo análisis técnico
- **Stops obligatorios**: SIEMPRE use stop loss
- **Capital de riesgo**: Solo dinero que pueda perder
- **Backtest recomendado**: Pruebe en paper trading primero
- **Targets ambiciosos**: No todos se alcanzarán
- **Gestión de posición**: No arriesgue más del 2% por trade

## 🎯 Próximos Pasos

1. **Copia** todos los archivos actualizados a tu repositorio
2. **Verifica** que uses las versiones optimizadas (con profit metrics)
3. **Activa** GitHub Pages en Settings
4. **Opcional**: Ejecuta manualmente para probar
5. **IMPORTANTE**: Practica con paper trading primero

---

**🚀 Maximum Profit Swing Trading Screener | Stop ≤ -10% | R:R ≥ 2:1**

*Optimizado para traders que buscan máximas ganancias con riesgo controlado*