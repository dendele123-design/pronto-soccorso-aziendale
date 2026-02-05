import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import time
import random

# =================================================================
# 1. CONNESSIONE A GOOGLE SHEETS (Archivio Diagnosi)
# =================================================================
def salva_diagnosi(sintomo, risultato, dettagli):
    try:
        creds_dict = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(st.secrets["private_gsheets_url"]).worksheet("Diagnosi")
        ora = datetime.now().strftime("%d/%m/%Y %H:%M")
        sheet.append_row([ora, sintomo, risultato, dettagli])
    except:
        pass # Silenzioso se fallisce, non vogliamo bloccare l'utente

# =================================================================
# 2. CONFIGURAZIONE E DESIGN (Stile Pronto Soccorso)
# =================================================================
st.set_page_config(page_title="Pronto Soccorso Aziendale", page_icon="🚑", layout="centered")

st.markdown("""
<style>
    /* ANTI DARK-MODE */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, span, label, div {
        color: #1a1a1a !important;
    }
    .stApp { background-color: #ffffff !important; }
    header {visibility: hidden !important;}

    /* BOX DIAGNOSI */
    .emergency-box {
        background-color: #fff5f5 !important;
        border: 2px solid #ff4b4b !important;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* BOX ESORCISTA */
    .verdetto-box {
        background-color: #000000 !important;
        color: #ffffff !important;
        padding: 30px;
        border-radius: 10px;
        font-style: italic;
        text-align: center;
        font-size: 20px;
        margin-top: 20px;
        line-height: 1.4;
    }

    /* BOTTONI */
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =================================================================
# 3. INTERFACCIA
# =================================================================
st.image("https://www.comunicattivamente.it/wp-content/uploads/2023/logo-comunicattivamente.png", width=180)
st.title("🚑 PRONTO SOCCORSO")
st.write("Identifica il virus che sta bloccando la tua azienda.")

st.divider()

sintomo = st.selectbox("DOVE TI FA MALE OGGI?", [
    "Scegli il sintomo principale...",
    "⌛ Le riunioni mi rubano tutto il tempo",
    "📱 Mail e Notifiche mi mangiano la vita",
    "👔 Faccio tutto io perché gli altri non sanno fare"
])

st.write("")

# =================================================================
# DIAGNOSI 1: RIUNIONI
# =================================================================
if "riunioni" in sintomo.lower():
    st.subheader("🚨 Analisi Costo Chiacchiere")
    with st.container(border=True):
        p = st.number_input("Quante persone partecipano mediamente?", 2, 50, 4)
        costo = st.number_input("Costo orario medio di un partecipante (€)", 10, 200, 35)
        durata = st.slider("Quanto dura la riunione? (minuti)", 15, 180, 60)
    
    costo_chiacchiera = (p * costo) * (durata / 60)

    if st.button("GENERA VERDETTO 🔍", type="primary"):
        st.markdown(f"""<div class="emergency-box">
            <h3 style="margin:0; color:#ff4b4b;">DIAGNOSI: Beneficenza Aziendale</h3>
            <h1 style="color:#ff4b4b; margin:10px 0;">€ {costo_chiacchiera:.2f}</h1>
            <p>È il capitale che hai appena bruciato.</p>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="verdetto-box">
            "Se la riunione dura più di 40 minuti ed esci senza un obiettivo scritto e una scadenza assegnata, 
            non hai fatto una riunione. Hai regalato soldi ai tuoi dipendenti per stare seduti a parlare."
        </div>""", unsafe_allow_html=True)
        
        salva_diagnosi("Riunioni", f"€{costo_chiacchiera:.2f}", f"{p} persone, {durata} min")
        st.link_button("ESORCIZZA LE RIUNIONI 🔥", "mailto:daniele@comunicattivamente.it")

# =================================================================
# DIAGNOSI 2: MAIL / NOTIFICHE
# =================================================================
elif "mail" in sintomo.lower():
    st.subheader("🚨 Analisi Nevrosi Digitale")
    with st.container(border=True):
        ding = st.number_input("Quante volte al giorno senti un 'Ding' o guardi le mail?", 5, 300, 40)
    
    # La scienza: 15 min per recuperare il focus
    ore_focus_perse = (ding * 15) / 60

    if st.button("GENERA VERDETTO 🔍", type="primary"):
        st.markdown(f"""<div class="emergency-box">
            <h3 style="margin:0; color:#ff4b4b;">DIAGNOSI: Reattività Patologica</h3>
            <h1 style="color:#ff4b4b; margin:10px 0;">{ore_focus_perse:.1f} Ore</h1>
            <p>Di concentrazione perse OGNI GIORNO.</p>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="verdetto-box">
            "La reattività immediata non è efficienza, è schiavitù digitale. 
            Se rispondi a tutto appena arriva, non sei un imprenditore: sei un citofono."
        </div>""", unsafe_allow_html=True)
        
        salva_diagnosi("Notifiche", f"{ore_focus_perse:.1f} ore perse", f"{ding} avvisi/die")
        st.link_button("LIBERATI DAL CITOFONO ⛓️", "mailto:daniele@comunicattivamente.it")

# =================================================================
# DIAGNOSI 3: DELEGA
# =================================================================
elif "faccio tutto io" in sintomo.lower():
    st.subheader("🚨 Analisi Titolare Tuttofare")
    with st.container(border=True):
        ore_operative = st.slider("Quante ore al giorno passi a fare compiti che potrebbe fare un dipendente?", 1, 10, 4)
        tuo_valore = st.number_input("Quanto vale un'ora del TUO tempo strategico? (€)", 50, 500, 100)
    
    spreco_strategico = ore_operative * tuo_valore

    if st.button("GENERA VERDETTO 🔍", type="primary"):
        st.markdown(f"""<div class="emergency-box">
            <h3 style="margin:0; color:#ff4b4b;">DIAGNOSI: Titolare Dipendente</h3>
            <h1 style="color:#ff4b4b; margin:10px 0;">€ {spreco_strategico:.2f}</h1>
            <p>È il valore che sottrai alla crescita dell'azienda OGNI GIORNO.</p>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="verdetto-box">
            "Ogni volta che dici 'Faccio prima a farlo io', stai rubando tempo al tuo futuro per fare un lavoro da 15 euro l'ora. 
            Complimenti: sei il dipendente più costoso e meno efficiente che hai."
        </div>""", unsafe_allow_html=True)
        
        salva_diagnosi("Delega", f"€{spreco_strategico} persi/die", f"{ore_operative} ore operative")
        st.link_button("SMETTI DI FARE IL DIPENDENTE 👔", "mailto:daniele@comunicattivamente.it")

# =================================================================
# FOOTER
# =================================================================
st.write("")
st.write("---")
st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <p style="font-weight:bold; margin-bottom:5px;">Daniele Salvatori | comunicAttivamente</p>
        <a href="https://wa.me/393929334563" style="color: #25D366; text-decoration: none; font-weight: bold; font-size:1.2em;">💬 CONTATTO DI EMERGENZA</a><br><br>
        <div style="color: #888; font-size: 12px;">Powered by SuPeR & Streamlit</div>
    </div>
""", unsafe_allow_html=True)
