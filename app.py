import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import time
import random

# =================================================================
# 1. CONNESSIONE A GOOGLE SHEETS
# =================================================================
def salva_diagnosi(azienda, email, sintomo, risultato, dettagli):
    try:
        creds_dict = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(st.secrets["private_gsheets_url"]).worksheet("valutazione cliente")
        ora = datetime.now().strftime("%d/%m/%Y %H:%M")
        # Aggiungiamo Azienda ed Email all'invio
        sheet.append_row([ora, azienda, email, sintomo, risultato, dettagli])
    except:
        pass

# =================================================================
# 2. CONFIGURAZIONE E DESIGN (Rosso #DC0612)
# =================================================================
st.set_page_config(page_title="Pronto Soccorso Aziendale", page_icon="🚑", layout="centered")

ROSSO_BRAND = "#DC0612"

st.markdown(f"""
<style>
    header {{visibility: hidden !important;}}
    .stApp {{ background-color: #ffffff !important; }}
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, span, label, div {{
        color: #1a1a1a !important;
    }}

    /* BOX DIAGNOSI */
    .emergency-box {{
        background-color: #fff5f5 !important;
        border: 2px solid {ROSSO_BRAND} !important;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }}
    
    /* TITOLI IN ROSSO BRAND */
    .brand-text {{ color: {ROSSO_BRAND} !important; font-weight: bold; }}

    /* BOTTONI */
    .stButton>button {{ 
        width: 100%; 
        border-radius: 10px; 
        height: 3.5em; 
        font-weight: bold; 
        background-color: {ROSSO_BRAND} !important; 
        color: white !important; 
        border: none;
    }}

    .wa-button {{
        background-color: #25D366;
        color: white !important;
        padding: 15px 25px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
        text-align: center;
        width: 100%;
    }}

    .ebook-button {{
        background-color: #1a1a1a;
        color: white !important;
        padding: 15px 25px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
        text-align: center;
        width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# =================================================================
# 3. INTERFACCIA (RACCOLTA DATI FACOLTATIVA)
# =================================================================
st.image("https://www.comunicattivamente.it/wp-content/uploads/2023/logo-comunicattivamente.png", width=200)
st.markdown(f"<h1 style='text-align: center; color: {ROSSO_BRAND};'>🚑 PRONTO SOCCORSO</h1>", unsafe_allow_html=True)
st.write("Identifica il virus che sta bloccando la tua crescita aziendale.")

with st.expander("📝 I tuoi riferimenti (Opzionale)", expanded=True):
    col_az, col_em = st.columns(2)
    nome_azienda = col_az.text_input("Nome Azienda", placeholder="Facoltativo")
    email_contatto = col_em.text_input("Tua Email", placeholder="Facoltativo")

st.divider()

sintomo = st.selectbox("DOVE TI FA MALE OGGI?", [
    "Scegli il sintomo principale...",
    "⌛ Le riunioni mi rubano tutto il tempo",
    "📱 Mail e Notifiche mi mangiano la vita",
    "👔 Faccio tutto io perché gli altri non sanno fare"
])

# =================================================================
# LOGICA DEI SINTOMI
# =================================================================
if "riunioni" in sintomo.lower():
    st.subheader("🚨 Analisi Costo Chiacchiere")
    p = st.number_input("Quante persone in media?", 2, 50, 4)
    costo = st.number_input("Costo orario medio persona (€)", 10, 200, 35)
    durata = st.slider("Durata media riunione (minuti)", 15, 180, 60)
    
    costo_chiacchiera = (p * costo) * (durata / 60)

    if st.button("GENERA VERDETTO 🔍"):
        st.markdown(f"""<div class="emergency-box">
            <h3 style="margin:0;">DIAGNOSI: Beneficenza Aziendale</h3>
            <h1 style="color:{ROSSO_BRAND}; margin:10px 0;">€ {costo_chiacchiera:.2f}</h1>
            <p>Bruciati per ogni singola riunione.</p>
        </div>""", unsafe_allow_html=True)
        st.error(f"📈 Se ne fai una a settimana, stai regalando **€ {costo_chiacchiera*52:,.0f} all'anno** al Caos.")
        
        salva_diagnosi(nome_azienda, email_contatto, "Riunioni", f"€{costo_chiacchiera}", f"{p} pers, {durata} min")

elif "mail" in sintomo.lower():
    st.subheader("🚨 Analisi Nevrosi Digitale")
    ding = st.number_input("Quante volte al giorno guardi il telefono/mail al 'Ding'?", 5, 300, 40)
    ore_perse = (ding * 15) / 60

    if st.button("GENERA VERDETTO 🔍"):
        st.markdown(f"""<div class="emergency-box">
            <h3 style="margin:0;">DIAGNOSI: Reattività Patologica</h3>
            <h1 style="color:{ROSSO_BRAND}; margin:10px 0;">{ore_perse:.1f} Ore</h1>
            <p>Di pura concentrazione perse OGNI GIORNO.</p>
        </div>""", unsafe_allow_html=True)
        st.warning(f"💡 È come se un tuo dipendente lavorasse **{ore_perse*220/8:.0f} giorni all'anno** solo per guardare notifiche.")
        
        salva_diagnosi(nome_azienda, email_contatto, "Notifiche", f"{ore_perse} ore", f"{ding} avvisi")

elif "faccio tutto io" in sintomo.lower():
    st.subheader("🚨 Analisi Titolare Tuttofare")
    ore_operative = st.slider("Ore al giorno passate a fare compiti delegabili?", 1, 10, 4)
    tuo_valore = st.number_input("Quanto vale un'ora del TUO tempo strategico? (€)", 50, 500, 100)
    spreco = ore_operative * tuo_valore

    if st.button("GENERA VERDETTO 🔍"):
        st.markdown(f"""<div class="emergency-box">
            <h3 style="margin:0;">DIAGNOSI: Titolare Dipendente</h3>
            <h1 style="color:{ROSSO_BRAND}; margin:10px 0;">€ {spreco:.2f}</h1>
            <p>Di valore sottratto al futuro dell'azienda OGNI GIORNO.</p>
        </div>""", unsafe_allow_html=True)
        st.info(f"💸 In un anno, la tua mancanza di delega ti costa **€ {spreco*220:,.0f}**.")
        
        salva_diagnosi(nome_azienda, email_contatto, "Delega", f"€{spreco}/die", f"{ore_operative} ore operative")

# =================================================================
# 4. AREA CONVERSIONE (Ebook, WhatsApp, Telefono)
# =================================================================
if sintomo != "Scegli il sintomo principale...":
    st.divider()
    st.markdown(f"<h3 style='text-align: center;'>L'Esorcismo inizia qui:</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<a href="https://wa.me/393929334563" class="wa-button">💬 SCRIVIMI SU WHATSAPP</a>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<a href="https://www.comunicattivamente.it/ebook-ansia-spa" class="ebook-button">📘 SCARICA EBOOK</a>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown(f"""
        <div style="text-align: center;">
            <p>Oppure chiama l'Unità di Crisi:</p>
            <a href="tel:+393929334563" style="font-size: 24px; color: {ROSSO_BRAND}; text-decoration: none; font-weight: bold;">+39 392 933 4563</a>
        </div>
    """, unsafe_allow_html=True)

# =================================================================
# 5. FOOTER CLICCABILE
# =================================================================
st.write("")
st.write("")
st.write("---")
st.markdown(f"""
    <div style="text-align: center; font-size: 14px;">
        © 2024 <a href="https://www.comunicattivamente.it" target="_blank" style="color: {ROSSO_BRAND}; text-decoration: none; font-weight: bold;">comunicAttivamente</a><br>
        Esorcismo del Caos Aziendale
    </div>
""", unsafe_allow_html=True)
