import streamlit as st
import json
import os

STATUS_FILE = "status.json"

def lade_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def speichere_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)

st.title("👥 Abo-Kosten-Manager für Gruppen")

# Lade gespeicherten Status
status = lade_status()

# Teilnehmerliste
st.header("1. Teilnehmer hinzufügen")
teilnehmer = st.text_input("Gib die Namen der Teilnehmer ein (getrennt mit Kommas)", "Anna, Ben, Chris")
teilnehmer_liste = [t.strip() for t in teilnehmer.split(",") if t.strip()]

# Abo-Eingabe
st.header("2. Abo hinzufügen")
abo_name = st.text_input("Name des Abos", "Netflix")
abo_kosten = st.number_input("Gesamtkosten (€)", min_value=0.0, step=0.01)
beteiligte = st.multiselect("Wer ist beteiligt?", teilnehmer_liste, default=teilnehmer_liste)

# Init Status-Einträge, wenn nicht vorhanden
for person in beteiligte:
    if person not in status:
        status[person] = False

# Berechnung & Anzeige
if st.button("Berechne Anteile"):
    if not beteiligte:
        st.warning("Bitte wähle mindestens eine Person aus.")
    else:
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
                        st.experimental_rerun()
                else:
                    if st.button(f"❌ Offen ({person})"):
                        status[person] = True
                        speichere_status(status)
                        st.experimental_rerun()
