# create_speculative_dashboard.py - ACTUALIZADO para scoring optimizado
import pandas as pd
import json
import glob
import os
from datetime import datetime

def create_speculative_dashboard():
    """Convierte los resultados del screener optimizado en datos JSON para el dashboard"""
    
    print("=== CREATE SPECULATIVE DASHBOARD (Versión Optimizada) ===")
    
    try:
        # Buscar archivos de resultados más recientes
        top10_files = glob.glob("speculative_top10_*.csv")
        all_files = glob.glob("speculative_screening_results_*.csv")
        
        print(f"Archivos TOP10 encontrados: {top10_files}")
        print(f"Archivos RESULTS encontrados: {all_files}")
        
        if not top10_files:
            print("❌ No se encontraron archivos de top 10")
            return create_fallback_dashboard()
        
        # Obtener archivos más recientes
        latest_top10 = max(top10_files, key=os.path.getctime)
        latest_all = max(all_files, key=os.path.getctime) if all_files else None
        
        print(f"Procesando TOP10: {latest_top10}")
        print(f"Procesando ALL: {latest_all if latest_all else 'Ninguno'}")
        
        # Leer datos
        try:
            top10_df = pd.read_csv(latest_top10)
            print(f"✓ TOP10 leído: {len(top10_df)} filas")
        except Exception as e:
            print(f"❌ Error leyendo TOP10: {e}")
            return create_fallback_dashboard()
        
        try:
            all_df = pd.read_csv(latest_all) if latest_all else pd.DataFrame()
            print(f"✓ ALL_RESULTS leído: {len(all_df)} filas")
        except Exception as e:
            print(f"⚠️ Error leyendo ALL_RESULTS (usando DataFrame vacío): {e}")
            all_df = pd.DataFrame()
        
        # Crear estructura del dashboard con métricas optimizadas
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "market_date": datetime.now().strftime("%Y-%m-%d"),
            "summary": {
                "total_candidates": len(all_df) if not all_df.empty else len(top10_df),
                "top_picks_count": len(top10_df),
                "avg_score": round(top10_df['total_score'].mean(), 1) if not top10_df.empty else 0,
                "avg_risk_reward": round(top10_df['risk_reward_ratio_numeric'].mean(), 1) if not top10_df.empty and 'risk_reward_ratio_numeric' in top10_df.columns else 0,
                "avg_relative_strength": round(top10_df['relative_strength_5d'].mean(), 1) if not top10_df.empty and 'relative_strength_5d' in top10_df.columns else 0,
                "message": "Oportunidades especulativas optimizadas para swing 1-2 semanas" if len(top10_df) > 0 else "Sin oportunidades especulativas"
            },
            "top_picks": [],
            "market_analysis": {},
            "screening_criteria": {
                "scoring_system": "Optimizado para swing 1-2 semanas",
                "relative_strength": "20% - Outperform SPY requerido",
                "setup_type": "15% - Prioriza breakouts inminentes", 
                "volume": "20% - Confirmación institucional",
                "momentum": "25% - RSI 40-70, tendencia alcista",
                "breakout_proximity": "10% - Cerca de resistencias",
                "momentum_acceleration": "5% - Detecta aceleración",
                "quality": "5% - Estabilidad técnica",
                "market_cap_range": "$100M - $200B",
                "price_range": "$5 - $150",
                "max_atr": "8% (volatilidad manejable)",
                "stop_loss": "Máximo -10% riesgo",
                "risk_reward": "Mínimo 1:1.5"
            }
        }
        
        print(f"Dashboard data estructura creada")
        print(f"Summary: {dashboard_data['summary']}")
        
        if not top10_df.empty:
            print("Procesando top picks con métricas optimizadas...")
            
            # Procesar cada acción del top 10
            for i, (_, row) in enumerate(top10_df.iterrows()):
                try:
                    # Datos básicos
                    symbol = row['symbol']
                    company_name = str(row.get('company_name', symbol))[:35]
                    sector = str(row.get('sector', 'N/A'))
                    current_price = float(row['current_price'])
                    total_score = float(row['total_score'])
                    
                    # Stop loss y take profit
                    stop_loss_data = row.get('stop_loss', {})
                    take_profit_data = row.get('take_profit', {})
                    
                    if isinstance(stop_loss_data, dict):
                        stop_loss_price = float(stop_loss_data.get('price', current_price * 0.9))
                        stop_loss_pct = float(stop_loss_data.get('loss_percentage', -10.0))
                        stop_loss_method = stop_loss_data.get('method', 'N/A')
                    else:
                        stop_loss_price = current_price * 0.9
                        stop_loss_pct = -10.0
                        stop_loss_method = 'Fallback'
                    
                    if isinstance(take_profit_data, dict):
                        take_profit_price = float(take_profit_data.get('price', current_price * 1.15))
                        take_profit_pct = float(take_profit_data.get('gain_percentage', 15.0))
                        take_profit_method = take_profit_data.get('method', 'N/A')
                    else:
                        take_profit_price = current_price * 1.15
                        take_profit_pct = 15.0
                        take_profit_method = 'Fallback'
                    
                    risk_reward_ratio = str(row.get('risk_reward_ratio', '1:1.5'))
                    
                    # Scores individuales (NUEVOS)
                    momentum_score = float(row.get('momentum_score', 0))
                    relative_strength_score = float(row.get('relative_strength_score', 0))
                    volume_score = float(row.get('volume_score', 0))
                    setup_score = float(row.get('setup_score', 0))
                    proximity_score = float(row.get('proximity_score', 0))
                    acceleration_score = float(row.get('acceleration_score', 0))
                    quality_score = float(row.get('quality_score', 0))
                    
                    # Compatibilidad con versión anterior
                    breakout_score = float(row.get('breakout_score', 0))
                    
                    setup_type = str(row.get('setup_type', 'Mixed Setup'))
                    
                    # Datos técnicos
                    technical_data = row.get('technical_data', {})
                    if isinstance(technical_data, str):
                        try:
                            technical_data = json.loads(technical_data.replace("'", '"'))
                        except:
                            technical_data = {}
                    
                    rsi = technical_data.get('rsi', 50)
                    pullback_pct = technical_data.get('pullback_pct', 0)
                    volume_spike = technical_data.get('volume_spike', 1.0)
                    atr_pct = technical_data.get('atr_pct', 0)
                    breakout_proximity_pct = technical_data.get('breakout_proximity_pct', 0)
                    
                    # Señales de entrada
                    entry_signals = row.get('entry_signals', [])
                    if isinstance(entry_signals, str):
                        try:
                            entry_signals = json.loads(entry_signals.replace("'", '"'))
                        except:
                            entry_signals = ["RSI momentum", "Setup confirmado", "Volume increase"]
                    
                    # Relative strength (NUEVO CAMPO IMPORTANTE)
                    relative_strength = row.get('relative_strength_5d', 0)
                    
                    pick = {
                        "rank": i + 1,
                        "symbol": symbol,
                        "company": company_name,
                        "sector": sector,
                        "price": round(current_price, 2),
                        "score": round(total_score, 1),
                        "stop_loss": {
                            "price": round(stop_loss_price, 2),
                            "loss_percentage": round(stop_loss_pct, 1),
                            "method": stop_loss_method
                        },
                        "take_profit": {
                            "price": round(take_profit_price, 2),
                            "gain_percentage": round(take_profit_pct, 1),
                            "method": take_profit_method
                        },
                        "risk_reward": risk_reward_ratio,
                        "setup_type": setup_type,
                        "metrics": {
                            # Métricas básicas (compatibilidad)
                            "momentum_score": round(momentum_score, 1),
                            "breakout_score": round(breakout_score, 1),
                            "volume_score": round(volume_score, 1),
                            "rsi": round(float(rsi), 1),
                            "pullback_pct": round(float(pullback_pct), 1),
                            "volume_spike": round(float(volume_spike), 2),
                            "atr_pct": round(float(atr_pct), 1),
                            "relative_strength_5d": round(float(relative_strength), 1) if relative_strength else 0,
                            
                            # NUEVAS MÉTRICAS DEL SCORING OPTIMIZADO
                            "relative_strength_score": round(relative_strength_score, 1),
                            "setup_score": round(setup_score, 1),
                            "proximity_score": round(proximity_score, 1),
                            "acceleration_score": round(acceleration_score, 1),
                            "quality_score": round(quality_score, 1),
                            "breakout_proximity_pct": round(float(breakout_proximity_pct), 1)
                        },
                        "entry_signals": entry_signals[:3] if isinstance(entry_signals, list) else ["Setup técnico confirmado"],
                        "market_cap_millions": int(row.get('market_cap_millions', 0)),
                        
                        # SCORING BREAKDOWN PARA ANÁLISIS
                        "scoring_breakdown": {
                            "momentum": round(momentum_score, 1),
                            "relative_strength": round(relative_strength_score, 1),
                            "volume": round(volume_score, 1),
                            "setup_type": round(setup_score, 1),
                            "proximity": round(proximity_score, 1),
                            "acceleration": round(acceleration_score, 1),
                            "quality": round(quality_score, 1)
                        }
                    }
                    
                    dashboard_data["top_picks"].append(pick)
                    
                except Exception as e:
                    print(f"⚠️ Error procesando fila {i}: {e}")
                    # Crear entrada básica en caso de error
                    pick = {
                        "rank": i + 1,
                        "symbol": str(row.get('symbol', f'STOCK{i}')),
                        "company": str(row.get('company_name', 'N/A'))[:35],
                        "sector": str(row.get('sector', 'N/A')),
                        "price": round(float(row.get('current_price', 0)), 2),
                        "score": round(float(row.get('total_score', 0)), 1),
                        "stop_loss": {
                            "price": round(float(row.get('current_price', 0)) * 0.9, 2),
                            "loss_percentage": -10.0,
                            "method": "Fallback"
                        },
                        "take_profit": {
                            "price": round(float(row.get('current_price', 0)) * 1.15, 2),
                            "gain_percentage": 15.0,
                            "method": "Fallback"
                        },
                        "risk_reward": "1:1.5",
                        "setup_type": "Mixed Setup",
                        "metrics": {
                            "momentum_score": 0,
                            "breakout_score": 0,
                            "volume_score": 0,
                            "rsi": 50,
                            "pullback_pct": 0,
                            "volume_spike": 1.0,
                            "atr_pct": 0,
                            "relative_strength_5d": 0,
                            "relative_strength_score": 0,
                            "setup_score": 0,
                            "proximity_score": 0,
                            "acceleration_score": 0,
                            "quality_score": 0
                        },
                        "entry_signals": ["Error en procesamiento"],
                        "market_cap_millions": 0,
                        "scoring_breakdown": {
                            "momentum": 0,
                            "relative_strength": 0,
                            "volume": 0,
                            "setup_type": 0,
                            "proximity": 0,
                            "acceleration": 0,
                            "quality": 0
                        }
                    }
                    dashboard_data["top_picks"].append(pick)
            
            print(f"✓ {len(dashboard_data['top_picks'])} acciones añadidas a top_picks")
            
            # Análisis del mercado con nuevas métricas
            if not top10_df.empty:
                try:
                    # Distribución por setup type
                    setup_distribution = {}
                    for pick in dashboard_data["top_picks"]:
                        setup = pick["setup_type"]
                        setup_distribution[setup] = setup_distribution.get(setup, 0) + 1
                    
                    # Sectores más representados
                    sector_distribution = {}
                    for pick in dashboard_data["top_picks"]:
                        sector = pick["sector"]
                        if sector != 'N/A':
                            sector_distribution[sector] = sector_distribution.get(sector, 0) + 1
                    
                    # Análisis de relative strength
                    rs_values = [pick["metrics"]["relative_strength_5d"] for pick in dashboard_data["top_picks"] if pick["metrics"]["relative_strength_5d"] != 0]
                    avg_relative_strength = round(sum(rs_values) / len(rs_values), 1) if rs_values else 0
                    
                    # Análisis de scores optimizados
                    scoring_analysis = {
                        "avg_momentum": round(sum(pick["scoring_breakdown"]["momentum"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "avg_relative_strength": round(sum(pick["scoring_breakdown"]["relative_strength"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "avg_volume": round(sum(pick["scoring_breakdown"]["volume"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "avg_setup": round(sum(pick["scoring_breakdown"]["setup_type"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "avg_proximity": round(sum(pick["scoring_breakdown"]["proximity"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1)
                    }
                    
                    dashboard_data["market_analysis"] = {
                        "setup_distribution": setup_distribution,
                        "sector_distribution": sector_distribution,
                        "avg_rsi": round(sum(pick["metrics"]["rsi"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "avg_pullback": round(sum(pick["metrics"]["pullback_pct"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "avg_volume_spike": round(sum(pick["metrics"]["volume_spike"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 2),
                        "avg_relative_strength_vs_spy": avg_relative_strength,
                        "scoring_analysis": scoring_analysis,
                        "optimization_note": "Criterios optimizados para swing trading de 1-2 semanas"
                    }
                    
                    print(f"✓ Análisis de mercado calculado con métricas optimizadas")
                    
                except Exception as e:
                    print(f"⚠️ Error calculando análisis de mercado: {e}")
        
        # Estadísticas adicionales con nuevas métricas
        if dashboard_data["top_picks"]:
            dashboard_data["statistics"] = {
                "avg_score": round(sum(pick["score"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                "price_range": {
                    "min": round(min(pick["price"] for pick in dashboard_data["top_picks"]), 2),
                    "max": round(max(pick["price"] for pick in dashboard_data["top_picks"]), 2)
                },
                "avg_risk_percentage": round(sum(abs(pick["stop_loss"]["loss_percentage"]) for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                "avg_reward_percentage": round(sum(pick["take_profit"]["gain_percentage"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                "relative_strength_stats": {
                    "outperformers": len([pick for pick in dashboard_data["top_picks"] if pick["metrics"]["relative_strength_5d"] > 0]),
                    "avg_outperformance": round(sum([pick["metrics"]["relative_strength_5d"] for pick in dashboard_data["top_picks"] if pick["metrics"]["relative_strength_5d"] > 0]) / len([pick for pick in dashboard_data["top_picks"] if pick["metrics"]["relative_strength_5d"] > 0]), 1) if len([pick for pick in dashboard_data["top_picks"] if pick["metrics"]["relative_strength_5d"] > 0]) > 0 else 0
                },
                "setup_type_breakdown": {
                    setup: len([pick for pick in dashboard_data["top_picks"] if pick["setup_type"] == setup])
                    for setup in set(pick["setup_type"] for pick in dashboard_data["top_picks"])
                }
            }
            print("✓ Estadísticas calculadas con métricas optimizadas")
        else:
            dashboard_data["statistics"] = {
                "message": "Sin oportunidades especulativas que cumplan criterios optimizados",
                "suggestion": "Filtros optimizados para swing 1-2 semanas son muy selectivos"
            }
        
        # Crear directorio docs si no existe
        print("Creando directorio docs...")
        os.makedirs('docs', exist_ok=True)
        print("✓ Directorio docs creado/verificado")
        
        # Guardar JSON
        json_path = 'docs/data.json'
        print(f"Guardando JSON optimizado en: {json_path}")
        
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Dashboard data optimizado creado: {json_path}")
            
            # Verificar que se creó
            if os.path.exists(json_path):
                size = os.path.getsize(json_path)
                print(f"✅ Archivo verificado - Tamaño: {size} bytes")
                
                # Mostrar resumen del contenido optimizado
                print(f"📊 Resumen del dashboard optimizado:")
                print(f"   - Candidatos totales: {dashboard_data['summary']['total_candidates']}")
                print(f"   - Top picks: {dashboard_data['summary']['top_picks_count']}")
                print(f"   - Score promedio: {dashboard_data['summary']['avg_score']}")
                print(f"   - R:R promedio: {dashboard_data['summary']['avg_risk_reward']}")
                print(f"   - Relative Strength promedio: {dashboard_data['summary']['avg_relative_strength']}")
                
            else:
                print("❌ El archivo no se pudo verificar")
                return False
                
        except Exception as e:
            print(f"❌ Error guardando JSON: {e}")
            return False
        
        # Crear archivo de última actualización
        try:
            with open('docs/last_update.txt', 'w') as f:
                f.write(datetime.now().isoformat())
            print("✓ Archivo last_update.txt creado")
        except Exception as e:
            print(f"⚠️ Error creando last_update.txt: {e}")
        
        print(f"🎉 Dashboard especulativo optimizado completamente generado!")
        print(f"🎯 Scoring optimizado para swing trading de 1-2 semanas aplicado")
        return True
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_fallback_dashboard():
    """Crea un dashboard de fallback cuando no hay datos - versión optimizada"""
    print("Creando dashboard de fallback optimizado...")
    
    fallback_data = {
        "timestamp": datetime.now().isoformat(),
        "market_date": datetime.now().strftime("%Y-%m-%d"),
        "summary": {
            "total_candidates": 0,
            "top_picks_count": 0,
            "avg_score": 0,
            "avg_risk_reward": 0,
            "avg_relative_strength": 0,
            "message": "Sin oportunidades especulativas - Criterios optimizados muy selectivos"
        },
        "top_picks": [],
        "market_analysis": {
            "message": "No hay datos suficientes para análisis de mercado",
            "suggestion": "Los criterios optimizados para swing 1-2 semanas son muy estrictos"
        },
        "screening_criteria": {
            "scoring_system": "Optimizado para swing 1-2 semanas",
            "relative_strength": "20% - Outperform SPY requerido",
            "setup_type": "15% - Prioriza breakouts inminentes", 
            "volume": "20% - Confirmación institucional",
            "momentum": "25% - RSI 40-70, tendencia alcista",
            "breakout_proximity": "10% - Cerca de resistencias",
            "momentum_acceleration": "5% - Detecta aceleración",
            "quality": "5% - Estabilidad técnica",
            "market_cap_range": "$100M - $200B",
            "price_range": "$5 - $150",
            "max_atr": "8% (volatilidad manejable)",
            "stop_loss": "Máximo -10% riesgo",
            "risk_reward": "Mínimo 1:1.5"
        },
        "statistics": {
            "message": "Sin datos para mostrar estadísticas",
            "reasons": [
                "Scoring optimizado para swing trading de 1-2 semanas",
                "Relative strength vs SPY requerido",
                "Setup types específicos priorizados",
                "Criterios técnicos muy estrictos",
                "Próxima ejecución en 24 horas"
            ]
        }
    }
    
    # Guardar JSON de fallback
    os.makedirs('docs', exist_ok=True)
    
    try:
        with open('docs/data.json', 'w', encoding='utf-8') as f:
            json.dump(fallback_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Dashboard de fallback optimizado creado")
        return True
        
    except Exception as e:
        print(f"❌ Error creando dashboard de fallback: {e}")
        return False

if __name__ == "__main__":
    success = create_speculative_dashboard()
    if success:
        print("\n✅ SUCCESS: Dashboard especulativo optimizado creado correctamente")
        print("📱 Abre docs/index.html en tu navegador")
        print("🎯 Nuevo sistema de scoring para swing trading de 1-2 semanas activo")
    else:
        print("\n❌ FAILED: Revisar errores arriba")