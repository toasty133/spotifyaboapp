import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

STATUS_FILE = "status.json"

# JSON laden
def lade_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

# JSON speichern
def speichere_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)

st.title("👥 Abo-Kosten-Manager mit Verlauf")

status = lade_status()

# Session State initialisieren
if "teilnehmer_input" not in st.session_state:
    st.session_state.teilnehmer_input = "Thushanth, Yannik, Paul, Ines, Mona, Benedikt"
if "abo_name" not in st.session_state:
    st.session_state.abo_name = "Spotify"
if "abo_kosten" not in st.session_state:
    st.session_state.abo_kosten = 18.00
if "beteiligte" not in st.session_state:
    st.session_state.beteiligte = []
if "berechnet" not in st.session_state:
    st.session_state.berechnet = False

# Abschnitt: Teilnehmer
st.header("1. Teilnehmer hinzufügen")
teilnehmer = st.text_input("Teilnehmer (getrennt mit Kommas)", st.session_state.teilnehmer_input)
st.session_state.teilnehmer_input = teilnehmer
teilnehmer_liste = [t.strip() for t in teilnehmer.split(",") if t.strip()]

# Abschnitt: Abo & Zeitraum
st.header("2. Abo & Zeitraum")
abo_name = st.text_input("Name des Abos", st.session_state.abo_name)
st.session_state.abo_name = abo_name

abo_kosten = st.number_input("Gesamtkosten (€)", min_value=0.0, step=0.01, value=st.session_state.abo_kosten)
st.session_state.abo_kosten = abo_kosten

# Monat auswählen
heute = datetime.today()
monate = [f"{heute.year}-{str(m).zfill(2)}" for m in range(1, 13)]
aktueller_monat = f"{heute.year}-{str(heute.month).zfill(2)}"
monat = st.selectbox("Zeitraum (Monat)", monate, index=heute.month - 1)

# Beteiligte
beteiligte = st.multiselect("Wer ist beteiligt?", teilnehmer_liste, default=st.session_state.beteiligte)
st.session_state.beteiligte = beteiligte

# Initialisiere Statusstruktur
if abo_name not in status:
    status[abo_name] = {}
if monat not in status[abo_name]:
    status[abo_name][monat] = {}

for person in beteiligte:
    if person not in status[abo_name][monat]:
        status[abo_name][monat][person] = False

# Berechnung
if st.button("Berechne Anteile"):
    st.session_state.berechnet = True

# Anzeige & Zahlungsbuttons
if st.session_state.berechnet and beteiligte:
    anteil = abo_kosten / len(beteiligte)
    st.subheader(f"💰 Aufteilung für {abo_name} ({monat})")

    for person in beteiligte:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"- **{person}** zahlt **{anteil:.2f} €**")
        with col2:
            if status[abo_name][monat][person]:
                if st.button(f"✅ Bezahlt ({person})"):
                    status[abo_name][monat][person] = False
                    speichere_status(status)
                    st.rerun()
            else:
                if st.button(f"❌ Offen ({person})"):
                    status[abo_name][monat][person] = True
                    speichere_status(status)
                    st.rerun()

# Abschnitt: Verlauf als Tabelle
st.markdown("---")
st.subheader("📊 Verlauf als Tabelle")

for abo in status:
    st.markdown(f"### 📦 {abo}")

    # Alle Monate & Teilnehmer einsammeln
    monate = sorted(status[abo].keys())
    alle_personen = set()
    for eintraege in status[abo].values():
        alle_personen.update(eintraege.keys())
    alle_personen = sorted(alle_personen)

    # Tabelle aufbauen
    data = []
    for monat in monate:
        zeile = {"Monat": monat}
        for person in alle_personen:
            bezahlt = status[abo][monat].get(person, False)
            zeile[person] = "✅" if bezahlt else "❌"
        data.append(zeile)

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
