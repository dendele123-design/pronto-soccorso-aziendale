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
        sheet.append_row([ora, azienda if azienda else "Anonima", email if email else "N/D", sintomo, risultato, dettagli])
    except:
        pass

# =================================================================
# 2. CONFIGURAZIONE E DESIGN (#DC0612)
# =================================================================
st.set_page_config(page_title="Pronto Soccorso Aziendale", page_icon="🚑", layout="centered")

ROSSO_BRAND = "#DC0612"

st.markdown(f"""
<style>
    header {{visibility: hidden !important;}}
    .stApp {{ background-color: #ffffff !important; }}
    
    /* FORZA TUTTI I TESTI FUORI DAL BOX NERO */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, span, label, div {{
        color: #1a1a1a;
    }}

    /* BOX PROFIT LEAK - TESTO BIANCO BRILLANTE */
    .leak-box {{
        background-color: #000000 !important;
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        margin: 25px 0;
        border-bottom: 10px solid {ROSSO_BRAND};
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .leak-box p, .leak-box div, .leak-box h3 {{
        color: #ffffff !important; /* BIANCO PURO */
    }}
    
    .leak-label {{
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 10px;
    }}

    .leak-amount {{
        color: {ROSSO_BRAND} !important; /* IL NUMERO RESTA ROSSO */
        font-size: 60px !important;
        font-weight: 900 !important;
        margin: 15px 0;
        text-shadow: 0 0 15px rgba(220, 6, 18, 0.3);
    }

    .leak-footer {{
        font-size: 18px !important;
        font-style: italic;
        opacity: 0.9;
    }}

    .waste-item {{
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 5px solid {ROSSO_BRAND};
        font-size: 16px;
        font-weight: 500;
    }}

    /* BOTTONE PRINCIPALE */
    .stButton>button {{ 
        width: 100%; 
        border-radius: 12px; 
        height: 4em; 
        font-weight: bold; 
        background-color: {ROSSO_BRAND} !important; 
        color: white !important; 
        border: none;
        font-size: 20px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(220, 6, 18, 0.3);
    }}
</style>
""", unsafe_allow_html=True)

# =================================================================
# 3. INTERFACCIA
# =================================================================
st.image("https://www.comunicattivamente.it/wp-content/uploads/2023/logo-comunicattivamente.png", width=220)
st.markdown(f"<h1 style='text-align: center; color: {ROSSO_BRAND};'>🚑 PRONTO SOCCORSO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em;'>Benvenuto nell'Unità di Crisi dell'Esorcista del Caos.</p>", unsafe_allow_html=True)

with st.expander("📝 Identifica la 'Cartella Clinica' (Facoltativo)", expanded=True):
    col_az, col_em = st.columns(2)
    nome_azienda = col_az.text_input("Nome Azienda", placeholder="Esempio: Rossi Srl")
    email_contatto = col_em.text_input("Tua Email", placeholder="email@esempio.it")

st.divider()

sintomo = st.selectbox("QUALE VIRUS TI STA COLPENDO OGGI?", [
    "Scegli il sintomo...",
    "⌛ Le riunioni mi rubano tutto il tempo",
    "📱 Mail e Notifiche mi mangiano la vita",
    "👔 Faccio tutto io perché gli altri non sanno fare",
    "💸 Vendo molto, ma non vedo mai i soldi (Margini)"
])

# =================================================================
# 4. LOGICA DI CALCOLO
# =================================================================
if sintomo != "Scegli il sintomo principale...":
    
    if "riunioni" in sintomo.lower():
        p = st.number_input("Partecipanti medi in sala", 2, 50, 4)
        costo = st.number_input("Costo orario medio collaboratore (€)", 10, 200, 30)
        durata = st.slider("Durata media della riunione (minuti)", 15, 180, 60)
        spreco_annuo = (p * costo) * (durata / 60) * 52 
        dettagli_log = f"{p} persone, {durata} min"

    elif "mail" in sintomo.lower():
        ding = st.number_input("Quante volte al giorno guardi notifiche/mail appena arriva il 'Ding'?", 5, 300, 40)
        costo_impr = st.number_input("Quanto vale un'ora del tuo tempo strategico? (€)", 50, 500, 100)
        ore_perse_die = (ding * 15) / 60 
        spreco_annuo = ore_perse_die * costo_impr * 220 
        dettagli_log = f"{ding} avvisi/die"

    elif "faccio tutto io" in sintomo.lower():
        ore_operative = st.slider("Quante ore al giorno passi a fare compiti che potrebbe fare un dipendente?", 1, 10, 4)
        costo_impr = st.number_input("Valore della tua ora da Imprenditore (€)", 50, 500, 100)
        spreco_annuo = ore_operative * (costo_impr - 15) * 220 
        dettagli_log = f"{ore_operative} ore/die"

    elif "margini" in sintomo.lower():
        fatturato = st.number_input("Fatturato Annuo stimato (€)", 50000, 5000000, 500000, step=50000)
        errore_prezzo = st.slider("Sconti inutili o errori nei prezzi (stima % del fatturato)", 1, 15, 5)
        spreco_annuo = fatturato * (errore_prezzo / 100)
        dettagli_log = f"Fatturato {fatturato}, Errore {errore_prezzo}%"

    if st.button("AVVIA DIAGNOSI PROFONDA 🔍"):
        progress_text = "Analisi in corso..."
        my_bar = st.progress(0, text=progress_text)
        scan_messages = ["Mappatura processi...", "Rilevazione emorragie finanziarie...", "Calcolo impatto sulla salute...", "Generazione Verdetto..."]
        for i, msg in enumerate(scan_messages):
            my_bar.progress((i + 1) * 25, text=msg)
            time.sleep(0.6)
        my_bar.empty()

        # --- BOX RISULTATO (CORRETTO VISIVAMENTE) ---
        st.markdown(f"""
            <div class="leak-box">
                <div class="leak-label">🩸 PROFIT LEAK ANNUALE</div>
                <div class="leak-amount">€ {spreco_annuo:,.0f}</div>
                <div class="leak-footer">Soldi che la tua azienda brucia nel silenzio.</div>
            </div>
        """, unsafe_allow_html=True)

        st.write("### 💸 Con questi soldi ogni anno potevi comprare:")
        col_w1, col_w2 = st.columns(2)
        
        with col_w1:
            if spreco_annuo > 2000: st.markdown('<div class="waste-item">⌚ <b>1 Rolex Submariner</b></div>', unsafe_allow_html=True)
            if spreco_annuo > 8000: st.markdown('<div class="waste-item">🏖️ <b>Viaggio Business Class</b> alle Maldive</div>', unsafe_allow_html=True)
            if spreco_annuo > 25000: st.markdown('<div class="waste-item">🚗 <b>Porsche Macan</b> (Canone leasing annuo)</div>', unsafe_allow_html=True)

        with col_w2:
            if spreco_annuo > 5000: st.markdown(f'<div class="waste-item">👥 <b>{int(spreco_annuo/2000)} Mensilità</b> per un nuovo braccio destro</div>', unsafe_allow_html=True)
            if spreco_annuo > 15000: st.markdown('<div class="waste-item">🏢 <b>Nuova sede</b> o restyling uffici</div>', unsafe_allow_html=True)
            if spreco_annuo > 40000: st.markdown('<div class="waste-item">💎 <b>Dividendi puliti</b> per la tua famiglia</div>', unsafe_allow_html=True)

        salva_diagnosi(nome_azienda, email_contatto, sintomo, f"€{spreco_annuo:,.0f}", dettagli_log)
        
        # --- CALL TO ACTION ---
        st.divider()
        st.markdown("<h3 style='text-align: center;'>Smetti di essere l'ultimo a pagarsi:</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<a href="https://wa.me/393929334563?text=Daniele,%20ho%20fatto%20il%20test%20Pronto%20Soccorso.%20Il%20mio%20Profit%20Leak%20è%20€{spreco_annuo:,.0f}.%20Voglio%20fermare%20lo%20spreco!" style="background-color:#25D366; color:white; padding:15px; border-radius:50px; text-decoration:none; font-weight:bold; display:block; text-align:center;">💬 WHATSAPP DI EMERGENZA</a>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<a href="https://www.comunicattivamente.it/ebook-ansia-spa" style="background-color:#1a1a1a; color:white; padding:15px; border-radius:50px; text-decoration:none; font-weight:bold; display:block; text-align:center;">📘 SCARICA EBOOK</a>', unsafe_allow_html=True)
        
        st.write("")
        st.markdown(f"<div style='text-align: center;'><a href='tel:+393929334563' style='font-size: 24px; color: {ROSSO_BRAND}; text-decoration: none; font-weight: bold;'>📞 CHIAMA: +39 392 933 4563</a></div>", unsafe_allow_html=True)

# =================================================================
# 5. FOOTER
# =================================================================
st.write("")
st.write("")
st.write("---")
st.markdown(f"""
    <div style="text-align: center; font-size: 14px;">
        © 2024 <a href="https://www.comunicattivamente.it" target="_blank" style="color: {ROSSO_BRAND}; text-decoration: none; font-weight: bold;">comunicAttivamente</a><br>
        La medicina per il tuo tempo e il tuo profitto.
    </div>
""", unsafe_allow_html=True)
