import streamlit as st
import pandas as pd
import random
import os
import base64
from openai import OpenAI

# 0. CONFIGURAZIONE PAGINA (Aggiunge la fiammella e il titolo nella scheda del browser)
st.set_page_config(
    page_title="It's a match!",
    page_icon="🔥",
    layout="centered"
)

# 1. Caricamento dati
df = pd.read_csv("clustered_bios.csv")

# 2. Configurazione della pagina e pulizia CSS (Iniezione totale nel cuore di Streamlit)
st.markdown(
    """
    <style>
    /* Importazione font: Inter per i testi e Syne per il titolo moderno d'impatto */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Syne:wght@700;800&display=swap');
    
    /* Font di lettura pulito per i testi nativi di Streamlit per fare contrasto */
    html, body, [class*="st-"], p, div, label, span, button, select, input, textarea {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sfondo sfumato dell'applicazione */
    .stApp {
        background: linear-gradient(135deg, #FFF0F2 0%, #FF1F76 100%) !important;
    }
    
    /* CONTENITORE TITOLO */
    .titolo-custom-container {
        text-align: center !important; 
        margin-top: 20px !important; 
        margin-bottom: 10px !important;
        width: 100% !important;
        display: block !important;
    }

    /* TITOLO PRINCIPALE: NUOVO STILE BOLD, MODERNO E D'IMPATTO */
    .titolo-custom-container h1 {
        font-family: 'Syne', sans-serif !important;
        text-transform: uppercase !important;
        color: #FF1744 !important; /* Rosso vivo acceso */
        font-size: 110px !important; /* Dimensione gigante bilanciata */
        font-weight: 800 !important; /* Extra bold massiccio */
        margin: 0px auto !important;
        padding: 0px !important;
        letter-spacing: -4px !important; /* Lettere vicine e compatte stile poster */
        line-height: 0.9 !important;
    }

    /* Sottotitolo pulito e moderno */
    .titolo-custom-container p {
        font-family: 'Inter', sans-serif !important;
        font-size: 22px !important;
        font-weight: 600 !important;
        color: #5A5A5A !important; 
        margin-top: 15px !important;
        margin-bottom: 30px !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Box contenitore del logo */
    .logo-container {
        text-align: center;
        margin: 15px auto;
        width: 100%;
    }
    
    /* Controllo totale dimensione logo */
    .logo-container img {
        max-width: 35% !important;
        height: auto !important;
        border-radius: 12px;
    }
    
    /* Bottone viola scuro personalizzato */
    .stButton>button {
        width: 100% !important;
        border-radius: 30px !important;
        background-color: #591C53 !important; 
        color: white !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        text-transform: 
        border: none !important;
        padding: 12px 0px !important;
    }
    
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- BLOCCO TITOLO AGGIORNATO ---
st.markdown(
    """
    <div class="titolo-custom-container">
        <h1>It's a match!</h1>
        <p>Il tuo assistente personale per un profilo perfetto</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- SEZIONE IMMAGINE ---
cartella_progetto = os.path.dirname(os.path.abspath(__file__))
percorso_immagine = os.path.join(cartella_progetto, "logo nero.png")

if os.path.exists(percorso_immagine):
    with open(percorso_immagine, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{img_base64}"></div>', unsafe_allow_html=True)
else:
    st.warning("File 'logo nero.png' non trovato nella cartella del progetto.")
# -----------------------------------------------------------------------

# 3. Configurazione OpenAI sicura per Streamlit Cloud
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# 4. INTERFACCIA A TRIPLICE TAB
tab1, tab2, tab3 = st.tabs(["✨ Generatore Bio", "🎯 Analisi Affinità & Icebreaker", "🔍 Analizza la tua Bio"])

# =====================================================================
# --- TAB 1: GENERATORE BIO ---
# =====================================================================
with tab1:
    st.subheader("Crea il tuo profilo ideale")
    
    col1, col2 = st.columns(2)
    with col1:
        genere = st.selectbox("Il tuo genere", ["Uomo", "Donna", "Non Binario", "Preferisco non specificare", "Altro"])
        eta = st.number_input("Età", min_value=18, max_value=99, value=18)
    with col2:
        orientamento = st.selectbox("Orientamento sessuale", [
            "Eterosessuale", "Gay", "Lesbica", "Bisessuale", "Panessuale", "Asessuale", "Queer", "Altro"
        ])
        
        toni_disponibili = [
            "Ironico", "Romantico", "Simpatico", "Diretto", 
            "Misterioso", "Sarcastico", "Intellettuale", "Avventuroso", 
            "Divertente", "Dolce", "Sfacciato", "Professionale"
        ]
        tono = st.selectbox("Tono della Bio", toni_disponibili)

    interessi = st.text_area("I tuoi interessi e passioni", placeholder="Esempio: Trekking, Vinili, Cucina Giapponese, Tech, Serie TV...")

    tutti_i_cluster = df["Cluster"].unique()
    cluster_scelto = random.choice(tutti_i_cluster)
    cluster_examples = df[df["Cluster"] == cluster_scelto]
    examples = cluster_examples["Biografia"].sample(3, replace=True)

    if st.button("Genera la mia Bio ✨"):
        if interessi.strip() == "":
            st.warning("Per favore, inserisci almeno qualche interesse per aiutare l'AI!")
        else:
            with st.spinner("L'esperto AI sta creando la tua bio..."):
                prompt_bio = f"""
                Sei un esperto di dating app e approcci sui comportamenti degli utenti.
                Genera una nuova bio per Tinder che sia originale, inclusiva e non banale.

                Dati Utente:
                Genere: {genere}
                Età: {eta}
                Orientamento: {orientamento}
                Interessi: {interessi}
                Tono desiderato: {tono}

                Questi sono esempi reali di bio dello stesso stile da cui prendere ispirazione solo per struttura e lunghezza:
                - {examples.iloc[0]}
                - {examples.iloc[1]}
                - {examples.iloc[2]}

                La bio generata deve essere unica. Non copiare assolutamente le frasi degli esempi.
                """
                
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_bio}]
                )
                st.success("### Ecco la tua nuova Bio personalizzata:")
                st.write(res.choices[0].message.content)

# =====================================================================
# --- TAB 2: ANALISI AFFINITÀ & ICEBREAKER ---
# =====================================================================
with tab2:
    st.subheader("Hai trovato una persona interessante?")
    st.write("Incolla qui sotto la tua bio e quella del tuo match per scoprire l'affinità e ricevere 3 frasi di apertura personalizzate!")

    my_bio_input = st.text_area("La tua bio (o i tuoi interessi principali)", key="my_bio", placeholder="Incolla la tua bio...")
    target_bio_input = st.text_area("Incolla qui la bio dell'altra persona", key="target_bio", placeholder="Incolla la bio del tuo match...")

    if st.button("Analizza Affinità 🎯"):
        if my_bio_input and target_bio_input:
            with st.spinner("Analisi della compatibilità in corso..."):
                prompt_affinity = f"""
                Analizza queste due biografie per una dating app.
                Bio Utente: {my_bio_input}
                Bio Match: {target_bio_input}
                
                Genera un resoconto strutturato in questo modo:
                1. **Punteggio di Affinità**: Calcola una percentuale da 0% a 100% basata sulle passioni comuni o complementari.
                2. **Analisi di Compatibilità**: Spiega in modo chiaro e amichevole cosa unisce queste due persone e quali sono i punti di forza del match.
                3. **3 Icebreaker Personalizzati**: Scrivi 3 frasi di apertura diverse (es. una divertente, una intrigante, una diretta) basate specificamente sugli elementi in comune trovati nelle bio, evitando assolutamente frasi fatte come 'Ciao, come va?'.
                """
                
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_affinity}]
                )
                st.info("### Risultato Analisi Match:")
                st.write(res.choices[0].message.content)
        else:
            st.warning("Per favore, inserisci entrambe le biografie per procedere con il calcolo dell'affinità!")

# =====================================================================
# --- TAB 3: ANALISI BIO PERSONALE & CRINGIOMETRO ---
# =====================================================================
with tab3:
    st.subheader("Fai un 'Check-up' alla tua biografia attuale 🔍")
    st.write("Inserisci la tua attuale bio per ricevere una pagella onesta dall'esperto e misurare il suo livello di cringe.")
    
    user_existing_bio = st.text_area("Incolla qui la bio che vuoi far analizzare", placeholder="Scrivi o incolla qui il testo...", key="existing_bio_audit")
    
    if st.button("Analizza e Calcola Cringiometro 📊"):
        if user_existing_bio:
            with st.spinner("L'esperto sta valutando il livello di imbarazzo digitale..."):
                
                prompt_audit = f"""
                Sei un ironico, schietto ma costruttivo esperto di profili per dating app (Tinder, Bumble, Hinge).
                Analizza la seguente biografia scritta da un utente:
                
                "{user_existing_bio}"
                
                Fornisci una risposta che contenga OBBLIGATORIAMENTE questa esatta stringa all'inizio:
                CRINGE_SCORE: [Inserisci qui SOLO un numero intero da 1 a 10, senza aggiungere altro testo su questa riga]
                
                Poi continua il resoconto con la seguente formattazione:
                **VOTO GENERALE**: da 1 a 10 con una breve motivazione.
                **PUNTI DI FORZA**: cosa funziona, cosa incuriosisce e cosa attira i match.
                **PUNTI DI DEBOLEZZA**: cosa annoia, quali cliché sono presenti, o cosa risulta oggettivamente 'cringe'.
                **VERSIONE MIGLIORATA**: Riscrivi la stessa identica bio ottimizzandola per renderla attraente e magnetica, mantenendo intatta la personalità dell'utente.
                """
                
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt_audit}]
                )
                
                risposta_ai = res.choices[0].message.content
                
                # Parsing del Cringe Score per la barra grafica di Streamlit
                try:
                    parts = risposta_ai.split("CRINGE_SCORE:")
                    cringe_score_raw = parts[1].split("\n")[0].strip()
                    cringe_score = int(''.join(filter(str.isdigit, cringe_score_raw)))
                    testo_pulito = parts[0] + parts[1].replace(cringe_score_raw, "", 1)
                except:
                    cringe_score = 5  # Fallback di sicurezza
                    testo_pulito = risposta_ai
                
                # Visualizzazione grafica del Cringiometro
                st.write("### 🚨 Risultato del Cringiometro:")
                
                if cringe_score <= 3:
                    st.success(f"**Livello di Cringe: {cringe_score}/10** — Profilo sicuro! Ottima naturalezza, eviti i vicoli ciechi dell'imbarazzo.")
                elif cringe_score <= 6:
                    st.warning(f"**Livello di Cringe: {cringe_score}/10** — Zona grigia. C'è qualche frase fatta, posa da intellettuale o cliché superato da sistemare.")
                else:
                    st.error(f"**Livello di Cringe: {cringe_score}/10** — EMERGENZA! Livello di cringe oltre i limiti consentiti dalla legge. Riscrivila subito.")
                
                # Visualizza la barra (Streamlit accetta float da 0.0 a 1.0)
                st.progress(cringe_score / 10)
                
                st.markdown("---")
                st.write("### 📋 Resoconto Dettagliato dell'Esperto:")
                st.write(testo_pulito.strip())
        else:
            st.warning("Inserisci del testo nella casella per calcolare il Cringiometro!")
