import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="MarocIndustrie - Gestion de Trésorerie",
    page_icon="⚡",
    layout="wide"
)

# ==================== DESIGN SYSTEM PREMIUM ====================
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fc;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9edf2;
        box-shadow: 2px 0 12px rgba(0,0,0,0.02);
    }
    
    [data-testid="stSidebar"] * {
        color: #1a2c3e !important;
    }
    
    .main-header {
        font-size: 28px;
        font-weight: 600;
        color: #0a2540;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    
    .sub-header {
        font-size: 14px;
        color: #5c6f87;
        border-bottom: 1px solid #e9edf2;
        padding-bottom: 20px;
        margin-bottom: 24px;
    }
    
    .kpi-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #e9edf2;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
    }
    
    .kpi-card:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .kpi-label {
        font-size: 13px;
        font-weight: 500;
        color: #5c6f87;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 32px;
        font-weight: 600;
        color: #0a2540;
        letter-spacing: -0.01em;
    }
    
    .insight-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e9edf2;
        overflow: hidden;
    }
    
    .insight-header {
        padding: 16px 20px;
        border-bottom: 1px solid #e9edf2;
        background: #fafbfc;
    }
    
    .insight-header h4 {
        font-size: 14px;
        font-weight: 600;
        color: #5c6f87;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin: 0;
    }
    
    .insight-body {
        padding: 20px;
    }
    
    .insight-message {
        font-size: 15px;
        font-weight: 500;
        color: #1a2c3e;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    
    .insight-reco {
        font-size: 13px;
        color: #5c6f87;
        padding-top: 12px;
        border-top: 1px solid #e9edf2;
    }
    
    .insight-reco strong {
        color: #0a2540;
    }
    
    .status-critical {
        border-left: 3px solid #ef4444;
    }
    .status-warning {
        border-left: 3px solid #f59e0b;
    }
    .status-success {
        border-left: 3px solid #10b981;
    }
    .status-info {
        border-left: 3px solid #3b82f6;
    }
    
    .alert-banner-warning {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 14px 18px;
        border-radius: 12px;
        color: #92400e;
        font-size: 13px;
        margin-bottom: 16px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 32px;
        border-bottom: 1px solid #e9edf2;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 14px;
        font-weight: 500;
        color: #5c6f87;
        padding: 10px 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0a2540;
        border-bottom: 2px solid #0a2540;
    }
    
    .stButton > button {
        background-color: #0a2540;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 13px;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #1a3c5e;
    }
    
    hr {
        margin: 20px 0;
        border-color: #e9edf2;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CONFIGURATION ====================
if "seuil_alerte" not in st.session_state:
    st.session_state.seuil_alerte = 50000
if "seuil_grosse_echeance" not in st.session_state:
    st.session_state.seuil_grosse_echeance = 30000

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

# ==================== FONCTIONS D'ANALYSE ====================
def analyser_position_tresorerie(solde, seuil):
    if solde < seuil:
        return {
            "status": "critical",
            "message": f"Solde actuel de {solde:,.0f} MAD inférieur au seuil de {seuil:,} MAD",
            "recommandation": "Action urgente : accélérer les encaissements, reporter les dépenses non essentielles"
        }
    elif solde < seuil * 1.5:
        return {
            "status": "warning",
            "message": f"Solde de {solde:,.0f} MAD proche du seuil d'alerte de {seuil:,} MAD",
            "recommandation": "Surveillance renforcée : accélérer les recouvrements, maîtriser les dépenses"
        }
    elif solde > seuil * 3:
        return {
            "status": "success",
            "message": f"Position excellente : {solde:,.0f} MAD, marge de {solde - seuil:,.0f} MAD",
            "recommandation": "Envisager un remboursement anticipé de dettes ou des investissements stratégiques"
        }
    else:
        return {
            "status": "info",
            "message": f"Position stable : {solde:,.0f} MAD",
            "recommandation": "Maintenir un suivi régulier des flux de trésorerie"
        }

def analyser_creances(df_echeances):
    retards = df_echeances[df_echeances["statut"] == "en_retard"]
    montant = retards["montant"].sum()
    nombre = len(retards)
    
    if nombre == 0:
        return {
            "status": "success",
            "message": "Aucune créance en retard",
            "recommandation": "Le processus de recouvrement est efficace"
        }
    elif nombre <= 2:
        return {
            "status": "warning",
            "message": f"{nombre} facture(s) en retard pour un total de {montant:,.0f} MAD",
            "recommandation": "Contacter les clients immédiatement"
        }
    else:
        return {
            "status": "critical",
            "message": f"{nombre} factures en retard totalisant {montant:,.0f} MAD",
            "recommandation": "Urgent : déployer une équipe de recouvrement, réviser les conditions de crédit"
        }

def analyser_prevision(df_prevision, seuil, solde_initial):
    if df_prevision.empty:
        return {
            "status": "info",
            "message": "Données insuffisantes pour la prévision",
            "recommandation": "Ajouter davantage d'échéances programmées"
        }
    
    semaines_critiques = df_prevision[df_prevision["Solde Cumulé"] < seuil]
    solde_final = df_prevision["Solde Cumulé"].iloc[-1] if not df_prevision.empty else solde_initial
    
    if len(semaines_critiques) > 0:
        premiere_semaine = semaines_critiques.iloc[0]["Semaine"]
        return {
            "status": "critical",
            "message": f"Rupture de trésorerie prévue à la semaine {premiere_semaine}",
            "recommandation": "Anticiper un besoin de financement ou renégocier les délais fournisseurs"
        }
    elif solde_final < seuil * 1.2:
        return {
            "status": "warning",
            "message": f"Tendance tendue : solde final prévu de {solde_final:,.0f} MAD",
            "recommandation": "Maîtriser les dépenses, suivre les encaissements de près"
        }
    else:
        return {
            "status": "success",
            "message": f"Prévisions favorables : {solde_final:,.0f} MAD projeté",
            "recommandation": "La position permet une flexibilité opérationnelle"
        }

def analyser_grosses_echeances(df_echeances, seuil):
    echeances_importantes = df_echeances[
        (df_echeances["statut"] == "en_attente") & 
        (df_echeances["montant"].abs() >= seuil)
    ]
    
    if len(echeances_importantes) == 0:
        return None
    
    total = echeances_importantes["montant"].abs().sum()
    return {
        "status": "warning",
        "message": f"{len(echeances_importantes)} échéance(s) importante(s) à venir pour un total de {total:,.0f} MAD",
        "recommandation": "S'assurer d'une liquidité suffisante pour ces paiements"
    }

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### MAROCINDUSTRIE")
    st.markdown("#### Tableau de bord Trésorerie")
    st.markdown("---")
    
    st.markdown("**Profil de l'entreprise**")
    st.markdown("- Ain Sebaa, Casablanca")
    st.markdown("- Fabrication métallique / BTP")
    st.markdown("- 12 employés")
    st.markdown("- 2,4 M MAD CA annuel")
    
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
    
    nouveau_seuil = st.number_input(
        "Seuil d'alerte (MAD)",
        min_value=10000,
        max_value=200000,
        value=st.session_state.seuil_alerte,
        step=5000
    )
    if nouveau_seuil != st.session_state.seuil_alerte:
        st.session_state.seuil_alerte = nouveau_seuil
        st.cache_data.clear()
        st.rerun()
    
    nouveau_seuil_grosse = st.number_input(
        "Seuil grosse échéance (MAD)",
        min_value=10000,
        max_value=200000,
        value=st.session_state.seuil_grosse_echeance,
        step=5000
    )
    if nouveau_seuil_grosse != st.session_state.seuil_grosse_echeance:
        st.session_state.seuil_grosse_echeance = nouveau_seuil_grosse
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption("Données : Jan - Mar 2025")
    st.caption("Prévision : 8 semaines glissantes")

# ==================== HEADER ====================
st.markdown('<div class="main-header">MarocIndustrie SARL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tableau de bord de gestion de trésorerie | Suivi en temps réel et prévisions</div>', unsafe_allow_html=True)

# ==================== TABS ====================
tabs = st.tabs(["Tableau de bord", "Flux de trésorerie", "Échéancier", "Prévisions"])

# ==================== TAB 1: TABLEAU DE BORD ====================
with tabs[0]:
    df = st.session_state.transactions
    solde_actuel = df["solde_cumule"].iloc[-1]
    total_entrees = df[df["type"] == "entree"]["montant"].sum()
    total_sorties = df[df["type"] == "sortie"]["montant"].sum()
    flux_net = total_entrees - total_sorties
    
    ech = st.session_state.echeances
    seuil = st.session_state.seuil_alerte
    seuil_grosse = st.session_state.seuil_grosse_echeance
    
    analyse_treso = analyser_position_tresorerie(solde_actuel, seuil)
    analyse_creances = analyser_creances(ech)
    grosses_echeances = analyser_grosses_echeances(ech, seuil_grosse)
    
    # Ligne des KPI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Solde actuel</div>
            <div class="kpi-value">{solde_actuel:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total encaissements (3 mois)</div>
            <div class="kpi-value">{total_entrees:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total décaissements (3 mois)</div>
            <div class="kpi-value">{total_sorties:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Flux net (3 mois)</div>
            <div class="kpi-value">{flux_net:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ligne des analyses
    col1, col2 = st.columns(2)
    
    with col1:
        status_class = f"status-{analyse_treso['status']}"
        st.markdown(f"""
        <div class="insight-card {status_class}">
            <div class="insight-header">
                <h4>Analyse de la trésorerie</h4>
            </div>
            <div class="insight-body">
                <div class="insight-message">{analyse_treso['message']}</div>
                <div class="insight-reco"><strong>Recommandation</strong><br>{analyse_treso['recommandation']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status_class = f"status-{analyse_creances['status']}"
        st.markdown(f"""
        <div class="insight-card {status_class}">
            <div class="insight-header">
                <h4>État des créances</h4>
            </div>
            <div class="insight-body">
                <div class="insight-message">{analyse_creances['message']}</div>
                <div class="insight-reco"><strong>Recommandation</strong><br>{analyse_creances['recommandation']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if grosses_echeances:
        st.markdown(f"""
        <div class="alert-banner-warning">
            <strong>Alertes échéances importantes</strong><br>
            {grosses_echeances['message']}<br>
            <strong>Action :</strong> {grosses_echeances['recommandation']}
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Évolution du solde")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df["date"],
            y=df["solde_cumule"],
            mode="lines",
            line=dict(color="#0a2540", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(10,37,64,0.05)",
            name="Solde"
        ))
        fig1.add_hline(y=seuil, line_dash="dash", line_color="#ef4444",
                       annotation_text=f"Seuil d'alerte ({seuil:,} MAD)", 
                       annotation_position="top left")
        fig1.update_layout(
            height=380,
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="white",
            xaxis_title="Date",
            yaxis_title="Montant (MAD)",
            xaxis=dict(gridcolor="#f0f2f5"),
            yaxis=dict(gridcolor="#f0f2f5")
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Répartition des dépenses")
        depenses = df[df["type"] == "sortie"].groupby("categorie")["montant"].sum().reset_index()
        depenses.columns = ["Catégorie", "Montant"]
        depenses["Catégorie"] = depenses["Catégorie"].str.replace("_", " ").str.title()
        
        fig2 = px.pie(
            depenses,
            values="Montant",
            names="Catégorie",
            hole=0.45,
            color_discrete_sequence=["#0a2540", "#1a3c5e", "#2a4c7e", "#3a5c9e", "#4a6cae"]
        )
        fig2.update_layout(height=380, template="plotly_white", showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("#### Flux mensuels entrants / sortants")
    df["mois"] = df["date"].dt.strftime("%B %Y")
    mensuel = df.groupby(["mois", "type"])["montant"].sum().reset_index()
    
    fig3 = px.bar(
        mensuel,
        x="mois",
        y="montant",
        color="type",
        barmode="group",
        color_discrete_map={"entree": "#10b981", "sortie": "#ef4444"},
        labels={"montant": "Montant (MAD)", "mois": "Mois", "type": "Type"}
    )
    fig3.update_layout(height=320, template="plotly_white", plot_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

# ==================== TAB 2: FLUX DE TRESORERIE ====================
with tabs[1]:
    st.markdown("#### Historique des transactions")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        filtre_type = st.selectbox("Filtrer par type", ["Tous", "entree", "sortie"])
    
    df_flux = st.session_state.transactions.copy()
    if filtre_type != "Tous":
        df_flux = df_flux[df_flux["type"] == filtre_type]
    
    df_affichage = df_flux.copy()
    df_affichage["date"] = df_affichage["date"].dt.strftime("%d/%m/%Y")
    df_affichage["montant"] = df_affichage["montant"].apply(lambda x: f"{x:,.0f} MAD")
    df_affichage["solde_cumule"] = df_affichage["solde_cumule"].apply(lambda x: f"{x:,.0f} MAD")
    df_affichage = df_affichage[["date", "type", "categorie", "description", "montant", "solde_cumule"]]
    df_affichage.columns = ["Date", "Type", "Catégorie", "Description", "Montant", "Solde cumulé"]
    
    st.dataframe(df_affichage, use_container_width=True, height=450)
    
    st.markdown("---")
    st.markdown("#### Ajouter une transaction")
    
    with st.form("add_transaction"):
        col1, col2 = st.columns(2)
        with col1:
            nouvelle_date = st.date_input("Date", datetime.now())
            nouveau_type = st.selectbox("Type", ["entree", "sortie"])
            nouveau_montant = st.number_input("Montant (MAD)", min_value=0.0, step=1000.0)
        with col2:
            nouvelle_categorie = st.selectbox("Catégorie", [
                "vente_client", "acompte", "salaires", "loyer", "matieres_premieres",
                "electricite", "cnss", "tva", "maintenance", "frais_generaux"
            ])
            nouvelle_description = st.text_input("Description")
        
        valide = st.form_submit_button("Enregistrer la transaction")
        
        if valide and nouveau_montant > 0 and nouvelle_description:
            dernier_solde = st.session_state.transactions["solde_cumule"].iloc[-1]
            if nouveau_type == "entree":
                nouveau_solde = dernier_solde + nouveau_montant
            else:
                nouveau_solde = dernier_solde - nouveau_montant
            
            nouvelle_ligne = pd.DataFrame([{
                "date": pd.to_datetime(nouvelle_date),
                "type": nouveau_type,
                "categorie": nouvelle_categorie,
                "description": nouvelle_description,
                "montant": nouveau_montant,
                "solde_cumule": nouveau_solde
            }])
            
            st.session_state.transactions = pd.concat([st.session_state.transactions, nouvelle_ligne], ignore_index=True)
            save_transactions(st.session_state.transactions)
            st.success(f"Transaction enregistrée - Nouveau solde : {nouveau_solde:,.0f} MAD")
            st.cache_data.clear()
            st.rerun()

# ==================== TAB 3: ECHEANCIER ====================
with tabs[2]:
    st.markdown("#### Échéancier des paiements")
    
    ech = st.session_state.echeances.copy()
    aujourdhui = pd.Timestamp(datetime.now().date())
    seuil_grosse = st.session_state.seuil_grosse_echeance
    
    # Alertes retards
    retards = ech[ech["statut"] == "en_retard"]
    for _, row in retards.iterrows():
        st.markdown(f"""
        <div class="alert-banner-warning">
            <strong>Paiement en retard</strong><br>
            {row['tiers']} - {row['description']} - {row['montant']:,.0f} MAD
        </div>
        """, unsafe_allow_html=True)
    
    # Alertes grosses échéances proches
    echeances_proches = ech[
        (ech["date_echeance"] <= aujourdhui + timedelta(days=7)) & 
        (ech["statut"] == "en_attente") & 
        (ech["montant"].abs() >= seuil_grosse)
    ]
    for _, row in echeances_proches.iterrows():
        st.markdown(f"""
        <div class="alert-banner-warning">
            <strong>Grosse échéance à venir</strong><br>
            {row['tiers']} - {row['montant']:,.0f} MAD le {row['date_echeance'].strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)
    
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
    
    ech_affichage = ech_filtre.copy()
    ech_affichage["date_echeance"] = ech_affichage["date_echeance"].dt.strftime("%d/%m/%Y")
    ech_affichage["montant"] = ech_affichage["montant"].apply(lambda x: f"{x:,.0f} MAD")
    ech_affichage = ech_affichage[["date_echeance", "type", "tiers", "description", "montant", "statut"]]
    ech_affichage.columns = ["Date", "Type", "Tiers", "Description", "Montant", "Statut"]
    
    st.dataframe(ech_affichage, use_container_width=True, height=400)
    
    # Totaux
    total_a_encaisser = ech[ech["type"] == "a_encaisser"]["montant"].sum()
    total_a_payer = ech[ech["type"] == "a_payer"]["montant"].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total à encaisser", f"{total_a_encaisser:,.0f} MAD")
    col2.metric("Total à payer", f"{total_a_payer:,.0f} MAD")
    col3.metric("Position nette", f"{total_a_encaisser - total_a_payer:,.0f} MAD")
    
    st.markdown("---")
    st.markdown("#### Ajouter une échéance")
    
    with st.form("add_echeance"):
        col1, col2 = st.columns(2)
        with col1:
            nouvelle_date_ech = st.date_input("Date d'échéance", datetime.now() + timedelta(days=7))
            nouveau_type_ech = st.selectbox("Type", ["a_encaisser", "a_payer"])
            nouveau_montant_ech = st.number_input("Montant (MAD)", min_value=0.0, step=1000.0)
        with col2:
            nouveau_tiers = st.text_input("Tiers (client / fournisseur)")
            nouvelle_desc_ech = st.text_input("Description")
            nouveau_statut = st.selectbox("Statut", ["en_attente", "en_retard"])
        
        valide_ech = st.form_submit_button("Enregistrer l'échéance")
        
        if valide_ech and nouveau_montant_ech > 0 and nouveau_tiers:
            nouvelle_ligne_ech = pd.DataFrame([{
                "date_echeance": pd.to_datetime(nouvelle_date_ech),
                "type": nouveau_type_ech,
                "tiers": nouveau_tiers,
                "description": nouvelle_desc_ech,
                "montant": nouveau_montant_ech,
                "statut": nouveau_statut
            }])
            
            st.session_state.echeances = pd.concat([st.session_state.echeances, nouvelle_ligne_ech], ignore_index=True)
            save_echeances(st.session_state.echeances)
            st.success("Échéance enregistrée avec succès")
            st.cache_data.clear()
            st.rerun()

# ==================== TAB 4: PREVISIONS ====================
with tabs[3]:
    st.markdown("#### Prévision de trésorerie sur 8 semaines")
    
    donnees_prevision = st.session_state.echeances.copy()
    donnees_prevision["semaine"] = donnees_prevision["date_echeance"].dt.strftime("S%W")
    
    encaissements_hebdo = donnees_prevision[donnees_prevision["type"] == "a_encaisser"].groupby("semaine")["montant"].sum()
    decaissements_hebdo = donnees_prevision[donnees_prevision["type"] == "a_payer"].groupby("semaine")["montant"].sum()
    
    toutes_semaines = sorted(set(encaissements_hebdo.index) | set(decaissements_hebdo.index))
    toutes_semaines = toutes_semaines[:8]
    
    df_prevision = pd.DataFrame({
        "Semaine": toutes_semaines,
        "Encaissements": [encaissements_hebdo.get(s, 0) for s in toutes_semaines],
        "Décaissements": [decaissements_hebdo.get(s, 0) for s in toutes_semaines],
    })
    df_prevision["Flux net"] = df_prevision["Encaissements"] - df_prevision["Décaissements"]
    
    solde_initial = st.session_state.transactions["solde_cumule"].iloc[-1]
    df_prevision["Solde Cumulé"] = solde_initial + df_prevision["Flux net"].cumsum()
    
    seuil = st.session_state.seuil_alerte
    
    analyse_prevision = analyser_prevision(df_prevision, seuil, solde_initial)
    status_class = f"status-{analyse_prevision['status']}"
    
    st.markdown(f"""
    <div class="insight-card {status_class}" style="margin-bottom: 20px;">
        <div class="insight-header">
            <h4>Analyse prévisionnelle</h4>
        </div>
        <div class="insight-body">
            <div class="insight-message">{analyse_prevision['message']}</div>
            <div class="insight-reco"><strong>Recommandation</strong><br>{analyse_prevision['recommandation']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Flux hebdomadaires")
        df_bar = df_prevision.melt(id_vars=["Semaine"], value_vars=["Encaissements", "Décaissements"],
                                   var_name="Type", value_name="Montant")
        fig_bar = px.bar(df_bar, x="Semaine", y="Montant", color="Type",
                         barmode="group",
                         color_discrete_map={"Encaissements": "#10b981", "Décaissements": "#ef4444"})
        fig_bar.update_layout(height=380, template="plotly_white", plot_bgcolor="white")
        fig_bar.update_xaxes(title_text="Semaine")
        fig_bar.update_yaxes(title_text="Montant (MAD)")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("#### Évolution du solde prévisionnel")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_prevision["Semaine"],
            y=df_prevision["Solde Cumulé"],
            mode="lines+markers",
            line=dict(color="#0a2540", width=2.5),
            marker=dict(size=7, color="#0a2540"),
            text=[f"{v:,.0f}" for v in df_prevision["Solde Cumulé"]],
            textposition="top center",
            textfont=dict(size=11)
        ))
        fig_line.add_hline(y=seuil, line_dash="dash", line_color="#ef4444",
                           annotation_text=f"Seuil d'alerte ({seuil:,} MAD)")
        fig_line.update_layout(height=380, template="plotly_white", plot_bgcolor="white")
        fig_line.update_xaxes(title_text="Semaine")
        fig_line.update_yaxes(title_text="Solde (MAD)")
        st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("#### Détail des prévisions")
    df_affichage_prev = df_prevision.copy()
    for col in ["Encaissements", "Décaissements", "Flux net", "Solde Cumulé"]:
        df_affichage_prev[col] = df_affichage_prev[col].apply(lambda x: f"{x:,.0f} MAD")
    st.dataframe(df_affichage_prev, use_container_width=True)
    
    st.markdown("#### Indicateurs clés de prévision")
    col1, col2, col3 = st.columns(3)
    
    solde_min = df_prevision["Solde Cumulé"].min()
    solde_max = df_prevision["Solde Cumulé"].max()
    flux_moyen = df_prevision["Flux net"].mean()
    
    col1.metric("Solde minimum projeté", f"{solde_min:,.0f} MAD")
    col2.metric("Solde maximum projeté", f"{solde_max:,.0f} MAD")
    col3.metric("Flux net moyen hebdomadaire", f"{flux_moyen:,.0f} MAD")
