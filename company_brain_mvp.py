import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
import openai
import os
import tempfile
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from dotenv import load_dotenv
from pathlib import Path


# Titel
st.title("Company Brain – Erweiterter MVP")
st.subheader("Nutze CSV-Daten, Knowledge Graphs und LLM-Unterstützung zur Entscheidungsfindung")

# API-Key sicher laden (entweder als Umgebungsvariable oder per secrets)
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# CSV-Datei hochladen
st.sidebar.header("Lade Unternehmensdaten hoch (CSV)")
uploaded_file = st.sidebar.file_uploader("CSV-Datei auswählen", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown("### Vorschau der Daten")
    st.dataframe(df.head())

    # Extrahiere Spaltennamen als Entitäten
    entities = list(df.columns[:4])  # z. B. erste 4 Spalten als Beispiel-Entitäten

    # Beispielhafte Rückkopplungsgewichte (hier zufällig / vereinfachte Heuristik)
    weight_matrix = {
        (entities[0], entities[1]): +15,
        (entities[0], entities[2]): -10,
        (entities[0], entities[3]): +5,
    }

    # Knowledge Graph erstellen
    G = nx.DiGraph()
    for (src, tgt), weight in weight_matrix.items():
        G.add_edge(src, tgt, weight=weight)

    # Visualisierung
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 5))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightgreen', font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:+.1f}%" for k, v in labels.items()})
    st.pyplot(plt)

    # Tabelle mit simulierten Änderungen anzeigen
    st.markdown("### Simulierte Auswirkungen (heuristisch)")
    summary_df = pd.DataFrame({
        "Faktor": [tgt for (_, tgt) in weight_matrix],
        "Veränderung in %": [v for v in weight_matrix.values()]
    })
    st.table(summary_df)

    # LLM Feedback – Echtzeit mit OpenAI
    st.markdown("### KI-Feedback zur Entscheidung (GPT-4)")
    user_prompt = f"Gegeben sind folgende Rückkopplungen im Unternehmen: {weight_matrix}. Was sind mögliche Risiken und Empfehlungen für nachhaltige Entscheidungen?"
    st.code(user_prompt, language='markdown')

    if openai.api_key:
        with st.spinner("Generiere Antwort von GPT-4..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Du bist ein Unternehmensberater mit Fokus auf systemisches Denken und nachhaltige Geschäftsstrategien."},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                gpt_output = response.choices[0].message.content
                st.success(gpt_output)
            except Exception as e:
                st.error(f"Fehler bei OpenAI-Abfrage: {e}")
    else:
        st.warning("Kein OpenAI API-Key gefunden. Bitte setze `OPENAI_API_KEY` als Umgebungsvariable oder nutze Streamlit Secrets.")
else:
    st.warning("Bitte lade eine CSV-Datei mit Unternehmensdaten hoch, um den Prototypen zu starten.")
