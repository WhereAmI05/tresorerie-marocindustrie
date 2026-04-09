import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="MarocIndustrie - Treasury Management",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DESIGN SYSTEM ULTRA PREMIUM ====================
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
    
    .kpi-card {
        background: white;
        border-radius: 24px;
        padding: 20px 24px;
        transition: all 0.2s ease;
        border: 1px solid rgba(0,0,0,0.04);
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
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
    
    .kpi-trend-up { color: #10b981; font-size: 12px; margin-top: 8px; }
    .kpi-trend-down { color: #ef4444; font-size: 12px; margin-top: 8px; }
    
    .insight-card {
        background: white;
        border-radius: 20px;
        border: 1px solid rgba(0,0,0,0.04);
        overflow: hidden;
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
    
    .alert-critical {
        background: #fef2f2;
        border: 1px solid #fee2e2;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 20px;
        color: #991b1b;
        font-size: 13px;
    }
    
    .alert-warning {
        background: #fffbeb;
        border: 1px solid #fef3c7;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 20px;
        color: #92400e;
    }
    
    .alert-success {
        background: #f0fdf4;
        border: 1px solid #dcfce7;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 20px;
        color: #166534;
    }
    
    .positive-amount {
        color: #10b981;
        font-weight: 600;
    }
    
    .negative-amount {
        color: #ef4444;
        font-weight: 600;
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
</style>
""", unsafe_allow_html=True)

# ==================== CONFIGURATION ====================
if "seuil_alerte" not in st.session_state:
    st.session_state.seuil_alerte = 50000
if "seuil_grosse_echeance" not in st.session_state:
    st.session_state.seuil_grosse_echeance = 30000
if "monthly_salary" not in st.session_state:
    st.session_state.monthly_salary = 45000
if "monthly_rent" not in st.session_state:
    st.session_state.monthly_rent = 8000
if "monthly_cnss" not in st.session_state:
    st.session_state.monthly_cnss = 9200

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

# ==================== ANALYTICS FUNCTIONS ====================
def analyze_cash_position(balance, threshold):
    if balance < threshold:
        return {"status": "critical", "message": f"Balance at {balance:,.0f} MAD below {threshold:,} MAD threshold", "recommendation": "Immediate action: accelerate collections, delay non-essential payments"}
    elif balance < threshold * 1.5:
        return {"status": "warning", "message": f"Balance at {balance:,.0f} MAD close to {threshold:,} MAD threshold", "recommendation": "Monitor closely: accelerate collections, control spending"}
    elif balance > threshold * 3:
        return {"status": "success", "message": f"Excellent position: {balance:,.0f} MAD above threshold", "recommendation": "Consider early debt repayment or strategic investments"}
    else:
        return {"status": "info", "message": f"Stable position: {balance:,.0f} MAD", "recommendation": "Maintain regular monitoring of cash flows"}

def analyze_receivables(df_echeances):
    overdue = df_echeances[df_echeances["statut"] == "en_retard"]
    amount = overdue["montant"].sum()
    count = len(overdue)
    if count == 0:
        return {"status": "success", "message": "No overdue receivables", "recommendation": "Collection process is effective"}
    elif count <= 2:
        return {"status": "warning", "message": f"{count} overdue invoice(s) totaling {amount:,.0f} MAD", "recommendation": "Contact clients immediately"}
    else:
        return {"status": "critical", "message": f"{count} overdue invoices totaling {amount:,.0f} MAD", "recommendation": "Urgent: deploy collection team"}

def analyze_forecast(df_forecast, threshold, initial_balance):
    if df_forecast.empty:
        return {"status": "info", "message": "Insufficient data for forecast", "recommendation": "Add more scheduled payments/receipts"}
    critical_weeks = df_forecast[df_forecast["Cumulative Balance"] < threshold]
    final_balance = df_forecast["Cumulative Balance"].iloc[-1] if not df_forecast.empty else initial_balance
    if len(critical_weeks) > 0:
        first_week = critical_weeks.iloc[0]["Week"]
        return {"status": "critical", "message": f"Liquidity gap forecasted in week {first_week}", "recommendation": "Secure financing or renegotiate payables"}
    elif final_balance < threshold * 1.2:
        return {"status": "warning", "message": f"Tight position ahead: forecasted balance {final_balance:,.0f} MAD", "recommendation": "Control expenses, monitor collections"}
    else:
        return {"status": "success", "message": f"Healthy forecast: {final_balance:,.0f} MAD projected", "recommendation": "Position allows operational flexibility"}

# ==================== HEADER ====================
st.markdown(f"""
<div class="top-nav">
    <div>
        <div class="company-name">MarocIndustrie SARL</div>
        <div class="company-sub">Ain Sebaa · Casablanca · Metal Fabrication</div>
    </div>
    <div class="badge">Treasury Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚙️ Parameters")
    st.markdown("---")
    
    current_balance = st.session_state.transactions["solde_cumule"].iloc[-1]
    st.markdown(f"""
    <div class="param-card">
        <div class="param-label">Current Cash Position</div>
        <div class="param-value">{current_balance:,.0f} MAD</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Alert Thresholds")
    
    new_threshold = st.slider(
        "Alert Threshold (MAD)",
        min_value=10000,
        max_value=150000,
        value=st.session_state.seuil_alerte,
        step=5000,
        help="When balance falls below this, a critical alert is triggered"
    )
    if new_threshold != st.session_state.seuil_alerte:
        st.session_state.seuil_alerte = new_threshold
        st.cache_data.clear()
        st.rerun()
    
    new_large = st.slider(
        "Large Obligation Threshold (MAD)",
        min_value=10000,
        max_value=100000,
        value=st.session_state.seuil_grosse_echeance,
        step=5000,
        help="Obligations above this amount trigger a warning alert"
    )
    if new_large != st.session_state.seuil_grosse_echeance:
        st.session_state.seuil_grosse_echeance = new_large
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### Company Assumptions")
    
    col1, col2 = st.columns(2)
    with col1:
        new_salary = st.number_input(
            "Monthly Salary (MAD)",
            min_value=20000,
            max_value=100000,
            value=st.session_state.monthly_salary,
            step=5000
        )
        if new_salary != st.session_state.monthly_salary:
            st.session_state.monthly_salary = new_salary
    
    with col2:
        new_rent = st.number_input(
            "Monthly Rent (MAD)",
            min_value=3000,
            max_value=30000,
            value=st.session_state.monthly_rent,
            step=1000
        )
        if new_rent != st.session_state.monthly_rent:
            st.session_state.monthly_rent = new_rent
    
    new_cnss = st.number_input(
        "Monthly CNSS (MAD)",
        min_value=3000,
        max_value=20000,
        value=st.session_state.monthly_cnss,
        step=500
    )
    if new_cnss != st.session_state.monthly_cnss:
        st.session_state.monthly_cnss = new_cnss
    
    st.markdown("---")
    if st.button("🔄 Reset to Default Values"):
        st.session_state.seuil_alerte = 50000
        st.session_state.seuil_grosse_echeance = 30000
        st.session_state.monthly_salary = 45000
        st.session_state.monthly_rent = 8000
        st.session_state.monthly_cnss = 9200
        st.cache_data.clear()
        st.rerun()
    
    with st.expander("📋 View All Hypotheses"):
        st.markdown(f"""
        **Financial Assumptions**
        | Parameter | Value |
        |-----------|-------|
        | Initial Balance | 120,000 MAD |
        | Alert Threshold | {st.session_state.seuil_alerte:,} MAD |
        | Large Obligation Threshold | {st.session_state.seuil_grosse_echeance:,} MAD |
        | Monthly Salaries | {st.session_state.monthly_salary:,} MAD |
        | Monthly Rent | {st.session_state.monthly_rent:,} MAD |
        | Monthly CNSS | {st.session_state.monthly_cnss:,} MAD |
        | Payment Delay (Clients) | 30-60 days |
        | Forecast Horizon | 8 weeks |
        
        **Technical Assumptions**
        - Data storage: CSV files
        - Hosting: Streamlit Cloud
        - Charts: Plotly interactive
        - Updates: Real-time on form submit
        """)

# ==================== MAIN CONTENT ====================
tabs = st.tabs(["📊 Overview", "💰 Cash Flow", "📅 Schedule", "🔮 Forecast"])

# ==================== TAB 1: OVERVIEW ====================
with tabs[0]:
    df = st.session_state.transactions
    current_balance = df["solde_cumule"].iloc[-1]
    total_inflows = df[df["type"] == "entree"]["montant"].sum()
    total_outflows = df[df["type"] == "sortie"]["montant"].sum()
    net_cashflow = total_inflows - total_outflows
    
    ech = st.session_state.echeances
    threshold = st.session_state.seuil_alerte
    
    cash_analysis = analyze_cash_position(current_balance, threshold)
    receivables_analysis = analyze_receivables(ech)
    
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
        trend_class = "kpi-trend-up" if net_cashflow > 0 else "kpi-trend-down"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Net Cash Flow (3M)</div>
            <div class="kpi-value">{net_cashflow:,.0f} MAD</div>
            <div class="{trend_class}">{'Positive' if net_cashflow > 0 else 'Negative'} trend</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_class = f"status-{cash_analysis['status']}"
        st.markdown(f"""
        <div class="insight-card {status_class}">
            <div class="insight-header"><h4>Cash Position Analysis</h4></div>
            <div class="insight-body">
                <div class="insight-message">{cash_analysis['message']}</div>
                <div class="insight-recommendation"><strong>Recommendation</strong><br>{cash_analysis['recommendation']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status_class = f"status-{receivables_analysis['status']}"
        st.markdown(f"""
        <div class="insight-card {status_class}">
            <div class="insight-header"><h4>Receivables Status</h4></div>
            <div class="insight-body">
                <div class="insight-message">{receivables_analysis['message']}</div>
                <div class="insight-recommendation"><strong>Recommendation</strong><br>{receivables_analysis['recommendation']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### Balance Evolution")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df["date"], y=df["solde_cumule"],
        mode="lines",
        line=dict(color="#0a2540", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(10,37,64,0.05)",
        name="Balance"
    ))
    fig1.add_hline(y=threshold, line_dash="dash", line_color="#ef4444",
                   annotation_text=f"Alert Threshold ({threshold:,} MAD)")
    fig1.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Expense Breakdown")
        expenses = df[df["type"] == "sortie"].groupby("categorie")["montant"].sum().reset_index()
        expenses.columns = ["Category", "Amount"]
        expenses["Category"] = expenses["Category"].str.replace("_", " ").str.title()
        fig2 = px.pie(expenses, values="Amount", names="Category", hole=0.4,
                      color_discrete_sequence=["#0a2540", "#2c7da0", "#61a5c2", "#89c2d9"])
        fig2.update_layout(height=320, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### Monthly Cash Flow")
        df["month"] = df["date"].dt.strftime("%b %Y")
        monthly = df.groupby(["month", "type"])["montant"].sum().reset_index()
        fig3 = px.bar(monthly, x="month", y="montant", color="type",
                      barmode="group",
                      color_discrete_map={"entree": "#10b981", "sortie": "#ef4444"})
        fig3.update_layout(height=320, template="plotly_white", margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig3, use_container_width=True)

# ==================== TAB 2: CASH FLOW ====================
with tabs[1]:
    st.markdown("#### Transaction History")
    
    df_flow = st.session_state.transactions.copy()
    df_flow["date"] = df_flow["date"].dt.strftime("%d/%m/%Y")
    df_flow["Amount"] = df_flow.apply(
        lambda row: f'<span class="{"positive-amount" if row["type"] == "entree" else "negative-amount"}">{row["montant"]:,.0f} MAD</span>',
        axis=1
    )
    df_flow["Balance"] = df_flow["solde_cumule"].apply(lambda x: f"{x:,.0f} MAD")
    df_display = df_flow[["date", "type", "categorie", "description", "Amount", "Balance"]]
    df_display.columns = ["Date", "Type", "Category", "Description", "Amount", "Balance"]
    
    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    
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
    
    overdue = ech[ech["statut"] == "en_retard"]
    for _, row in overdue.iterrows():
        st.markdown(f"""
        <div class="alert-warning">
            <strong>⚠️ Overdue Payment</strong><br>
            {row['tiers']} - {row['description']} - <span class="negative-amount">{row['montant']:,.0f} MAD</span>
        </div>
        """, unsafe_allow_html=True)
    
    upcoming_large = ech[(ech["date_echeance"] <= today + timedelta(days=7)) & 
                         (ech["statut"] == "en_attente") & 
                         (ech["montant"].abs() >= large_threshold)]
    for _, row in upcoming_large.iterrows():
        st.markdown(f"""
        <div class="alert-warning">
            <strong>⚠️ Large Payment Due Soon</strong><br>
            {row['tiers']} - {row['montant']:,.0f} MAD on {row['date_echeance'].strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)
    
    ech["date_echeance"] = ech["date_echeance"].dt.strftime("%d/%m/%Y")
    ech["Amount"] = ech.apply(
        lambda row: f'<span class="{"positive-amount" if row["type"] == "a_encaisser" else "negative-amount"}">{abs(row["montant"]):,.0f} MAD</span>',
        axis=1
    )
    ech_display = ech[["date_echeance", "type", "tiers", "description", "Amount", "statut"]]
    ech_display.columns = ["Date", "Type", "Counterparty", "Description", "Amount", "Status"]
    
    st.write(ech_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    total_to_receive = ech[ech["type"] == "a_encaisser"]["montant"].sum()
    total_to_pay = ech[ech["type"] == "a_payer"]["montant"].abs().sum()
    
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
            final_amount = new_schedule_amount if new_schedule_type == "a_encaisser" else -new_schedule_amount
            new_schedule_row = pd.DataFrame([{
                "date_echeance": pd.to_datetime(new_schedule_date),
                "type": new_schedule_type,
                "tiers": new_schedule_counterparty,
                "description": new_schedule_description,
                "montant": final_amount,
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
    weekly_outflows = forecast_data[forecast_data["type"] == "a_payer"].groupby("week")["montant"].abs().sum()
    
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
    forecast_analysis = analyze_forecast(forecast_df, threshold, starting_balance)
    status_class = f"status-{forecast_analysis['status']}"
    
    st.markdown(f"""
    <div class="insight-card {status_class}" style="margin-bottom: 24px;">
        <div class="insight-header"><h4>Forecast Analysis</h4></div>
        <div class="insight-body">
            <div class="insight-message">{forecast_analysis['message']}</div>
            <div class="insight-recommendation"><strong>Recommendation</strong><br>{forecast_analysis['recommendation']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Weekly Flows")
        bar_df = forecast_df.melt(id_vars=["Week"], value_vars=["Inflows", "Outflows"],
                                   var_name="Type", value_name="Amount")
        fig_bar = px.bar(bar_df, x="Week", y="Amount", color="Type",
                         barmode="group",
                         color_discrete_map={"Inflows": "#10b981", "Outflows": "#ef4444"})
        fig_bar.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("#### Cumulative Forecast")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=forecast_df["Week"], y=forecast_df["Cumulative Balance"],
            mode="lines+markers",
            line=dict(color="#0a2540", width=2.5),
            marker=dict(size=7, color="#0a2540"),
            text=[f"{v:,.0f}" for v in forecast_df["Cumulative Balance"]],
            textposition="top center"
        ))
        fig_line.add_hline(y=threshold, line_dash="dash", line_color="#ef4444",
                           annotation_text=f"Alert Threshold ({threshold:,} MAD)")
        fig_line.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("#### Forecast Details")
    display_forecast = forecast_df.copy()
    for col in ["Inflows", "Outflows", "Net Flow", "Cumulative Balance"]:
        display_forecast[col] = display_forecast[col].apply(lambda x: f"{x:,.0f} MAD")
    st.dataframe(display_forecast, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Min Projected Balance", f"{forecast_df['Cumulative Balance'].min():,.0f} MAD")
    col2.metric("Max Projected Balance", f"{forecast_df['Cumulative Balance'].max():,.0f} MAD")
    col3.metric("Avg Weekly Net Flow", f"{forecast_df['Net Flow'].mean():,.0f} MAD")
