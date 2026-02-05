import streamlit as st
import time
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# =================================================================
# 1. CONNESSIONE A SHEET (Cartella Clinica Clienti)
# =================================================================
def salva_diagnosi(problema, risultato, nota):
    try:
        creds_dict = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        # Assicurati di avere un foglio chiamato "Diagnosi"
        sheet = client.open_by_url(st.secrets["private_gsheets_url"]).worksheet("Diagnosi")
        ora = datetime.now().strftime("%d/%m/%Y %H:%M")
        sheet.append_row([ora, problema, risultato, nota])
    except:
        pass # Se non c'è connessione, l'app non deve crashare

# =================================================================
# 2. DESIGN E STILE
# =================================================================
st.set_page_config(page_title="Pronto Soccorso Aziendale", page_icon="🚑", layout="centered")

st.markdown("""
<style>
    header {visibility: hidden !important;}
    .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
    html, body, [class*="css"], p, h1, h2, h3, label { color: #1a1a1a !important; }
    
    .emergency-box {
        background-color: #fff5f5;
        border: 2px solid #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .verdetto-esorcista {
        background-color: #000000;
        color: #ffffff !important;
        padding: 25px;
        border-radius: 10px;
        font-style: italic;
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =================================================================
# 3. INTERFACCIA
# =================================================================
st.image("https://www.comunicattivamente.it/wp-content/uploads/2023/logo-comunicattivamente.png", width=150)
st.title("🚑 PRONTO SOCCORSO")
st.subheader("Individua il tumore del tempo nella tua azienda.")

st.write("### Dove senti più dolore oggi?")
sintomo = st.selectbox("Seleziona il tuo problema principale:", [
    "Scegli il sintomo...",
    "⌛ Le riunioni sono infinite e inutili",
    "📱 Mail e Notifiche mi mangiano la testa",
    "🗣️ I dipendenti non sanno cosa fare"
])

st.divider()

# =================================================================
# CASO 1: RIUNIONI
# =================================================================
if sintomo == "⌛ Le riunioni sono infinite e inutili":
    st.write("### 🚨 L'Analizzatore di Riunioni")
    col1, col2 = st.columns(2)
    p = col1.number_input("Partecipanti", 1, 20, 4)
    c = col2.number_input("Costo orario medio persona (€)", 10, 100, 35)
    durata = st.slider("Durata media riunione (minuti)", 10, 180, 60)
    
    costo_totale = (p * c) * (durata / 60)
    
    if st.button("GENERA DIAGNOSI 🔍"):
        st.markdown(f"""
        <div class="emergency-box">
            <h2 style="text-align:center; color:#ff4b4b;">Questa chiacchierata ti costa: € {costo_totale:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="verdetto-esorcista">
            "Se la riunione dura più di 40 minuti ed esci senza un obiettivo scritto e una scadenza assegnata, 
            non hai fatto una riunione. Hai fatto beneficenza oraria ai tuoi dipendenti."
        </div>
        """, unsafe_allow_html=True)
        
        salva_diagnosi("Riunioni", f"€{costo_totale}", f"Durata {durata} min")
        st.link_button("ESORCIZZA LE RIUNIONI 🔥", "mailto:daniele@comunicattivamente.it")

# =================================================================
# CASO 2: MAIL E NOTIFICHE
# =================================================================
elif sintomo == "📱 Mail e Notifiche mi mangiano la testa":
    st.write("### 🚨 Il Calcolatore della Distrazione")
    avvisi = st.number_input("Quante volte al giorno guardi il telefono o le mail appena arriva il 'Ding'?", 1, 200, 30)
    
    # La scienza dice che servono 15 min per tornare focalizzati
    tempo_perso_h = (avvisi * 15) / 60
    
    if st.button("GENERA DIAGNOSI 🔍"):
        st.markdown(f"""
        <div class="emergency-box">
            <h2 style="text-align:center; color:#ff4b4b;">Oggi hai buttato: {tempo_perso_h:.1f} ore di concentrazione</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="verdetto-esorcista">
            "La reattività immediata non è efficienza, è nevrosi aziendale. 
            Se rispondi a tutto subito, sei uno schiavo della tecnologia, non un imprenditore."
        </div>
        """, unsafe_allow_html=True)
        
        salva_diagnosi("Notifiche", f"{tempo_perso_h} ore", f"{avvisi} avvisi")
        st.link_button("LIBERATI DALLE CATENE ⛓️", "mailto:daniele@comunicattivamente.it")

# =================================================================
# CASO 3: DELEGA (PROSSIMAMENTE)
# =================================================================
elif sintomo == "🗣️ I dipendenti non sanno cosa fare":
    st.info("Questo modulo di diagnosi è in fase di attivazione. Ma sappiamo già che il problema è la mancanza di procedure scritte.")
    st.link_button("CHIAMA L'ESORCISTA SUBITO", "mailto:daniele@comunicattivamente.it")

# --- FOOTER ---
st.write("")
st.write("---")
st.markdown("<div style='text-align: center; color: #888;'>comunicAttivamente | Ansia S.p.A. Division</div>", unsafe_allow_html=True)
