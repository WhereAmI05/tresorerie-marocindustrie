import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Trésorerie - MarocIndustrie", layout="wide")

# ---------------- STYLE LIGHT ----------------
st.markdown("""
    <style>
        body {background-color: #ffffff;}
        .stMetric {border: 1px solid #eee; padding: 10px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df_flux = pd.read_csv("transactions.csv")
    df_ech = pd.read_csv("echeances.csv")

    df_flux["Date"] = pd.to_datetime(df_flux["Date"])
    df_ech["Date"] = pd.to_datetime(df_ech["Date"])

    return df_flux, df_ech

df_flux, df_ech = load_data()

# ---------------- CALCUL SOLDE ----------------
df_flux = df_flux.sort_values("Date")

df_flux["Montant signé"] = df_flux.apply(
    lambda x: x["Montant"] if x["Type"] == "Entrée" else -x["Montant"], axis=1
)

df_flux["Solde cumulé"] = df_flux["Montant signé"].cumsum()

solde_actuel = df_flux["Solde cumulé"].iloc[-1]

SEUIL = 50000

# ---------------- NAVIGATION ----------------
menu = st.sidebar.radio("Navigation", ["Dashboard", "Flux", "Échéancier", "Prévision"])

# =========================================================
# DASHBOARD
# =========================================================
if menu == "Dashboard":
    st.title("Dashboard de Trésorerie")

    col1, col2 = st.columns(2)
    col1.metric("Solde actuel (MAD)", f"{solde_actuel:,.0f}")
    col2.metric("Seuil d'alerte", f"{SEUIL:,.0f}")

    if solde_actuel < SEUIL:
        st.error("Alerte : trésorerie faible")

    fig = px.line(df_flux, x="Date", y="Solde cumulé", title="Évolution du solde")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FLUX
# =========================================================
elif menu == "Flux":
    st.title("Gestion des Flux")

    st.subheader("Ajouter un flux")

    with st.form("form_flux"):
        date = st.date_input("Date")
        type_flux = st.selectbox("Type", ["Entrée", "Sortie"])
        categorie = st.text_input("Catégorie")
        description = st.text_input("Description")
        montant = st.number_input("Montant", min_value=0.0)

        submit = st.form_submit_button("Ajouter")

        if submit:
            new_row = pd.DataFrame([{
                "Date": date,
                "Type": type_flux,
                "Catégorie": categorie,
                "Description": description,
                "Montant": montant
            }])

            df_flux_updated = pd.concat([df_flux, new_row], ignore_index=True)
            df_flux_updated.to_csv("transactions.csv", index=False)
            st.success("Flux ajouté avec succès")

    st.subheader("Historique des flux")

    df_display = df_flux.copy()

    st.dataframe(df_display)

# =========================================================
# ÉCHÉANCIER
# =========================================================
elif menu == "Échéancier":
    st.title("Échéancier")

    st.subheader("Ajouter une échéance")

    with st.form("form_ech"):
        date = st.date_input("Date échéance")
        type_ech = st.selectbox("Type", ["Encaissement", "Décaissement"])
        description = st.text_input("Description")
        montant = st.number_input("Montant", min_value=0.0)

        submit = st.form_submit_button("Ajouter")

        if submit:
            new_row = pd.DataFrame([{
                "Date": date,
                "Type": type_ech,
                "Description": description,
                "Montant": montant
            }])

            df_ech_updated = pd.concat([df_ech, new_row], ignore_index=True)
            df_ech_updated.to_csv("echeances.csv", index=False)
            st.success("Échéance ajoutée")

    st.subheader("Tableau des échéances")

    st.dataframe(df_ech)

# =========================================================
# PRÉVISION
# =========================================================
elif menu == "Prévision":
    st.title("Prévision de trésorerie (8 semaines)")

    df_prev = df_ech.copy()
    df_prev = df_prev.sort_values("Date")

    df_prev["Montant signé"] = df_prev.apply(
        lambda x: x["Montant"] if x["Type"] == "Encaissement" else -x["Montant"], axis=1
    )

    df_prev["Solde prévisionnel"] = solde_actuel + df_prev["Montant signé"].cumsum()

    fig = px.line(df_prev, x="Date", y="Solde prévisionnel", title="Prévision de trésorerie")
    st.plotly_chart(fig, use_container_width=True)

    if df_prev["Solde prévisionnel"].min() < SEUIL:
        st.error("Risque de tension de trésorerie détecté")