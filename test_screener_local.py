# test_screener_local.py - ACTUALIZADO para versión optimizada
import yfinance as yf
import pandas as pd
import numpy as np
import time
from datetime import datetime

# IMPORTAR CLASES CON NOMBRES ACTUALIZADOS
from speculative_screener_automated import OptimizedSpeculativeSwingScreener, DynamicUniverseBuilder

def test_with_sample_stocks():
    """Test del screener optimizado con acciones de muestra"""
    
    print("=== TEST LOCAL DEL SCREENER ESPECULATIVO OPTIMIZADO ===")
    
    # Muestra de acciones especulativas conocidas para testing
    test_symbols = [
        # Fintech/Trading
        'HOOD', 'COIN', 'SQ', 'SOFI', 'UPST', 'AFRM',
        
        # Tech/AI
        'PLTR', 'SNOW', 'DDOG', 'CRWD', 'ZS', 'OKTA',
        
        # Biotech
        'MRNA', 'BNTX', 'NVAX', 'VEEV',
        
        # Space/Defense
        'LUNR', 'RKLB', 'SPCE',
        
        # Gaming/Entertainment
        'RBLX', 'U', 'TTWO', 'ROKU',
        
        # Growth/High-vol
        'PTON', 'ZOOM', 'PINS', 'SNAP', 'UBER', 'LYFT'
    ]
    
    print(f"🧪 Testing con {len(test_symbols)} acciones de muestra")
    print(f"🎯 Usando scoring optimizado para swing trading 1-2 semanas")
    
    # Inicializar screener optimizado
    screener = OptimizedSpeculativeSwingScreener()
    spy_return = screener.calculate_spy_return_5d()
    
    candidates = []
    processed = 0
    errors = 0
    
    print(f"\n📊 Procesando acciones de test...")
    print(f"{'SYMBOL':>6} {'STATUS':>15} {'PRICE':>8} {'SCORE':>6} {'R:R':>6} {'REL.STR':>7} {'SETUP':>15}")
    print("-" * 75)
    
    for symbol in test_symbols:
        processed += 1
        
        try:
            # Simular datos básicos para Stage 1 - Valores realistas
            market_caps = {
                'HOOD': 8_000_000_000,      # ~$8B
                'COIN': 25_000_000_000,     # ~$25B  
                'PLTR': 40_000_000_000,     # ~$40B
                'RBLX': 20_000_000_000,     # ~$20B
                'SNOW': 35_000_000_000,     # ~$35B
                'default': 5_000_000_000    # $5B para otros
            }
            
            mock_stock_data = {
                'symbol': symbol,
                'market_cap': market_caps.get(symbol, market_caps['default']),
                'price': 25.0,  # $25 (pasa filtros)
                'sector': 'Technology'  # Sector especulativo
            }
            
            # Stage 1: Quick filters
            if not screener.quick_filters(mock_stock_data):
                print(f"{symbol:>6s} {'❌ Stage1':>15s} {'N/A':>8s} {'N/A':>6s} {'N/A':>6s} {'N/A':>7s} {'N/A':>15s}")
                continue
            
            # Stage 2 & 3: Análisis optimizado completo
            result = screener.analyze_stock_optimized(symbol)
            
            if result and result.get('passes_all_filters'):
                candidates.append(result)
                
                # Mostrar resultado con nuevas métricas
                price = result.get('current_price', 0)
                score = result.get('total_score', 0)
                setup = result.get('setup_type', '')
                setup_short = setup.replace("Momentum ", "Mom.").replace("Breakout ", "Brk.").replace("Anticipation", "Ant")[:13]
                rr = result.get('risk_reward_ratio', '')
                rs = result.get('relative_strength_5d', 0)
                rs_str = f"{rs:+.1f}%" if rs else "N/A"
                
                print(f"{symbol:>6s} {'✅ CANDIDATO':>15s} ${price:7.2f} {score:6.1f} {rr:>6s} {rs_str:>7s} {setup_short:>15s}")
            else:
                if result:
                    reasons = result.get('filter_reasons', ['Sin datos'])
                    first_reason = reasons[0] if reasons else 'Sin razón'
                    reason_short = first_reason[:12]
                    print(f"{symbol:>6s} {'⚪ ' + reason_short:>15s} {'N/A':>8s} {'N/A':>6s} {'N/A':>6s} {'N/A':>7s} {'N/A':>15s}")
                else:
                    print(f"{symbol:>6s} {'❌ Error':>15s} {'N/A':>8s} {'N/A':>6s} {'N/A':>6s} {'N/A':>7s} {'N/A':>15s}")
                
        except Exception as e:
            errors += 1
            error_short = str(e)[:12]
            print(f"{symbol:>6s} {'❌ ' + error_short:>15s} {'N/A':>8s} {'N/A':>6s} {'N/A':>6s} {'N/A':>7s} {'N/A':>15s}")
    
    # Resultados con métricas optimizadas
    print(f"\n{'='*75}")
    print(f"📊 RESULTADOS DEL TEST OPTIMIZADO:")
    print(f"   - Acciones procesadas: {processed}")
    print(f"   - Candidatos encontrados: {len(candidates)}")
    print(f"   - Errores: {errors}")
    print(f"   - Tasa de éxito: {(len(candidates)/processed)*100:.1f}%")
    
    if spy_return:
        print(f"   - SPY 5d (benchmark): {spy_return:+.2f}%")
    
    if candidates:
        print(f"\n🔝 TOP CANDIDATOS (Scoring Optimizado):")
        # Ordenar por score optimizado
        top_candidates = sorted(candidates, key=lambda x: x['total_score'], reverse=True)
        
        print(f"{'#':>2} {'SYMBOL':>6} {'PRICE':>8} {'SCORE':>6} {'R:R':>6} {'REL.STR':>7} {'SETUP':>15}")
        print("-" * 65)
        
        for i, candidate in enumerate(top_candidates[:5], 1):
            symbol = candidate['symbol']
            price = candidate['current_price']
            score = candidate['total_score']
            setup = candidate['setup_type']
            setup_short = setup.replace("Momentum ", "Mom.").replace("Breakout ", "Brk.").replace("Anticipation", "Ant")[:13]
            rr = candidate['risk_reward_ratio']
            rs = candidate.get('relative_strength_5d', 0)
            rs_str = f"{rs:+.1f}%" if rs else "N/A"
            
            print(f"{i:>2d} {symbol:>6s} ${price:7.2f} {score:6.1f} {rr:>6s} {rs_str:>7s} {setup_short:>15s}")
        
        # Mostrar desglose de scoring optimizado
        print(f"\n📊 DESGLOSE DE SCORING OPTIMIZADO (Top 3):")
        for i, candidate in enumerate(top_candidates[:3], 1):
            symbol = candidate['symbol']
            
            # Obtener scores individuales con fallbacks
            mom_score = candidate.get('momentum_score', 0)
            rs_score = candidate.get('relative_strength_score', 0)
            vol_score = candidate.get('volume_score', 0)
            setup_score = candidate.get('setup_score', 0)
            prox_score = candidate.get('proximity_score', 0)
            accel_score = candidate.get('acceleration_score', 0)
            qual_score = candidate.get('quality_score', 0)
            
            print(f"{i}. {symbol}: Total:{candidate['total_score']:.1f} = "
                  f"Mom:{mom_score:.0f} + RS:{rs_score:.0f} + Vol:{vol_score:.0f} + "
                  f"Setup:{setup_score:.0f} + Prox:{prox_score:.0f} + Accel:{accel_score:.0f} + Qual:{qual_score:.0f}")
        
        # Mostrar análisis detallado del mejor candidato
        if top_candidates:
            best = top_candidates[0]
            print(f"\n🎯 ANÁLISIS DETALLADO DEL MEJOR CANDIDATO ({best['symbol']}):")
            
            print(f"   💰 Precio actual: ${best['current_price']:.2f}")
            print(f"   📊 Score total: {best['total_score']:.1f}/200")
            print(f"   🛑 Stop Loss: ${best['stop_loss']['price']:.2f} ({best['stop_loss']['loss_percentage']:+.1f}%)")
            print(f"   🎯 Take Profit: ${best['take_profit']['price']:.2f} (+{best['take_profit']['gain_percentage']:.1f}%)")
            print(f"   ⚖️ Risk:Reward: {best['risk_reward_ratio']}")
            print(f"   📈 Relative Strength vs SPY: {best.get('relative_strength_5d', 0):+.1f}%")
            print(f"   🎭 Setup Type: {best['setup_type']}")
            
            # Señales de entrada
            signals = best.get('entry_signals', [])
            if signals:
                print(f"   🎯 Señales de entrada:")
                for signal in signals:
                    print(f"      • {signal}")
        
        # Test dashboard creation
        print(f"\n🎨 Probando generación de dashboard optimizado...")
        try:
            from create_speculative_dashboard import create_speculative_dashboard
            
            # Crear archivo CSV temporal para el test
            test_df = pd.DataFrame(top_candidates)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_filename = f"speculative_top10_{timestamp}.csv"
            test_df.to_csv(test_filename, index=False)
            
            print(f"✓ CSV temporal creado: {test_filename}")
            
            # Intentar crear dashboard
            dashboard_success = create_speculative_dashboard()
            if dashboard_success:
                print(f"✅ Dashboard optimizado generado exitosamente!")
                print(f"📱 Abre docs/index.html para ver el resultado")
                print(f"🎯 Nuevas métricas de scoring disponibles en dashboard")
            else:
                print(f"⚠️ Error generando dashboard")
                
        except Exception as e:
            print(f"⚠️ Error en test de dashboard: {e}")
    
    else:
        print(f"\n🤔 Sin candidatos encontrados. Esto es NORMAL con el scoring optimizado:")
        print(f"   - Filtros más selectivos para swing 1-2 semanas")
        print(f"   - Relative strength vs SPY requerido")
        print(f"   - Setup types específicos priorizados")
        print(f"   - Volume confirmation más estricto")
        print(f"   - Mayor calidad = menos cantidad")

def test_universe_builder():
    """Test del constructor de universo dinámico"""
    
    print("\n=== TEST DYNAMIC UNIVERSE BUILDER ===")
    
    try:
        universe_builder = DynamicUniverseBuilder()
        
        print("🔍 Probando descarga de símbolos...")
        
        # Test solo NASDAQ con límite pequeño para rapidez
        print("📡 Descargando muestra de NASDAQ...")
        nasdaq_stocks = universe_builder._fetch_exchange_universe('NASDAQ')
        
        if nasdaq_stocks:
            print(f"✅ NASDAQ: {len(nasdaq_stocks)} acciones obtenidas")
            
            # Mostrar muestra
            print("\n📋 Muestra de acciones obtenidas:")
            for i, stock in enumerate(nasdaq_stocks[:10]):
                symbol = stock['symbol']
                name = stock.get('name', 'N/A')[:30]
                sector = stock.get('sector', 'N/A')
                price = stock.get('price', 0)
                print(f"{i+1:2d}. {symbol:6s} - ${price:6.2f} - {name} - {sector}")
            
            # Test filtros de sanidad
            clean_stocks = universe_builder._apply_sanity_filters(nasdaq_stocks)
            filtered_rate = (len(clean_stocks) / len(nasdaq_stocks)) * 100
            print(f"\n🧹 Filtros de sanidad: {len(clean_stocks)}/{len(nasdaq_stocks)} ({filtered_rate:.1f}% pasaron)")
            
        else:
            print("❌ No se pudieron obtener símbolos de NASDAQ")
            
    except Exception as e:
        print(f"❌ Error en test de universe builder: {e}")

if __name__ == "__main__":
    print("🎯 SPECULATIVE SWING SCREENER OPTIMIZADO - TEST LOCAL")
    print("=" * 70)
    print("🎯 Scoring optimizado para swing trading de 1-2 semanas")
    print("📊 Nuevas métricas: Relative Strength, Setup Type, Breakout Proximity")
    print()
    
    # Test 1: Universe Builder
    test_universe_builder()
    
    print("\n" + "=" * 70)
    
    # Test 2: Screener optimizado con muestra
    test_with_sample_stocks()
    
    print("\n" + "=" * 70)
    print("✅ Test local del sistema optimizado completado!")
    print("💡 Para ejecutar el screener completo: python speculative_screener_automated.py")
    print("🎯 Sistema configurado para maximizar ganancias en swing trading de 1-2 semanas")