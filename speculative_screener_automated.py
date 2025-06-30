# speculative_screener_automated.py - SCREENER ESPECULATIVO OPTIMIZADO PARA SWING 1-2 SEMANAS
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import json
from io import StringIO
import logging

# Configurar logging más silencioso
logging.getLogger('yfinance').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

class DynamicUniverseBuilder:
    """Construye universo de acciones completamente dinámico - Versión con logs resumidos"""
    
    def __init__(self):
        self.nasdaq_api_url = "https://api.nasdaq.com/api/screener/stocks"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_all_tradeable_stocks(self):
        """Obtiene TODOS los tickers sin hardcode - logs resumidos"""
        
        # FUENTE 1-3: NASDAQ, NYSE, AMEX
        nasdaq_stocks = self._fetch_exchange_universe('NASDAQ')
        nyse_stocks = self._fetch_exchange_universe('NYSE')
        amex_stocks = self._fetch_exchange_universe('AMEX')
        
        # Combinar y limpiar
        all_stocks = self._combine_and_deduplicate(nasdaq_stocks, nyse_stocks, amex_stocks)
        clean_universe = self._apply_sanity_filters(all_stocks)
        
        print(f"✓ Universo dinámico: {len(clean_universe)} acciones (NASDAQ:{len(nasdaq_stocks)} NYSE:{len(nyse_stocks)} AMEX:{len(amex_stocks)})")
        return clean_universe
    
    def _fetch_exchange_universe(self, exchange):
        """Descarga acciones - versión con logs resumidos"""
        try:
            params = {
                'tableonly': 'true',
                'limit': '25000',
                'exchange': exchange
            }
            
            response = requests.get(self.nasdaq_api_url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                stocks = []
                
                if 'data' in data and 'table' in data['data'] and 'rows' in data['data']['table']:
                    for row in data['data']['table']['rows']:
                        stocks.append({
                            'symbol': row['symbol'].strip(),
                            'name': row.get('name', ''),
                            'exchange': exchange,
                            'market_cap': self._parse_market_cap(row.get('marketCap', '0')),
                            'sector': row.get('sector', ''),
                            'price': self._parse_price(row.get('lastsale', '0'))
                        })
                
                print(f"✓ {exchange}: {len(stocks)}")
                return stocks
            else:
                print(f"⚠️ {exchange}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {exchange}: {str(e)[:30]}...")
            
        return []
    
    def _combine_and_deduplicate(self, *stock_lists):
        """Combina listas y elimina duplicados por símbolo"""
        all_stocks = []
        seen_symbols = set()
        
        for stock_list in stock_lists:
            for stock in stock_list:
                symbol = stock['symbol']
                if symbol not in seen_symbols and self._is_valid_symbol(symbol):
                    all_stocks.append(stock)
                    seen_symbols.add(symbol)
        
        return all_stocks
    
    def _apply_sanity_filters(self, stocks):
        """Filtros básicos de sanidad"""
        filtered = []
        
        for stock in stocks:
            symbol = stock['symbol']
            if (len(symbol) <= 6 and
                not symbol.endswith('.W') and  # Evitar warrants
                not symbol.endswith('.U') and  # Evitar units
                '$' not in symbol and
                '/' not in symbol and
                symbol.isalpha()):  # Solo letras
                
                filtered.append(stock)
        
        return filtered
    
    def _is_valid_symbol(self, symbol):
        """Validación básica de símbolo"""
        if not symbol or len(symbol) < 1 or len(symbol) > 6:
            return False
        return True
    
    def _parse_market_cap(self, market_cap_str):
        """Convierte string de market cap a número"""
        try:
            if isinstance(market_cap_str, (int, float)):
                return market_cap_str
            
            clean_str = str(market_cap_str).replace('$', '').replace(',', '').strip()
            
            if 'B' in clean_str:
                return float(clean_str.replace('B', '')) * 1_000_000_000
            elif 'M' in clean_str:
                return float(clean_str.replace('M', '')) * 1_000_000
            elif 'K' in clean_str:
                return float(clean_str.replace('K', '')) * 1_000
            else:
                return float(clean_str) if clean_str else 0
        except:
            return 0
    
    def _parse_price(self, price_str):
        """Convierte string de precio a número"""
        try:
            return float(str(price_str).replace('$', '').replace(',', ''))
        except:
            return 0

class OptimizedSpeculativeSwingScreener:
    """Screener optimizado para swing trading de 1-2 semanas con scoring avanzado"""
    
    def __init__(self):
        self.spy_return_5d = None
        
    def calculate_spy_return_5d(self):
        """Calcula rendimiento de SPY en 5 días - logs resumidos"""
        print("📊 Descargando SPY para comparación...")
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                spy_ticker = yf.Ticker("SPY")
                spy_data = spy_ticker.history(period="1mo")
                
                if len(spy_data) >= 6:
                    spy_current = spy_data['Close'].iloc[-1]
                    spy_5d_ago = spy_data['Close'].iloc[-6]
                    spy_return_5d = ((spy_current / spy_5d_ago) - 1) * 100
                    
                    print(f"✅ SPY 5d: {spy_return_5d:+.2f}%")
                    self.spy_return_5d = spy_return_5d
                    return spy_return_5d
                else:
                    print("⚠️ SPY: Datos insuficientes")
                    return None
                    
            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    print(f"⏳ SPY retry {retry_count}/{max_retries} en {wait_time}s")
                    time.sleep(wait_time)
                else:
                    print(f"❌ SPY error: {str(e)[:30]}...")
                    return None
    
    def quick_filters(self, stock_data):
        """STAGE 1: Filtros ultra-rápidos sin descarga de datos históricos"""
        try:
            market_cap = stock_data.get('market_cap', 0)
            price = stock_data.get('price', 0)
            
            # Filtro 1: Market Cap entre $100M - $200B
            if market_cap < 100_000_000 or market_cap > 200_000_000_000:
                return False
            
            # Filtro 2: Precio entre $5 - $150
            if price < 5 or price > 150:
                return False
            
            # Filtro 3: Sectores conservadores (excluir)
            sector = stock_data.get('sector', '').lower()
            conservative_sectors = ['utilities', 'real estate', 'consumer staples']
            if any(cons_sector in sector for cons_sector in conservative_sectors):
                return False
                
            return True
            
        except Exception as e:
            return False
    
    def analyze_stock_optimized(self, symbol):
        """STAGE 2 & 3: Análisis optimizado para swing 1-2 semanas - SIN LOGS DETALLADOS"""
        max_retries = 2
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # PASO 1: Descargar datos históricos
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="6mo")
                
                if hist.empty or len(hist) < 50:
                    return {'passes_all_filters': False, 'filter_reasons': ['Datos insuficientes']}
                
                # PASO 2: Obtener info básica
                ticker_info = {}
                try:
                    ticker_info = ticker.info
                    if not ticker_info:
                        ticker_info = {}
                except Exception:
                    ticker_info = {
                        'marketCap': 1_000_000_000,
                        'beta': 1.5,
                        'sector': 'Technology'
                    }
                
                # PASO 3: STAGE 2 - Filtros técnicos básicos
                if not self._passes_technical_basics(hist, ticker_info):
                    return {'passes_all_filters': False, 'filter_reasons': ['Filtros técnicos básicos']}
                
                # PASO 4: STAGE 3 - Análisis optimizado para swing 1-2 semanas
                result = self._complete_analysis_optimized_for_short_swing(hist, ticker_info, symbol)
                
                return result if result else {'passes_all_filters': False, 'filter_reasons': ['Error análisis']}
                
            except Exception as e:
                error_msg = str(e).lower()
                
                if "rate" in error_msg or "429" in error_msg or "too many requests" in error_msg:
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(2 ** retry_count)
                        continue
                    else:
                        return {'passes_all_filters': False, 'filter_reasons': ['Rate limit']}
                else:
                    return {'passes_all_filters': False, 'filter_reasons': [f'Error: {type(e).__name__}']}
    
    def _passes_technical_basics(self, df, ticker_info):
        """STAGE 2: Filtros técnicos básicos - sin logs"""
        try:
            if df.empty or len(df) < 50:
                return False
            
            required_columns = ['Close', 'High', 'Low', 'Volume', 'Open']
            if not all(col in df.columns for col in required_columns):
                return False
            
            current_price = df['Close'].iloc[-1]
            if pd.isna(current_price) or current_price <= 0:
                return False
            
            # ATR check
            atr_20 = self._calculate_atr(df, 20)
            if not atr_20 or pd.isna(atr_20) or atr_20 <= 0:
                return False
                
            atr_percentage = (atr_20 / current_price) * 100
            if atr_percentage > 8.0:
                return False
            
            # Beta check
            beta = ticker_info.get('beta', 1.5)
            if beta and beta > 3.0:
                return False
            
            # Tendencia alcista
            if len(df) < 50:
                return False
                
            ma21 = df['Close'].rolling(21).mean().iloc[-1]
            ma50 = df['Close'].rolling(50).mean().iloc[-1]
            
            if pd.isna(ma21) or pd.isna(ma50):
                return False
            
            if current_price < ma50 or ma21 < ma50:
                return False
            
            # Volumen mínimo
            avg_volume = df['Volume'].tail(50).mean()
            if pd.isna(avg_volume) or avg_volume < 500_000:
                return False
                
            return True
            
        except Exception:
            return False
    
    def _complete_analysis_optimized_for_short_swing(self, df, ticker_info, symbol):
        """
        ANÁLISIS OPTIMIZADO PARA SWING TRADING 1-2 SEMANAS
        Sistema de scoring rebalanceado basado en research
        """
        try:
            current_price = df['Close'].iloc[-1]
            
            # === ANÁLISIS BASE ===
            momentum_data = self._analyze_momentum(df)
            breakout_data = self._analyze_breakout_potential(df)
            volume_data = self._analyze_volume(df)
            quality_score = self._calculate_quality_score(df)
            
            # === NUEVOS FACTORES PARA SWING 1-2 SEMANAS ===
            
            # 1. RELATIVE STRENGTH vs SPY (CRÍTICO)
            relative_strength = self._calculate_relative_strength(df)
            relative_strength_score = self._calculate_relative_strength_score(relative_strength)
            
            # 2. SETUP TYPE WEIGHTING (NUEVO)
            setup_type = self._determine_setup_type(momentum_data, breakout_data)
            setup_score = self._calculate_setup_type_score(setup_type, momentum_data, breakout_data)
            
            # 3. BREAKOUT PROXIMITY (NUEVO)
            proximity_score = self._calculate_breakout_proximity_score(df, current_price)
            
            # 4. MOMENTUM ACCELERATION (NUEVO)
            acceleration_score = self._calculate_momentum_acceleration_score(df)
            
            # === SCORING OPTIMIZADO PARA 1-2 SEMANAS ===
            
            # PESOS REBALANCEADOS (basado en research):
            weights = {
                'momentum': 0.25,           # 25% (reducido de 40%)
                'relative_strength': 0.20,  # 20% (NUEVO - crítico)
                'volume': 0.20,             # 20% (aumentado de 15%)
                'setup_type': 0.15,         # 15% (NUEVO)
                'breakout_proximity': 0.10, # 10% (NUEVO)
                'acceleration': 0.05,       # 5% (NUEVO)
                'quality': 0.05            # 5% (reducido de 20%)
            }
            
            # SCORE TOTAL OPTIMIZADO
            base_score = (
                momentum_data['score'] * weights['momentum'] +
                relative_strength_score * weights['relative_strength'] +
                volume_data['score'] * weights['volume'] +
                setup_score * weights['setup_type'] +
                proximity_score * weights['breakout_proximity'] +
                acceleration_score * weights['acceleration'] +
                quality_score * weights['quality']
            ) * 2  # Escalar a 0-200
            
            # === FILTROS ADICIONALES PARA SWING CORTO ===
            
            # Filtro 1: Must outperform SPY (o neutral)
            if relative_strength and relative_strength < -2:
                return {'passes_all_filters': False, 'filter_reasons': ['Underperform SPY significativo']}
            
            # Filtro 2: Setup type propicio para swing corto
            if setup_type == "Oversold Bounce" and momentum_data['score'] < 50:
                return {'passes_all_filters': False, 'filter_reasons': ['Setup no óptimo swing corto']}
            
            # Filtro 3: Volume confirmation mínimo
            if volume_data['score'] < 15:
                return {'passes_all_filters': False, 'filter_reasons': ['Volume insuficiente']}
            
            # === RISK/REWARD CALCULATION ===
            risk_reward_data = self._calculate_stop_loss_take_profit_silent(df, current_price)
            
            if risk_reward_data['stop_loss']['loss_percentage'] < -12:
                return {'passes_all_filters': False, 'filter_reasons': ['Riesgo excesivo']}
            
            if risk_reward_data['risk_reward_ratio_numeric'] < 1.5:
                return {'passes_all_filters': False, 'filter_reasons': ['R:R insuficiente']}
            
            # === ENTRY SIGNALS OPTIMIZADOS ===
            entry_signals = self._generate_optimized_entry_signals(
                df, momentum_data, breakout_data, volume_data, 
                relative_strength, setup_type, proximity_score
            )
            
            # === DATOS PARA DASHBOARD ===
            company_name = ticker_info.get('longName', ticker_info.get('shortName', symbol))
            sector = ticker_info.get('sector', 'N/A')
            market_cap = ticker_info.get('marketCap', 0)
            
            return {
                'symbol': symbol,
                'company_name': company_name[:40] if company_name else symbol,
                'sector': sector,
                'current_price': round(current_price, 2),
                'market_cap_millions': round(market_cap / 1000000, 0) if market_cap else 0,
                
                # SCORES DETALLADOS
                'total_score': round(base_score, 1),
                'momentum_score': momentum_data['score'],
                'relative_strength_score': relative_strength_score,
                'volume_score': volume_data['score'],
                'setup_score': setup_score,
                'proximity_score': proximity_score,
                'acceleration_score': acceleration_score,
                'quality_score': quality_score,
                
                # COMPATIBILIDAD CON DASHBOARD EXISTENTE
                'breakout_score': breakout_data['score'],  # Para dashboard
                
                # RISK/REWARD
                'stop_loss': risk_reward_data['stop_loss'],
                'take_profit': risk_reward_data['take_profit'],
                'risk_reward_ratio': risk_reward_data['risk_reward_ratio'],
                'risk_reward_ratio_numeric': risk_reward_data['risk_reward_ratio_numeric'],
                
                # DATOS TÉCNICOS
                'relative_strength_5d': relative_strength,
                'setup_type': setup_type,
                'entry_signals': entry_signals,
                'technical_data': {
                    'rsi': momentum_data['rsi'],
                    'pullback_pct': breakout_data['pullback_from_high'],
                    'volume_spike': volume_data['recent_volume_ratio'],
                    'atr_pct': round((self._calculate_atr(df, 20) / current_price) * 100, 1),
                    'breakout_proximity_pct': round(proximity_score, 1)
                },
                
                'passes_all_filters': True
            }
            
        except Exception as e:
            return {'passes_all_filters': False, 'filter_reasons': [f'Error análisis: {type(e).__name__}']}
    
    # === NUEVAS FUNCIONES PARA SCORING OPTIMIZADO ===
    
    def _calculate_relative_strength_score(self, relative_strength):
        """Score basado en relative strength vs SPY (0-100 pts) - CRÍTICO para swing 1-2 semanas"""
        if not relative_strength:
            return 50  # Neutral si no hay datos
        
        if relative_strength > 10:
            return 100  # Muy fuerte outperformance
        elif relative_strength > 5:
            return 85   # Fuerte outperformance
        elif relative_strength > 2:
            return 70   # Buena outperformance
        elif relative_strength > 0:
            return 55   # Leve outperformance
        elif relative_strength > -2:
            return 40   # Leve underperformance
        else:
            return 0    # Fuerte underperformance
    
    def _calculate_setup_type_score(self, setup_type, momentum_data, breakout_data):
        """Score basado en tipo de setup (0-100 pts) - Prioriza setups para swing 1-2 semanas"""
        base_scores = {
            "Breakout Anticipation": 90,  # MEJOR para swing corto
            "Momentum Pullback": 80,      # MUY BUENO
            "Mixed Setup": 60,            # ACEPTABLE
            "Oversold Bounce": 30         # MENOS IDEAL para swing corto
        }
        
        base_score = base_scores.get(setup_type, 50)
        
        # BONUS por calidad del setup
        if setup_type == "Breakout Anticipation":
            pullback = breakout_data.get('pullback_from_high', 0)
            if -3 <= pullback <= 1:
                base_score += 10
        
        elif setup_type == "Momentum Pullback":
            pullback = breakout_data.get('pullback_from_high', 0)
            if -8 <= pullback <= -3:
                base_score += 10
        
        return min(base_score, 100)
    
    def _calculate_breakout_proximity_score(self, df, current_price):
        """Score basado en proximidad a breakout (0-100 pts) - Stocks cerca de resistencia"""
        try:
            high_20d = df['High'].tail(20).max()
            distance_to_high = ((high_20d - current_price) / current_price) * 100
            
            if distance_to_high <= 2:
                return 100  # Muy cerca del breakout
            elif distance_to_high <= 5:
                return 80   # Cerca del breakout
            elif distance_to_high <= 8:
                return 60   # Proximidad moderada
            elif distance_to_high <= 12:
                return 40   # Algo lejos
            else:
                return 20   # Lejos del breakout
                
        except Exception:
            return 50
    
    def _calculate_momentum_acceleration_score(self, df):
        """Score basado en aceleración del momentum (0-100 pts) - Detecta aceleración"""
        try:
            returns_5d = df['Close'].pct_change().tail(5)
            returns_10d = df['Close'].pct_change().tail(10)
            
            recent_avg = returns_5d.mean()
            longer_avg = returns_10d.mean()
            
            if recent_avg > longer_avg * 1.5:
                return 100  # Momentum acelerando fuerte
            elif recent_avg > longer_avg * 1.2:
                return 80   # Momentum acelerando
            elif recent_avg > longer_avg:
                return 60   # Momentum positivo
            else:
                return 30   # Momentum desacelerando
                
        except Exception:
            return 50
    
    def _generate_optimized_entry_signals(self, df, momentum_data, breakout_data, 
                                        volume_data, relative_strength, setup_type, proximity_score):
        """Genera señales optimizadas para swing trading 1-2 semanas"""
        signals = []
        
        # Signal 1: Relative Strength
        if relative_strength and relative_strength > 5:
            signals.append(f"Outperform SPY +{relative_strength:.1f}%")
        elif relative_strength and relative_strength > 0:
            signals.append(f"Beat SPY +{relative_strength:.1f}%")
        
        # Signal 2: Setup específico
        if setup_type == "Breakout Anticipation":
            signals.append("Breakout inminente")
        elif setup_type == "Momentum Pullback":
            signals.append("Pullback saludable")
        
        # Signal 3: Volume confirmation
        vol_ratio = volume_data.get('recent_volume_ratio', 1)
        if vol_ratio > 1.5:
            signals.append(f"Volume spike +{((vol_ratio-1)*100):.0f}%")
        
        # Signal 4: Proximidad
        if proximity_score > 80:
            signals.append("Cerca de breakout")
        
        # Signal 5: RSI momentum
        rsi = momentum_data.get('rsi', 50)
        if 55 <= rsi <= 68:
            signals.append(f"RSI momentum {rsi:.0f}")
        
        return signals[:3]
    
    # === FUNCIONES EXISTENTES (sin logs detallados) ===
    
    def _analyze_momentum(self, df):
        """Análisis de momentum con RSI y MAs"""
        try:
            current_price = df['Close'].iloc[-1]
            
            rsi = self._calculate_rsi(df['Close'], 14)
            rsi_current = rsi.iloc[-1] if not rsi.empty else 50
            
            ma21 = df['Close'].rolling(21).mean().iloc[-1]
            ma50 = df['Close'].rolling(50).mean().iloc[-1]
            
            # Score RSI
            if 45 <= rsi_current <= 65:
                rsi_score = 30
            elif 40 <= rsi_current <= 70:
                rsi_score = 20
            else:
                rsi_score = 5
            
            # Score posición vs MAs
            price_vs_ma21 = ((current_price - ma21) / ma21) * 100
            if -5 <= price_vs_ma21 <= 3:
                ma_score = 25
            elif 0 <= price_vs_ma21 <= 8:
                ma_score = 15
            else:
                ma_score = 5
            
            # Score tendencia MA
            ma21_vs_ma50 = ((ma21 - ma50) / ma50) * 100
            if ma21_vs_ma50 > 2:
                trend_score = 25
            elif ma21_vs_ma50 > 0:
                trend_score = 15
            else:
                trend_score = 0
            
            total_momentum_score = rsi_score + ma_score + trend_score
            
            return {
                'score': total_momentum_score,
                'rsi': round(rsi_current, 1),
                'price_vs_ma21': round(price_vs_ma21, 1),
                'ma21_vs_ma50': round(ma21_vs_ma50, 1)
            }
            
        except Exception:
            return {'score': 0, 'rsi': 50, 'price_vs_ma21': 0, 'ma21_vs_ma50': 0}
    
    def _analyze_breakout_potential(self, df):
        """Análisis de potencial de breakout"""
        try:
            current_price = df['Close'].iloc[-1]
            
            high_20d = df['High'].tail(20).max()
            pullback_from_high = ((current_price - high_20d) / high_20d) * 100
            
            if -8 <= pullback_from_high <= -2:
                pullback_score = 30
            elif -12 <= pullback_from_high <= 0:
                pullback_score = 20
            else:
                pullback_score = 5
            
            range_15d = ((df['High'].tail(15).max() - df['Low'].tail(15).min()) / current_price) * 100
            if range_15d < 12:
                consolidation_score = 20
            elif range_15d < 20:
                consolidation_score = 10
            else:
                consolidation_score = 0
            
            total_breakout_score = pullback_score + consolidation_score
            
            return {
                'score': total_breakout_score,
                'pullback_from_high': round(pullback_from_high, 1),
                'consolidation_range': round(range_15d, 1)
            }
            
        except Exception:
            return {'score': 0, 'pullback_from_high': 0, 'consolidation_range': 0}
    
    def _analyze_volume(self, df):
        """Análisis de volumen"""
        try:
            volume_50d = df['Volume'].tail(50).mean()
            volume_5d = df['Volume'].tail(5).mean()
            
            recent_volume_ratio = volume_5d / volume_50d if volume_50d > 0 else 1
            
            if recent_volume_ratio > 1.5:
                volume_score = 30
            elif recent_volume_ratio > 1.2:
                volume_score = 20
            else:
                volume_score = 10
            
            return {
                'score': volume_score,
                'recent_volume_ratio': round(recent_volume_ratio, 2),
                'volume_50d_millions': round(volume_50d / 1000000, 1)
            }
            
        except Exception:
            return {'score': 0, 'recent_volume_ratio': 1.0, 'volume_50d_millions': 0}
    
    def _calculate_stop_loss_take_profit_silent(self, df, current_price):
        """Versión sin logs del cálculo de stop loss y take profit"""
        try:
            # STOP LOSS TÉCNICO
            technical_support = self._detect_support_level(df, lookback=30)
            atr_20 = self._calculate_atr(df, 20)
            atr_multiplier = 2.0
            atr_stop = current_price - (atr_20 * atr_multiplier) if atr_20 else None
            
            ma21 = df['Close'].rolling(21).mean().iloc[-1]
            ma50 = df['Close'].rolling(50).mean().iloc[-1]
            
            ma_support = None
            if ma21 < current_price and ma21 > current_price * 0.88:
                ma_support = ma21
            elif ma50 < current_price and ma50 > current_price * 0.88:
                ma_support = ma50
            
            max_loss_stop = current_price * 0.90
            
            stop_candidates = []
            stop_methods = []
            
            if technical_support and technical_support >= max_loss_stop:
                stop_candidates.append(technical_support)
                stop_methods.append("Soporte técnico")
                
            if atr_stop and atr_stop >= max_loss_stop:
                stop_candidates.append(atr_stop)
                stop_methods.append("ATR-based")
                
            if ma_support and ma_support >= max_loss_stop:
                stop_candidates.append(ma_support)
                stop_methods.append("MA soporte")
            
            if stop_candidates:
                optimal_stop = max(stop_candidates)
                best_method_idx = stop_candidates.index(optimal_stop)
                stop_method = stop_methods[best_method_idx]
            else:
                optimal_stop = max_loss_stop
                stop_method = "Límite máximo -10%"
            
            stop_loss_price = round(optimal_stop, 2)
            stop_loss_percentage = round(((stop_loss_price - current_price) / current_price) * 100, 1)
            
            # TAKE PROFIT TÉCNICO
            technical_resistance = self._detect_resistance_level(df, lookback=30)
            atr_target_multiplier = 3.0
            atr_target = current_price + (atr_20 * atr_target_multiplier) if atr_20 else None
            
            max_target = current_price * 1.35
            min_target = current_price * 1.08
            
            target_candidates = []
            target_methods = []
            
            if technical_resistance and min_target <= technical_resistance <= max_target:
                target_candidates.append(technical_resistance)
                target_methods.append("Resistencia técnica")
                
            if atr_target and min_target <= atr_target <= max_target:
                target_candidates.append(atr_target)
                target_methods.append("ATR projection")
            
            if target_candidates:
                optimal_target = min(target_candidates)
                best_target_idx = target_candidates.index(optimal_target)
                target_method = target_methods[best_target_idx]
            else:
                optimal_target = current_price * 1.15
                target_method = "Target conservador +15%"
            
            take_profit_price = round(optimal_target, 2)
            take_profit_percentage = round(((take_profit_price - current_price) / current_price) * 100, 1)
            
            # RISK/REWARD RATIO
            risk = abs(stop_loss_percentage)
            reward = take_profit_percentage
            risk_reward_numeric = reward / risk if risk > 0 else 999
            risk_reward_ratio = f"1:{risk_reward_numeric:.1f}"
            
            return {
                'stop_loss': {
                    'price': stop_loss_price,
                    'loss_percentage': stop_loss_percentage,
                    'method': stop_method
                },
                'take_profit': {
                    'price': take_profit_price,
                    'gain_percentage': take_profit_percentage,
                    'method': target_method
                },
                'risk_reward_ratio': risk_reward_ratio,
                'risk_reward_ratio_numeric': round(risk_reward_numeric, 1)
            }
            
        except Exception:
            # Fallback conservador
            conservative_stop = current_price * 0.92
            conservative_target = current_price * 1.12
            
            stop_price = round(conservative_stop, 2)
            target_price = round(conservative_target, 2)
            
            stop_pct = round(((stop_price - current_price) / current_price) * 100, 1)
            target_pct = round(((target_price - current_price) / current_price) * 100, 1)
            
            risk_reward_numeric = abs(target_pct / stop_pct) if stop_pct != 0 else 1.5
            
            return {
                'stop_loss': {
                    'price': stop_price,
                    'loss_percentage': stop_pct,
                    'method': 'Fallback conservador'
                },
                'take_profit': {
                    'price': target_price,
                    'gain_percentage': target_pct,
                    'method': 'Fallback conservador'
                },
                'risk_reward_ratio': f"1:{risk_reward_numeric:.1f}",
                'risk_reward_ratio_numeric': round(risk_reward_numeric, 1)
            }
    
    def _calculate_relative_strength(self, df):
        """Calcula relative strength vs SPY"""
        try:
            if self.spy_return_5d is None or len(df) < 6:
                return None
                
            current_price = df['Close'].iloc[-1]
            price_5d_ago = df['Close'].iloc[-6]
            stock_return_5d = ((current_price / price_5d_ago) - 1) * 100
            
            relative_strength = stock_return_5d - self.spy_return_5d
            return round(relative_strength, 1)
            
        except Exception:
            return None
    
    def _calculate_quality_score(self, df):
        """Score de calidad técnica general"""
        try:
            volume_consistency = 1 - (df['Volume'].tail(20).std() / df['Volume'].tail(20).mean())
            volume_score = min(volume_consistency * 15, 15)
            
            price_gaps = []
            for i in range(1, min(11, len(df))):
                prev_close = df['Close'].iloc[-i-1]
                curr_open = df['Open'].iloc[-i]
                gap = abs((curr_open - prev_close) / prev_close) * 100
                price_gaps.append(gap)
            
            avg_gap = np.mean(price_gaps) if price_gaps else 0
            gap_score = max(15 - avg_gap, 0)
            
            return round(volume_score + gap_score, 1)
            
        except Exception:
            return 10
    
    def _determine_setup_type(self, momentum_data, breakout_data):
        """Determina el tipo de setup"""
        pullback = breakout_data['pullback_from_high']
        rsi = momentum_data['rsi']
        
        if -8 <= pullback <= -2 and 50 <= rsi <= 65:
            return "Momentum Pullback"
        elif -3 <= pullback <= 1 and rsi > 60:
            return "Breakout Anticipation"
        elif pullback < -8 and rsi < 50:
            return "Oversold Bounce"
        else:
            return "Mixed Setup"
    
    # FUNCIONES AUXILIARES (sin cambios)
    def _calculate_rsi(self, prices, period=14):
        """Calcula RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_atr(self, df, period=20):
        """Calcula Average True Range"""
        try:
            if len(df) < period + 1:
                return None
                
            if not all(col in df.columns for col in ['High', 'Low', 'Close']):
                return None
            
            high_low = df['High'] - df['Low']
            high_close_prev = np.abs(df['High'] - df['Close'].shift())
            low_close_prev = np.abs(df['Low'] - df['Close'].shift())
            
            if high_low.isna().all() or high_close_prev.isna().all() or low_close_prev.isna().all():
                return None
            
            true_range = np.maximum(high_low, np.maximum(high_close_prev, low_close_prev))
            atr = true_range.rolling(window=period).mean().iloc[-1]
            
            if pd.isna(atr) or atr <= 0:
                return None
                
            return atr
            
        except Exception:
            return None
    
    def _detect_support_level(self, df, lookback=20):
        """Detecta nivel de soporte técnico"""
        try:
            current_price = df['Close'].iloc[-1]
            
            # Swing lows recientes
            recent_swing_lows = []
            for i in range(max(0, len(df) - 40), len(df) - 2):
                if (i >= 2 and i < len(df) - 2 and
                    df['Low'].iloc[i] < df['Low'].iloc[i-1] and 
                    df['Low'].iloc[i] < df['Low'].iloc[i+1]):
                    recent_swing_lows.append(df['Low'].iloc[i])
            
            # MAs como soporte
            ma21 = df['Close'].rolling(21).mean().iloc[-1]
            ma50 = df['Close'].rolling(50).mean().iloc[-1]
            
            support_candidates = []
            
            if recent_swing_lows:
                support_candidates.extend([max(recent_swing_lows)])
            
            if ma21 < current_price and ma21 > current_price * 0.88:
                support_candidates.append(ma21)
            if ma50 < current_price and ma50 > current_price * 0.88:
                support_candidates.append(ma50)
            
            if support_candidates:
                valid_supports = [s for s in support_candidates if s >= current_price * 0.90]
                if valid_supports:
                    return max(valid_supports)
                else:
                    return current_price * 0.90
            else:
                return current_price * 0.92
                
        except Exception:
            current_price = df['Close'].iloc[-1]
            return current_price * 0.92
    
    def _detect_resistance_level(self, df, lookback=20):
        """Detecta nivel de resistencia técnico"""
        try:
            current_price = df['Close'].iloc[-1]
            
            # Swing highs recientes
            recent_swing_highs = []
            for i in range(max(0, len(df) - 40), len(df) - 2):
                if (i >= 2 and i < len(df) - 2 and
                    df['High'].iloc[i] > df['High'].iloc[i-1] and 
                    df['High'].iloc[i] > df['High'].iloc[i+1]):
                    recent_swing_highs.append(df['High'].iloc[i])
            
            # Máximo reciente
            recent_high_20d = df['High'].tail(20).max()
            
            resistance_candidates = []
            
            if recent_swing_highs:
                valid_highs = [h for h in recent_swing_highs if h > current_price * 1.02]
                if valid_highs:
                    resistance_candidates.append(min(valid_highs))
            
            if recent_high_20d > current_price * 1.02:
                resistance_candidates.append(recent_high_20d)
            
            if resistance_candidates:
                valid_resistances = [r for r in resistance_candidates 
                                   if current_price * 1.05 <= r <= current_price * 1.35]
                
                if valid_resistances:
                    return min(valid_resistances)
                else:
                    return current_price * 1.15
            else:
                return current_price * 1.15
                
        except Exception:
            current_price = df['Close'].iloc[-1]
            return current_price * 1.15

def main():
    """Función principal optimizada - logs resumidos + scoring mejorado para swing 1-2 semanas"""
    print("=== SCREENER ESPECULATIVO OPTIMIZADO PARA SWING 1-2 SEMANAS ===")
    
    # 1. CONSTRUIR UNIVERSO DINÁMICO
    print("🔍 Construyendo universo dinámico...")
    universe_builder = DynamicUniverseBuilder()
    all_stocks = universe_builder.get_all_tradeable_stocks()
    
    if not all_stocks:
        print("❌ No se pudieron obtener tickers")
        exit(1)
    
    print(f"📊 Iniciando filtros en cascada sobre {len(all_stocks)} acciones...")
    
    # 2. SCREENER OPTIMIZADO
    screener = OptimizedSpeculativeSwingScreener()
    spy_return = screener.calculate_spy_return_5d()
    
    candidates = []
    stage1_passed = 0
    processed = 0
    errors = 0
    
    total_stocks = len(all_stocks)
    batch_size = 100
    total_batches = (total_stocks + batch_size - 1) // batch_size
    
    print(f"🎯 Scoring optimizado: RelativeStrength(20%) + SetupType(15%) + Volume(20%) + Momentum(25%) + Proximity(10%)")
    print(f"📦 Procesando en {total_batches} lotes de {batch_size} acciones c/u")
    print()
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_stocks)
        batch_stocks = all_stocks[start_idx:end_idx]
        
        print(f"📦 Lote {batch_num + 1}/{total_batches} ({start_idx + 1}-{end_idx})")
        
        for i, stock in enumerate(batch_stocks, start_idx + 1):
            # STAGE 1: Filtros rápidos
            if not screener.quick_filters(stock):
                continue
            
            stage1_passed += 1
            
            # STAGE 2 & 3: Análisis optimizado
            try:
                result = screener.analyze_stock_optimized(stock['symbol'])
                processed += 1
                
                if result and result.get('passes_all_filters'):
                    candidates.append(result)
                    
                    # LOG RESUMIDO DE UNA LÍNEA
                    symbol = stock['symbol']
                    score = result.get('total_score', 0)
                    price = result.get('current_price', 0)
                    setup = result.get('setup_type', '')
                    # Truncar setup para mantener alineación
                    setup_short = setup.replace("Momentum ", "Mom.").replace("Breakout ", "Brk.").replace("Anticipation", "Ant")[:12]
                    rr = result.get('risk_reward_ratio', '')
                    rs = result.get('relative_strength_5d', 0)
                    rs_str = f"RS:{rs:+.1f}" if rs else "RS:N/A"
                    
                    print(f"✅ {symbol:6s} ${price:6.2f} Score:{score:5.1f} {setup_short:12s} R:R{rr:6s} {rs_str:7s} #{len(candidates):2d}")
                
                # Progreso cada 25 acciones
                if processed % 25 == 0:
                    candidates_rate = (len(candidates) / processed * 100) if processed > 0 else 0
                    print(f"   📊 {processed:4d}/{total_stocks} | Stage1:{stage1_passed:4d} | Candidatos:{len(candidates):2d} ({candidates_rate:.1f}%)")
                
            except Exception as e:
                errors += 1
                if errors <= 3:  # Solo primeros 3 errores
                    print(f"❌ {stock['symbol']:6s}: {str(e)[:25]}...")
        
        # Pausa reducida
        if batch_num < total_batches - 1:
            print(f"   ⏸️  Pausa 3s...")
            time.sleep(3)
    
    # RESUMEN FINAL COMPACTO
    print(f"\n{'='*70}")
    final_rate = (len(candidates) / total_stocks * 100) if total_stocks > 0 else 0
    print(f"📊 RESUMEN: {total_stocks} total | {stage1_passed} stage1 | {processed} analizadas | {len(candidates)} candidatos ({final_rate:.2f}%) | {errors} errores")
    
    if spy_return:
        print(f"📈 SPY 5d: {spy_return:+.2f}% (benchmark para relative strength)")
    
    # TOP 10 RESUMIDO CON NUEVAS MÉTRICAS
    if candidates:
        top_candidates = sorted(candidates, key=lambda x: x['total_score'], reverse=True)[:20]
        
        print(f"\n🔝 TOP 10 ESPECULATIVOS (Scoring optimizado para swing 1-2 semanas):")
        print(f"{'#':>2} {'SYMBOL':>6} {'PRICE':>8} {'SCORE':>6} {'R:R':>6} {'REL.STR':>7} {'SETUP':>15}")
        print("-" * 65)
        
        for i, candidate in enumerate(top_candidates[:10], 1):
            symbol = candidate['symbol']
            price = candidate['current_price']
            score = candidate['total_score']
            setup = candidate['setup_type']
            if len(setup) > 13:
                setup = setup.replace("Momentum ", "Mom.").replace("Breakout ", "Brk.").replace("Anticipation", "Ant")[:13]
            rr = candidate['risk_reward_ratio']
            rs = candidate.get('relative_strength_5d', 0)
            rs_str = f"{rs:+.1f}%" if rs else "N/A"
            
            print(f"{i:2d} {symbol:>6s} ${price:7.2f} {score:6.1f} {rr:>6s} {rs_str:>7s} {setup:>15s}")
        
        print(f"\n📊 DESGLOSE DE SCORES (Top 3):")
        for i, candidate in enumerate(top_candidates[:3], 1):
            symbol = candidate['symbol']
            print(f"{i}. {symbol}: Total:{candidate['total_score']:.1f} = "
                  f"Mom:{candidate['momentum_score']:.0f} + "
                  f"RS:{candidate['relative_strength_score']:.0f} + "
                  f"Vol:{candidate['volume_score']:.0f} + "
                  f"Setup:{candidate['setup_score']:.0f} + "
                  f"Prox:{candidate['proximity_score']:.0f} + "
                  f"Accel:{candidate['acceleration_score']:.0f} + "
                  f"Qual:{candidate['quality_score']:.0f}")
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Archivo completo
        all_df = pd.DataFrame(candidates)
        all_filename = f"speculative_screening_results_{timestamp}.csv"
        all_df.to_csv(all_filename, index=False)
        print(f"💾 Resultados completos: {all_filename}")
        
        # Top 10 para dashboard
        top_10_df = pd.DataFrame(top_candidates[:10])
        top_filename = f"speculative_top10_{timestamp}.csv"
        top_10_df.to_csv(top_filename, index=False)
        print(f"💾 Top 10 guardado: {top_filename}")
        
        print(f"\n🎯 Criterios optimizados para ganancias máximas en 1-2 semanas aplicados")
        print(f"📱 Dashboard se actualizará automáticamente con estos resultados")
        
    else:
        print("❌ Sin candidatos - Filtros optimizados muy selectivos (normal)")
        print("💡 Los nuevos criterios priorizan calidad sobre cantidad para swing trading corto")

if __name__ == "__main__":
    main()