def get_custom_css():
    """Mengembalikan string CSS kustom untuk styling antarmuka Streamlit Kira-inspired modern SaaS."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Base Reset */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
    }

    /* Main Container & Layout */
    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 1.75rem;
        padding-bottom: 3.5rem;
        max-width: 1200px;
    }

    /* Kira-inspired Light Clean Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
        box-shadow: 1px 0 3px rgba(0, 0, 0, 0.02);
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3, 
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #334155;
    }

    /* Radio Navigation in Sidebar */
    section[data-testid="stSidebar"] [data-testid="stRadio"] {
        gap: 6px;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent;
        color: #475569 !important;
        font-weight: 500;
        font-size: 0.92rem;
        padding: 9px 14px;
        border-radius: 12px;
        border: 1px solid transparent;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
        margin-bottom: 2px;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #F1F5F9;
        color: #1E293B !important;
    }

    /* Active Radio Item */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: #EEF2FF !important;
        color: #4F46E5 !important;
        font-weight: 700;
        border: 1px solid #C7D2FE !important;
        box-shadow: 0 1px 3px rgba(79, 70, 229, 0.08);
    }

    /* Kira Badges & Pills */
    .kira-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }
    .kira-badge-indigo {
        background: #EEF2FF;
        color: #4F46E5;
        border: 1px solid #C7D2FE;
    }
    .kira-badge-violet {
        background: #F5F3FF;
        color: #7C3AED;
        border: 1px solid #DDD6FE;
    }
    .kira-badge-emerald {
        background: #ECFDF5;
        color: #059669;
        border: 1px solid #A7F3D0;
    }
    .kira-badge-amber {
        background: #FFFBEB;
        color: #D97706;
        border: 1px solid #FDE68A;
    }
    .kira-badge-slate {
        background: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
    }

    /* Kira Card Containers */
    .kira-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03), 0 1px 2px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.25rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .kira-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }

    /* Kira Hero Welcome Banner */
    .kira-hero {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5F3FF 50%, #EEF2FF 100%);
        border: 1px solid #DDD6FE;
        border-radius: 20px;
        padding: 2.25rem 2.25rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.05);
        position: relative;
        overflow: hidden;
    }

    /* Metric Display Tile */
    .kira-metric-tile {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .kira-metric-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.08);
        border-color: #C7D2FE;
    }
    .kira-metric-tile::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4F46E5, #8B5CF6);
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
    }
    .kira-metric-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .kira-metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.15;
    }
    .kira-metric-sub {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.45rem;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Prediction Result Cards */
    .kira-result-card-positive {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2px solid #86EFAC;
        border-radius: 20px;
        padding: 1.75rem;
        color: #14532D;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.1);
    }
    .kira-result-card-negative {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border: 2px solid #CBD5E1;
        border-radius: 20px;
        padding: 1.75rem;
        color: #1E293B;
        box-shadow: 0 6px 20px rgba(100, 116, 139, 0.08);
    }

    /* Mono & Code Tags */
    .kira-code-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        background: #F1F5F9;
        padding: 3px 8px;
        border-radius: 8px;
        color: #475569;
        border: 1px solid #E2E8F0;
    }

    /* Primary and Secondary Buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.35) !important;
    }

    div.stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #334155 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #F8FAFC !important;
        border-color: #CBD5E1 !important;
        color: #0F172A !important;
        transform: translateY(-1px) !important;
    }

    /* Tabs Styling - Kira Pill Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #F1F5F9;
        border-radius: 14px;
        padding: 6px;
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #64748B;
        border: none;
        background: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #FFFFFF !important;
        color: #4F46E5 !important;
        font-weight: 700;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }

    /* Streamlit Form & Inputs */
    div[data-testid="stForm"] {
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        background: #FFFFFF;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    
    /* Input Labels */
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        color: #334155 !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4F46E5 0%, #8B5CF6 100%);
        border-radius: 9999px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #FFFFFF;
        border-radius: 12px;
        font-weight: 600;
        color: #334155;
    }

    /* Alert Boxes (Info, Success) */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid #E2E8F0;
    }
    </style>
    """

