import streamlit as st
import pandas as pd
import yfinance as yf

# Setările principale ale paginii web - optimizate pentru ecrane mici
st.set_page_config(page_title="Optimizare BVB", layout="wide", page_icon="📊")

# Titlu simplificat
st.title("🏛️ Optimizare BVB")
st.write("Instrument de scanare pentru cele 20 de acțiuni din indicele BET și emisiunile Fidelis.")

# Selector de Strategie în Bara Laterală
strategie = st.sidebar.selectbox(
    "Modul scanare:",
    ["📊 Acțiuni Indice BET", "🛡️ Emisiuni Fidelis Active"]
)

# Funcție matematică pentru RSI
def calculeaza_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Optimizare pentru mobil: Funcție cu Cache pentru descărcarea datelor
@st.cache_data(ttl=3600)
def descarca_date_bet(companii):
    rezultate = []
    for ticker in companii:
        try:
            # Descărcăm datele istorice
            df = yf.download(ticker, period="2y", interval="1d", progress=False)
            
            if not df.empty:
                # REPARARE: Aplatizăm structura Multi-Index generată de noile versiuni yfinance
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                
                # Extrege prețurile de închidere în siguranță
                preturi_inchidere = df['Close'].dropna()
                
                if len(preturi_inchidere) >= 200:
                    pret_curent = float(preturi_inchidere.iloc[-1])
                    sma_200 = float(preturi_inchidere.rolling(window=200).mean().iloc[-1])
                    rsi_seria = calculeaza_rsi(preturi_inchidere)
                    rsi_actual = float(rsi_seria.iloc[-1])
                    
                    if pret_curent > sma_200 and rsi_actual < 45:
                        decizie = "🟢 CUMPĂRĂ"
                        scor = 1
                    elif pret_curent < sma_200 and rsi_actual < 35:
                        decizie = "🔵 ACUMULARE"
                        scor = 2
                    elif rsi_actual > 70:
                        decizie = "🔴 VINDE"
                        scor = 4
                    else:
                        decizie = "🟡 AȘTEAPTĂ"
                        scor = 3
                    
                    rezultate.append({
                        "Scor": scor,
                        "Simbol": ticker.replace(".RO", ""),
                        "Preț (RON)": round(pret_curent, 2),
                        "RSI": round(rsi_actual, 1),
                        ">SMA200": "✅ DA" if pret_curent > sma_200 else "❌ NU",
                        "Semnal": decizie
                    })
        except Exception as e:
            continue
    return rezultate

# --- MODULUL 1: ACȚIUNI INDICE BET ---
if strategie == "📊 Acțiuni Indice BET":
    st.write("Scanare automată bazată pe indicatorii tehnici RSI și SMA200.")
    
    companii_bet = [
        "TLV.RO", "SNP.RO", "BRD.RO", "SNG.RO", "H2O.RO", 
        "DIGI.RO", "ONE.RO", "TEL.RO", "TGN.RO", "EL.RO", 
        "TTS.RO", "AQ.RO", "ATB.RO", "FP.RO", "BVB.RO",
        "ALR.RO", "WINE.RO", "SMTL.RO", "M.RO", "COTE.RO"
    ]
    
    if st.button("🚀 Rulează Scanarea"):
        with st.spinner("Se încarcă..."):
            rezultate = descarca_date_bet(companii_bet)
        
        if rezultate:
            # Sortare automată în funcție de cel mai mic RSI
            df_final_bet = pd.DataFrame(rezultate).sort_values(by="RSI", ascending=True).drop(columns=["Scor"])
            
            # --- SECȚIUNE ALERTE GRAFICE PE MOBIL (REPARATĂ) ---
            alerte = df_final_bet[df_final_bet["Semnal"].isin(["🟢 CUMPĂRĂ", "🔵 ACUMULARE"])]
            if not alerte.empty:
                st.markdown("### 🚨 Alerte Oportunități")
                cols = st.columns(min(len(alerte), 3))
                for i, row in enumerate(alerte.itertuples()):
                    with cols[i % len(cols)]:
                        # REPARARE: Accesăm prețul direct prin numele proprietății sigure din rând
                        pret_afisat = getattr(row, "Preț__RON_")
                        st.metric(
                            label=f"{row.Simbol} ({row.Semnal})", 
                            value=f"{pret_afisat} RON", 
                            delta=f"RSI: {row.RSI}"
                        )
                st.divider()
            
            st.success("Scanare finalizată!")
            st.dataframe(df_final_bet, use_container_width=True, hide_index=True)
        else:
            st.error("Eroare la preluarea datelor de pe bursă. Reîncearcă.")

# --- MODULUL 2: TITLURILE FIDELIS ACTIVE ---
elif strategie == "🛡️ Emisiuni Fidelis Active":
    st.subheader("🛡️ Matricea Fidelis")
    st.write("Editează prețurile direct în celule pentru a recalcula randamentul real.")
    
    toate_emisiunile_fidelis = [
        {"Simbol": "R2612A", "Cupon": 7.25, "Ani": 0.5, "Valută": "RON"},
        {"Simbol": "R2704A", "Cupon": 6.00, "Ani": 0.8, "Valută": "RON"},
        {"Simbol": "R2707B", "Cupon": 8.25, "Ani": 1.0, "Valută": "RON"},
        {"Simbol": "R2710A", "Cupon": 6.85, "Ani": 1.3, "Valută": "RON"},
        {"Simbol": "R2712A", "Cupon": 6.10, "Ani": 1.5, "Valută": "RON"},
        {"Simbol": "R2804A", "Cupon": 6.85, "Ani": 1.8, "Valută": "RON"},
        {"Simbol": "R2805A", "Cupon": 7.40, "Ani": 1.9, "Valută": "RON"},
        {"Simbol": "R2904A", "Cupon": 7.00, "Ani": 2.8, "Valută": "RON"},
        {"Simbol": "R3005A", "Cupon": 7.80, "Ani": 3.9, "Valută": "RON"},
        {"Simbol": "R3104A", "Cupon": 7.25, "Ani": 4.8, "Valută": "RON"},
        {"Simbol": "R2704B", "Cupon": 7.00, "Ani": 0.8, "Valută": "RON"},
        {"Simbol": "R2710B", "Cupon": 7.85, "Ani": 1.3, "Valută": "RON"},
        {"Simbol": "R2804B", "Cupon": 7.85, "Ani": 1.8, "Valută": "RON"},
        {"Simbol": "R2612AE", "Cupon": 4.00, "Ani": 0.5, "Valută": "EUR"},
        {"Simbol": "R2612BE", "Cupon": 3.75, "Ani": 0.5, "Valută": "EUR"},
        {"Simbol": "R2704AE", "Cupon": 4.00, "Ani": 0.8, "Valută": "EUR"},
        {"Simbol": "R2707BE", "Cupon": 4.40, "Ani": 1.0, "Valută": "EUR"},
        {"Simbol": "R2804AE", "Cupon": 5.00, "Ani": 1.8, "Valută": "EUR"},
        {"Simbol": "R2805AE", "Cupon": 3.85, "Ani": 1.9, "Valută": "EUR"},
        {"Simbol": "R2904AE", "Cupon": 5.00, "Ani": 2.8, "Valută": "EUR"},
        {"Simbol": "R2908AE", "Cupon": 5.00, "Ani": 3.2, "Valută": "EUR"},
        {"Simbol": "R2912AE", "Cupon": 4.95, "Ani": 3.5, "Valută": "EUR"},
        {"Simbol": "R3009AE", "Cupon": 5.25, "Ani": 4.2, "Valută": "EUR"},
        {"Simbol": "R3205AE", "Cupon": 6.25, "Ani": 5.9, "Valută": "EUR"}
    ]
    
    df_baza = pd.DataFrame(toate_emisiunile_fidelis)
    df_baza["Preț (%)"] = 99.5
    
    tabel_editabil = st.data_editor(
        df_baza[["Simbol", "Valută", "Cupon", "Ani", "Preț (%)"]],
        hide_index=True,
        use_container_width=True,
        disabled=["Simbol", "Valută", "Cupon", "Ani"]
    )
    
    rezultate_ytm = []
    for index, row in tabel_editabil.iterrows():
        P = float(row["Preț (%)"])
        C = float(row["Cupon"])
        N = float(row["Ani"])
        
        numitor = (100.0 + P) / 2.0
        numarator = C + ((100.0 - P) / N)
        ytm = (numarator / numitor) * 100.0
        
        if P < 100.0:
            recomandare = f"🟢 Sub par (YTM: {round(ytm, 2)}%)"
        elif P == 100.0:
            recomandare = f"🟡 La par (YTM: {C}%)"
        else:
            recomandare = f"⚠️ Peste par (YTM: {round(ytm, 2)}%)"
            
        rezultate_ytm.append({
            "Simbol": row["Simbol"],
            "Valută": row["Valută"],
            "Preț %": P,
            "Cupon": f"{C}%",
            "YTM_Val": round(ytm, 2),
            "YTM Real": f"{round(ytm, 2)}%",
            "Ghid": recomandare
        })
        
    df_final_fidelis = pd.DataFrame(rezultate_ytm).sort_values(by="YTM_Val", ascending=False).drop(columns=["YTM_Val"])
    st.dataframe(df_final_fidelis, use_container_width=True, hide_index=True)
    
    with st.expander("ℹ️ Ce înseamnă Ghidul Fidelis?"):
        st.markdown("""
        * **Sub par**: Cumperi mai ieftin de 100%. **Randamentul anual real (YTM) crește** peste cupon.
        * **La par**: Cumperi exact la 100%. Randamentul este egal cu cuponul.
        * **Peste par**: Cumperi mai scump de 100%. **Randamentul scade** sub valoarea cuponului.
        """)
