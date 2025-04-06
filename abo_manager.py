import streamlit as st
import json
import os
from datetime import datetime

STATUS_FILE = "status.json"

# JSON-Datei laden
def lade_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

# JSON-Datei speichern
def speichere_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)

st.title("👥 Abo-Kosten-Manager mit Verlauf")

status = lade_status()

# Session State
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

# Teilnehmer-Eingabe
st.header("1. Teilnehmer hinzufügen")
teilnehmer = st.text_input("Teilnehmer (getrennt mit Kommas)", st.session_state.teilnehmer_input)
st.session_state.teilnehmer_input = teilnehmer
teilnehmer_liste = [t.strip() for t in teilnehmer.split(",") if t.strip()]

# Abo-Eingabe
st.header("2. Abo & Zeitraum")
abo_name = st.text_input("Name des Abos", st.session_state.abo_name)
st.session_state.abo_name = abo_name

abo_kosten = st.number_input("Gesamtkosten (€)", min_value=0.0, step=0.01, value=st.session_state.abo_kosten)
st.session_state.abo_kosten = abo_kosten

# Monat als Dropdown
heute = datetime.today()
monate = [f"{heute.year}-{str(m).zfill(2)}" for m in range(1, 13)]
aktueller_monat = f"{heute.year}-{str(heute.month).zfill(2)}"
monat = st.selectbox("Zeitraum (Monat)", monate, index=heute.month - 1)

# Beteiligte auswählen
beteiligte = st.multiselect("Wer ist beteiligt?", teilnehmer_liste, default=st.session_state.beteiligte)
st.session_state.beteiligte = beteiligte

# Initialisiere Status
if abo_name not in status:
    status[abo_name] = {}
if monat not in status[abo_name]:
    status[abo_name][monat] = {}

for person in beteiligte:
    if person not in status[abo_name][monat]:
        status[abo_name][monat][person] = False

# Anteile berechnen
if st.button("Berechne Anteile"):
    st.session_state.berechnet = True

# Anzeige & Buttons
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

# Verlauf (optional unten)
st.markdown("---")
st.subheader("📜 Verlauf anzeigen")

for abo in status:
    st.markdown(f"### 📦 {abo}")
    for monat_eintrag in status[abo]:
        st.markdown(f"**🗓 {monat_eintrag}**")
        eintraege = status[abo][monat_eintrag]
        for person, bezahlt in eintraege.items():
            icon = "✅" if bezahlt else "❌"
            st.write(f"- {person}: {icon}")
