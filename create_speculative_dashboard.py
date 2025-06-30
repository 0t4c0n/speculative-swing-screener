# create_speculative_dashboard.py - CORREGIDO para mostrar valores técnicos exactos
import pandas as pd
import json
import glob
import os
from datetime import datetime

def create_speculative_dashboard():
    """Convierte resultados del screener en JSON con valores técnicos exactos para dashboard profesional"""
    
    print("=== CREATE SPECULATIVE DASHBOARD PROFESIONAL ===")
    
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
        except Exception as e:
            print(f"❌ Error leyendo TOP10: {e}")
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
                "message": f"Oportunidades especulativas optimizadas para swing 1-2 semanas ({len(top10_df)} encontradas)" if len(top10_df) > 0 else "Sin oportunidades especulativas"
            },
            "top_picks": [],
            "screening_criteria": {
                "scoring_system": "Optimizado para swing 1-2 semanas",
                "relative_strength": "20% - Outperform SPY requerido",
                "setup_type": "15% - Prioriza breakouts inminentes", 
                "volume": "20% - Confirmación institucional",
                "momentum": "25% - RSI 40-70, tendencia alcista",
                "breakout_proximity": "10% - Cerca de resistencias",
                "momentum_acceleration": "5% - Detecta aceleración",
                "quality": "5% - Estabilidad técnica"
            }
        }
        
        print(f"Dashboard estructura creada")
        print(f"Summary calculado: {dashboard_data['summary']}")
        
        if not top10_df.empty:
            print("🔧 Procesando top picks con valores técnicos exactos...")
            
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
                    
                    # === STOP LOSS Y TAKE PROFIT TÉCNICOS ===
                    
                    # Método 1: Leer directamente si son diccionarios
                    stop_loss_data = row.get('stop_loss', {})
                    take_profit_data = row.get('take_profit', {})
                    
                    # Método 2: Si son strings JSON, parsear
                    if isinstance(stop_loss_data, str):
                        try:
                            stop_loss_data = json.loads(stop_loss_data.replace("'", '"'))
                        except:
                            print(f"    ⚠️ Error parseando stop_loss para {symbol}")
                            stop_loss_data = {}
                    
                    if isinstance(take_profit_data, str):
                        try:
                            take_profit_data = json.loads(take_profit_data.replace("'", '"'))
                        except:
                            print(f"    ⚠️ Error parseando take_profit para {symbol}")
                            take_profit_data = {}
                    
                    # Extraer valores técnicos exactos
                    if isinstance(stop_loss_data, dict) and stop_loss_data:
                        stop_loss_price = float(stop_loss_data.get('price', current_price * 0.9))
                        stop_loss_pct = float(stop_loss_data.get('loss_percentage', -10.0))
                        stop_loss_method = str(stop_loss_data.get('method', 'Técnico'))
                        print(f"    ✓ Stop Loss: ${stop_loss_price:.2f} ({stop_loss_pct:+.1f}%) - {stop_loss_method}")
                    else:
                        # Fallback técnico conservador
                        stop_loss_price = current_price * 0.92
                        stop_loss_pct = -8.0
                        stop_loss_method = 'Conservador técnico'
                        print(f"    ⚠️ Stop Loss fallback: ${stop_loss_price:.2f}")
                    
                    if isinstance(take_profit_data, dict) and take_profit_data:
                        take_profit_price = float(take_profit_data.get('price', current_price * 1.15))
                        take_profit_pct = float(take_profit_data.get('gain_percentage', 15.0))
                        take_profit_method = str(take_profit_data.get('method', 'Técnico'))
                        print(f"    ✓ Take Profit: ${take_profit_price:.2f} (+{take_profit_pct:.1f}%) - {take_profit_method}")
                    else:
                        # Fallback técnico conservador
                        take_profit_price = current_price * 1.12
                        take_profit_pct = 12.0
                        take_profit_method = 'Conservador técnico'
                        print(f"    ⚠️ Take Profit fallback: ${take_profit_price:.2f}")
                    
                    # Risk/Reward ratio
                    risk_reward_ratio = str(row.get('risk_reward_ratio', '1:1.5'))
                    
                    # Scores optimizados
                    momentum_score = float(row.get('momentum_score', 0))
                    volume_score = float(row.get('volume_score', 0))
                    relative_strength_score = float(row.get('relative_strength_score', 0))
                    setup_score = float(row.get('setup_score', 0))
                    
                    # Compatibilidad con versión anterior
                    breakout_score = float(row.get('breakout_score', 0))
                    
                    setup_type = str(row.get('setup_type', 'Mixed Setup'))
                    
                    # Datos técnicos adicionales
                    technical_data = row.get('technical_data', {})
                    if isinstance(technical_data, str):
                        try:
                            technical_data = json.loads(technical_data.replace("'", '"'))
                        except:
                            technical_data = {}
                    
                    rsi = float(technical_data.get('rsi', 50))
                    pullback_pct = float(technical_data.get('pullback_pct', 0))
                    volume_spike = float(technical_data.get('volume_spike', 1.0))
                    atr_pct = float(technical_data.get('atr_pct', 0))
                    
                    # Señales de entrada
                    entry_signals = row.get('entry_signals', [])
                    if isinstance(entry_signals, str):
                        try:
                            entry_signals = json.loads(entry_signals.replace("'", '"'))
                        except:
                            entry_signals = ["RSI momentum zone", "Volume confirmation", "Technical setup"]
                    
                    # Relative strength
                    relative_strength = float(row.get('relative_strength_5d', 0))
                    
                    # Crear objeto final para dashboard
                    pick = {
                        "rank": i + 1,
                        "symbol": symbol,
                        "company": company_name,
                        "sector": sector,
                        "price": round(current_price, 2),
                        "score": round(total_score, 1),
                        
                        # === VALORES TÉCNICOS EXACTOS ===
                        "stop_loss": {
                            "price": round(stop_loss_price, 2),           # ← PRECIO EXACTO TÉCNICO
                            "loss_percentage": round(stop_loss_pct, 1),   # ← PORCENTAJE EXACTO TÉCNICO
                            "method": stop_loss_method                    # ← MÉTODO TÉCNICO USADO
                        },
                        "take_profit": {
                            "price": round(take_profit_price, 2),         # ← PRECIO EXACTO TÉCNICO
                            "gain_percentage": round(take_profit_pct, 1), # ← PORCENTAJE EXACTO TÉCNICO
                            "method": take_profit_method                  # ← MÉTODO TÉCNICO USADO
                        },
                        
                        "risk_reward": risk_reward_ratio,
                        "setup_type": setup_type,
                        
                        "metrics": {
                            # Métricas técnicas principales
                            "momentum_score": round(momentum_score, 1),
                            "breakout_score": round(breakout_score, 1),
                            "volume_score": round(volume_score, 1),
                            "rsi": round(rsi, 1),
                            "pullback_pct": round(pullback_pct, 1),
                            "volume_spike": round(volume_spike, 2),
                            "atr_pct": round(atr_pct, 1),
                            "relative_strength_5d": round(relative_strength, 1),
                            
                            # Nuevas métricas optimizadas
                            "relative_strength_score": round(relative_strength_score, 1),
                            "setup_score": round(setup_score, 1)
                        },
                        
                        "entry_signals": entry_signals[:3] if isinstance(entry_signals, list) else ["Setup técnico confirmado"],
                        "market_cap_millions": int(row.get('market_cap_millions', 0))
                    }
                    
                    dashboard_data["top_picks"].append(pick)
                    print(f"    ✅ {symbol} añadido al dashboard")
                    
                except Exception as e:
                    print(f"    ❌ Error procesando {row.get('symbol', f'fila_{i}')}: {e}")
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
                        "stop_loss": {
                            "price": round(current_price * 0.92, 2),
                            "loss_percentage": -8.0,
                            "method": "Fallback técnico"
                        },
                        "take_profit": {
                            "price": round(current_price * 1.12, 2),
                            "gain_percentage": 12.0,
                            "method": "Fallback técnico"
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
                            "setup_score": 0
                        },
                        "entry_signals": ["Error en procesamiento"],
                        "market_cap_millions": 0
                    }
                    dashboard_data["top_picks"].append(fallback_pick)
                    print(f"    🔧 Fallback añadido para {symbol}")
            
            print(f"✅ {len(dashboard_data['top_picks'])} acciones procesadas para dashboard")
        
        # Estadísticas finales
        if dashboard_data["top_picks"]:
            dashboard_data["statistics"] = {
                "avg_score": round(sum(pick["score"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                "price_range": {
                    "min": round(min(pick["price"] for pick in dashboard_data["top_picks"]), 2),
                    "max": round(max(pick["price"] for pick in dashboard_data["top_picks"]), 2)
                },
                "avg_risk_percentage": round(sum(abs(pick["stop_loss"]["loss_percentage"]) for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                "avg_reward_percentage": round(sum(pick["take_profit"]["gain_percentage"] for pick in dashboard_data["top_picks"]) / len(dashboard_data["top_picks"]), 1),
                "technical_methods": {
                    "stop_methods": list(set(pick["stop_loss"]["method"] for pick in dashboard_data["top_picks"])),
                    "target_methods": list(set(pick["take_profit"]["method"] for pick in dashboard_data["top_picks"]))
                }
            }
            print("✅ Estadísticas calculadas")
        else:
            dashboard_data["statistics"] = {
                "message": "Sin oportunidades especulativas que cumplan criterios optimizados",
                "suggestion": "Filtros optimizados para swing 1-2 semanas son muy selectivos"
            }
        
        # Crear directorio y guardar JSON
        print("💾 Guardando JSON con valores técnicos exactos...")
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
                
                # Mostrar muestra de valores técnicos
                if dashboard_data["top_picks"]:
                    first_pick = dashboard_data["top_picks"][0]
                    print(f"🔍 Muestra de valores técnicos ({first_pick['symbol']}):")
                    print(f"   Stop Loss: ${first_pick['stop_loss']['price']} ({first_pick['stop_loss']['loss_percentage']:+.1f}%) - {first_pick['stop_loss']['method']}")
                    print(f"   Take Profit: ${first_pick['take_profit']['price']} (+{first_pick['take_profit']['gain_percentage']:.1f}%) - {first_pick['take_profit']['method']}")
                    print(f"   Risk:Reward: {first_pick['risk_reward']}")
                
                print(f"📊 Resumen del dashboard:")
                print(f"   - Candidatos totales: {dashboard_data['summary']['total_candidates']}")
                print(f"   - Top picks: {dashboard_data['summary']['top_picks_count']}")
                print(f"   - Score promedio: {dashboard_data['summary']['avg_score']}")
                
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
        
        print(f"🎉 Dashboard profesional con valores técnicos exactos completado!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_fallback_dashboard():
    """Crea dashboard de fallback profesional"""
    print("Creando dashboard de fallback profesional...")
    
    fallback_data = {
        "timestamp": datetime.now().isoformat(),
        "market_date": datetime.now().strftime("%Y-%m-%d"),
        "summary": {
            "total_candidates": 0,
            "top_picks_count": 0,
            "avg_score": 0,
            "avg_risk_reward": 0,
            "message": "Sin oportunidades especulativas - Criterios optimizados muy selectivos"
        },
        "top_picks": [],
        "screening_criteria": {
            "scoring_system": "Optimizado para swing 1-2 semanas",
            "relative_strength": "20% - Outperform SPY requerido",
            "setup_type": "15% - Prioriza breakouts inminentes", 
            "volume": "20% - Confirmación institucional",
            "momentum": "25% - RSI 40-70, tendencia alcista",
            "breakout_proximity": "10% - Cerca de resistencias",
            "momentum_acceleration": "5% - Detecta aceleración",
            "quality": "5% - Estabilidad técnica"
        },
        "statistics": {
            "message": "Sin datos para mostrar estadísticas",
            "reasons": [
                "Scoring optimizado para swing trading de 1-2 semanas",
                "Stop loss y take profit calculados técnicamente",
                "Relative strength vs SPY requerido",
                "Setup types específicos priorizados",
                "Próxima ejecución en 24 horas"
            ]
        }
    }
    
    os.makedirs('docs', exist_ok=True)
    
    try:
        with open('docs/data.json', 'w', encoding='utf-8') as f:
            json.dump(fallback_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Dashboard de fallback profesional creado")
        return True
        
    except Exception as e:
        print(f"❌ Error creando dashboard de fallback: {e}")
        return False

if __name__ == "__main__":
    success = create_speculative_dashboard()
    if success:
        print("\n✅ SUCCESS: Dashboard profesional con valores técnicos exactos creado")
        print("📱 Abre docs/index.html en tu navegador")
        print("🎯 Stop Loss y Take Profit técnicos se muestran correctamente")
    else:
        print("\n❌ FAILED: Revisar errores arriba")