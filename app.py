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
        # Ordine Sheet: Data, Azienda, Email, Sintomo, Risultato, Dettagli
        sheet.append_row([ora, azienda if azienda else "Anonima", email if email else "N/D", sintomo, risultato, dettagli])
    except:
        pass

# =================================================================
# 2. CONFIGURAZIONE E DESIGN (Rosso comunicAttivamente #DC0612)
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

    /* BOX PROFIT LEAK */
    .leak-box {{
        background-color: #000000 !important;
        color: #ffffff !important;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        border-bottom: 5px solid {ROSSO_BRAND};
    }}
    .leak-amount {{
        color: {ROSSO_BRAND} !important;
        font-size: 50px !important;
        font-weight: bold;
        margin: 10px 0;
    }}

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
        text-align: center;
        width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# =================================================================
# 3. INTERFACCIA
# =================================================================
st.image("https://www.comunicattivamente.it/wp-content/uploads/2023/logo-comunicattivamente.png", width=200)
st.markdown(f"<h1 style='text-align: center; color: {ROSSO_BRAND};'>🚑 PRONTO SOCCORSO</h1>", unsafe_allow_html=True)
st.write("Calcola quanto ti costa il Caos che hai in azienda.")

with st.expander("📝 Identifica la 'Cartella Clinica' (Facoltativo)", expanded=True):
    col_az, col_em = st.columns(2)
    nome_azienda = col_az.text_input("Nome Azienda", placeholder="Esempio: Rossi Srl")
    email_contatto = col_em.text_input("Tua Email", placeholder="email@esempio.it")

st.divider()

sintomo = st.selectbox("QUALE VIRUS TI STA COLPENDO?", [
    "Scegli il sintomo...",
    "⌛ Le riunioni mi rubano tutto il tempo",
    "📱 Mail e Notifiche mi mangiano la vita",
    "👔 Faccio tutto io perché gli altri non sanno fare"
])

# =================================================================
# 4. CALCOLATORI E PROFIT LEAK
# =================================================================
if sintomo != "Scegli il sintomo principale...":
    
    if "riunioni" in sintomo.lower():
        p = st.number_input("Partecipanti medi in sala", 2, 50, 4)
        costo = st.number_input("Costo orario medio collaboratore (€)", 10, 200, 30)
        durata = st.slider("Durata media della riunione (minuti)", 15, 180, 60)
        
        spreco_singolo = (p * costo) * (durata / 60)
        spreco_annuo = spreco_singolo * 52 # Una a settimana
        dettagli_log = f"{p} persone, {durata} min"

    elif "mail" in sintomo.lower():
        ding = st.number_input("Quante volte al giorno guardi notifiche/mail al 'Ding'?", 5, 300, 40)
        costo_impr = st.number_input("Quanto vale un'ora del tuo tempo? (€)", 50, 500, 100)
        
        ore_perse_die = (ding * 15) / 60 # 15 min per recuperare focus
        spreco_annuo = ore_perse_die * costo_impr * 220 # Giorni lavorativi
        dettagli_log = f"{ding} avvisi/die"

    elif "faccio tutto io" in sintomo.lower():
        ore_operative = st.slider("Ore al giorno passate a fare compiti delegabili?", 1, 10, 4)
        costo_impr = st.number_input("Valore della tua ora strategica (€)", 50, 500, 100)
        
        spreco_annuo = ore_operative * (costo_impr - 15) * 220 # -15 perché è il costo di un dipendente che lo farebbe al posto tuo
        dettagli_log = f"{ore_operative} ore/die"

    if st.button("VEDI IL PROFIT LEAK 🩸"):
        st.markdown(f"""
            <div class="leak-box">
                <p style="text-align:center; font-weight:bold; margin:0; text-transform:uppercase; letter-spacing:2px;">🩸 PROFIT LEAK ANNUALE</p>
                <div class="leak-amount">€ {spreco_annuo:,.0f}</div>
                <p style="font-size:18px;">È la ricchezza che stai regalando al Caos ogni anno.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Traduzione emotiva dello spreco
        if spreco_annuo > 20000:
            st.error(f"⚠️ **IMPATTO:** Con questi soldi potresti assumere un nuovo collaboratore o regalarti **4 mesi di vacanza extra**.")
        elif spreco_annuo > 5000:
            st.warning(f"⚠️ **IMPATTO:** Stai bruciando l'equivalente di un'auto nuova o dell'affitto di un ufficio prestigioso.")
        
        salva_diagnosi(nome_azienda, email_contatto, sintomo, f"€{spreco_annuo:,.0f} (annui)", dettagli_log)
        
        # --- CALL TO ACTION ---
        st.divider()
        st.markdown("<h3 style='text-align: center;'>L'Esorcismo inizia qui:</h3>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<a href="https://wa.me/393929334563?text=Ho%20calcolato%20il%20mio%20Profit%20Leak:%20€{spreco_annuo:,.0f}.%20Aiutami!" class="wa-button">💬 WHATSAPP</a>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<a href="https://www.comunicattivamente.it/ebook-ansia-spa" class="wa-button" style="background-color:#1a1a1a;">📘 SCARICA EBOOK</a>', unsafe_allow_html=True)
        
        st.write("")
        st.markdown(f"<div style='text-align: center;'><a href='tel:+393929334563' style='font-size: 24px; color: {ROSSO_BRAND}; text-decoration: none; font-weight: bold;'>📞 +39 392 933 4563</a></div>", unsafe_allow_html=True)

# =================================================================
# 5. FOOTER
# =================================================================
st.write("")
st.write("")
st.write("---")
st.markdown(f"""
    <div style="text-align: center; font-size: 14px;">
        © 2024 <a href="https://www.comunicattivamente.it" target="_blank" style="color: {ROSSO_BRAND}; text-decoration: none; font-weight: bold;">comunicAttivamente</a><br>
        Il software per estirpare l'inefficienza.
    </div>
""", unsafe_allow_html=True)
