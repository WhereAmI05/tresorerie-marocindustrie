import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import os

st.set_page_config(
    page_title="MarocIndustrie - Gestion de Trésorerie",
    page_icon=":factory:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== GESTION DE LA SESSION ====================
if "authentifie" not in st.session_state:
    st.session_state.authentifie = False
if "transactions" not in st.session_state:
    st.session_state.transactions = None
if "echeances" not in st.session_state:
    st.session_state.echeances = None

# ==================== FONCTIONS D AUTHENTIFICATION ====================
def verifier_login(email, mot_de_passe):
    # Identifiants par défaut
    identifiants = {
        "tresorier@marocindustrie.ma": "tresorier123",
        "admin@marocindustrie.ma": "admin123",
        "directeur@marocindustrie.ma": "directeur123"
    }
    return identifiants.get(email) == mot_de_passe

def charger_donnees_defaut():
    """Charge les données par défaut depuis les fichiers CSV"""
    try:
        df_transactions = pd.read_csv("transactions.csv", parse_dates=["date"])
        df_echeances = pd.read_csv("echeances.csv", parse_dates=["date_echeance"])
        return df_transactions, df_echeances
    except:
        return None, None

# ==================== PAGE DE LOGIN ====================
if not st.session_state.authentifie:
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.05);
            border: 1px solid #eef2f6;
        }
        .login-title {
            font-size: 24px;
            font-weight: 600;
            color: #0a2540;
            text-align: center;
            margin-bottom: 8px;
        }
        .login-subtitle {
            font-size: 13px;
            color: #6b7a8a;
            text-align: center;
            margin-bottom: 32px;
        }
    </style>
    
    <div class="login-container">
        <div class="login-title">MarocIndustrie SARL</div>
        <div class="login-subtitle">Accès tableau de bord trésorerie</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email professionnel")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("Se connecter", use_container_width=True)
        
        if submit:
            if verifier_login(email, mot_de_passe):
                st.session_state.authentifie = True
                df_trans, df_ech = charger_donnees_defaut()
                if df_trans is not None and df_ech is not None:
                    st.session_state.transactions = df_trans.copy()
                    st.session_state.echeances = df_ech.copy()
                st.rerun()
            else:
                st.error("Email ou mot de passe incorrect")
    
    st.stop()

# ==================== FONCTIONS DE GESTION DES DONNEES ====================
def sauvegarder_transactions(df):
    df.to_csv("transactions.csv", index=False)

def sauvegarder_echeances(df):
    df.to_csv("echeances.csv", index=False)

def importer_transactions(fichier):
    """Importe un fichier CSV de transactions"""
    try:
        df = pd.read_csv(fichier, parse_dates=["date"])
        colonnes_requises = ["date", "type", "categorie", "description", "montant", "solde_cumule"]
        for col in colonnes_requises:
            if col not in df.columns:
                st.error(f"Colonne manquante : {col}")
                return None
        return df
    except Exception as e:
        st.error(f"Erreur lors de l'import : {e}")
        return None

def importer_echeances(fichier):
    """Importe un fichier CSV d'échéances"""
    try:
        df = pd.read_csv(fichier, parse_dates=["date_echeance"])
        colonnes_requises = ["date_echeance", "type", "tiers", "description", "montant", "statut"]
        for col in colonnes_requises:
            if col not in df.columns:
                st.error(f"Colonne manquante : {col}")
                return None
        return df
    except Exception as e:
        st.error(f"Erreur lors de l'import : {e}")
        return None

# ==================== CHARGEMENT INITIAL ====================
if st.session_state.transactions is None or st.session_state.echeances is None:
    df_trans, df_ech = charger_donnees_defaut()
    if df_trans is not None and df_ech is not None:
        st.session_state.transactions = df_trans
        st.session_state.echeances = df_ech

# ==================== DESIGN SYSTEM PREMIUM ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8edf3 100%);
    }
    
    .top-nav {
        background: white;
        padding: 16px 32px;
        border-radius: 0px 0px 20px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 32px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .company-name {
        font-size: 20px;
        font-weight: 600;
        color: #0a2540;
        letter-spacing: -0.3px;
    }
    
    .company-sub {
        font-size: 12px;
        color: #6b7a8a;
        margin-top: 2px;
    }
    
    .badge {
        background: #f0f4f8;
        padding: 8px 16px;
        border-radius: 40px;
        font-size: 12px;
        color: #2c7da0;
    }
    
    .logout-btn {
        background: none;
        border: 1px solid #eef2f6;
        padding: 8px 16px;
        border-radius: 40px;
        cursor: pointer;
        font-size: 12px;
        color: #6b7a8a;
    }
    
    .kpi-card {
        background: white;
        border-radius: 24px;
        padding: 20px 24px;
        transition: all 0.2s ease;
        border: 1px solid rgba(0,0,0,0.04);
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        margin-bottom: 16px;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.08);
    }
    
    .kpi-label {
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #8b9eb0;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: #0a2540;
    }
    
    .insight-card {
        background: white;
        border-radius: 20px;
        border: 1px solid rgba(0,0,0,0.04);
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .insight-header {
        padding: 16px 20px;
        background: #fafcff;
        border-bottom: 1px solid #eef2f6;
    }
    
    .insight-header h4 {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #8b9eb0;
        margin: 0;
    }
    
    .insight-body {
        padding: 20px;
    }
    
    .insight-message {
        font-size: 15px;
        font-weight: 500;
        color: #1a2c3e;
        margin-bottom: 16px;
    }
    
    .insight-recommendation {
        font-size: 13px;
        color: #6b7a8a;
        padding-top: 12px;
        border-top: 1px solid #eef2f6;
    }
    
    .status-critical { border-left: 4px solid #ef4444; }
    .status-warning { border-left: 4px solid #f59e0b; }
    .status-success { border-left: 4px solid #10b981; }
    .status-info { border-left: 4px solid #3b82f6; }
    
    .positive-amount {
        color: #10b981;
        font-weight: 600;
    }
    
    .negative-amount {
        color: #ef4444;
        font-weight: 600;
    }
    
    .form-container {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 30px;
        border: 1px solid #eef2f6;
    }
    
    .form-title {
        font-size: 16px;
        font-weight: 600;
        color: #0a2540;
        margin-bottom: 16px;
    }
    
    .import-container {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 30px;
        border: 2px dashed #cbd5e1;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 8px;
        border-radius: 60px;
        margin-bottom: 24px;
        border: 1px solid #eef2f6;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        padding: 10px 24px;
        font-size: 14px;
        font-weight: 500;
        color: #6b7a8a;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0a2540;
        color: white;
    }
    
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #eef2f6;
    }
    
    .stButton > button {
        background: #0a2540;
        color: white;
        border: none;
        border-radius: 40px;
        padding: 10px 28px;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #1a3c5e;
        transform: translateY(-1px);
    }
    
    .param-card {
        background: #f8fafc;
        border-radius: 16px;
        padding: 16px;
        margin: 12px 0;
        border: 1px solid #eef2f6;
    }
    
    .param-label {
        font-size: 12px;
        font-weight: 500;
        color: #6b7a8a;
        margin-bottom: 8px;
    }
    
    .param-value {
        font-size: 18px;
        font-weight: 600;
        color: #0a2540;
    }
    
    hr {
        margin: 24px 0;
        border-color: #eef2f6;
    }
    
    .alert-badge {
        display: inline-flex;
        align-items: center;
        background: #fef2f2;
        border-radius: 40px;
        padding: 6px 14px;
        margin-right: 12px;
        margin-bottom: 12px;
        font-size: 12px;
        color: #991b1b;
    }
    
    .alert-badge-warning {
        background: #fffbeb;
        color: #92400e;
    }
    
    .row-encaisser {
        background-color: rgba(16, 185, 129, 0.05);
        border-left: 3px solid #10b981;
    }
    
    .row-payer {
        background-color: rgba(239, 68, 68, 0.05);
        border-left: 3px solid #ef4444;
    }
    
    .badge-encaisser {
        background-color: #10b981;
        color: white;
        padding: 4px 12px;
        border-radius: 40px;
        font-size: 11px;
        font-weight: 500;
        display: inline-block;
    }
    
    .badge-payer {
        background-color: #ef4444;
        color: white;
        padding: 4px 12px;
        border-radius: 40px;
        font-size: 11px;
        font-weight: 500;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CONFIGURATION ====================
if "seuil_alerte" not in st.session_state:
    st.session_state.seuil_alerte = 50000
if "seuil_grosse_echeance" not in st.session_state:
    st.session_state.seuil_grosse_echeance = 30000

# ==================== FONCTIONS D ANALYSE ====================
def analyser_position_tresorerie(solde, seuil):
    if solde < seuil:
        return {"status": "critical", "message": f"Solde actuel de {solde:,.0f} MAD inférieur au seuil de {seuil:,} MAD", "recommandation": "Action urgente : accélérer les encaissements, reporter les dépenses non essentielles"}
    elif solde < seuil * 1.5:
        return {"status": "warning", "message": f"Solde de {solde:,.0f} MAD proche du seuil d'alerte de {seuil:,} MAD", "recommandation": "Surveillance renforcée : accélérer les recouvrements, maîtriser les dépenses"}
    elif solde > seuil * 3:
        return {"status": "success", "message": f"Position excellente : {solde:,.0f} MAD, marge de {solde - seuil:,.0f} MAD", "recommandation": "Envisager un remboursement anticipé ou des investissements stratégiques"}
    else:
        return {"status": "info", "message": f"Position stable : {solde:,.0f} MAD", "recommandation": "Maintenir un suivi régulier des flux de trésorerie"}

def analyser_creances(df_echeances):
    retards = df_echeances[df_echeances["statut"] == "en_retard"]
    montant = retards["montant"].sum()
    nombre = len(retards)
    if nombre == 0:
        return {"status": "success", "message": "Aucune créance en retard", "recommandation": "Le processus de recouvrement est efficace"}
    elif nombre <= 2:
        return {"status": "warning", "message": f"{nombre} facture(s) en retard pour un total de {montant:,.0f} MAD", "recommandation": "Contacter les clients immédiatement"}
    else:
        return {"status": "critical", "message": f"{nombre} factures en retard totalisant {montant:,.0f} MAD", "recommandation": "Urgent : déployer une équipe de recouvrement"}

def analyser_prevision(df_prevision, seuil, solde_initial):
    if df_prevision.empty:
        return {"status": "info", "message": "Données insuffisantes pour la prévision", "recommandation": "Ajouter davantage d'échéances programmées"}
    semaines_critiques = df_prevision[df_prevision["Solde Cumule"] < seuil]
    solde_final = df_prevision["Solde Cumule"].iloc[-1] if not df_prevision.empty else solde_initial
    if len(semaines_critiques) > 0:
        premiere_semaine = semaines_critiques.iloc[0]["Semaine"]
        return {"status": "critical", "message": f"Rupture de trésorerie prévue à la semaine {premiere_semaine}", "recommandation": "Anticiper un besoin de financement ou renégocier les délais fournisseurs"}
    elif solde_final < seuil * 1.2:
        return {"status": "warning", "message": f"Tendance tendue : solde final prévu de {solde_final:,.0f} MAD", "recommandation": "Maîtriser les dépenses, suivre les encaissements de près"}
    else:
        return {"status": "success", "message": f"Prévisions favorables : {solde_final:,.0f} MAD projeté", "recommandation": "La position permet une flexibilité opérationnelle"}

# ==================== FONCTION EXPORT CSV ====================
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ==================== HEADER ====================
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"""
    <div class="top-nav" style="margin-bottom: 0;">
        <div>
            <div class="company-name">MarocIndustrie SARL</div>
            <div class="company-sub">Ain Sebaa · Casablanca · Fabrication métallique</div>
        </div>
        <div class="badge">Tableau de bord trésorerie</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("Déconnexion", use_container_width=True):
        st.session_state.authentifie = False
        st.session_state.transactions = None
        st.session_state.echeances = None
        st.rerun()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### Paramètres")
    st.markdown("---")
    
    solde_actuel = st.session_state.transactions["solde_cumule"].iloc[-1]
    st.markdown(f"""
    <div class="param-card">
        <div class="param-label">Trésorerie actuelle</div>
        <div class="param-value">{solde_actuel:,.0f} MAD</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Seuils d'alerte")
    
    nouveau_seuil = st.slider(
        "Seuil d'alerte (MAD)",
        min_value=10000,
        max_value=150000,
        value=st.session_state.seuil_alerte,
        step=5000
    )
    if nouveau_seuil != st.session_state.seuil_alerte:
        st.session_state.seuil_alerte = nouveau_seuil
        st.cache_data.clear()
        st.rerun()
    
    nouveau_seuil_grosse = st.slider(
        "Seuil grosse échéance (MAD)",
        min_value=10000,
        max_value=100000,
        value=st.session_state.seuil_grosse_echeance,
        step=5000
    )
    if nouveau_seuil_grosse != st.session_state.seuil_grosse_echeance:
        st.session_state.seuil_grosse_echeance = nouveau_seuil_grosse
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    if st.button("Réinitialiser les valeurs par défaut"):
        st.session_state.seuil_alerte = 50000
        st.session_state.seuil_grosse_echeance = 30000
        st.cache_data.clear()
        st.rerun()
    
    with st.expander("Voir les hypothèses"):
        st.markdown(f"""
        **Hypothèses financières**
        
        | Paramètre | Valeur |
        |-----------|--------|
        | Solde initial | 120 000 MAD |
        | Seuil d'alerte | {st.session_state.seuil_alerte:,} MAD |
        | Seuil grosse échéance | {st.session_state.seuil_grosse_echeance:,} MAD |
        | Charges fixes mensuelles | 73 200 MAD |
        | Délai paiement clients | 30-60 jours |
        | Horizon de prévision | 8 semaines |
        """)

# ==================== ONGLETS ====================
onglets = st.tabs(["Tableau de bord", "Flux de trésorerie", "Échéancier", "Prévisions"])

# ==================== SECTION IMPORT ====================
with st.expander("Importer des données (CSV)", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Transactions**")
        fichier_transactions = st.file_uploader("Choisir un fichier CSV", type=["csv"], key="import_trans")
        if fichier_transactions is not None:
            df_import = importer_transactions(fichier_transactions)
            if df_import is not None:
                st.session_state.transactions = df_import
                sauvegarder_transactions(df_import)
                st.success(f"{len(df_import)} transactions importées avec succès")
                st.cache_data.clear()
                st.rerun()
    
    with col2:
        st.markdown("**Échéances**")
        fichier_echeances = st.file_uploader("Choisir un fichier CSV", type=["csv"], key="import_ech")
        if fichier_echeances is not None:
            df_import = importer_echeances(fichier_echeances)
            if df_import is not None:
                st.session_state.echeances = df_import
                sauvegarder_echeances(df_import)
                st.success(f"{len(df_import)} échéances importées avec succès")
                st.cache_data.clear()
                st.rerun()

# ==================== ONGLET 1: TABLEAU DE BORD ====================
with onglets[0]:
    df = st.session_state.transactions
    solde_actuel = df["solde_cumule"].iloc[-1]
    total_entrees = df[df["type"] == "entree"]["montant"].sum()
    total_sorties = df[df["type"] == "sortie"]["montant"].sum()
    flux_net = total_entrees - total_sorties
    
    ech = st.session_state.echeances
    seuil = st.session_state.seuil_alerte
    
    analyse_treso = analyser_position_tresorerie(solde_actuel, seuil)
    analyse_creances = analyser_creances(ech)
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_class = f"status-{analyse_treso['status']}"
        st.markdown(f"""
        <div class="insight-card {status_class}">
            <div class="insight-header"><h4>Analyse de la trésorerie</h4></div>
            <div class="insight-body">
                <div class="insight-message">{analyse_treso['message']}</div>
                <div class="insight-recommendation"><strong>Recommandation</strong><br>{analyse_treso['recommandation']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status_class = f"status-{analyse_creances['status']}"
        st.markdown(f"""
        <div class="insight-card {status_class}">
            <div class="insight-header"><h4>État des créances</h4></div>
            <div class="insight-body">
                <div class="insight-message">{analyse_creances['message']}</div>
                <div class="insight-recommendation"><strong>Recommandation</strong><br>{analyse_creances['recommandation']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### Évolution du solde")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df["date"], y=df["solde_cumule"],
        mode="lines",
        line=dict(color="#0a2540", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(10,37,64,0.05)",
        name="Solde"
    ))
    fig1.add_hline(y=seuil, line_dash="dash", line_color="#ef4444",
                   annotation_text=f"Seuil d'alerte ({seuil:,} MAD)")
    fig1.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Répartition des dépenses")
        depenses = df[df["type"] == "sortie"].groupby("categorie")["montant"].sum().reset_index()
        depenses.columns = ["Categorie", "Montant"]
        depenses["Categorie"] = depenses["Categorie"].str.replace("_", " ").str.title()
        fig2 = px.pie(depenses, values="Montant", names="Categorie", hole=0.4,
                      color_discrete_sequence=["#0a2540", "#2c7da0", "#61a5c2", "#89c2d9"])
        fig2.update_layout(height=320, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### Flux mensuels entrants / sortants")
        df["mois"] = df["date"].dt.strftime("%b %Y")
        mensuel = df.groupby(["mois", "type"])["montant"].sum().reset_index()
        fig3 = px.bar(mensuel, x="mois", y="montant", color="type",
                      barmode="group",
                      color_discrete_map={"entree": "#10b981", "sortie": "#ef4444"})
        fig3.update_layout(height=320, template="plotly_white", margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig3, use_container_width=True)

# ==================== ONGLET 2: FLUX DE TRESORERIE ====================
with onglets[1]:
    st.markdown("""
    <div class="form-container">
        <div class="form-title">Ajouter une transaction</div>
    </div>
    """, unsafe_allow_html=True)
    
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
            sauvegarder_transactions(st.session_state.transactions)
            st.success(f"Transaction ajoutée - Nouveau solde : {nouveau_solde:,.0f} MAD")
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")
    st.markdown("#### Historique des transactions")
    
    col1, col2 = st.columns([2, 2])
    with col1:
        filtre_type = st.selectbox("Filtrer par type", ["Tous", "entree", "sortie"])
    with col2:
        categories = ["Toutes"] + sorted(st.session_state.transactions["categorie"].unique().tolist())
        filtre_categorie = st.selectbox("Filtrer par catégorie", categories)
    
    df_flux = st.session_state.transactions.copy()
    if filtre_type != "Tous":
        df_flux = df_flux[df_flux["type"] == filtre_type]
    if filtre_categorie != "Toutes":
        df_flux = df_flux[df_flux["categorie"] == filtre_categorie]
    
    df_flux["date"] = df_flux["date"].dt.strftime("%d/%m/%Y")
    df_flux["Montant"] = df_flux.apply(
        lambda row: f'<span class="{"positive-amount" if row["type"] == "entree" else "negative-amount"}">{row["montant"]:,.0f} MAD</span>',
        axis=1
    )
    df_flux["Solde"] = df_flux["solde_cumule"].apply(lambda x: f"{x:,.0f} MAD")
    df_affichage = df_flux[["date", "type", "categorie", "description", "Montant", "Solde"]]
    df_affichage.columns = ["Date", "Type", "Catégorie", "Description", "Montant", "Solde"]
    
    st.write(df_affichage.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    csv_transactions = convert_df_to_csv(st.session_state.transactions)
    st.download_button(
        label="Télécharger les transactions (CSV)",
        data=csv_transactions,
        file_name="transactions.csv",
        mime="text/csv"
    )

# ==================== ONGLET 3: ECHEANCIER ====================
with onglets[2]:
    st.markdown("""
    <div class="form-container">
        <div class="form-title">Ajouter une échéance</div>
    </div>
    """, unsafe_allow_html=True)
    
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
            montant_final = nouveau_montant_ech if nouveau_type_ech == "a_encaisser" else -nouveau_montant_ech
            nouvelle_ligne_ech = pd.DataFrame([{
                "date_echeance": pd.to_datetime(nouvelle_date_ech),
                "type": nouveau_type_ech,
                "tiers": nouveau_tiers,
                "description": nouvelle_desc_ech,
                "montant": montant_final,
                "statut": nouveau_statut
            }])
            
            st.session_state.echeances = pd.concat([st.session_state.echeances, nouvelle_ligne_ech], ignore_index=True)
            sauvegarder_echeances(st.session_state.echeances)
            st.success("Échéance ajoutée avec succès")
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")
    st.markdown("#### Liste des échéances")
    
    ech = st.session_state.echeances.copy()
    aujourdhui = pd.Timestamp(datetime.now().date())
    seuil_grosse = st.session_state.seuil_grosse_echeance
    
    retards = ech[ech["statut"] == "en_retard"]
    if len(retards) > 0:
        st.markdown("**Paiements en retard**")
        cols = st.columns(min(len(retards), 4))
        for idx, (_, row) in enumerate(retards.iterrows()):
            with cols[idx % 4]:
                st.markdown(f'<div class="alert-badge">⚠️ {row["tiers"]} | {abs(row["montant"]):,.0f} MAD</div>', unsafe_allow_html=True)
    
    echeances_proches = ech[(ech["date_echeance"] <= aujourdhui + timedelta(days=7)) & 
                            (ech["statut"] == "en_attente") & 
                            (abs(ech["montant"]) >= seuil_grosse)]
    if len(echeances_proches) > 0:
        st.markdown("**Grosses échéances à venir**")
        cols = st.columns(min(len(echeances_proches), 4))
        for idx, (_, row) in enumerate(echeances_proches.iterrows()):
            with cols[idx % 4]:
                st.markdown(f'<div class="alert-badge alert-badge-warning">🔔 {row["tiers"]} | {abs(row["montant"]):,.0f} MAD</div>', unsafe_allow_html=True)
    
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
    
    html_table = '<table style="width:100%; border-collapse: collapse;">'
    html_table += '<thead><tr style="border-bottom: 2px solid #eef2f6; text-align: left;">'
    html_table += '<th style="padding: 12px 8px;">Date</th>'
    html_table += '<th style="padding: 12px 8px;">Type</th>'
    html_table += '<th style="padding: 12px 8px;">Tiers</th>'
    html_table += '<th style="padding: 12px 8px;">Description</th>'
    html_table += '<th style="padding: 12px 8px;">Montant</th>'
    html_table += '<th style="padding: 12px 8px;">Statut</th>'
    html_table += '</tr></thead><tbody>'
    
    for _, row in ech_filtre.iterrows():
        row_class = "row-encaisser" if row["type"] == "a_encaisser" else "row-payer"
        badge_class = "badge-encaisser" if row["type"] == "a_encaisser" else "badge-payer"
        badge_text = "À encaisser" if row["type"] == "a_encaisser" else "À payer"
        amount_class = "positive-amount" if row["type"] == "a_encaisser" else "negative-amount"
        
        statut_text = "En attente" if row["statut"] == "en_attente" else "En retard"
        statut_color = "#f59e0b" if row["statut"] == "en_retard" else "#10b981"
        
        html_table += f'<tr class="{row_class}" style="border-bottom: 1px solid #eef2f6;">'
        html_table += f'<td style="padding: 12px 8px;">{row["date_echeance"].strftime("%d/%m/%Y")}</td>'
        html_table += f'<td style="padding: 12px 8px;"><span class="{badge_class}">{badge_text}</span></td>'
        html_table += f'<td style="padding: 12px 8px; font-weight: 500;">{row["tiers"]}</td>'
        html_table += f'<td style="padding: 12px 8px; color: #6b7a8a;">{row["description"]}</td>'
        html_table += f'<td style="padding: 12px 8px;" class="{amount_class}">{abs(row["montant"]):,.0f} MAD</td>'
        html_table += f'<td style="padding: 12px 8px;"><span style="background: {statut_color}; color: white; padding: 4px 12px; border-radius: 40px; font-size: 11px;">{statut_text}</span></td>'
        html_table += '</tr>'
    
    html_table += '</tbody></table>'
    
    st.markdown(html_table, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        csv_echeances = convert_df_to_csv(st.session_state.echeances)
        st.download_button(
            label="Télécharger les échéances (CSV)",
            data=csv_echeances,
            file_name="echeances.csv",
            mime="text/csv"
        )
    
    total_encaisser = ech[ech["type"] == "a_encaisser"]["montant"].sum()
    total_payer = ech[ech["type"] == "a_payer"]["montant"].abs().sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total à encaisser", f"{total_encaisser:,.0f} MAD")
    col2.metric("Total à payer", f"{total_payer:,.0f} MAD")
    col3.metric("Position nette", f"{total_encaisser - total_payer:,.0f} MAD")

# ==================== ONGLET 4: PREVISIONS ====================
with onglets[3]:
    st.markdown("#### Prévision de trésorerie sur 8 semaines")
    
    donnees_prevision = st.session_state.echeances.copy()
    donnees_prevision["semaine"] = donnees_prevision["date_echeance"].dt.strftime("S%W")
    
    encaissements_hebdo = donnees_prevision[donnees_prevision["type"] == "a_encaisser"].groupby("semaine")["montant"].sum()
    decaissements_hebdo_temp = donnees_prevision[donnees_prevision["type"] == "a_payer"].groupby("semaine")["montant"].sum()
    decaissements_hebdo = decaissements_hebdo_temp.abs()
    
    toutes_semaines = sorted(set(encaissements_hebdo.index) | set(decaissements_hebdo.index))
    toutes_semaines = toutes_semaines[:8]
    
    df_prevision = pd.DataFrame({
        "Semaine": toutes_semaines,
        "Encaissements": [encaissements_hebdo.get(s, 0) for s in toutes_semaines],
        "Décaissements": [decaissements_hebdo.get(s, 0) for s in toutes_semaines],
    })
    df_prevision["Flux net"] = df_prevision["Encaissements"] - df_prevision["Décaissements"]
    
    solde_initial = st.session_state.transactions["solde_cumule"].iloc[-1]
    df_prevision["Solde Cumule"] = solde_initial + df_prevision["Flux net"].cumsum()
    
    seuil = st.session_state.seuil_alerte
    analyse_prevision = analyser_prevision(df_prevision, seuil, solde_initial)
    status_class = f"status-{analyse_prevision['status']}"
    
    st.markdown(f"""
    <div class="insight-card {status_class}" style="margin-bottom: 24px;">
        <div class="insight-header"><h4>Analyse prévisionnelle</h4></div>
        <div class="insight-body">
            <div class="insight-message">{analyse_prevision['message']}</div>
            <div class="insight-recommendation"><strong>Recommandation</strong><br>{analyse_prevision['recommandation']}</div>
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
        fig_bar.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("#### Évolution du solde prévisionnel")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_prevision["Semaine"], y=df_prevision["Solde Cumule"],
            mode="lines+markers",
            line=dict(color="#0a2540", width=2.5),
            marker=dict(size=7, color="#0a2540"),
            text=[f"{v:,.0f}" for v in df_prevision["Solde Cumule"]],
            textposition="top center"
        ))
        fig_line.add_hline(y=seuil, line_dash="dash", line_color="#ef4444",
                           annotation_text=f"Seuil d'alerte ({seuil:,} MAD)")
        fig_line.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("#### Détail des prévisions")
    df_affichage_prev = df_prevision.copy()
    for col in ["Encaissements", "Décaissements", "Flux net", "Solde Cumule"]:
        df_affichage_prev[col] = df_affichage_prev[col].apply(lambda x: f"{x:,.0f} MAD")
    st.dataframe(df_affichage_prev, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        csv_previsions = convert_df_to_csv(df_prevision)
        st.download_button(
            label="Télécharger les prévisions (CSV)",
            data=csv_previsions,
            file_name="previsions.csv",
            mime="text/csv"
        )
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Solde minimum projeté", f"{df_prevision['Solde Cumule'].min():,.0f} MAD")
    col2.metric("Solde maximum projeté", f"{df_prevision['Solde Cumule'].max():,.0f} MAD")
    col3.metric("Flux net moyen hebdomadaire", f"{df_prevision['Flux net'].mean():,.0f} MAD")
