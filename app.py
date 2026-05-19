import streamlit as st
import pandas as pd
import plotly.express as px
import csv
import requests

# --- INTESTAZIONI UFFICIALI UPS ---
INTESTAZIONI_DEFAULT = [
    'Versione', 'Numero destinatari', 'Numero di codice cliente', 'Paese codice cliente', 
    'Data della fattura', 'Numero della fattura', 'Codice del tipo di fattura', 'Codice dettaglio del tipo di fattura', 
    'ID fiscale codice cliente', 'Codice valuta della fattura', 'Importo della fattura', 'Data spedizione', 
    'Numero di registrazione del ritiro', 'Numero spedizione principale', 'Numero World Ease', 
    'Numero di riferimento 1 spedizione', 'Numero di riferimento 2 spedizione', "Codice dell'opzione di fatturazione", 
    'Quantità pacchi', 'Quantità fuori misura', 'Numero di ricerca', 'Numero di riferimento pacco 1', 
    'Numero di riferimento pacco 2', 'Numero di riferimento pacco 3', 'Numero di riferimento pacco 4', 
    'Numero di riferimento pacco 5', 'Peso specificato', 'Unità di misura del peso specificato', 
    'Peso fatturato', 'Unità di misura del peso fatturato', 'Tipo di contenitore', 'Tipo di peso fatturato', 
    'Dimensioni dei pacchi', 'Zona', 'Codice categoria spese', 'Codice dettaglio per categoria spese', 
    'Origine dei costi', 'Digita codice 1', 'Digita codice dettaglio 1', 'Digita valore dettaglio 1', 
    'Digita codice 2', 'Digita codice dettaglio 2', 'Digita valore dettaglio 2', 'Codice classificazione spese', 
    'Codice descrizione spesa', 'Descrizione spesa', 'Quantità unitaria addebitata', 'Codice valuta di base', 
    'Valore di base', 'Indicatore imposte', 'Codice valuta della transazione', 'Importo incentivo', 
    'Importo netto', 'Codice valute varie', 'Importo incentivo varie', 'Importo netto varie', 
    'Codice valuta della fattura alternativa', 'Importo fattura alternativa', 'Tasso di cambio in fattura', 
    'Importo variazioni di imposta', 'Importo variazioni di valuta', 'Spesa a livello di fattura', 
    'Data di scadenza della fattura', 'Numero della fattura alternativa', 'Numero di magazzino', 
    'Numero di riferimento del cliente', 'Nome mittente', 'Nome società del mittente', 
    'Riga 1 indirizzo del mittente', 'Riga 2 indirizzo del mittente', 'Città del mittente', 
    'Stato del mittente', 'CAP mittente', 'Paese del mittente', 'Nome destinatario', 
    'Nome società del destinatario', 'Riga 1 indirizzo del destinatario', 'Riga 2 indirizzo del destinatario', 
    'Città del destinatario', 'Stato del destinatario', 'CAP destinatario', 'Paese del destinatario', 
    'Nome terza parte', 'Nome società terza parte', 'Riga 1 indirizzo terza parte', 
    'Riga 2 indirizzo terza parte', 'Città terza parte', 'Stato terza parte', 'CAP terza parte', 
    'Paese terza parte', 'Nome acquirente', 'Nome società dell’acquirente', 'Riga 1 indirizzo acquirente', 
    'Riga 2 indirizzo acquirente', 'Città dell’acquirente', 'Stato dell’acquirente', 'CAP acquirente', 
    'Paese dell’acquirente', 'Qual indirizzo 1 varie', 'Nome indirizzo 1 varie', 
    'Nome società indirizzo 1 varie', 'Riga 1 indirizzo 1 varie', 'Riga 1 indirizzo 2 varie', 
    'Città indirizzo 1 varie', 'Stato indirizzo 1 varie', 'CAP indirizzo 1 varie', 
    'Paese indirizzo 1 varie', 'Qual indirizzo 2 varie', 'Nome indirizzo 2 varie', 
    'Nome società indirizzo 2 varie', 'Riga 2 indirizzo 1 varie', 'Riga 2 indirizzo 2 varie', 
    'Città indirizzo 2 varie', 'Stato indirizzo 2 varie', 'CAP indirizzo 2 varie', 
    'Paese indirizzo 2 varie', 'Data di spedizione', 'Data di esportazione spedizione', 
    'Data di importazione spedizione', 'Data di ingresso', 'Data spedizione diretta', 
    'Data di consegna della spedizione', 'Data rilascio spedizione', 'Data ciclo', 'Data EFT', 
    'Data di convalida', 'Porto di ingresso', 'Numero Entry', 'Luogo di esportazione', 
    'Importo valore di spedizione', 'Descrizione spedizione', 'Codice valuta immesso', 'Numero dogana', 
    'Tasso di cambio', 'Lettera di vettura aerea principale', 'EPU', 'Tipo di immissione', 
    'Codice CPC', 'Numero voce di riga', 'Descrizione merce', 'Valore immesso', 'Importo dazi', 
    'Peso', 'Unità di misura', 'Quantità articoli', 'Unità di misura della quantità articoli', 
    'ID fiscale importazione', 'Numero di dichiarazione', 'Nome vettore', 'Numero RCCD', 
    'Numero cicli', 'Numero di riferimento commercio estero', 'Numero attività', 'Modalità trasporto', 
    'Tipo di tassa', 'Codice tariffe', 'Quota tariffaria', 'Numero tariffa', 'Persona da contattare', 
    'Numero classe', 'Tipo di documento', 'Numero ufficio', 'Numero documento', 'Valore dazi', 
    'Valore totale per i dazi', 'Importo imposte indirette', 'Aliquota imposte indirette', 
    'Importo GST', 'Tasso GST', 'Order In Council', 'Paese di origine', 'Accesso SIMA', 
    'Valore fiscale', 'Importo doganale totale', 'Riga 1 varie', 'Riga 2 varie', 'Riga 3 varie', 
    'Riga 4 varie', 'Riga 5 varie', 'Codice ruolo pagante', 'Riga 7 varie', 'Riga 8 varie', 
    'Riga 9 varie', 'Riga 10 varie', 'Riga 11 varie', 'Tariffa dazi', 'Importo di base IVA', 
    'Importo IVA', 'Aliquota IVA', 'Importo altra base', 'Altro importo', 'Altra tariffa', 
    'Indicatore Altro numero doganale', 'Altro numero doganale', 'Nome ufficio doganale', 
    'Unità di misura dimensioni del pacco', 'Quantità pacchi di spedizione originale', 'Zona Corretta', 
    'Numero Articolo secondo Legge Tasse', 'Ammontare Base Articolo secondo Legge Tasse', 
    'Numero Tracking originale', 'Quantità scala di peso', 'Unità di misura della scala di peso', 
    'Unità di misura dimensioni reali', 'Dimensioni reali', 'Numero di polizza di carico 1', 
    'Numero di polizza di carico 2', 'Numero di polizza di carico 3', 'Numero di polizza di carico 4', 
    'Numero di polizza di carico 5', 'Numero OA 1', 'Numero OA 2', 'Numero OA 3', 'Numero OA 4', 
    'Numero OA 5', 'Numero OA 6', 'Numero OA 7', 'Numero OA 8', 'Numero OA 9', 'Numero OA 10', 
    'NMFC', 'Dettaglio della classe', 'Numero sequenza cargo', 'Classe di trasporto dichiarata', 
    'Numero EORI', 'Segnaposto 35', 'Segnaposto 36', 'Segnaposto 37', 'Segnaposto 38', 'Segnaposto 39', 
    'Segnaposto 40', 'Segnaposto 41', 'Segnaposto 42', 'Segnaposto 43', 'Segnaposto 44', 'Segnaposto 45', 
    'Segnaposto 46', 'Segnaposto 47', 'Segnaposto 48', 'Segnaposto 49', 'Segnaposto 50', 'Segnaposto 51', 
    'Segnaposto 52', 'Segnaposto 53', 'Segnaposto 54', 'Segnaposto 55', 'Segnaposto 56', 'Segnaposto 57', 
    'Segnaposto 58', 'Segnaposto 59', 'Unnamed: 250', 'Uso interno UPS'
]

# Configurazione iniziale
st.set_page_config(page_title="Invoice Analyzer", page_icon="📦", layout="wide")

# CSS personalizzato per correggere la visualizzazione delle metriche
st.markdown("""
<style>
/* Evita il troncamento dei numeri (puntini...) nelle metriche e li ridimensiona dinamicamente */
[data-testid="stMetricValue"] > div {
    font-size: clamp(1.1rem, 2.5vw, 1.8rem) !important;
    white-space: normal !important;
    text-overflow: clip !important;
    line-height: 1.2 !important;
    word-break: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SISTEMA DI SICUREZZA (UTENTI E PIN)
# ==============================
# Le credenziali vengono lette in modo sicuro dai "Secrets" di Streamlit Cloud.
EMAIL_AUTORE = "stefano@my.com" # L'email mostrata a chi vuole usare il programma

def invia_notifica_telegram(messaggio):
    if "telegram" in st.secrets and "bot_token" in st.secrets["telegram"] and "chat_id" in st.secrets["telegram"]:
        bot_token = st.secrets["telegram"]["bot_token"]
        chat_id = st.secrets["telegram"]["chat_id"]
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": messaggio}
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception:
            pass # Ignoriamo errori di connessione per non bloccare l'app

if "autorizzato" not in st.session_state:
    st.session_state.autorizzato = False
if "utente_corrente" not in st.session_state:
    st.session_state.utente_corrente = ""

if not st.session_state.autorizzato:
    st.title("🔒 Software Protetto")
    st.markdown(f"Questo programma è ad uso esclusivo. Se non hai le credenziali, richiedile a: **{EMAIL_AUTORE}**")
    
    st.info("""
    **Avviso di Servizio (Fase Beta) e Monitoraggio Accessi**  
    Questo strumento è attualmente ospitato su un server condiviso gratuito per una fase di test riservata a pochi clienti selezionati.  
    - **Possibili rallentamenti:** Se più persone caricano file di grandi dimensioni contemporaneamente, l'applicazione potrebbe subire forti rallentamenti o riavviarsi temporaneamente (errore di memoria).  
    - **Riattivazione:** Se l'app non viene utilizzata per qualche giorno, entrerà in modalità riposo. Al primo accesso successivo, potrebbe impiegare fino a 1 minuto per "risvegliarsi".
    - 🛡️ **Sicurezza e Privacy:** Per prevenire abusi e garantire le performance del server, **tutti gli accessi a questa piattaforma sono strettamente monitorati**. Ogni tentativo di login (sia corretto che errato) viene notificato in tempo reale all'amministratore di sistema. Si prega di non condividere le proprie credenziali personali.
    """)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        utente_inserito = st.text_input("Nome Utente:")
        pin_inserito = st.text_input("PIN Personale:", type="password")
        if st.button("Accedi"):
            utente_chiave = utente_inserito.strip().lower()
            
            # Controllo credenziali nei secrets
            if "utenti" in st.secrets and utente_chiave in st.secrets["utenti"]:
                pin_corretto = str(st.secrets["utenti"][utente_chiave])
                if pin_inserito == pin_corretto:
                    st.session_state.autorizzato = True
                    st.session_state.utente_corrente = utente_inserito.strip().capitalize()
                    invia_notifica_telegram(f"✅ ACCESSO CONSENTITO: L'utente '{st.session_state.utente_corrente}' è entrato nell'app Invoice Analyzer.")
                    st.rerun()
                else:
                    invia_notifica_telegram(f"🚨 TENTATIVO DI INTRUSIONE: Qualcuno ha provato ad accedere con l'utente '{utente_inserito}' ma ha inserito un PIN errato.")
                    st.error("❌ PIN errato.")
            else:
                # Fallback per accesso locale in caso di problemi di configurazione
                if utente_chiave == "admin" and pin_inserito == "2026UPS":
                    st.session_state.autorizzato = True
                    st.session_state.utente_corrente = "Admin (Locale)"
                    invia_notifica_telegram(f"⚠️ ACCESSO ADMIN (FALLBACK): L'amministratore è entrato tramite password di fallback locale.")
                    st.rerun()
                else:
                    invia_notifica_telegram(f"🚨 TENTATIVO DI INTRUSIONE: Utente sconosciuto '{utente_inserito}' ha tentato l'accesso.")
                    st.error("❌ Utente non trovato o credenziali errate.")
    
    st.stop() # Blocca l'esecuzione di tutto il resto del programma finché non si inserisce il PIN corretto

st.title("📦 Invoice Analyzer")

st.sidebar.success(f"👤 Connesso come: **{st.session_state.utente_corrente}**")
st.sidebar.markdown("---")
st.sidebar.header("📂 Carica file fattura")
uploaded_file = st.sidebar.file_uploader("Upload CSV fattura", type=["csv", "txt"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Impostazioni Alert")
escludi_residenziale = st.sidebar.checkbox("Nascondi Alert 'Consegna Residenziale'", value=True, help="Se spuntato, la consegna a domicilio privato non verrà segnalata in rosso come anomalia.")

st.sidebar.markdown("---")
st.sidebar.subheader("⚖️ Audit Penali Correction Fee")
attiva_audit_scc = st.sidebar.checkbox("Attiva Audit Previsione Correction Fee", value=True, help="Evidenzia le spedizioni che rischiano penali per discrepanza di peso nella prossima fattura.")

debug_mode = st.sidebar.checkbox("🛠 Mostra dati grezzi (Debug)", value=False)

if uploaded_file:
    try:
        raw_text = uploaded_file.getvalue().decode('latin1')
        lines = raw_text.splitlines()
        
        parsed_data = []
        for line in lines:
            if not line.strip(): continue
            sep = ';' if line.count(';') > line.count(',') else ','
            reader = csv.reader([line], delimiter=sep)
            try:
                parsed_data.append(next(reader))
            except StopIteration:
                pass
                
        df = pd.DataFrame(parsed_data)
        
        num_cols = df.shape[1]
        
        if df.iloc[0].astype(str).str.contains('Versione|Numero', case=False, na=False).any():
            df = df.iloc[1:].reset_index(drop=True)
        
        num_cols = df.shape[1]
        
        if num_cols <= len(INTESTAZIONI_DEFAULT):
            df.columns = INTESTAZIONI_DEFAULT[:num_cols]
        else:
            extra_cols = [f"ColonnaExtra_{i}" for i in range(num_cols - len(INTESTAZIONI_DEFAULT))]
            df.columns = INTESTAZIONI_DEFAULT + extra_cols
            
        df.columns = df.columns.str.strip()

        # Campi chiave attesi
        COL_SPEDIZIONE = "Numero spedizione principale"
        COL_IMPORTO = "Importo netto"
        COL_CLASSIFICAZIONE = "Codice classificazione spese"
        COL_DESCRIZIONE = "Descrizione spesa"
        COL_PACCHI = "Quantità pacchi"
        COL_PESO_FATT = "Peso fatturato"
        COL_PESO_SPEC = "Peso specificato"
        COL_UM = "Unità di misura del peso fatturato"

        colonne_minime = [COL_SPEDIZIONE, COL_IMPORTO, COL_CLASSIFICAZIONE, COL_DESCRIZIONE]
        colonne_mancanti = [col for col in colonne_minime if col not in df.columns]

        if debug_mode:
            st.markdown("---")
            st.error("⚠️ MODALITÀ DEBUG ATTIVA")
            st.write(f"Numero di colonne trovate: **{df.shape[1]}**")
            st.dataframe(df.head(10))

        if not colonne_mancanti:
            df[COL_IMPORTO] = pd.to_numeric(df[COL_IMPORTO].astype(str).str.strip().str.replace(',', '.'), errors='coerce').fillna(0.0)
            
            if COL_PESO_FATT in df.columns and COL_PESO_SPEC in df.columns:
                df[COL_PESO_FATT] = pd.to_numeric(df[COL_PESO_FATT].astype(str).str.strip().str.replace(',', '.'), errors='coerce').fillna(0.0)
                df[COL_PESO_SPEC] = pd.to_numeric(df[COL_PESO_SPEC].astype(str).str.strip().str.replace(',', '.'), errors='coerce').fillna(0.0)

            # SCC Calcolo
            def calcola_rischio_scc(row):
                if COL_PESO_FATT in row and COL_PESO_SPEC in row:
                    peso_dich = row[COL_PESO_SPEC]
                    peso_fatt = row[COL_PESO_FATT]
                    if pd.notna(peso_dich) and pd.notna(peso_fatt) and peso_dich > 0 and peso_fatt > peso_dich:
                        delta_perc = ((peso_fatt - peso_dich) / peso_dich) * 100
                        if delta_perc >= 25.0:
                            return True, delta_perc
                return False, 0.0

            scc_results = df.apply(calcola_rischio_scc, axis=1)
            df['Rischio_SCC'] = [res[0] for res in scc_results]
            df['Delta_Peso_Perc'] = [res[1] for res in scc_results]

            # Funzione per classificare i costi nei 4 bucket richiesti
            def classifica_costo(row):
                cod = str(row[COL_CLASSIFICAZIONE]).upper().strip()
                desc = str(row[COL_DESCRIZIONE]).upper()
                if cod == 'FRT':
                    return 'Nolo'
                elif cod == 'FSC' or 'FUEL' in desc or 'CARBURANTE' in desc:
                    return 'Fuel'
                elif cod in ['TAX', 'VAT', 'DUT'] or 'TAX' in desc or 'IVA' in desc or 'IMPOSTA' in desc:
                    return 'Tax'
                else:
                    return 'Supplementi'
            
            df['Categoria_Costo'] = df.apply(classifica_costo, axis=1)

            # Identificazione Alert Anomali
            parole_escluse = []
            
            # Se la spunta è attiva, escludiamo il residenziale dagli alert
            if escludi_residenziale:
                parole_escluse.extend(["residential", "residenziale", "domicilio privato"])

            def is_alert(row):
                # Nolo, Fuel e Tax non generano MAI alert
                if row['Categoria_Costo'] in ['Nolo', 'Tax', 'Fuel']:
                    return False
                    
                # Se l'importo è 0.00, non è un'anomalia (UPS inserisce spesso righe informative a zero)
                try:
                    if float(row[COL_IMPORTO]) == 0.0:
                        return False
                except:
                    pass
                
                desc = str(row[COL_DESCRIZIONE]).lower()
                
                # Se è residenziale E la spunta è attiva, non genera alert
                if any(escl in desc for escl in parole_escluse):
                    return False
                
                # ALTRIMENTI, se siamo arrivati qui, è sempre un alert!
                return True

            df["Alert_Final"] = df.apply(is_alert, axis=1)

            # Estrazione informazioni aggiuntive per ogni tracking
            info_spedizione = df.groupby(COL_SPEDIZIONE).agg(
                Pacchi=(COL_PACCHI, lambda x: next(iter([v for v in x if pd.notna(v) and str(v).strip() != '']), '') if COL_PACCHI in df.columns else ''),
                Peso_Fatt=(COL_PESO_FATT, 'max'),
                Peso_Spec=(COL_PESO_SPEC, 'max'),
                UM=(COL_UM, lambda x: next(iter([v for v in x if pd.notna(v) and str(v).strip() != '']), '') if COL_UM in df.columns else ''),
                Rischio_SCC=('Rischio_SCC', 'max'),
                Delta_Peso_Perc=('Delta_Peso_Perc', 'max')
            ).reset_index()

            pivot_costi = df.pivot_table(index=COL_SPEDIZIONE, columns='Categoria_Costo', values=COL_IMPORTO, aggfunc='sum', fill_value=0).reset_index()
            
            for c in ['Nolo', 'Fuel', 'Tax', 'Supplementi']:
                if c not in pivot_costi.columns:
                    pivot_costi[c] = 0.0

            # Estrai il nome del Servizio (Descrizione della riga Nolo)
            df_nolo = df[df['Categoria_Costo'] == 'Nolo']
            servizi = df_nolo.groupby(COL_SPEDIZIONE)[COL_DESCRIZIONE].first().reset_index()
            servizi.rename(columns={COL_DESCRIZIONE: 'Servizio'}, inplace=True)

            grouped_base = df.groupby(COL_SPEDIZIONE).agg(
                Totale_Spedizione=(COL_IMPORTO, "sum"),
                Presenza_Alert=("Alert_Final", "max")
            ).reset_index()

            grouped = pd.merge(grouped_base, pivot_costi, on=COL_SPEDIZIONE)
            grouped = pd.merge(grouped, info_spedizione, on=COL_SPEDIZIONE)
            grouped = pd.merge(grouped, servizi, on=COL_SPEDIZIONE, how='left')
            grouped['Servizio'] = grouped['Servizio'].fillna('Sconosciuto')

            grouped["Stato"] = grouped["Presenza_Alert"].apply(lambda x: "⚠️ Alert" if x else "✅ OK")

            def format_pacchi(p):
                try:
                    val = float(p)
                    if val > 1:
                        return f"Multipla ({int(val)} colli)"
                    elif val == 1:
                        return "1 collo"
                    return str(p)
                except:
                    return str(p) if str(p).strip() != "" else "N/D"

            grouped['Pacchi_Display'] = grouped['Pacchi'].apply(format_pacchi)

            # ==============================
            # SEZIONE 1: KPI DASHBOARD
            # ==============================
            st.markdown("---")
            st.header("📈 Dashboard Analitica Costi")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            totale_fattura = grouped["Totale_Spedizione"].sum()
            totale_nolo = grouped["Nolo"].sum()
            totale_fuel = grouped["Fuel"].sum()
            totale_tax = grouped["Tax"].sum()
            totale_supplementi = grouped["Supplementi"].sum()
            
            # Calcolo importo fattura escludendo le tasse (per calcolare le vere incidenze operative)
            fattura_no_tax = totale_fattura - totale_tax
            
            # Calcoliamo i "Supplementi Anomali" (cioè quelli che hanno generato l'alert, escludendo Nolo, Fuel, Tax e Residenziale se spuntato)
            totale_anomali = df[df['Alert_Final'] == True][COL_IMPORTO].sum()
            
            col1.metric("Spesa Totale (con Tax)", f"€ {totale_fattura:,.2f}")
            col2.metric("Spesa Netta (Senza Tax)", f"€ {fattura_no_tax:,.2f}")
            col3.metric("Incidenza Nolo Base", f"{(totale_nolo/fattura_no_tax*100) if fattura_no_tax > 0 else 0:.1f}%", f"€ {totale_nolo:,.2f}")
            col4.metric("Incidenza Fuel", f"{(totale_fuel/fattura_no_tax*100) if fattura_no_tax > 0 else 0:.1f}%", f"€ {totale_fuel:,.2f}")
            col5.metric("KPI Surcharge (su Netto)", f"{(totale_anomali/fattura_no_tax*100) if fattura_no_tax > 0 else 0:.1f}%", f"€ {totale_anomali:,.2f}", delta_color="inverse")

            # ==============================
            # SEZIONE 1.2: VOLUMI E SERVIZI
            # ==============================
            st.markdown("---")
            st.subheader("📦 Volumi e Servizi")
            
            # Calcolo volumi
            grouped['Pacchi_Num'] = pd.to_numeric(grouped['Pacchi'], errors='coerce').fillna(1.0)
            tot_spedizioni = len(grouped)
            singole = len(grouped[grouped['Pacchi_Num'] == 1.0])
            multiple = len(grouped[grouped['Pacchi_Num'] > 1.0])
            
            col_v1, col_v2, col_v3 = st.columns(3)
            col_v1.metric("Spedizioni Totali", tot_spedizioni)
            col_v2.metric("Spedizioni Singole (1 Collo)", singole)
            col_v3.metric("Spedizioni Multiple (>1 Collo)", multiple)
            
            st.markdown("**Ripartizione per Servizio:**")
            sped_per_servizio = grouped['Servizio'].value_counts().reset_index()
            sped_per_servizio.columns = ['Servizio', 'Numero Spedizioni']
            st.dataframe(sped_per_servizio, hide_index=True, use_container_width=True)

            # ==============================
            # SEZIONE 1.5: FOCUS SUPPLEMENTI ANOMALI
            # ==============================
            st.markdown("---")
            st.subheader("📊 KPI Surcharge: Analisi Incidenza Supplementi")
            st.markdown("Questa sezione analizza in dettaglio i **Surcharge (Supplementi Anomali)**, escludendo Nolo, Fuel, Tasse e Residenziale se ignorato. Mostra quanto incidono sul totale della fattura al netto delle tasse.")
            
            df_anomali = df[df['Alert_Final'] == True]
            if not df_anomali.empty:
                # Raggruppiamo per Descrizione
                breakdown = df_anomali.groupby(COL_DESCRIZIONE)[COL_IMPORTO].sum().reset_index()
                breakdown = breakdown[breakdown[COL_IMPORTO] > 0]
                breakdown['Incidenza % (su Netto)'] = (breakdown[COL_IMPORTO] / fattura_no_tax) * 100
                breakdown = breakdown.sort_values(by=COL_IMPORTO, ascending=False)
                
                st.dataframe(
                    breakdown.style.format({
                        COL_IMPORTO: "€ {:.2f}",
                        'Incidenza % (su Netto)': "{:.2f}%"
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.success("Nessun supplemento anomalo rilevato in questa fattura!")

            # ==============================
            # SEZIONE 2: ANALISI PER SERVIZIO SPEDIZIONI SINGOLE
            # ==============================
            st.markdown("---")
            st.subheader("📊 KPI: Outlier >30%")
            st.info("💡 **Disclaimer:** Il KPI “Outlier >30%” segnala spedizioni con uno scostamento significativo rispetto al costo medio del cliente. La sua rilevanza aumenta per clienti con formati di spedizione standardizzati, mentre può risultare meno indicativo in presenza di ampia variabilità di pesi e dimensioni.")
            
            if len(grouped) > 0:
                grouped['Pacchi_Num'] = pd.to_numeric(grouped['Pacchi'], errors='coerce').fillna(1.0)
                
                # Filtriamo SOLO le spedizioni singole
                grouped_singole = grouped[grouped['Pacchi_Num'] == 1.0].copy()
                
                if len(grouped_singole) > 0:
                    # Calcolo indice di omogeneità sui pesi
                    pesi_validi = grouped_singole['Peso_Fatt'].dropna()
                    if len(pesi_validi) > 0:
                        pesi_arrotondati = pesi_validi.round()
                        percentuale_dominante = (pesi_arrotondati.value_counts().max() / len(pesi_validi)) * 100
                    else:
                        percentuale_dominante = 0
                        
                    if percentuale_dominante >= 80:
                        with st.expander(f"🟢 **Contesto Omogeneo ({percentuale_dominante:.0f}%)** - Dato altamente significativo"):
                            st.markdown("Oltre l’80% delle spedizioni rientra nello stesso range di peso reale o volumetrico.\n\nL’indicatore Outlier >30% è considerato **altamente significativo**.")
                    else:
                        with st.expander(f"🟡 **Alta Variabilità ({percentuale_dominante:.0f}%)** - Interpretare con cautela"):
                            st.markdown("Le spedizioni risultano distribuite su più range di peso e volume.\n\nL’indicatore Outlier >30% può riflettere **variabilità operativa fisiologica**.")
                            
                    st.markdown("<br>", unsafe_allow_html=True)
                    stats_servizio = grouped_singole.groupby('Servizio').agg(
                        Num_Spedizioni=('Totale_Spedizione', 'count'),
                        Costo_Totale_Servizio=('Totale_Spedizione', 'sum'),
                        Peso_Totale_Servizio=('Peso_Fatt', 'sum')
                    ).reset_index()
                    
                    stats_servizio['Costo_Medio'] = stats_servizio['Costo_Totale_Servizio'] / stats_servizio['Num_Spedizioni']
                    stats_servizio['Peso_Medio'] = stats_servizio['Peso_Totale_Servizio'] / stats_servizio['Num_Spedizioni']
                    stats_servizio = stats_servizio.sort_values('Num_Spedizioni', ascending=False)
                    
                    for _, row_srv in stats_servizio.iterrows():
                        srv = row_srv['Servizio']
                        n_sped = row_srv['Num_Spedizioni']
                        c_medio = row_srv['Costo_Medio']
                        p_medio = row_srv['Peso_Medio']
                        soglia = c_medio * 1.30
                        
                        outliers_srv = grouped_singole[(grouped_singole['Servizio'] == srv) & (grouped_singole['Totale_Spedizione'] > soglia)]
                        num_out = len(outliers_srv)
                        
                        # Definisci icona e stato per l'expander
                        status_icon = "🚨" if num_out > 0 else "✅"
                        
                        with st.expander(f"{status_icon} {srv} | Spedizioni Singole: {n_sped} | Peso Medio: {p_medio:.2f} | Costo Medio: € {c_medio:.2f}"):
                            if num_out > 0:
                                st.warning(f"**{num_out}** spedizioni superano la soglia del +30% (**€ {soglia:.2f}**)")
                                out_display = outliers_srv[[COL_SPEDIZIONE, 'Totale_Spedizione', 'Peso_Fatt']].copy()
                                out_display['Scostamento %'] = ((out_display['Totale_Spedizione'] - c_medio) / c_medio * 100)
                                out_display = out_display.sort_values('Scostamento %', ascending=False)
                                
                                st.dataframe(
                                    out_display.style.format({
                                        'Totale_Spedizione': '€ {:.2f}',
                                        'Scostamento %': '+{:.1f}%',
                                        'Peso_Fatt': '{:.2f}'
                                    }),
                                    use_container_width=True,
                                    hide_index=True
                                )
                            else:
                                st.success("Tutte le spedizioni sono in linea con il costo medio.")
                else:
                    st.info("Non ci sono spedizioni a collo singolo in questa fattura da poter analizzare.")

            # ==============================
            # SEZIONE 3: AUDIT CORRECTION FEE (PREVISIONE PENALI)
            # ==============================
            if attiva_audit_scc:
                st.markdown("---")
                st.header("⚖️ Audit Pesi e Previsione Correction Fee")
                
                with st.expander("ℹ️ INFO TECNICA: Come viene calcolato il Rischio Correction Fee", expanded=False):
                    st.markdown("""
                    **Shipping Charge Correction (Correction Fee)**  
                    UPS applica un supplemento in fattura ("Correction Fee", mediamente **1,50€ a spedizione**) quando rileva una forte discrepanza tra il **Peso Dichiarato** dal cliente e il **Peso Reale/Volumetrico Rilevato** dai loro sistemi.
                    
                    💡 **La nostra Analisi:**  
                    Per aiutarti a prevenire future penali, il sistema analizza tutte le spedizioni confrontando il peso originariamente specificato con quello effettivamente fatturato. 
                    Se la discrepanza rilevata da UPS è **superiore al 25%**, la spedizione viene evidenziata come "A Rischio". 
                    In questo modo potrai agire proattivamente ed educare chi prepara i colli a pesare e misurare con maggiore precisione.
                    """)

                df_rischio = grouped[grouped['Rischio_SCC'] == True]
                
                if not df_rischio.empty:
                    tot_scc = len(df_rischio) * 1.50
                    incidenza_su_totale = (tot_scc / totale_fattura) * 100 if totale_fattura > 0 else 0
                    incidenza_media_spedizione = tot_scc / len(grouped)

                    st.warning(f"🚨 Trovate **{len(df_rischio)} spedizioni** con scostamento di peso ≥ 25%. Rischio penali Correction Fee stimate in fattura successiva: **€ {tot_scc:.2f}**")
                    
                    st.markdown("### 📊 Impatto Globale Previsto")
                    col_scc1, col_scc2, col_scc3 = st.columns(3)
                    col_scc1.metric("Aumento Costo Fattura", f"+€ {tot_scc:.2f}", help="Totale dei Correction Fee stimati che potrebbero essere addebitati nella prossima fattura.")
                    col_scc2.metric("Aumento % su Fattura", f"+{incidenza_su_totale:.2f}%", help="Incidenza percentuale delle penali previste rispetto al costo totale dell'attuale fattura.")
                    col_scc3.metric("Incidenza per Spedizione", f"+€ {incidenza_media_spedizione:.2f}", help="Il peso economico di questi futuri supplementi spalmato equamente su tutte le spedizioni di questa fattura.")
                    
                    st.success(f"💡 **L'Impatto Nascosto sui tuoi Margini:**\n\n"
                            f"La previsione di queste penali, pari a **€ {tot_scc:.2f}**, ci rivela un costo occulto. Se distribuiamo questa cifra sull'intero volume analizzato, stiamo subendo **un aumento reale dei costi di € {incidenza_media_spedizione:.2f} per ogni singola spedizione** di questa fattura. Intervenire e formare chi imballa i colli significa trasformare questa perdita in puro margine recuperato!")
                    
                    st.markdown("### 🔎 Dettaglio Spedizioni a Rischio (+1,50€ stimati)")
                    
                    # Preparo tabella display
                    df_scc_display = df_rischio[[COL_SPEDIZIONE, 'Peso_Spec', 'Peso_Fatt', 'Delta_Peso_Perc', 'UM', 'Totale_Spedizione']].copy()
                    df_scc_display['Penale Stimata'] = 1.50
                    df_scc_display['Nuovo Costo Stimato'] = df_scc_display['Totale_Spedizione'] + 1.50
                    
                    df_scc_display = df_scc_display.rename(columns={
                        'Peso_Spec': 'Peso Dichiarato', 
                        'Peso_Fatt': 'Peso Fatturato UPS', 
                        'Totale_Spedizione': 'Spesa Attuale'
                    })
                    
                    st.dataframe(
                        df_scc_display.style.format({
                            'Peso Dichiarato': "{:.2f}",
                            'Peso Fatturato UPS': "{:.2f}",
                            'Delta_Peso_Perc': "+{:.1f}%",
                            'Spesa Attuale': "€ {:.2f}",
                            'Penale Stimata': "+€ {:.2f}",
                            'Nuovo Costo Stimato': "€ {:.2f}"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.success("🎉 Nessuna spedizione a rischio Correction Fee rilevata in questa fattura. I pesi dichiarati sono in linea con quelli rilevati da UPS.")

            # ==============================
            # SEZIONE 4: TABELLA RIEPILOGATIVA ELEGANTE
            # ==============================
            st.markdown("---")
            st.header("📊 Spedizioni con supplemento")
            
            colonne_display = [COL_SPEDIZIONE, "Stato", "Pacchi_Display", "Peso_Fatt", "UM", "Totale_Spedizione", "Nolo", "Fuel", "Tax", "Supplementi"]
            
            # Mostriamo solo le spedizioni che hanno un alert di supplemento
            df_display = grouped[grouped["Stato"] == "⚠️ Alert"][colonne_display].sort_values("Totale_Spedizione", ascending=False)
            df_display = df_display.rename(columns={"Pacchi_Display": "Pacchi"})
            
            if not df_display.empty:
                st.dataframe(
                    df_display.style.format({
                        "Totale_Spedizione": "€ {:.2f}",
                        "Nolo": "€ {:.2f}",
                        "Fuel": "€ {:.2f}",
                        "Tax": "€ {:.2f}",
                        "Supplementi": "€ {:.2f}",
                        "Peso_Fatt": "{:.2f}"
                    }).apply(lambda x: ['background-color: #5c2020; color: white;' if x['Stato'] == '⚠️ Alert' else '' for _ in x], axis=1),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.success("🎉 Nessuna spedizione con supplemento anomalo trovata.")

            # ==============================
            # SEZIONE 5: DETTAGLIO TRACKING
            # ==============================
            st.markdown("---")
            st.header("🔎 Dettaglio Singolo Tracking")
            
            col_search, col_select = st.columns(2)
            with col_search:
                ricerca_tracking = st.text_input("🔍 Filtra Tracking (es. ultime cifre):", "", help="Scrivi parte del numero di tracking per trovare subito la spedizione che cerchi.")
            
            opzioni_tracking = grouped[COL_SPEDIZIONE].tolist()
            if ricerca_tracking.strip():
                opzioni_tracking = [t for t in opzioni_tracking if ricerca_tracking.strip().upper() in str(t).upper()]
                
            with col_select:
                if opzioni_tracking:
                    spedizione_selezionata = st.selectbox(
                        "Seleziona il tracking filtrato:",
                        opzioni_tracking
                    )
                else:
                    st.selectbox("Seleziona il tracking filtrato:", ["Nessun risultato trovato"])
                    spedizione_selezionata = None
            
            if spedizione_selezionata:
                dettaglio = df[df[COL_SPEDIZIONE] == spedizione_selezionata]
                
                info_trk = info_spedizione[info_spedizione[COL_SPEDIZIONE] == spedizione_selezionata].iloc[0]
                pacchi_str = format_pacchi(info_trk['Pacchi'])
                st.info(f"**📦 Pacchi Fatturati:** {pacchi_str} | **⚖️ Peso Fatturato:** {info_trk['Peso_Fatt']} {info_trk['UM']} | **⚖️ Peso Dichiarato:** {info_trk['Peso_Spec']} {info_trk['UM']}")
    
                def highlight_alerts_dettaglio(row):
                    if row['Alert_Final']:
                        return ['background-color: #5c2020; color: white;'] * len(row)
                    return [''] * len(row)
    
                colonne_dettaglio = [COL_DESCRIZIONE, COL_CLASSIFICAZIONE, 'Categoria_Costo', COL_IMPORTO, 'Alert_Final']
                
                st.dataframe(
                    dettaglio[colonne_dettaglio].style.apply(highlight_alerts_dettaglio, axis=1).format({COL_IMPORTO: "€ {:.2f}"}),
                    use_container_width=True,
                    hide_index=True,
                    column_config={"Alert_Final": None}
                )
            else:
                st.warning("Nessun tracking trovato con i criteri di ricerca inseriti.")

        else:
            st.error(f"⚠️ Mappatura fallita. Non trovo: {', '.join(colonne_mancanti)}")

    except Exception as e:
        st.error(f"Si è verificato un errore: {e}")

else:
    st.info("👈 Carica la fattura dalla barra laterale per iniziare.")

# ==============================
# DISCLAIMER LEGALE E FIRMA DIGITALE INVISIBILE
# ==============================
st.markdown("---")
st.markdown("""
<!-- DIGITAL_SIGNATURE_HASH: 9a7b-42c1-MEDION-AUTH-2026-UPS-ANALYZER-ORIGINAL -->
<!-- PROPERTY_OF: The original author of this script. Unauthorized copying is prohibited. -->
<div style='font-size: 0.85em; color: var(--text-color); text-align: justify; padding: 12px; border: 1px solid var(--border-color); border-radius: 5px; background-color: var(--secondary-background-color); opacity: 0.8;'>
    <strong>Disclaimer – Authorized Use, Liability Limitation, and Non‑Affiliation Notice</strong><br><br>
    This invoice‑analysis program has been designed, developed, and distributed solely by the author for informational and educational purposes. 
    The software is not an official UPS tool and has not been reviewed, approved, endorsed, or validated by UPS or any of its affiliated companies.<br><br>
    All outputs, analyses, and results generated by the program are non‑official, non‑binding, and must not be considered a substitute for UPS systems, documentation, or formal communications. UPS assumes no responsibility for the accuracy, completeness, or use of the information produced by this program.<br><br>
    <strong>Authorized Use Only</strong><br>
    Use of this program is strictly limited to companies and entities that have been explicitly authorized by the author. 
    Any use, access, reproduction, distribution, modification, or disclosure of the program—whether in whole or in part—by unauthorized companies or individuals is expressly prohibited.<br><br>
    Unauthorized use may result in civil liability and, where applicable, criminal consequences.<br><br>
    <strong>Responsibility</strong><br>
    The author remains the sole party responsible for the program’s content, functionality, and any consequences arising from its use. 
    No liability of any kind may be attributed to UPS.
</div>
""", unsafe_allow_html=True)
