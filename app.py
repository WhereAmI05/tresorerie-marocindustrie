import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="MarocIndustrie - Treasury Management",
    page_icon="⚡",
    layout="wide"
)

# ==================== DESIGN SYSTEM PREMIUM ====================
st.markdown("""
<style>
    /* Base */
    .stApp {
        background-color: #f5f7fc;
    }
    
    /* Sidebar Premium */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9edf2;
        box-shadow: 2px 0 12px rgba(0,0,0,0.02);
    }
    
    [data-testid="stSidebar"] * {
        color: #1a2c3e !important;
    }
    
    /* Typography */
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
    
    /* KPI Cards Premium */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 20px 0;
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
    
    .kpi-trend-up {
        font-size: 12px;
        color: #10b981;
        margin-top: 6px;
    }
    
    .kpi-trend-down {
        font-size: 12px;
        color: #ef4444;
        margin-top: 6px;
    }
    
    /* Insight Cards */
    .insight-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin: 20px 0;
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
    
    /* Status Colors */
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
    
    /* Alert Banners */
    .alert-banner {
        background: #ffffff;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 16px;
        border: 1px solid #e9edf2;
        font-size: 13px;
    }
    
    .alert-banner-critical {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        color: #991b1b;
    }
    
    .alert-banner-warning {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        color: #92400e;
    }
    
    /* Tables */
    .stDataFrame {
        border: 1px solid #e9edf2 !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 32px;
        border-bottom: 1px solid #e9edf2;
        background: transparent;
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
    
    /* Buttons */
    .stButton > button {
        background-color: #0a2540;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #1a3c5e;
        transform: translateY(-1px);
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div,
    .stNumberInput > div > div {
        border-radius: 10px;
        border-color: #e2e8f0;
    }
    
    /* Metrics in sidebar */
    .sidebar-metric {
        background: #f8fafc;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
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

# ==================== DATA LOADING ====================
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

# ==================== ANALYTICS ENGINE ====================
def analyze_cash_position(balance, threshold):
    """Analyze current cash position"""
    if balance < threshold:
        return {
            "status": "critical",
            "message": f"Balance at {balance:,.0f} MAD is below {threshold:,} MAD threshold",
            "recommendation": "Immediate action required: accelerate collections, delay non-essential payments",
            "action": "Urgent: secure short-term financing"
        }
    elif balance < threshold * 1.5:
        return {
            "status": "warning",
            "message": f"Balance at {balance:,.0f} MAD is close to {threshold:,} MAD threshold",
            "recommendation": "Monitor closely: accelerate collections, control discretionary spending",
            "action": "Prepare contingency plan"
        }
    elif balance > threshold * 3:
        return {
            "status": "success",
            "message": f"Strong position: {balance:,.0f} MAD, {balance - threshold:,.0f} MAD above threshold",
            "recommendation": "Consider early debt repayment or strategic investments",
            "action": "Deploy excess cash efficiently"
        }
    else:
        return {
            "status": "info",
            "message": f"Stable position: {balance:,.0f} MAD",
            "recommendation": "Maintain regular monitoring of cash flows",
            "action": "Business as usual"
        }

def analyze_receivables(df_echeances):
    """Analyze overdue receivables"""
    overdue = df_echeances[df_echeances["statut"] == "en_retard"]
    amount = overdue["montant"].sum()
    count = len(overdue)
    
    if count == 0:
        return {
            "status": "success",
            "message": "No overdue receivables",
            "recommendation": "Collection process is effective",
            "action": "Maintain current practices"
        }
    elif count <= 2:
        return {
            "status": "warning",
            "message": f"{count} overdue invoice(s) totaling {amount:,.0f} MAD",
            "recommendation": "Contact clients immediately",
            "action": "Initiate collection process"
        }
    else:
        return {
            "status": "critical",
            "message": f"{count} overdue invoices totaling {amount:,.0f} MAD",
            "recommendation": "Urgent: deploy collection team, review credit terms",
            "action": "Escalate to management"
        }

def analyze_forecast(df_forecast, threshold, initial_balance):
    """Analyze cash forecast"""
    if df_forecast.empty:
        return {
            "status": "info",
            "message": "Insufficient data for forecast",
            "recommendation": "Add more scheduled payments/receipts",
            "action": "Complete forecast data"
        }
    
    critical_weeks = df_forecast[df_forecast["Cumulative Balance"] < threshold]
    final_balance = df_forecast["Cumulative Balance"].iloc[-1]
    
    if len(critical_weeks) > 0:
        first_week = critical_weeks.iloc[0]["Week"]
        return {
            "status": "critical",
            "message": f"Liquidity gap forecasted in week {first_week}",
            "recommendation": f"Secure {abs(final_balance):,.0f} MAD financing or renegotiate payables",
            "action": "Activate credit line"
        }
    elif final_balance < threshold * 1.2:
        return {
            "status": "warning",
            "message": f"Tight position ahead: forecasted balance {final_balance:,.0f} MAD",
            "recommendation": "Control expenses, monitor collections closely",
            "action": "Prepare mitigation measures"
        }
    else:
        return {
            "status": "success",
            "message": f"Healthy forecast: {final_balance:,.0f} MAD projected",
            "recommendation": "Position allows for operational flexibility",
            "action": "Proceed with normal operations"
        }

def analyze_upcoming_obligations(df_echeances, threshold):
    """Analyze upcoming large obligations"""
    upcoming = df_echeances[
        (df_echeances["statut"] == "en_attente") & 
        (df_echeances["montant"].abs() >= threshold)
    ]
    
    if len(upcoming) == 0:
        return None
    
    total = upcoming["montant"].abs().sum()
    return {
        "status": "warning",
        "message": f"{len(upcoming)} large obligation(s) totaling {total:,.0f} MAD due soon",
        "recommendation": "Ensure sufficient liquidity for these payments",
        "action": "Schedule payments strategically"
    }

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### MAROCINDUSTRIE")
    st.markdown("#### Treasury Dashboard")
    st.markdown("---")
    
    st.markdown("**Company Profile**")
    st.markdown("• Ain Sebaa, Casablanca")
    st.markdown("• Metal Fabrication / BTP")
    st.markdown("• 12 employees")
    st.markdown("• ~2.4M MAD annual revenue")
    
    st.markdown("---")
    
    current_balance = st.session_state.transactions["solde_cumule"].iloc[-1]
    st.markdown("**Current Cash Position**")
    if current_balance >= 80000:
        st.success(f"{current_balance:,.0f} MAD")
    elif current_balance >= 50000:
        st.warning(f"{current_balance:,.0f} MAD")
    else:
        st.error(f"{current_balance:,.0f} MAD")
    
    st.markdown("---")
    st.markdown("**Parameters**")
    
    new_threshold = st.number_input(
        "Alert Threshold (MAD)",
        min_value=10000,
        max_value=200000,
        value=st.session_state.seuil_alerte,
        step=5000
    )
    if new_threshold != st.session_state.seuil_alerte:
        st.session_state.seuil_alerte = new_threshold
        st.cache_data.clear()
        st.rerun()
    
    new_large = st.number_input(
        "Large Obligation Threshold (MAD)",
        min_value=10000,
        max_value=200000,
        value=st.session_state.seuil_grosse_echeance,
        step=5000
    )
    if new_large != st.session_state.seuil_grosse_echeance:
        st.session_state.seuil_grosse_echeance = new_large
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption("Data: Jan - Mar 2025")
    st.caption("Forecast: 8 weeks rolling")

# ==================== HEADER ====================
st.markdown('<div class="main-header">MarocIndustrie SARL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Treasury Management Dashboard | Real-time cash monitoring & forecasting</div>', unsafe_allow_html=True)

# ==================== TABS ====================
tabs = st.tabs(["Overview", "Cash Flow", "Schedule", "Forecast"])

# ==================== TAB 1: OVERVIEW ====================
with tabs[0]:
    df = st.session_state.transactions
    current_balance = df["solde_cumule"].iloc[-1]
    total_inflows = df[df["type"] == "entree"]["montant"].sum()
    total_outflows = df[df["type"] == "sortie"]["montant"].sum()
    net_cashflow = total_inflows - total_outflows
    
    ech = st.session_state.echeances
    threshold = st.session_state.seuil_alerte
    large_threshold = st.session_state.seuil_grosse_echeance
    
    # Analyses
    cash_analysis = analyze_cash_position(current_balance, threshold)
    receivables_analysis = analyze_receivables(ech)
    large_obligations = analyze_upcoming_obligations(ech, large_threshold)
    
    # KPI Row
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Current Balance</div>
            <div class="kpi-value">{current_balance:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Inflows (3M)</div>
            <div class="kpi-value">{total_inflows:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Outflows (3M)</div>
            <div class="kpi-value">{total_outflows:,.0f} MAD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        trend = "up" if net_cashflow > 0 else "down"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Net Cash Flow (3M)</div>
            <div class="kpi-value">{net_cashflow:,.0f} MAD</div>
            <div class="kpi-trend-{trend}">{'Positive' if net_cashflow > 0 else 'Negative'} trend</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights Row
    st.markdown('<div class="insight-grid">', unsafe_allow_html=True)
    
    # Cash Position Insight
    status_class = f"status-{cash_analysis['status']}"
    st.markdown(f"""
    <div class="insight-card {status_class}">
        <div class="insight-header">
            <h4>Cash Position Analysis</h4>
        </div>
        <div class="insight-body">
            <div class="insight-message">{cash_analysis['message']}</div>
            <div class="insight-reco"><strong>Recommendation</strong><br>{cash_analysis['recommendation']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Receivables Insight
    status_class = f"status-{receivables_analysis['status']}"
    st.markdown(f"""
    <div class="insight-card {status_class}">
        <div class="insight-header">
            <h4>Receivables Status</h4>
        </div>
        <div class="insight-body">
            <div class="insight-message">{receivables_analysis['message']}</div>
            <div class="insight-reco"><strong>Recommendation</strong><br>{receivables_analysis['recommendation']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Large obligations alert
    if large_obligations:
        st.markdown(f"""
        <div class="alert-banner alert-banner-warning">
            <strong>Large Obligations Alert</strong><br>
            {large_obligations['message']}<br>
            <strong>Action:</strong> {large_obligations['action']}
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Balance Evolution")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df["date"],
            y=df["solde_cumule"],
            mode="lines",
            line=dict(color="#0a2540", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(10,37,64,0.05)",
            name="Balance"
        ))
        fig1.add_hline(y=threshold, line_dash="dash", line_color="#ef4444",
                       annotation_text=f"Alert Threshold ({threshold:,} MAD)", 
                       annotation_position="top left")
        fig1.update_layout(
            height=380,
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="white",
            xaxis=dict(gridcolor="#f0f2f5"),
            yaxis=dict(gridcolor="#f0f2f5")
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Expense Breakdown")
        expenses = df[df["type"] == "sortie"].groupby("categorie")["montant"].sum().reset_index()
        expenses.columns = ["Category", "Amount"]
        expenses["Category"] = expenses["Category"].str.replace("_", " ").str.title()
        
        fig2 = px.pie(
            expenses,
            values="Amount",
            names="Category",
            hole=0.45,
            color_discrete_sequence=["#0a2540", "#1a3c5e", "#2a4c7e", "#3a5c9e", "#4a6cae"]
        )
        fig2.update_layout(height=380, template="plotly_white", showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Monthly chart
    st.markdown("#### Monthly Cash Flow")
    df["month"] = df["date"].dt.strftime("%B %Y")
    monthly = df.groupby(["month", "type"])["montant"].sum().reset_index()
    
    fig3 = px.bar(
        monthly,
        x="month",
        y="montant",
        color="type",
        barmode="group",
        color_discrete_map={"entree": "#10b981", "sortie": "#ef4444"},
        labels={"montant": "Amount (MAD)", "month": "Month", "type": "Type"}
    )
    fig3.update_layout(height=320, template="plotly_white", plot_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

# ==================== TAB 2: CASH FLOW ====================
with tabs[1]:
    st.markdown("#### Transaction History")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        filter_type = st.selectbox("Filter by Type", ["All", "entree", "sortie"])
    
    df_flow = st.session_state.transactions.copy()
    if filter_type != "All":
        df_flow = df_flow[df_flow["type"] == filter_type]
    
    display_df = df_flow.copy()
    display_df["date"] = display_df["date"].dt.strftime("%d/%m/%Y")
    display_df["montant"] = display_df["montant"].apply(lambda x: f"{x:,.0f} MAD")
    display_df["solde_cumule"] = display_df["solde_cumule"].apply(lambda x: f"{x:,.0f} MAD")
    display_df = display_df[["date", "type", "categorie", "description", "montant", "solde_cumule"]]
    display_df.columns = ["Date", "Type", "Category", "Description", "Amount", "Balance"]
    
    st.dataframe(display_df, use_container_width=True, height=450)
    
    st.markdown("---")
    st.markdown("#### Record New Transaction")
    
    with st.form("add_transaction"):
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("Date", datetime.now())
            new_type = st.selectbox("Type", ["entree", "sortie"])
            new_amount = st.number_input("Amount (MAD)", min_value=0.0, step=1000.0)
        with col2:
            new_category = st.selectbox("Category", [
                "vente_client", "acompte", "salaires", "loyer", "matieres_premieres",
                "electricite", "cnss", "tva", "maintenance", "frais_generaux"
            ])
            new_description = st.text_input("Description")
        
        submitted = st.form_submit_button("Record Transaction")
        
        if submitted and new_amount > 0 and new_description:
            last_balance = st.session_state.transactions["solde_cumule"].iloc[-1]
            if new_type == "entree":
                new_balance = last_balance + new_amount
            else:
                new_balance = last_balance - new_amount
            
            new_row = pd.DataFrame([{
                "date": pd.to_datetime(new_date),
                "type": new_type,
                "categorie": new_category,
                "description": new_description,
                "montant": new_amount,
                "solde_cumule": new_balance
            }])
            
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_row], ignore_index=True)
            save_transactions(st.session_state.transactions)
            st.success(f"Transaction recorded - New balance: {new_balance:,.0f} MAD")
            st.cache_data.clear()
            st.rerun()

# ==================== TAB 3: SCHEDULE ====================
with tabs[2]:
    st.markdown("#### Payment Schedule")
    
    ech = st.session_state.echeances.copy()
    today = pd.Timestamp(datetime.now().date())
    large_threshold = st.session_state.seuil_grosse_echeance
    
    # Alerts
    overdue = ech[ech["statut"] == "en_retard"]
    for _, row in overdue.iterrows():
        st.markdown(f"""
        <div class="alert-banner alert-banner-warning">
            <strong>Overdue Payment</strong><br>
            {row['tiers']} - {row['description']} - {row['montant']:,.0f} MAD
        </div>
        """, unsafe_allow_html=True)
    
    upcoming_large = ech[
        (ech["date_echeance"] <= today + timedelta(days=7)) & 
        (ech["statut"] == "en_attente") & 
        (ech["montant"].abs() >= large_threshold)
    ]
    for _, row in upcoming_large.iterrows():
        st.markdown(f"""
        <div class="alert-banner alert-banner-warning">
            <strong>Large Payment Due Soon</strong><br>
            {row['tiers']} - {row['montant']:,.0f} MAD on {row['date_echeance'].strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_schedule_type = st.selectbox("Filter by Type", ["All", "a_encaisser", "a_payer"])
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "en_attente", "en_retard"])
    
    filtered_ech = ech.copy()
    if filter_schedule_type != "All":
        filtered_ech = filtered_ech[filtered_ech["type"] == filter_schedule_type]
    if filter_status != "All":
        filtered_ech = filtered_ech[filtered_ech["statut"] == filter_status]
    
    display_ech = filtered_ech.copy()
    display_ech["date_echeance"] = display_ech["date_echeance"].dt.strftime("%d/%m/%Y")
    display_ech["montant"] = display_ech["montant"].apply(lambda x: f"{x:,.0f} MAD")
    display_ech = display_ech[["date_echeance", "type", "tiers", "description", "montant", "statut"]]
    display_ech.columns = ["Date", "Type", "Counterparty", "Description", "Amount", "Status"]
    
    st.dataframe(display_ech, use_container_width=True, height=400)
    
    # Totals
    total_to_receive = ech[ech["type"] == "a_encaisser"]["montant"].sum()
    total_to_pay = ech[ech["type"] == "a_payer"]["montant"].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total to Receive", f"{total_to_receive:,.0f} MAD")
    col2.metric("Total to Pay", f"{total_to_pay:,.0f} MAD")
    col3.metric("Net Position", f"{total_to_receive - total_to_pay:,.0f} MAD")
    
    st.markdown("---")
    st.markdown("#### Add New Obligation")
    
    with st.form("add_schedule"):
        col1, col2 = st.columns(2)
        with col1:
            new_schedule_date = st.date_input("Due Date", datetime.now() + timedelta(days=7))
            new_schedule_type = st.selectbox("Type", ["a_encaisser", "a_payer"])
            new_schedule_amount = st.number_input("Amount (MAD)", min_value=0.0, step=1000.0)
        with col2:
            new_schedule_counterparty = st.text_input("Counterparty")
            new_schedule_description = st.text_input("Description")
            new_schedule_status = st.selectbox("Status", ["en_attente", "en_retard"])
        
        submitted_schedule = st.form_submit_button("Record Obligation")
        
        if submitted_schedule and new_schedule_amount > 0 and new_schedule_counterparty:
            new_schedule_row = pd.DataFrame([{
                "date_echeance": pd.to_datetime(new_schedule_date),
                "type": new_schedule_type,
                "tiers": new_schedule_counterparty,
                "description": new_schedule_description,
                "montant": new_schedule_amount,
                "statut": new_schedule_status
            }])
            
            st.session_state.echeances = pd.concat([st.session_state.echeances, new_schedule_row], ignore_index=True)
            save_echeances(st.session_state.echeances)
            st.success("Obligation recorded successfully")
            st.cache_data.clear()
            st.rerun()

# ==================== TAB 4: FORECAST ====================
with tabs[3]:
    st.markdown("#### 8-Week Cash Forecast")
    
    forecast_data = st.session_state.echeances.copy()
    forecast_data["week"] = forecast_data["date_echeance"].dt.strftime("W%W")
    
    weekly_inflows = forecast_data[forecast_data["type"] == "a_encaisser"].groupby("week")["montant"].sum()
    weekly_outflows = forecast_data[forecast_data["type"] == "a_payer"].groupby("week")["montant"].sum()
    
    all_weeks = sorted(set(weekly_inflows.index) | set(weekly_outflows.index))
    all_weeks = all_weeks[:8]
    
    forecast_df = pd.DataFrame({
        "Week": all_weeks,
        "Inflows": [weekly_inflows.get(w, 0) for w in all_weeks],
        "Outflows": [weekly_outflows.get(w, 0) for w in all_weeks],
    })
    forecast_df["Net Flow"] = forecast_df["Inflows"] - forecast_df["Outflows"]
    
    starting_balance = st.session_state.transactions["solde_cumule"].iloc[-1]
    forecast_df["Cumulative Balance"] = starting_balance + forecast_df["Net Flow"].cumsum()
    
    threshold = st.session_state.seuil_alerte
    
    # Forecast analysis
    forecast_analysis = analyze_forecast(forecast_df, threshold, starting_balance)
    status_class = f"status-{forecast_analysis['status']}"
    
    st.markdown(f"""
    <div class="insight-card {status_class}" style="margin-bottom: 20px;">
        <div class="insight-header">
            <h4>Forecast Analysis</h4>
        </div>
        <div class="insight-body">
            <div class="insight-message">{forecast_analysis['message']}</div>
            <div class="insight-reco"><strong>Recommendation</strong><br>{forecast_analysis['recommendation']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Weekly Flows")
        bar_df = forecast_df.melt(id_vars=["Week"], value_vars=["Inflows", "Outflows"],
                                   var_name="Type", value_name="Amount")
        fig_bar = px.bar(bar_df, x="Week", y="Amount", color="Type",
                         barmode="group",
                         color_discrete_map={"Inflows": "#10b981", "Outflows": "#ef4444"})
        fig_bar.update_layout(height=380, template="plotly_white", plot_bgcolor="white")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("#### Cumulative Forecast")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=forecast_df["Week"],
            y=forecast_df["Cumulative Balance"],
            mode="lines+markers",
            line=dict(color="#0a2540", width=2.5),
            marker=dict(size=7, color="#0a2540"),
            text=[f"{v:,.0f}" for v in forecast_df["Cumulative Balance"]],
            textposition="top center",
            textfont=dict(size=11)
        ))
        fig_line.add_hline(y=threshold, line_dash="dash", line_color="#ef4444",
                           annotation_text=f"Alert Threshold ({threshold:,} MAD)")
        fig_line.update_layout(height=380, template="plotly_white", plot_bgcolor="white")
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Detailed table
    st.markdown("#### Forecast Details")
    display_forecast = forecast_df.copy()
    for col in ["Inflows", "Outflows", "Net Flow", "Cumulative Balance"]:
        display_forecast[col] = display_forecast[col].apply(lambda x: f"{x:,.0f} MAD")
    st.dataframe(display_forecast, use_container_width=True)
    
    # Key metrics
    st.markdown("#### Key Forecast Metrics")
    col1, col2, col3 = st.columns(3)
    
    min_balance = forecast_df["Cumulative Balance"].min()
    max_balance = forecast_df["Cumulative Balance"].max()
    avg_net_flow = forecast_df["Net Flow"].mean()
    
    col1.metric("Minimum Projected Balance", f"{min_balance:,.0f} MAD",
                delta=f"{min_balance - starting_balance:+,.0f} MAD" if min_balance != starting_balance else None)
    col2.metric("Maximum Projected Balance", f"{max_
