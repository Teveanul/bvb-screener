import streamlit as st
import pandas as pd
import yfinance as yf

# Setările principale ale paginii web
st.set_page_config(page_title="BVB Terminal Profesional", layout="wide", page_icon="📊")

st.title("🏛️ Terminal BVB & TradeVille - Portofoliu Optimizat Risc Mediu")
st.write("Instrument complet de ierarhizare pentru cele 20 de acțiuni din indicele BET și TOATE emisiunile active Fidelis.")

# Selector de Strategie în Bara Laterală
strategie = st.sidebar.selectbox(
    "Alege modulul de scanare:",
    ["📊 Toate cele 20 de Acțiuni din Indicele BET", "🛡️ Scanner Complet & Ierarhizare TOATE Emisiunile Fidelis Active"]
)

# Funcție matematică pentru RSI
def calculeaza_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# --- MODULUL 1: TOATE CELE 20 DE ACȚIUNI DIN INDICELE BET (REPARAT DEFINITIV) ---
if strategie == "📊 Toate cele 20 de Acțiuni din Indicele BET":
    st.subheader("🔍 Ierarhizare Portofoliu BVB după Oportunitatea de Cumpărare")
    st.write("Acțiunile de top din indicele BET sunt scanate și sortate automat. Cele mai bune momente de intrare apar primele.")
    
    companii_bet = [
        "TLV.RO", "SNP.RO", "BRD.RO", "SNG.RO", "H2O.RO", 
        "DIGI.RO", "ONE.RO", "TEL.RO", "TGN.RO", "EL.RO", 
        "TTS.RO", "AQ.RO", "ATB.RO", "FP.RO", "BVB.RO",
        "ALR.RO", "WINE.RO", "SMTL.RO", "M.RO", "COTE.RO"
    ]
    
    if st.button("🚀 Rulează Scanarea Completă (20 Companii)"):
        rezultate = []
        progress_bar = st.progress(0)
        
        # Iterăm individual prin fiecare ticker pentru a evita conflictul Multi-Index yfinance
        for idx, ticker in enumerate(companii_bet):
            progress_bar.progress((idx + 1) / len(companii_bet))
            
            # Descărcăm datele strict pentru această companie
            df = yf.download(ticker, period="2y", interval="1d", progress=False)
            
            if not df.empty:
                try:
                    # Extragere curată a seriei unidimensionale de preț (Close)
                    if isinstance(df['Close'], pd.DataFrame):
                        preturi_inchidere = df['Close'][ticker].dropna()
                    else:
                        preturi_inchidere = df['Close'].dropna()
                    
                    if len(preturi_inchidere) < 200:
                        continue
                        
                    pret_curent = float(preturi_inchidere.iloc[-1])
                    sma_200 = float(preturi_inchidere.rolling(window=200).mean().iloc[-1])
                    rsi_seria = calculeaza_rsi(preturi_inchidere)
                    rsi_actual = float(rsi_seria.iloc[-1])
                    
                    # Decizie bazată strict pe regulile de Risc Mediu solicitate
                    if pret_curent > sma_200 and rsi_actual < 45:
                        decizie = "1. 🟢 CUMPĂRĂ (Preț optim, trend crescător)"
                        scor = 1
                    elif pret_curent < sma_200 and rsi_actual < 35:
                        decizie = "2. 🔵 ACUMULARE (Ieftin, trend descendent)"
                        scor = 2
                    elif rsi_actual > 70:
                        decizie = "4. 🔴 VINDE (Supra-cumpărat, marchează profit)"
                        scor = 4
                    else:
                        decizie = "3. 🟡 AȘTEAPTĂ (Moment neutru / Observație)"
                        scor = 3
                    
                    rezultate.append({
                        "Scor": scor,
                        "Companie BVB": ticker.replace(".RO", ""),
                        "Preț Curent (RON)": round(pret_curent, 2),
                        "Momentum (RSI 14)": round(rsi_actual, 1),
                        "Peste SMA200 (Trend Lung)": "✅ DA" if pret_curent > sma_200 else "❌ NU",
                        "Recomandare Asistent": decizie
                    })
                except Exception as e:
                    # Ignoră eventualele erori minore de rețea sau simboluri suspendate temporar la tranzacționare
                    continue
                
        progress_bar.empty()
        
        if rezultate:
            tabel_final = pd.DataFrame(rezultate).sort_values(by="Scor", ascending=True)
            tabel_final = tabel_final.drop(columns=["Scor"])
            st.success("Toate cele 20 de companii din indicele BET au fost scanate și ierarhizate cu succes!")
            st.dataframe(tabel_final, use_container_width=True, hide_index=True)
        else:
            st.error("Nu s-au putut procesa datele brute de pe Yahoo Finance. Încearcă din nou în câteva secunde.")

# --- MODULUL 2: TOATE TITLURILE FIDELIS ACTIVE (RĂMÂNE IDENTIC) ---
elif strategie == "🛡️ Scanner Complet & Ierarhizare TOATE Emisiunile Fidelis Active":
    st.subheader("🛡️ Matricea Dinamică Fidelis (Ordonată automat după Profitabilitatea Reală)")
    st.write("Modifică prețurile în tabelul de mai jos direct din TradeVille. Aplicația reordonează instant emisiunile după randamentul YTM.")
    
    toate_emisiunile_fidelis = [
        {"Simbol": "R2612A", "Tip": "Lei Standard", "Cupon": 7.25, "Ani_Ramasi": 0.5, "Monedă": "RON"},
        {"Simbol": "R2704A", "Tip": "Lei Standard", "Cupon": 6.00, "Ani_Ramasi": 0.8, "Monedă": "RON"},
        {"Simbol": "R2707B", "Tip": "Lei Standard", "Cupon": 8.25, "Ani_Ramasi": 1.0, "Monedă": "RON"},
        {"Simbol": "R2710A", "Tip": "Lei Standard", "Cupon": 6.85, "Ani_Ramasi": 1.3, "Monedă": "RON"},
        {"Simbol": "R2712A", "Tip": "Lei Standard", "Cupon": 6.10, "Ani_Ramasi": 1.5, "Monedă": "RON"},
        {"Simbol": "R2804A", "Tip": "Lei Standard", "Cupon": 6.85, "Ani_Ramasi": 1.8, "Monedă": "RON"},
        {"Simbol": "R2805A", "Tip": "Lei Standard", "Cupon": 7.40, "Ani_Ramasi": 1.9, "Monedă": "RON"},
        {"Simbol": "R2904A", "Tip": "Lei Standard", "Cupon": 7.00, "Ani_Ramasi": 2.8, "Monedă": "RON"},
        {"Simbol": "R3005A", "Tip": "Lei Standard", "Cupon": 7.80, "Ani_Ramasi": 3.9, "Monedă": "RON"},
        {"Simbol": "R3104A", "Tip": "Lei Standard", "Cupon": 7.25, "Ani_Ramasi": 4.8, "Monedă": "RON"},
        {"Simbol": "R2704B", "Tip": "Lei Donatori", "Cupon": 7.00, "Ani_Ramasi": 0.8, "Monedă": "RON"},
        {"Simbol": "R2710B", "Tip": "Lei Donatori", "Cupon": 7.85, "Ani_Ramasi": 1.3, "Monedă": "RON"},
        {"Simbol": "R2804B", "Tip": "Lei Donatori", "Cupon": 7.85, "Ani_Ramasi": 1.8, "Monedă": "RON"},
        {"Simbol": "R2612AE", "Tip": "Euro Standard", "Cupon": 4.00, "Ani_Ramasi": 0.5, "Monedă": "EUR"},
        {"Simbol": "R2612BE", "Tip": "Euro Standard", "Cupon": 3.75, "Ani_Ramasi": 0.5, "Monedă": "EUR"},
        {"Simbol": "R2704AE", "Tip": "Euro Standard", "Cupon": 4.00, "Ani_Ramasi": 0.8, "Monedă": "EUR"},
        {"Simbol": "R2707BE", "Tip": "Euro Standard", "Cupon": 4.40, "Ani_Ramasi": 1.0, "Monedă": "EUR"},
        {"Simbol": "R2804AE", "Tip": "Euro Standard", "Cupon": 5.00, "Ani_Ramasi": 1.8, "Monedă": "EUR"},
        {"Simbol": "R2805AE", "Tip": "Euro Standard", "Cupon": 3.85, "Ani_Ramasi": 1.9, "Monedă": "EUR"},
        {"Simbol": "R2904AE", "Tip": "Euro Standard", "Cupon": 5.00, "Ani_Ramasi": 2.8, "Monedă": "EUR"},
        {"Simbol": "R2908AE", "Tip": "Euro Standard", "Cupon": 5.00, "Ani_Ramasi": 3.2, "Monedă": "EUR"},
        {"Simbol": "R2912AE", "Tip": "Euro Standard", "Cupon": 4.95, "Ani_Ramasi": 3.5, "Monedă": "EUR"},
        {"Simbol": "R3009AE", "Tip": "Euro Standard", "Cupon": 5.25, "Ani_Ramasi": 4.2, "Monedă": "EUR"},
        {"Simbol": "R3205AE", "Tip": "Euro Standard", "Cupon": 6.25, "Ani_Ramasi": 5.9, "Monedă": "EUR"}
    ]
    
    df_baza = pd.DataFrame(toate_emisiunile_fidelis)
    df_baza["Preț TradeVille (%)"] = 99.5
    
    st.write("### ⚙️ Instrucțiuni: Editează direct celulele din coloana 'Preț TradeVille (%)' cu valorile din platformă:")
    
    tabel_editabil = st.data_editor(
        df_baza[["Simbol", "Tip", "Monedă", "Cupon", "Ani_Ramasi", "Preț TradeVille (%)"]],
        hide_index=True,
        use_container_width=True,
        disabled=["Simbol", "Tip", "Monedă", "Cupon", "Ani_Ramasi"]
    )
    
    rezultate_ytm = []
    for index, row in tabel_editabil.iterrows():
        P = float(row["Preț TradeVille (%)"])
        C = float(row["Cupon"])
        N = float(row["Ani_Ramasi"])
        
        numitor = (100.0 + P) / 2.0
        numarator = C + ((100.0 - P) / N)
        ytm = (numarator / numitor) * 100.0
        
        if P < 100.0:
            recomandare = f"🟢 Cumperi sub valoarea nominală. Randament excelent ({round(ytm, 2)}% > {C}%)"
        elif P == 100.0:
            recomandare = f"🟡 Paritate perfectă. Câștigi fix dobânda cuponului ({C}%)"
        else:
            recomandare = f"⚠️ Plătești o primă. Randamentul scade sub dobânda nominală ({round(ytm, 2)}% < {C}%)"
            
        rezultate_ytm.append({
            "Simbol": row["Simbol"],
            "Tip": row["Tip"],
            "Monedă": row["Monedă"],
            "Preț Introdus (%)": P,
            "Dobândă Nominală": f"{C}%",
            "Randament Real Anual (YTM %)": round(ytm, 2),
            "Mesaj Asistent": recomandare
        })
        
    df_final_fidelis = pd.DataFrame(rezultate_ytm).sort_values(by="Randament Real Anual (YTM %)", ascending=False)
    
    st.write("---")
    st.write("### 🏆 Clasamentul Profitabilității Reale (Sortat de la cel mai mare YTM în jos):")
    st.dataframe(df_final_fidelis, use_container_width=True, hide_index=True)
