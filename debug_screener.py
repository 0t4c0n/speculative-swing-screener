# debug_screener.py - Script simplificado para debug
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

def test_single_stock(symbol):
    """Test detallado de una sola acción para debug"""
    
    print(f"🔍 DEBUGGING {symbol}")
    print("=" * 50)
    
    try:
        # Paso 1: Test básico de yfinance
        print("1️⃣ Testeando descarga básica...")
        ticker = yf.Ticker(symbol)
        
        # Test info
        print("   📋 Obteniendo ticker.info...")
        try:
            info = ticker.info
            print(f"   ✅ Info obtenida: {len(info)} campos")
            
            # Mostrar campos importantes
            important_fields = ['marketCap', 'beta', 'sector', 'longName']
            for field in important_fields:
                value = info.get(field, 'N/A')
                print(f"   - {field}: {value}")
                
        except Exception as e:
            print(f"   ❌ Error en ticker.info: {e}")
            info = {}
        
        # Test historical data
        print("   📊 Obteniendo datos históricos...")
        try:
            hist = ticker.history(period="6mo")
            print(f"   ✅ Históricos obtenidos: {len(hist)} días")
            print(f"   - Columnas: {list(hist.columns)}")
            print(f"   - Fecha inicio: {hist.index.min()}")
            print(f"   - Fecha fin: {hist.index.max()}")
            
            if not hist.empty:
                latest = hist.iloc[-1]
                print(f"   - Último precio: ${latest['Close']:.2f}")
                print(f"   - Último volumen: {latest['Volume']:,.0f}")
                
        except Exception as e:
            print(f"   ❌ Error en históricos: {e}")
            return
        
        # Paso 2: Test cálculos técnicos básicos
        print("\n2️⃣ Testeando cálculos técnicos...")
        
        if len(hist) < 50:
            print(f"   ❌ Datos insuficientes: {len(hist)} < 50")
            return
        
        current_price = hist['Close'].iloc[-1]
        print(f"   - Precio actual: ${current_price:.2f}")
        
        # Test ATR
        print("   🔧 Calculando ATR...")
        try:
            high_low = hist['High'] - hist['Low']
            high_close_prev = np.abs(hist['High'] - hist['Close'].shift())
            low_close_prev = np.abs(hist['Low'] - hist['Close'].shift())
            true_range = np.maximum(high_low, np.maximum(high_close_prev, low_close_prev))
            atr = true_range.rolling(window=20).mean().iloc[-1]
            atr_pct = (atr / current_price) * 100
            
            print(f"   ✅ ATR: {atr:.2f} ({atr_pct:.1f}%)")
            
            if atr_pct > 8.0:
                print(f"   ⚠️ ATR muy alto para swing trading")
            
        except Exception as e:
            print(f"   ❌ Error calculando ATR: {e}")
        
        # Test Moving Averages
        print("   🔧 Calculando Moving Averages...")
        try:
            ma21 = hist['Close'].rolling(21).mean().iloc[-1]
            ma50 = hist['Close'].rolling(50).mean().iloc[-1]
            
            print(f"   ✅ MA21: ${ma21:.2f}")
            print(f"   ✅ MA50: ${ma50:.2f}")
            
            above_ma50 = current_price > ma50
            ma21_above_ma50 = ma21 > ma50
            
            print(f"   - Precio > MA50: {above_ma50}")
            print(f"   - MA21 > MA50: {ma21_above_ma50}")
            
            if above_ma50 and ma21_above_ma50:
                print(f"   ✅ Tendencia alcista básica")
            else:
                print(f"   ❌ No cumple tendencia alcista")
                
        except Exception as e:
            print(f"   ❌ Error calculando MAs: {e}")
        
        # Test Volume
        print("   🔧 Analizando volumen...")
        try:
            avg_volume = hist['Volume'].tail(50).mean()
            last_volume = hist['Volume'].iloc[-1]
            
            print(f"   ✅ Volumen promedio 50d: {avg_volume:,.0f}")
            print(f"   ✅ Volumen último día: {last_volume:,.0f}")
            
            if avg_volume >= 500_000:
                print(f"   ✅ Volumen suficiente")
            else:
                print(f"   ❌ Volumen insuficiente")
                
        except Exception as e:
            print(f"   ❌ Error analizando volumen: {e}")
        
        # Paso 3: Test filtros quick
        print("\n3️⃣ Testeando filtros quick...")
        
        market_cap = info.get('marketCap', 0)
        sector = info.get('sector', '')
        
        print(f"   - Market Cap: ${market_cap:,.0f}")
        print(f"   - Sector: {sector}")
        
        # Market cap check (ACTUALIZADO: $100M - $200B)
        if 100_000_000 <= market_cap <= 200_000_000_000:
            print(f"   ✅ Market cap en rango ($100M - $200B)")
        else:
            print(f"   ❌ Market cap fuera de rango: ${market_cap/1000000:.0f}M (debe estar entre $100M - $200B)")
        
        # Price check
        if 5 <= current_price <= 150:
            print(f"   ✅ Precio en rango")
        else:
            print(f"   ❌ Precio fuera de rango")
        
        # Sector check
        conservative_sectors = ['utilities', 'real estate', 'consumer staples']
        if any(cons in sector.lower() for cons in conservative_sectors):
            print(f"   ❌ Sector conservador")
        else:
            print(f"   ✅ Sector especulativo")
        
        print(f"\n✅ Debug completado para {symbol}")
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

def test_multiple_stocks():
    """Test con varias acciones conocidas"""
    
    # Acciones que deberían funcionar bien
    test_stocks = ['AAPL', 'MSFT', 'GOOGL', 'HOOD', 'COIN', 'PLTR']
    
    for stock in test_stocks:
        test_single_stock(stock)
        print("\n" + "="*70 + "\n")
        
        # Pausa pequeña entre acciones
        import time
        time.sleep(1)

if __name__ == "__main__":
    print("🐛 DEBUG SCREENER - Diagnóstico Detallado")
    print("=" * 70)
    
    # Test una acción simple primero
    test_single_stock("AAPL")
    
    # Preguntar si continuar con más
    response = input("\n¿Quieres probar con más acciones? (y/n): ")
    if response.lower() == 'y':
        test_multiple_stocks()