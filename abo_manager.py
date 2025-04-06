import streamlit as st
import json
import os

STATUS_FILE = "status.json"

# JSON lesen
def lade_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

# JSON speichern
def speichere_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)

st.title("👥 Abo-Kosten-Manager für Gruppen")

# Status laden
status = lade_status()

# Zustand merken: Teilnehmer, Abo, Beteiligte & Berechnung
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
teilnehmer = st.text_input("Gib die Namen der Teilnehmer ein (getrennt mit Kommas)", st.session_state.teilnehmer_input)
st.session_state.teilnehmer_input = teilnehmer
teilnehmer_liste = [t.strip() for t in teilnehmer.split(",") if t.strip()]

# Abschnitt: Abo
st.header("2. Abo hinzufügen")
abo_name = st.text_input("Name des Abos", st.session_state.abo_name)
st.session_state.abo_name = abo_name

abo_kosten = st.number_input("Gesamtkosten (€)", min_value=0.0, step=0.01, value=st.session_state.abo_kosten)
st.session_state.abo_kosten = abo_kosten

beteiligte = st.multiselect("Wer ist beteiligt?", teilnehmer_liste, default=st.session_state.beteiligte)
st.session_state.beteiligte = beteiligte

# Initialisiere Status-Einträge
for person in beteiligte:
    if person not in status:
        status[person] = False

# Button: Anteile berechnen
if st.button("Berechne Anteile"):
    st.session_state.berechnet = True

# Anzeige der Aufteilung, wenn Berechnung aktiviert
if st.session_state.berechnet and beteiligte:
    anteil = abo_kosten / len(beteiligte)
    st.subheader(f"💰 Aufteilung für {abo_name}")

    for person in beteiligte:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"- **{person}** zahlt **{anteil:.2f} €**")

        with col2:
            if status[person]:
                if st.button(f"✅ Bezahlt ({person})"):
                    status[person] = False
                    speichere_status(status)
                    st.rerun()
            else:
                if st.button(f"❌ Offen ({person})"):
                    status[person] = True
                    speichere_status(status)
                    st.rerun()
