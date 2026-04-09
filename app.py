import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="MarocIndustrie - Gestion de Trésorerie",
    page_icon=":factory:",
    layout="wide"
)

# ==================== STYLE CSS EPURE PROFESSIONNEL ====================
st.markdown("""
<style>
    /* Fond général */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Sidebar professionnelle */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
    
    /* Cartes métriques */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 600;
        color: #0f172a;
        margin-top: 8px;
    }
    
    .metric-label {
        font-size: 13px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Alertes professionnelles */
    .alert-critical {
        background-color: #fef2f2;
        border-left: 4px solid #dc2626;
        padding: 14px 18px;
        border-radius: 8px;
        color: #991b1b;
        font-size: 14px;
        margin-bottom: 16px;
    }
    
    .alert-warning {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 14px 18px;
        border-radius: 8px;
        color: #92400e;
        font-size: 14px;
        margin-bottom: 16px;
    }
    
    .alert-success {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 14px 18px;
        border-radius: 8px;
        color: #166534;
        font-size: 14px;
        margin-bottom: 16px;
    }
    
    /* Titres */
    .main-header {
        font-size: 24px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 4px;
        letter-spacing: -0.3px;
    }
    
    .sub-header {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 24px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 16px;
    }
    
    /* Séparateur */
    hr {
        margin: 20px 0;
        border-color: #e2e8f0;
    }
    
    /* Boutons */
    .stButton > button {
        background-color: #1e293b;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #334155;
        border: none;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stSelectbox > div > div, .stDateInput > div > div {
        border-radius: 6px;
        border-color: #e2e8f0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 32px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 14px;
        font-weight: 500;
        color: #64748b;
        padding: 8px 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1e293b;
        border-bottom: 2px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# ==================== PARAMETRES ====================
SEUIL_ALERTE = 50000
SEUIL_GROSSE_ECHEANCE = 30000

# ==================== CHARGEMENT DES DONNEES ====================
@st.cache_data
def load_transactions():
    df = pd.read_csv("transactions.csv", parse_dates=["date"])
    return df

@st.cache_data
def load_echeances():
    df = pd.read_csv("echeances.csv", parse_dates=["date_echeance"])
    return df

transactions = load_transactions()
echeances = load_echeances()

if "transactions" not in st.session_state:
    st.session_state.transactions = transactions.copy()
if "echeances" not in st.session_state:
    st.session_state.echeances = echeances.copy()

def save_transactions(df):
    df.to_csv("transactions.csv", index=False)

def save_echeances(df):
    df.to_csv("echeances.csv", index=False)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### MarocIndustrie SARL")
    st.markdown("---")
    st.markdown("**Informations**")
    st.markdown("Siège : Ain Sebaa, Casablanca")
    st.markdown("Secteur : Fabrication métallique BTP")
    st.markdown("Effectif : 12 employés")
    st.markdown("---")
    
    solde_actuel = st.session_state.transactions["solde_cumule"].iloc[-1]
    st.markdown("**Trésorerie actuelle**")
    if solde_actuel >= 80000:
        st.success(f"{solde_actuel:,.0f} MAD")
    elif solde_actuel >= 50000:
        st.warning(f"{solde_actuel:,.0f} MAD")
    else:
        st.error(f"{solde_actuel:,.0f} MAD")
    
    st.markdown("---")
    st.markdown("**Paramètres**")
    st.markdown(f"Seuil d'alerte : {SEUIL_ALERTE:,} MAD")
    st.markdown(f"Horizon prévision : 8 semaines")
    st.caption("Données : Janvier - Mars 2025")

# ==================== HEADER ====================
st.markdown('<div class="main-header">MarocIndustrie SARL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tableau de bord de gestion de trésorerie</div>', unsafe_allow_html=True)

# ==================== TABS ====================
tabs = st.tabs(["Dashboard", "Flux de trésorerie", "Echéancier", "Prévisions"])

# ==================== TAB 1: DASHBOARD ====================
with tabs[0]:
    df = st.session_state.transactions
    solde_actuel = df["solde_cumule"].iloc[-1]
    total_entrees = df[df["type"] == "entree"]["montant"].sum()
    total_sorties = df[df["type"] == "sortie"]["montant"].sum()
    
    ech = st.session_state.echeances
    nb_retards = len(ech[ech["statut"] == "en_retard"])
    montant_retards = ech[ech["statut"] == "en_retard"]["montant"].sum()
    
    # Alertes
    if solde_actuel < SEUIL_ALERTE:
        st.markdown(f'<div class="alert-critical">Alerte critique : Le solde de {solde_actuel:,.0f} MAD est inférieur au seuil de {SEUIL_ALERTE:,} MAD</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-success">Trésorerie saine : {solde_actuel:,.0f} MAD au-dessus du seuil d\'alerte</div>', unsafe_allow_html=True)
    
    if nb_retards > 0:
        st.markdown(f'<div class="alert-warning">Attention : {nb_retards} paiement(s) client en retard pour un total de {montant_retards:,.0f} MAD</div>', unsafe_allow_html=True)
    
    # Indicateurs
    st.markdown("### Indicateurs clés")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Solde actuel</div>
            <div class="metric-value">{solde_actuel:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total encaissements (3 mois)</div>
            <div class="metric-value">{total_entrees:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total décaissements (3 mois)</div>
            <div class="metric-value">{total_sorties:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Créances impayées</div>
            <div class="metric-value">{nb_retards}</div>
            <div class="metric-label">facture(s)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Evolution du solde")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df["date"], 
            y=df["solde_cumule"],
            mode="lines",
            line=dict(color="#1e293b", width=2),
            fill="tozeroy",
            fillcolor="rgba(30,41,59,0.1)",
            name="Solde"
        ))
        fig1.add_hline(y=SEUIL_ALERTE, line_dash="dash", line_color="#dc2626",
                       annotation_text="Seuil d'alerte", annotation_position="top left")
        fig1.update_layout(
            xaxis_title="Date",
            yaxis_title="Montant (MAD)",
            height=380,
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="#f8fafc",
            title_font_size=14
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Répartition des dépenses")
        sorties_df = df[df["type"] == "sortie"].groupby("categorie")["montant"].sum().reset_index()
        sorties_df.columns = ["Categorie", "Montant"]
        sorties_df["Categorie"] = sorties_df["Categorie"].str.replace("_", " ").str.title()
        
        fig2 = px.pie(
            sorties_df, 
            values="Montant", 
            names="Categorie",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greys_r
        )
        fig2.update_layout(height=380, template="plotly_white", showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Graphique mensuel
    st.markdown("#### Encaissements vs Décaissements par mois")
    df["mois"] = df["date"].dt.strftime("%B %Y")
    monthly = df.groupby(["mois", "type"])["montant"].sum().reset_index()
    
    fig3 = px.bar(
        monthly, 
        x="mois", 
        y="montant", 
        color="type",
        barmode="group",
        color_discrete_map={"entree": "#22c55e", "sortie": "#ef4444"},
        labels={"montant": "Montant (MAD)", "mois": "Mois", "type": "Type"}
    )
    fig3.update_layout(height=320, template="plotly_white", plot_bgcolor="#f8fafc")
    st.plotly_chart(fig3, use_container_width=True)

# ==================== TAB 2: FLUX ====================
with tabs[1]:
    st.markdown("### Historique des transactions")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        filtre_type = st.selectbox("Filtrer par type", ["Tous", "entree", "sortie"])
    
    df_flux = st.session_state.transactions.copy()
    if filtre_type != "Tous":
        df_flux = df_flux[df_flux["type"] == filtre_type]
    
    df_display = df_flux.copy()
    df_display["date"] = df_display["date"].dt.strftime("%d/%m/%Y")
    df_display["montant"] = df_display["montant"].apply(lambda x: f"{x:,.0f} MAD")
    df_display["solde_cumule"] = df_display["solde_cumule"].apply(lambda x: f"{x:,.0f} MAD")
    df_display = df_display[["date", "type", "categorie", "description", "montant", "solde_cumule"]]
    df_display.columns = ["Date", "Type", "Catégorie", "Description", "Montant", "Solde cumulé"]
    
    st.dataframe(df_display, use_container_width=True, height=400)
    
    st.markdown("---")
    st.markdown("### Ajouter une transaction")
    
    with st.form("add_transaction"):
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("Date", datetime.now())
            new_type = st.selectbox("Type", ["entree", "sortie"])
            new_montant = st.number_input("Montant (MAD)", min_value=0.0, step=1000.0)
        with col2:
            new_categorie = st.selectbox("Catégorie", [
                "vente_client", "acompte", "salaires", "loyer", "matieres_premieres",
                "electricite", "cnss", "tva", "maintenance", "frais_generaux"
            ])
            new_description = st.text_input("Description")
        
        submitted = st.form_submit_button("Enregistrer")
        
        if submitted and new_montant > 0 and new_description:
            dernier_solde = st.session_state.transactions["solde_cumule"].iloc[-1]
            if new_type == "entree":
                nouveau_solde = dernier_solde + new_montant
            else:
                nouveau_solde = dernier_solde - new_montant
            
            nouvelle_ligne = pd.DataFrame([{
                "date": pd.to_datetime(new_date),
                "type": new_type,
                "categorie": new_categorie,
                "description": new_description,
                "montant": new_montant,
                "solde_cumule": nouveau_solde
            }])
            
            st.session_state.transactions = pd.concat([st.session_state.transactions, nouvelle_ligne], ignore_index=True)
            save_transactions(st.session_state.transactions)
            st.success(f"Transaction ajoutée - Nouveau solde : {nouveau_solde:,.0f} MAD")
            st.cache_data.clear()
            st.rerun()

# ==================== TAB 3: ECHANCIER ====================
with tabs[2]:
    st.markdown("### Echéancier")
    
    ech = st.session_state.echeances.copy()
    today = pd.Timestamp(datetime.now().date())
    
    # Alertes
    retards = ech[ech["statut"] == "en_retard"]
    for _, row in retards.iterrows():
        st.markdown(f'<div class="alert-warning">Paiement en retard : {row["tiers"]} - {row["description"]} - {row["montant"]:,.0f} MAD</div>', unsafe_allow_html=True)
    
    prochaines = ech[(ech["date_echeance"] <= today + timedelta(days=7)) & 
                     (ech["statut"] == "en_attente") & 
                     (ech["montant"] >= SEUIL_GROSSE_ECHEANCE)]
    for _, row in prochaines.iterrows():
        st.markdown(f'<div class="alert-warning">Echéance importante : {row["tiers"]} - {row["montant"]:,.0f} MAD le {row["date_echeance"].strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        filtre_type_ech = st.selectbox("Filtrer par type", ["Tous", "a_encaisser", "a_payer"])
    with col2:
        filtre_statut = st.selectbox("Filtrer par statut", ["Tous", "en_attente", "en_retard"])
    
    ech_filtre = ech.copy()
    if filtre_type_ech != "Tous":
        ech_filtre = ech_filtre[ech_filtre["type"] == filtre_type_ech]
    if filtre_statut != "Tous":
        ech_filtre = ech_filtre[ech_filtre["statut"] == filtre_statut]
    
    ech_display = ech_filtre.copy()
    ech_display["date_echeance"] = ech_display["date_echeance"].dt.strftime("%d/%m/%Y")
    ech_display["montant"] = ech_display["montant"].apply(lambda x: f"{x:,.0f} MAD")
    ech_display = ech_display[["date_echeance", "type", "tiers", "description", "montant", "statut"]]
    ech_display.columns = ["Date", "Type", "Tiers", "Description", "Montant", "Statut"]
    
    st.dataframe(ech_display, use_container_width=True, height=400)
    
    # Totaux
    total_encaisser = ech[ech["type"] == "a_encaisser"]["montant"].sum()
    total_payer = ech[ech["type"] == "a_payer"]["montant"].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total à encaisser", f"{total_encaisser:,.0f} MAD")
    col2.metric("Total à payer", f"{total_payer:,.0f} MAD")
    col3.metric("Solde net prévisionnel", f"{total_encaisser - total_payer:,.0f} MAD")
    
    # Formulaire ajout échéance
    st.markdown("---")
    st.markdown("### Ajouter une échéance")
    
    with st.form("add_echeance"):
        col1, col2 = st.columns(2)
        with col1:
            new_ech_date = st.date_input("Date d'échéance", datetime.now() + timedelta(days=7))
            new_ech_type = st.selectbox("Type", ["a_encaisser", "a_payer"])
            new_ech_montant = st.number_input("Montant (MAD)", min_value=0.0, step=1000.0)
        with col2:
            new_ech_tiers = st.text_input("Tiers (client / fournisseur)")
            new_ech_description = st.text_input("Description")
            new_ech_statut = st.selectbox("Statut", ["en_attente", "en_retard"])
        
        submitted_ech = st.form_submit_button("Enregistrer")
        
        if submitted_ech and new_ech_montant > 0 and new_ech_tiers:
            nouvelle_ech = pd.DataFrame([{
                "date_echeance": pd.to_datetime(new_ech_date),
                "type": new_ech_type,
                "tiers": new_ech_tiers,
                "description": new_ech_description,
                "montant": new_ech_montant,
                "statut": new_ech_statut
            }])
            
            st.session_state.echeances = pd.concat([st.session_state.echeances, nouvelle_ech], ignore_index=True)
            save_echeances(st.session_state.echeances)
            st.success("Echéance ajoutée avec succès")
            st.cache_data.clear()
            st.rerun()

# ==================== TAB 4: PREVISIONS ====================
with tabs[3]:
    st.markdown("### Prévision de trésorerie sur 8 semaines")
    
    ech_prev = st.session_state.echeances.copy()
    ech_prev["semaine"] = ech_prev["date_echeance"].dt.strftime("%Y-W%W")
    
    encaissements_sem = ech_prev[ech_prev["type"] == "a_encaisser"].groupby("semaine")["montant"].sum()
    decaissements_sem = ech_prev[ech_prev["type"] == "a_payer"].groupby("semaine")["montant"].sum()
    
    toutes_semaines = sorted(set(encaissements_sem.index) | set(decaissements_sem.index))
    toutes_semaines = toutes_semaines[:8]
    
    df_prev = pd.DataFrame({
        "Semaine": toutes_semaines,
        "Encaissements": [encaissements_sem.get(s, 0) for s in toutes_semaines],
        "Décaissements": [decaissements_sem.get(s, 0) for s in toutes_semaines],
    })
    df_prev["Solde net"] = df_prev["Encaissements"] - df_prev["Décaissements"]
    
    solde_initial = st.session_state.transactions["solde_cumule"].iloc[-1]
    df_prev["Solde cumulé"] = solde_initial + df_prev["Solde net"].cumsum()
    
    # Alerte prévisionnelle
    semaines_critiques = df_prev[df_prev["Solde cumulé"] < SEUIL_ALERTE]
    if not semaines_critiques.empty:
        st.markdown(f'<div class="alert-critical">Alerte prévisionnelle : Le solde passera sous le seuil de {SEUIL_ALERTE:,} MAD dans les {len(semaines_critiques)} prochaines semaines</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-success">Solde prévisionnel maintenu au-dessus du seuil d\'alerte sur l\'horizon de 8 semaines</div>', unsafe_allow_html=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Encaissements vs Décaissements")
        df_bar = df_prev.melt(id_vars=["Semaine"], value_vars=["Encaissements", "Décaissements"],
                              var_name="Type", value_name="Montant")
        fig_bar = px.bar(df_bar, x="Semaine", y="Montant", color="Type",
                         barmode="group",
                         color_discrete_map={"Encaissements": "#22c55e", "Décaissements": "#ef4444"})
        fig_bar.update_layout(height=380, template="plotly_white", plot_bgcolor="#f8fafc")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("#### Evolution du solde prévisionnel")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_prev["Semaine"], 
            y=df_prev["Solde cumulé"],
            mode="lines+markers",
            line=dict(color="#1e293b", width=2),
            marker=dict(size=6, color="#1e293b"),
            text=[f"{v:,.0f}" for v in df_prev["Solde cumulé"]],
            textposition="top center",
            textfont=dict(size=11)
        ))
        fig_line.add_hline(y=SEUIL_ALERTE, line_dash="dash", line_color="#dc2626",
                           annotation_text="Seuil d'alerte")
        fig_line.update_layout(height=380, template="plotly_white", plot_bgcolor="#f8fafc")
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Tableau détaillé
    st.markdown("#### Détail des prévisions")
    df_display_prev = df_prev.copy()
    for col in ["Encaissements", "Décaissements", "Solde net", "Solde cumulé"]:
        df_display_prev[col] = df_display_prev[col].apply(lambda x: f"{x:,.0f} MAD")
    st.dataframe(df_display_prev, use_container_width=True)
    
    # Hypothèses
    with st.expander("Hypothèses du modèle de prévision"):
        st.markdown(f"""
        **Modèle de prévision**
        
        | Paramètre | Valeur |
        |-----------|--------|
        | Solde initial | {solde_initial:,.0f} MAD |
        | Seuil d'alerte | {SEUIL_ALERTE:,} MAD |
        | Seuil grosse échéance | {SEUIL_GROSSE_ECHEANCE:,} MAD |
        | Horizon de prévision | 8 semaines |
        
        **Méthodologie**
        - Les prévisions intègrent l'ensemble des échéances enregistrées
        - Les encaissements clients sont basés sur les factures à recevoir
        - Les décaissements incluent les charges sociales, fournisseurs et TVA
        
        **Limites**
        - Les nouveaux contrats non encore signés ne sont pas intégrés
        - Les retards de paiement client sont basés sur l'historique constaté
        """)

# ==================== FOOTER ====================
st.markdown("---")
st.caption("MarocIndustrie SARL - Mini-application de gestion de trésorerie | Données fictives à usage pédagogique")
