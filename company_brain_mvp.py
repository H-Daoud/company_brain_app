import os
import tempfile
import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from dotenv import load_dotenv
from pathlib import Path

# --- Load .env if it exists (for local use or streamlit secrets) ---
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"⚠️ No .env file found at {dotenv_path}. Relying on Streamlit secrets...")

# --- Load credentials: .env (local) or st.secrets (cloud) ---
form_endpoint   = os.getenv("form_endpoint")     or st.secrets.get("form_endpoint")
form_key        = os.getenv("form_key")          or st.secrets.get("form_key")
openai_key      = os.getenv("openai_key")        or st.secrets.get("openai_key")
openai_endpoint = os.getenv("openai_endpoint")   or st.secrets.get("openai_endpoint")
openai_version  = os.getenv("openai_version")    or st.secrets.get("openai_version")
deployment_name = os.getenv("deployment_name")   or st.secrets.get("deployment_name")

# --- Streamlit UI setup ---
st.set_page_config(page_title="Entscheidungsanalyse", layout="wide")
st.title("🧐 Company Brain\nEntscheidungsfeedback anhand der Unternehmensdatenbank")

# --- File upload field ---
uploaded_file = st.file_uploader(
    "Lade relevante Unternehmensdokumente hoch (z.\u202fB. langfristige Unternehmensstrategie, KPI-Berichte, Vision, ROI-Konzepte oder andere entscheidungsrelevante Unterlagen)",
    type=["pdf", "png", "jpg", "jpeg"]
)

# --- Free-text field for stakeholder question ---
stakeholder_input = st.text_area(
    label=" ",
    placeholder=(
        "z. B. Wie wirkt sich die Zusammenlegung von Vertrieb und Marketing auf unsere KPIs und das Jahresziel aus?\n"
        "Welche Risiken und Chancen ergeben sich durch den geplanten Personalabbau im Bereich X Abteilung?\n"
        "Sollte das Projekt Alpha priorisiert oder zurückgestellt werden – was empfiehlt das System?\n"
        "Ist die Investition in eine neue Produktionslinie im Einklang mit unserer aktuellen Strategie?\n"
    )
)

# --- Button to start analysis ---
analyse_button = st.button("🔍 Analyse starten")

if uploaded_file and stakeholder_input.strip() and analyse_button:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.info("🔍 Extrahiere Inhalte aus den Dokumenten...")
    try:
        ocr_client = DocumentAnalysisClient(
            endpoint=form_endpoint,
            credential=AzureKeyCredential(form_key)
        )

        with open(tmp_path, "rb") as f:
            poller = ocr_client.begin_analyze_document("prebuilt-document", f)
            result = poller.result()

        document_text = "\n".join(
            line.content for page in result.pages for line in page.lines
        )

        st.success("✅ Text erfolgreich extrahiert.")
        st.subheader("📄 Extrahierter Inhalt:")
        st.text_area("Dokumentinhalt", document_text, height=300)

        # --- Display stakeholder question in its own section ---
        st.markdown("---")
        st.subheader("❓ Stakeholder-Frage")
        st.info(stakeholder_input)

        st.subheader("🤖 KI-gestütztes Entscheidungsfeedback")

        with st.spinner("Analysiere unter Berücksichtigung strategischer Unternehmenskontexte..."):
            prompt = f"""
Du bist ein CEO, CFO, CTO und COO in einem hochentwickelten KI-System. Deine Expertise umfasst:
- Geschäftsstrategie und Management (inkl. Vision, ROI, KPIs)
- Projektmanagement (PMP)
- Prozessoptimierung (Six Sigma)
- Systemdenken und unternehmensweite Architektur

Du analysierst jetzt ein oder mehrere hochgeladene Dokumente im Kontext:
- Abteilungsdaten
- Langfriststrategien & Visionen
- Finanzkennzahlen & KPIs
- Konzepte & Initiativen

Hier ist der extrahierte Dokumentinhalt:
\"\"\"
{document_text}
\"\"\"

Stakeholder-Frage:
\"\"\"
{stakeholder_input}
\"\"\"

Bitte beantworte:
1. Welche relevanten Entitäten, Beziehungen und Einflussfaktoren lassen sich identifizieren?
2. Wie hängen diese mit bestehenden Unternehmenszielen, KPIs und ROI zusammen?
3. Wo entstehen mögliche Zielkonflikte, Abweichungen oder Synergien?
4. Wie lässt sich dieses Dokument systemisch in ein semantisches Entscheidungsmodell (z. B. Knowledge Graph) integrieren?
5. Was ist deine Antwort auf die Stakeholder-Anfrage – unter Berücksichtigung von Governance, Ethik, rechtlichen Rahmenbedingungen und Strategie?
"""

            llm_client = AzureOpenAI(
                api_key=openai_key,
                api_version=openai_version,
                azure_endpoint=openai_endpoint,
            )

            response = llm_client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "system", "content": "Du bist ein KI-gestütztes Executive Team für strategische Entscheidungsunterstützung auf Unternehmensebene mit Fokus auf Systemarchitektur, Governance, KPIs, ROI und ethisch-strategische Bewertung."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            output = response.choices[0].message.content
            st.markdown("---")
            st.subheader("💡 Systemisches Entscheidungsfeedback")
            st.success(output)

    except Exception as e:
        st.error(f"❌ Fehler bei der Analyse: {e}")

elif uploaded_file and not analyse_button:
    st.info("Bitte gib deine Stakeholder-Frage ein und klicke dann auf „Analyse starten“.")

# --- (Remove duplicate code below this line!) ---
