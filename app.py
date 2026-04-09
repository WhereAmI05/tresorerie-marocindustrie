import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

st.set_page_config(
    page_title="MarocIndustrie - Gestion de Trésorerie",
    page_icon="🏭",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 28px;
        font-weight: 700;
        color: #1a3a5c;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 14px;
        color: #6c757d;
        margin-bottom: 20px;
    }
    .alert-red {
        background-color: #ffe0e0;
        border-left: 5px solid #e53935;
        padding: 12px 16px;
        border-radius: 4px;
        color: #b71c1c;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .alert-orange {
        background-color: #fff3e0;
        border-left: 5px solid #fb8c00;
        padding: 12px 16px;
        border-radius: 4px;
        color: #e65100;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .alert-green {
        background-color: #e8f5e9;
        border-left: 5px solid #43a047;
        padding: 12px 16px;
        border-radius: 4px;
        color: #1b5e20;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 13px;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

SEUIL_ALERTE = 50000
SEUIL_GROSSE_ECHEANCE = 30000

@st.cache_data
def load_data():
    transactions = pd.read_csv("transactions.csv", parse_dates=["date"])
    echeances = pd.read_csv("echeances.csv", parse_dates=["date_echeance"])
    return transactions, echeances

def save_transactions(df):
    df.to_csv("transactions.csv", index=False)

def save_echeances(df):
    df.to_csv("echeances.csv", index=False)

transactions, echeances = load_data()

if "transactions" not in st.session_state:
    st.session_state.transactions = transactions.copy()
if "echeances" not in st.session_state:
    st.session_state.echeances = echeances.copy()

st.markdown('<div class="main-header">🏭 MarocIndustrie SARL — Gestion de Trésorerie</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tableau de bord financier | Ain Sebaa, Casablanca</div>', unsafe_allow_html=True)

tabs = st.tabs(["📊 Dashboard", "💸 Flux", "📅 Échéancier", "📈 Prévision"])

# ─────────────────────────────────────────────────────────
# TAB 1 — DASHBOARD
# ─────────────────────────────────────────────────────────
with tabs[0]:
    df = st.session_state.transactions
    solde_actuel = df["solde_cumule"].iloc[-1]
    total_entrees = df[df["type"] == "entree"]["montant"].sum()
    total_sorties = df[df["type"] == "sortie"]["montant"].sum()
    nb_retards = len(st.session_state.echeances[st.session_state.echeances["statut"] == "en_retard"])

    # Alertes
    if solde_actuel < SEUIL_ALERTE:
        st.markdown(f'<div class="alert-red">🚨 ALERTE : Solde critique ! {solde_actuel:,.0f} MAD — en dessous du seuil de {SEUIL_ALERTE:,} MAD</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-green">✅ Trésorerie saine : {solde_actuel:,.0f} MAD — au-dessus du seuil d\'alerte</div>', unsafe_allow_html=True)

    if nb_retards > 0:
        st.markdown(f'<div class="alert-orange">⚠️ {nb_retards} paiement(s) client en retard — impact immédiat sur la trésorerie</div>', unsafe_allow_html=True)

    # Métriques
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Solde Actuel", f"{solde_actuel:,.0f} MAD")
    c2.metric("📥 Total Entrées", f"{total_entrees:,.0f} MAD")
    c3.metric("📤 Total Sorties", f"{total_sorties:,.0f} MAD")
    c4.metric("⚠️ Retards Clients", f"{nb_retards} facture(s)")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Évolution du solde de trésorerie")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df["date"], y=df["solde_cumule"],
            mode="lines+markers",
            line=dict(color="#1a3a5c", width=2),
            marker=dict(size=4),
            fill="tozeroy",
            fillcolor="rgba(26,58,92,0.1)",
            name="Solde"
        ))
        fig1.add_hline(y=SEUIL_ALERTE, line_dash="dash", line_color="red",
                       annotation_text=f"Seuil alerte ({SEUIL_ALERTE:,} MAD)", annotation_position="top left")
        fig1.update_layout(
            xaxis_title="Date", yaxis_title="Solde (MAD)",
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Répartition des sorties par catégorie")
        sorties = df[df["type"] == "sortie"].groupby("categorie")["montant"].sum().reset_index()
        sorties.columns = ["Catégorie", "Montant"]
        sorties["Catégorie"] = sorties["Catégorie"].str.replace("_", " ").str.title()
        fig2 = px.pie(sorties, values="Montant", names="Catégorie",
                      color_discrete_sequence=px.colors.sequential.Blues_r,
                      hole=0.35)
        fig2.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Entrées vs Sorties par mois")
    df["mois"] = df["date"].dt.to_period("M").astype(str)
    monthly = df.groupby(["mois", "type"])["montant"].sum().reset_index()
    fig3 = px.bar(monthly, x="mois", y="montant", color="type",
                  barmode="group",
                  color_discrete_map={"entree": "#2e7d32", "sortie": "#c62828"},
                  labels={"montant": "Montant (MAD)", "mois": "Mois", "type": "Type"})
    fig3.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10),
                       plot_bgcolor="white", paper_bgcolor="white",
                       yaxis=dict(gridcolor="#f0f0f0"))
    st.plotly_chart(fig3, use_container_width=True)


# ─────────────────────────────────────────────────────────
# TAB 2 — FLUX
# ─────────────────────────────────────────────────────────
with tabs[1]:
    st.subheader("Historique des flux de trésorerie")

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        filtre_type = st.selectbox("Filtrer par type", ["Tous", "entree", "sortie"])
    with col_f2:
        filtre_cat = st.selectbox("Filtrer par catégorie",
            ["Toutes"] + sorted(st.session_state.transactions["categorie"].unique().tolist()))

    df_flux = st.session_state.transactions.copy()
    if filtre_type != "Tous":
        df_flux = df_flux[df_flux["type"] == filtre_type]
    if filtre_cat != "Toutes":
        df_flux = df_flux[df_flux["categorie"] == filtre_cat]

    df_flux_display = df_flux.copy()
    df_flux_display["date"] = df_flux_display["date"].dt.strftime("%d/%m/%Y")
    df_flux_display["montant"] = df_flux_display["montant"].apply(lambda x: f"{x:,.0f} MAD")
    df_flux_display["solde_cumule"] = df_flux_display["solde_cumule"].apply(lambda x: f"{x:,.0f} MAD")
    df_flux_display.columns = ["Date", "Type", "Catégorie", "Description", "Montant", "Solde cumulé"]

    st.dataframe(df_flux_display, use_container_width=True, height=350)

    st.markdown("---")
    st.subheader("➕ Ajouter un nouveau flux")

    with st.form("form_flux"):
        fc1, fc2 = st.columns(2)
        with fc1:
            f_date = st.date_input("Date", value=datetime.today())
            f_type = st.selectbox("Type", ["entree", "sortie"])
            f_montant = st.number_input("Montant (MAD)", min_value=0, step=500)
        with fc2:
            f_categorie = st.selectbox("Catégorie", [
                "vente_client", "acompte", "salaires", "loyer", "matieres_premieres",
                "electricite", "cnss", "tva", "maintenance", "frais_generaux"
            ])
            f_description = st.text_input("Description")

        submit_flux = st.form_submit_button("✅ Ajouter le flux")
        if submit_flux and f_montant > 0 and f_description:
            dernier_solde = st.session_state.transactions["solde_cumule"].iloc[-1]
            if f_type == "entree":
                nouveau_solde = dernier_solde + f_montant
            else:
                nouveau_solde = dernier_solde - f_montant

            nouvelle_ligne = pd.DataFrame([{
                "date": pd.to_datetime(f_date),
                "type": f_type,
                "categorie": f_categorie,
                "description": f_description,
                "montant": f_montant,
                "solde_cumule": nouveau_solde
            }])
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, nouvelle_ligne], ignore_index=True)
            save_transactions(st.session_state.transactions)
            st.success(f"✅ Flux ajouté ! Nouveau solde : {nouveau_solde:,.0f} MAD")
            st.cache_data.clear()
            st.rerun()


# ─────────────────────────────────────────────────────────
# TAB 3 — ÉCHÉANCIER
# ─────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("Échéancier des 8 prochaines semaines")

    ech = st.session_state.echeances.copy()
    today = pd.Timestamp(datetime.today().date())

    # Alertes retards
    retards = ech[ech["statut"] == "en_retard"]
    if not retards.empty:
        for _, row in retards.iterrows():
            st.markdown(f'<div class="alert-orange">⚠️ RETARD : {row["tiers"]} — {row["description"]} — {row["montant"]:,.0f} MAD</div>', unsafe_allow_html=True)

    # Alertes grosses échéances à venir (7 jours)
    prochaines = ech[(ech["date_echeance"] <= today + timedelta(days=7)) &
                     (ech["statut"] == "en_attente") &
                     (ech["montant"] >= SEUIL_GROSSE_ECHEANCE)]
    if not prochaines.empty:
        for _, row in prochaines.iterrows():
            st.markdown(f'<div class="alert-orange">🔔 ÉCHÉANCE PROCHE : {row["tiers"]} — {row["montant"]:,.0f} MAD — le {row["date_echeance"].strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)

    ec1, ec2 = st.columns(2)
    with ec1:
        filtre_ech = st.selectbox("Filtrer par type", ["Tous", "a_encaisser", "a_payer"])
    with ec2:
        filtre_stat = st.selectbox("Filtrer par statut", ["Tous", "en_attente", "en_retard"])

    ech_display = ech.copy()
    if filtre_ech != "Tous":
        ech_display = ech_display[ech_display["type"] == filtre_ech]
    if filtre_stat != "Tous":
        ech_display = ech_display[ech_display["statut"] == filtre_stat]

    ech_display["date_echeance"] = ech_display["date_echeance"].dt.strftime("%d/%m/%Y")
    ech_display["montant"] = ech_display["montant"].apply(lambda x: f"{x:,.0f} MAD")
    ech_display.columns = ["Date échéance", "Type", "Tiers", "Description", "Montant", "Statut"]

    st.dataframe(ech_display, use_container_width=True, height=350)

    total_a_encaisser = ech[ech["type"] == "a_encaisser"]["montant"].sum()
    total_a_payer = ech[ech["type"] == "a_payer"]["montant"].sum()
    solde_prev = total_a_encaisser - total_a_payer

    m1, m2, m3 = st.columns(3)
    m1.metric("📥 Total à encaisser", f"{total_a_encaisser:,.0f} MAD")
    m2.metric("📤 Total à payer", f"{total_a_payer:,.0f} MAD")
    m3.metric("📊 Solde prévisionnel net", f"{solde_prev:,.0f} MAD",
              delta=f"{'positif' if solde_prev >= 0 else 'négatif'}")

    st.markdown("---")
    st.subheader("➕ Ajouter une échéance")

    with st.form("form_echeance"):
        e1, e2 = st.columns(2)
        with e1:
            e_date = st.date_input("Date d'échéance", value=datetime.today() + timedelta(days=7))
            e_type = st.selectbox("Type", ["a_encaisser", "a_payer"])
            e_montant = st.number_input("Montant (MAD)", min_value=0, step=500)
        with e2:
            e_tiers = st.text_input("Tiers (client / fournisseur)")
            e_desc = st.text_input("Description")
            e_statut = st.selectbox("Statut", ["en_attente", "en_retard"])

        submit_ech = st.form_submit_button("✅ Ajouter l'échéance")
        if submit_ech and e_montant > 0 and e_tiers:
            nouvelle_ech = pd.DataFrame([{
                "date_echeance": pd.to_datetime(e_date),
                "type": e_type,
                "tiers": e_tiers,
                "description": e_desc,
                "montant": e_montant,
                "statut": e_statut
            }])
            st.session_state.echeances = pd.concat(
                [st.session_state.echeances, nouvelle_ech], ignore_index=True)
            save_echeances(st.session_state.echeances)
            st.success("✅ Échéance ajoutée avec succès !")
            st.cache_data.clear()
            st.rerun()


# ─────────────────────────────────────────────────────────
# TAB 4 — PRÉVISION
# ─────────────────────────────────────────────────────────
with tabs[3]:
    st.subheader("Prévision de trésorerie sur 8 semaines")

    ech_prev = st.session_state.echeances.copy()
    ech_prev["semaine"] = ech_prev["date_echeance"].dt.to_period("W").astype(str)

    encaissements_sem = ech_prev[ech_prev["type"] == "a_encaisser"].groupby("semaine")["montant"].sum()
    decaissements_sem = ech_prev[ech_prev["type"] == "a_payer"].groupby("semaine")["montant"].sum()

    toutes_semaines = sorted(set(encaissements_sem.index) | set(decaissements_sem.index))

    df_prev = pd.DataFrame({
        "Semaine": toutes_semaines,
        "Encaissements": [encaissements_sem.get(s, 0) for s in toutes_semaines],
        "Décaissements": [decaissements_sem.get(s, 0) for s in toutes_semaines],
    })
    df_prev["Solde net"] = df_prev["Encaissements"] - df_prev["Décaissements"]

    solde_initial = st.session_state.transactions["solde_cumule"].iloc[-1]
    df_prev["Solde cumulé prévisionnel"] = solde_initial + df_prev["Solde net"].cumsum()

    # Alerte si solde prévisionnel passe sous le seuil
    semaines_critiques = df_prev[df_prev["Solde cumulé prévisionnel"] < SEUIL_ALERTE]
    if not semaines_critiques.empty:
        st.markdown(f'<div class="alert-red">🚨 ALERTE PRÉVISION : Le solde passera sous {SEUIL_ALERTE:,} MAD durant {len(semaines_critiques)} semaine(s) !</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-green">✅ Solde prévisionnel au-dessus du seuil sur toutes les semaines</div>', unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("**Encaissements vs Décaissements par semaine**")
        df_bar = df_prev.melt(id_vars=["Semaine"], value_vars=["Encaissements", "Décaissements"],
                              var_name="Type", value_name="Montant")
        fig_bar = px.bar(df_bar, x="Semaine", y="Montant", color="Type", barmode="group",
                         color_discrete_map={"Encaissements": "#2e7d32", "Décaissements": "#c62828"})
        fig_bar.update_layout(height=320, margin=dict(l=5, r=5, t=5, b=5),
                              plot_bgcolor="white", paper_bgcolor="white",
                              yaxis=dict(gridcolor="#f0f0f0"),
                              xaxis_tickangle=-30)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_p2:
        st.markdown("**Évolution du solde prévisionnel cumulé**")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_prev["Semaine"], y=df_prev["Solde cumulé prévisionnel"],
            mode="lines+markers+text",
            line=dict(color="#1a3a5c", width=2),
            marker=dict(size=7, color="#1a3a5c"),
            text=[f"{v:,.0f}" for v in df_prev["Solde cumulé prévisionnel"]],
            textposition="top center",
            textfont=dict(size=10),
            name="Solde prévisionnel"
        ))
        fig_line.add_hline(y=SEUIL_ALERTE, line_dash="dash", line_color="red",
                           annotation_text="Seuil alerte", annotation_position="bottom right")
        fig_line.update_layout(height=320, margin=dict(l=5, r=5, t=5, b=5),
                               plot_bgcolor="white", paper_bgcolor="white",
                               yaxis=dict(gridcolor="#f0f0f0"),
                               xaxis_tickangle=-30)
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("**Tableau prévisionnel détaillé**")
    df_display = df_prev.copy()
    for col in ["Encaissements", "Décaissements", "Solde net", "Solde cumulé prévisionnel"]:
        df_display[col] = df_display[col].apply(lambda x: f"{x:,.0f} MAD")
    st.dataframe(df_display, use_container_width=True)

    st.markdown("---")
    st.markdown(f"""
    **📋 Hypothèses du modèle**
    - Solde initial (fin mars 2025) : **{solde_initial:,.0f} MAD**
    - Seuil d'alerte trésorerie : **{SEUIL_ALERTE:,} MAD**
    - Seuil grosse échéance : **{SEUIL_GROSSE_ECHEANCE:,} MAD**
    - Les prévisions sont basées sur les échéances enregistrées (à encaisser et à payer)
    - Les retards clients ne sont pas supposés être réglés dans les délais
    """)
