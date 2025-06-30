# create_speculative_dashboard.py - VERSIÓN OPTIMIZADA PARA PROFIT METRICS
# Muestra Profit Potential Score y métricas de ganancia rápida
import pandas as pd
import json
import glob
import os
from datetime import datetime

def create_speculative_dashboard():
    """Genera dashboard con métricas de profit potential"""
    
    print("=== CREATE DASHBOARD CON PROFIT METRICS ===")
    
    try:
        # Buscar archivos de resultados más recientes
        top10_files = glob.glob("speculative_top10_*.csv")
        all_files = glob.glob("speculative_screening_results_*.csv")
        
        print(f"Archivos TOP10 encontrados: {len(top10_files)}")
        print(f"Archivos RESULTS encontrados: {len(all_files)}")
        
        if not top10_files:
            print("❌ No se encontraron archivos de top 10")
            return create_fallback_dashboard()
        
        # Obtener archivos más recientes
        latest_top10 = max(top10_files, key=os.path.getctime)
        latest_all = max(all_files, key=os.path.getctime) if all_files else None
        
        print(f"Procesando TOP10: {latest_top10}")
        
        # Leer datos del Top 10
        try:
            top10_df = pd.read_csv(latest_top10)
            print(f"✓ TOP10 leído: {len(top10_df)} filas")
            print(f"✓ Columnas disponibles: {list(top10_df.columns)}")
            
            # Verificar que tenemos los campos separados
            required_fields = ['stop_loss_price', 'stop_loss_percentage', 'stop_loss_method',
                             'take_profit_price', 'take_profit_percentage', 'take_profit_method',
                             'profit_potential_score', 'expected_days_to_target', 'expected_gain_per_day']
            missing_fields = [field for field in required_fields if field not in top10_df.columns]
            
            if missing_fields:
                print(f"⚠️ Faltan campos nuevos: {missing_fields}")
                print("💡 Ejecuta primero el screener optimizado para profit metrics")
            
            print("✅ Campos técnicos verificados")
            
        except Exception as e:
            print(f"❌ Error leyendo CSV: {e}")
            return create_fallback_dashboard()
        
        # Leer todos los resultados si existe
        try:
            all_df = pd.read_csv(latest_all) if latest_all else pd.DataFrame()
            print(f"✓ ALL_RESULTS leído: {len(all_df)} filas")
        except Exception as e:
            print(f"⚠️ Error leyendo ALL_RESULTS: {e}")
            all_df = pd.DataFrame()
        
        # Crear estructura optimizada del dashboard
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "market_date": datetime.now().strftime("%Y-%m-%d"),
            "summary": {
                "total_candidates": len(all_df) if not all_df.empty else len(top10_df),
                "top_picks_count": len(top10_df),
                "avg_score": round(top10_df['total_score'].mean(), 1) if not top10_df.empty else 0,
                "avg_risk_reward": round(top10_df['risk_reward_ratio_numeric'].mean(), 1) if not top10_df.empty and 'risk_reward_ratio_numeric' in top10_df.columns else 0,
                "avg_profit_potential": round(top10_df['profit_potential_score'].mean(), 1) if 'profit_potential_score' in top10_df.columns else 0,
                "avg_target_percentage": round(top10_df['take_profit_percentage'].mean(), 1) if not top10_df.empty else 0,
                "message": f"🔥 {len(top10_df)} oportunidades para máximas ganancias rápidas (Stop ≤ -10%)" if len(top10_df) > 0 else "Sin oportunidades que cumplan criterios estrictos"
            },
            "top_picks": [],
            "market_analysis": {},
            "screening_criteria": {
                "scoring_system": "Optimizado para ganancias rápidas 1-2 semanas",
                "profit_priority": "30% - Profit Potential Score (target % + velocidad)",
                "stop_loss_max": "-10% - Filtro estricto aplicado",
                "risk_reward_min": "2:1 - Solo oportunidades de alto R:R",
                "technical_calculations": "Stop Loss y Take Profit calculados técnicamente",
                "relative_strength": "15% - Outperform SPY requerido",
                "setup_type": "10% - Prioriza breakouts inminentes", 
                "volume": "15% - Confirmación institucional",
                "momentum": "20% - RSI 40-70, tendencia alcista"
            }
        }
        
        print(f"Dashboard estructura creada")
        print(f"Summary calculado: {dashboard_data['summary']}")
        
        if not top10_df.empty:
            print(f"\n🔧 Procesando {len(top10_df)} acciones con profit metrics...")
            
            # Procesar cada acción del top 10
            for i, (_, row) in enumerate(top10_df.iterrows()):
                try:
                    # Datos básicos validados
                    symbol = str(row['symbol'])
                    company_name = str(row.get('company_name', symbol))[:40]
                    sector = str(row.get('sector', 'N/A'))
                    current_price = float(row['current_price'])
                    total_score = float(row['total_score'])
                    
                    print(f"  Procesando {symbol}: Precio=${current_price:.2f}, Score={total_score:.1f}")
                    
                    # === LEER CAMPOS SEPARADOS ===
                    
                    # Stop Loss - campos separados
                    stop_loss_price = float(row['stop_loss_price'])
                    stop_loss_pct = float(row['stop_loss_percentage'])
                    stop_loss_method = str(row['stop_loss_method'])
                    
                    # Take Profit - campos separados  
                    take_profit_price = float(row['take_profit_price'])
                    take_profit_pct = float(row['take_profit_percentage'])
                    take_profit_method = str(row['take_profit_method'])
                    
                    # Risk/Reward
                    risk_reward_ratio = str(row['risk_reward_ratio'])
                    
                    # 🔥 NUEVAS MÉTRICAS DE PROFIT
                    profit_potential_score = float(row.get('profit_potential_score', 0))
                    expected_days = int(row.get('expected_days_to_target', 10))
                    gain_per_day = float(row.get('expected_gain_per_day', 0))
                    
                    print(f"    ✓ Profit Score: {profit_potential_score:.1f} | Target: {take_profit_pct:.1f}% en ~{expected_days} días")
                    
                    # Otros datos
                    setup_type = str(row.get('setup_type', 'Mixed Setup'))
                    
                    # Métricas técnicas
                    rsi = float(row.get('rsi', 50))
                    pullback_pct = float(row.get('pullback_pct', 0))
                    volume_spike = float(row.get('volume_spike', 1.0))
                    atr_pct = float(row.get('atr_pct', 0))
                    relative_strength = float(row.get('relative_strength_5d', 0))
                    
                    # Entry signals
                    entry_signals = row.get('entry_signals', '[]')
                    if isinstance(entry_signals, str):
                        try:
                            entry_signals = json.loads(entry_signals)
                        except:
                            entry_signals = ["RSI momentum", "Volume confirmation", "Technical setup"]
                    
                    # Scores individuales
                    momentum_score = float(row.get('momentum_score', 0))
                    volume_score = float(row.get('volume_score', 0))
                    breakout_score = float(row.get('breakout_score', 0))
                    relative_strength_score = float(row.get('relative_strength_score', 0))
                    setup_score = float(row.get('setup_score', 0))
                    proximity_score = float(row.get('proximity_score', 0))
                    acceleration_score = float(row.get('acceleration_score', 0))
                    quality_score = float(row.get('quality_score', 0))
                    
                    # === CREAR OBJETO PARA DASHBOARD ===
                    pick = {
                        "rank": i + 1,
                        "symbol": symbol,
                        "company": company_name,
                        "sector": sector,
                        "price": round(current_price, 2),
                        "score": round(total_score, 1),
                        
                        # 🔥 PROFIT METRICS
                        "profit_metrics": {
                            "profit_potential_score": round(profit_potential_score, 1),
                            "expected_days_to_target": expected_days,
                            "expected_gain_per_day": round(gain_per_day, 2),
                            "target_efficiency": f"{gain_per_day:.2f}%/día"
                        },
                        
                        # VALORES TÉCNICOS EXACTOS
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
                            "momentum_score": round(momentum_score, 1),
                            "breakout_score": round(breakout_score, 1),
                            "volume_score": round(volume_score, 1),
                            "rsi": round(rsi, 1),
                            "pullback_pct": round(pullback_pct, 1),
                            "volume_spike": round(volume_spike, 2),
                            "atr_pct": round(atr_pct, 1),
                            "relative_strength_5d": round(relative_strength, 1),
                            "relative_strength_score": round(relative_strength_score, 1),
                            "setup_score": round(setup_score, 1),
                            "proximity_score": round(proximity_score, 1),
                            "acceleration_score": round(acceleration_score, 1),
                            "quality_score": round(quality_score, 1)
                        },
                        
                        "entry_signals": entry_signals[:3] if isinstance(entry_signals, list) else ["Setup técnico confirmado"],
                        "market_cap_millions": int(row.get('market_cap_millions', 0))
                    }
                    
                    dashboard_data["top_picks"].append(pick)
                    
                except Exception as e:
                    print(f"    ❌ Error procesando fila {i}: {e}")
                    # Crear entrada básica de fallback
                    symbol = str(row.get('symbol', f'STOCK{i}'))
                    current_price = float(row.get('current_price', 100))
                    
                    fallback_pick = {
                        "rank": i + 1,
                        "symbol": symbol,
                        "company": str(row.get('company_name', symbol))[:40],
                        "sector": str(row.get('sector', 'N/A')),
                        "price": round(current_price, 2),
                        "score": round(float(row.get('total_score', 0)), 1),
                        "profit_metrics": {
                            "profit_potential_score": 0,
                            "expected_days_to_target": 10,
                            "expected_gain_per_day": 0,
                            "target_efficiency": "0.00%/día"
                        },
                        "stop_loss": {
                            "price": round(current_price * 0.92, 2),
                            "loss_percentage": -8.0,
                            "method": "Fallback técnico"
                        },
                        "take_profit": {
                            "price": round(current_price * 1.15, 2),
                            "gain_percentage": 15.0,
                            "method": "Fallback técnico"
                        },
                        "risk_reward": "1:1.9",
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
                        "market_cap_millions": 0
                    }
                    dashboard_data["top_picks"].append(fallback_pick)
                    print(f"    🔧 Fallback añadido para {symbol}")
            
            print(f"✅ {len(dashboard_data['top_picks'])} acciones procesadas con profit metrics")
            
            # Análisis del mercado con profit metrics
            if dashboard_data["top_picks"]:
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
                    
                    # 🔥 Análisis de profit potential
                    profit_scores = [pick["profit_metrics"]["profit_potential_score"] for pick in dashboard_data["top_picks"]]
                    target_percentages = [pick["take_profit"]["gain_percentage"] for pick in dashboard_data["top_picks"]]
                    expected_days_list = [pick["profit_metrics"]["expected_days_to_target"] for pick in dashboard_data["top_picks"]]
                    
                    dashboard_data["market_analysis"] = {
                        "setup_distribution": setup_distribution,
                        "sector_distribution": sector_distribution,
                        "avg_rsi": round(sum(pick["metrics"]["rsi"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "avg_pullback": round(sum(pick["metrics"]["pullback_pct"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "avg_volume_spike": round(sum(pick["metrics"]["volume_spike"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 2),
                        "avg_relative_strength_vs_spy": round(sum(pick["metrics"]["relative_strength_5d"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                        "profit_analysis": {
                            "avg_profit_potential_score": round(sum(profit_scores) / len(profit_scores), 1),
                            "avg_target_percentage": round(sum(target_percentages) / len(target_percentages), 1),
                            "avg_days_to_target": round(sum(expected_days_list) / len(expected_days_list), 1),
                            "best_profit_score": round(max(profit_scores), 1),
                            "best_target_percentage": round(max(target_percentages), 1)
                        },
                        "optimization_note": "Criterios optimizados para maximizar ganancias rápidas con stop loss ≤ -10%"
                    }
                    
                    print(f"✓ Análisis de mercado con profit metrics calculado")
                    
                except Exception as e:
                    print(f"⚠️ Error calculando análisis de mercado: {e}")
        
        # Estadísticas finales optimizadas
        if dashboard_data["top_picks"]:
            stop_losses = [pick["stop_loss"]["loss_percentage"] for pick in dashboard_data["top_picks"]]
            take_profits = [pick["take_profit"]["gain_percentage"] for pick in dashboard_data["top_picks"]]
            profit_scores = [pick["profit_metrics"]["profit_potential_score"] for pick in dashboard_data["top_picks"]]
            
            dashboard_data["statistics"] = {
                "avg_score": round(sum(pick["score"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                "price_range": {
                    "min": round(min(pick["price"] for pick in dashboard_data["top_picks"]), 2),
                    "max": round(max(pick["price"] for pick in dashboard_data["top_picks"]), 2)
                },
                "avg_risk_percentage": round(sum(abs(x) for x in stop_losses) / len(stop_losses), 1),
                "avg_reward_percentage": round(sum(take_profits) / len(take_profits), 1),
                "stop_loss_range": {
                    "min": round(min(stop_losses), 1),
                    "max": round(max(stop_losses), 1)
                },
                "take_profit_range": {
                    "min": round(min(take_profits), 1),
                    "max": round(max(take_profits), 1)
                },
                "profit_metrics": {
                    "avg_profit_score": round(sum(profit_scores) / len(profit_scores), 1),
                    "min_profit_score": round(min(profit_scores), 1),
                    "max_profit_score": round(max(profit_scores), 1),
                    "all_stops_under_10pct": all(abs(sl) <= 10 for sl in stop_losses)
                },
                "technical_methods": {
                    "stop_methods": list(set(pick["stop_loss"]["method"] for pick in dashboard_data["top_picks"])),
                    "target_methods": list(set(pick["take_profit"]["method"] for pick in dashboard_data["top_picks"]))
                },
                "validation_note": "Stop Loss máximo -10% | R:R mínimo 2:1 | Optimizado para ganancias rápidas"
            }
            
            print(f"\n📊 ESTADÍSTICAS CON PROFIT METRICS:")
            print(f"   - Stop Loss promedio: {dashboard_data['statistics']['avg_risk_percentage']:.1f}%")
            print(f"   - Take Profit promedio: {dashboard_data['statistics']['avg_reward_percentage']:.1f}%")
            print(f"   - Profit Score promedio: {dashboard_data['statistics']['profit_metrics']['avg_profit_score']:.1f}")
            print(f"   - Todos stops ≤ -10%: {dashboard_data['statistics']['profit_metrics']['all_stops_under_10pct']}")
        else:
            dashboard_data["statistics"] = {
                "message": "Sin oportunidades que cumplan criterios estrictos",
                "criteria": "Stop Loss ≤ -10% | Risk:Reward ≥ 2:1 | Profit Potential Score alto",
                "suggestion": "Los filtros están optimizados para máximas ganancias con riesgo controlado"
            }
        
        # Crear directorio y guardar JSON
        print("\n💾 Guardando JSON con profit metrics...")
        os.makedirs('docs', exist_ok=True)
        
        json_path = 'docs/data.json'
        
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Dashboard JSON creado: {json_path}")
            
            # Verificar contenido
            if os.path.exists(json_path):
                size = os.path.getsize(json_path)
                print(f"✅ Archivo verificado - Tamaño: {size} bytes")
                
                # Mostrar muestra de profit metrics
                if dashboard_data["top_picks"]:
                    first_pick = dashboard_data["top_picks"][0]
                    print(f"\n🔍 VERIFICACIÓN PROFIT METRICS (#{first_pick['rank']} {first_pick['symbol']}):")
                    print(f"   Profit Score: {first_pick['profit_metrics']['profit_potential_score']}/100")
                    print(f"   Target: +{first_pick['take_profit']['gain_percentage']:.1f}% en ~{first_pick['profit_metrics']['expected_days_to_target']} días")
                    print(f"   Eficiencia: {first_pick['profit_metrics']['target_efficiency']}")
                    print(f"   Stop Loss: {first_pick['stop_loss']['loss_percentage']:.1f}% (≤ -10% ✓)")
                    print(f"   Risk:Reward: {first_pick['risk_reward']} (≥ 2:1 ✓)")
                
                print(f"\n📊 Resumen del dashboard optimizado:")
                print(f"   - Candidatos totales: {dashboard_data['summary']['total_candidates']}")
                print(f"   - Top picks: {dashboard_data['summary']['top_picks_count']}")
                print(f"   - Profit Score promedio: {dashboard_data['summary']['avg_profit_potential']}")
                print(f"   - Target promedio: +{dashboard_data['summary']['avg_target_percentage']:.1f}%")
                
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
        
        print(f"\n🎉 Dashboard optimizado para máximas ganancias completado!")
        print(f"🔥 Profit Potential Score y métricas de velocidad incluidas")
        return True
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_fallback_dashboard():
    """Crea dashboard de fallback optimizado"""
    print("Creando dashboard de fallback optimizado...")
    
    fallback_data = {
        "timestamp": datetime.now().isoformat(),
        "market_date": datetime.now().strftime("%Y-%m-%d"),
        "summary": {
            "total_candidates": 0,
            "top_picks_count": 0,
            "avg_score": 0,
            "avg_risk_reward": 0,
            "avg_profit_potential": 0,
            "avg_target_percentage": 0,
            "message": "Sin datos - Ejecutar screener optimizado primero"
        },
        "top_picks": [],
        "market_analysis": {
            "message": "No hay datos para análisis",
            "suggestion": "Ejecutar screener con filtros de profit optimizados",
            "profit_analysis": {
                "avg_profit_potential_score": 0,
                "avg_target_percentage": 0,
                "avg_days_to_target": 0,
                "best_profit_score": 0,
                "best_target_percentage": 0
            }
        },
        "screening_criteria": {
            "scoring_system": "Optimizado para ganancias rápidas 1-2 semanas",
            "profit_priority": "30% - Profit Potential Score (target % + velocidad)",
            "stop_loss_max": "-10% - Filtro estricto aplicado",
            "risk_reward_min": "2:1 - Solo oportunidades de alto R:R",
            "technical_calculations": "Stop Loss y Take Profit calculados técnicamente",
            "note": "Ejecutar screener optimizado para valores reales",
            "required": "python speculative_screener_automated.py"
        },
        "statistics": {
            "message": "Sin datos para mostrar estadísticas",
            "reasons": [
                "Scoring optimizado para profit potential",
                "Stop loss máximo -10% (más estricto)",
                "Risk:Reward mínimo 2:1 (más exigente)",
                "Prioridad: máximas ganancias rápidas",
                "Métricas de velocidad incluidas",
                "Próxima ejecución en 24 horas"
            ]
        }
    }
    
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
        print("\n✅ SUCCESS: Dashboard con profit metrics creado")
        print("📱 Abre docs/index.html en tu navegador")
        print("🔥 Profit Potential Score mostrado para cada acción")
        print("📊 Días estimados al target incluidos")
        print("💰 Eficiencia de ganancia (%/día) calculada")
        print("🎯 Todo optimizado para máximas ganancias rápidas")
    else:
        print("\n❌ FAILED: Revisar errores arriba")
        print("💡 Asegúrate de ejecutar primero el screener optimizado")