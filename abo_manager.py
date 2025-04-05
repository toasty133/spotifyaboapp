import streamlit as st

st.title("👥 Abo-Kosten-Manager für Gruppen")

# Teilnehmerliste
st.header("1. Teilnehmer hinzufügen")
teilnehmer = st.text_input("Gib die Namen der Teilnehmer ein (getrennt mit Kommas)", "Anna, Ben, Chris")
teilnehmer_liste = [t.strip() for t in teilnehmer.split(",") if t.strip()]

# Abo-Eingabe
st.header("2. Abo hinzufügen")
abo_name = st.text_input("Name des Abos", "Netflix")
abo_kosten = st.number_input("Gesamtkosten (€)", min_value=0.0, step=0.01)
beteiligte = st.multiselect("Wer ist beteiligt?", teilnehmer_liste, default=teilnehmer_liste)

# Berechnung
if st.button("Berechne Anteile"):
    if not beteiligte:
        st.warning("Bitte wähle mindestens eine Person aus.")
    else:
        anteil = abo_kosten / len(beteiligte)
        st.subheader(f"💰 Aufteilung für {abo_name}")
        for person in beteiligte:
            st.write(f"- **{person}** zahlt **{anteil:.2f} €**")
