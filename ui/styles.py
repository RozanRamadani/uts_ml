def get_custom_css():
    """Mengembalikan string CSS kustom untuk antarmuka Kira-inspired modern SaaS
    dengan dukungan penuh Light/Dark Mode dan Responsive Layout (Desktop, Tablet, Mobile).
    """
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ============================================================
       1. THEME DESIGN TOKENS (LIGHT THEME DEFAULT)
       ============================================================ */
    :root {
        --app-bg: #F8FAFC;
        --sidebar-bg: #FFFFFF;
        --sidebar-border: #E2E8F0;
        --card-bg: #FFFFFF;
        --card-bg-hover: #F8FAFC;
        --card-border: #E2E8F0;
        --card-border-hover: #CBD5E1;
        --hero-bg: linear-gradient(135deg, #FFFFFF 0%, #F5F3FF 50%, #EEF2FF 100%);
        --hero-border: #DDD6FE;
        --hero-shadow: 0 4px 20px rgba(124, 58, 237, 0.05);

        --text-main: #0F172A;
        --text-sub: #475569;
        --text-muted: #64748B;

        --accent-indigo: #4F46E5;
        --accent-indigo-light: #6366F1;
        --accent-violet: #7C3AED;
        
        --badge-indigo-bg: #EEF2FF;
        --badge-indigo-text: #4F46E5;
        --badge-indigo-border: #C7D2FE;

        --badge-violet-bg: #F5F3FF;
        --badge-violet-text: #7C3AED;
        --badge-violet-border: #DDD6FE;

        --badge-emerald-bg: #ECFDF5;
        --badge-emerald-text: #059669;
        --badge-emerald-border: #A7F3D0;

        --badge-amber-bg: #FFFBEB;
        --badge-amber-text: #D97706;
        --badge-amber-border: #FDE68A;

        --badge-slate-bg: #F1F5F9;
        --badge-slate-text: #475569;
        --badge-slate-border: #E2E8F0;

        --metric-border-top: linear-gradient(90deg, #4F46E5, #8B5CF6);
        --metric-card-bg: #FFFFFF;
        --metric-card-border: #E2E8F0;

        --form-bg: #FFFFFF;
        --form-border: #E2E8F0;
        --input-label: #334155;
        --tab-list-bg: #F1F5F9;
        --tab-active-bg: #FFFFFF;
        --tab-active-text: #4F46E5;
        --tab-inactive-text: #64748B;

        --res-pos-bg: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        --res-pos-border: #86EFAC;
        --res-pos-title: #14532D;
        --res-pos-text: #166534;

        --res-neg-bg: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        --res-neg-border: #CBD5E1;
        --res-neg-title: #0F172A;
        --res-neg-text: #475569;

        --radio-active-bg: #EEF2FF;
        --radio-active-text: #4F46E5;
        --radio-active-border: #C7D2FE;
        --radio-hover-bg: #F1F5F9;
        --radio-text: #475569;
    }

    /* ============================================================
       2. DARK THEME TOKENS (PREFERS-COLOR-SCHEME & STREAMLIT DARK)
       ============================================================ */
    @media (prefers-color-scheme: dark) {
        :root {
            --app-bg: #0E1117;
            --sidebar-bg: #161B22;
            --sidebar-border: #30363D;
            --card-bg: #1E293B;
            --card-bg-hover: #243248;
            --card-border: #334155;
            --card-border-hover: #475569;
            --hero-bg: linear-gradient(135deg, #1E1B4B 0%, #1E293B 60%, #0F172A 100%);
            --hero-border: #4338CA;
            --hero-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);

            --text-main: #F8FAFC;
            --text-sub: #CBD5E1;
            --text-muted: #94A3B8;

            --badge-indigo-bg: rgba(79, 70, 229, 0.22);
            --badge-indigo-text: #A5B4FC;
            --badge-indigo-border: rgba(99, 102, 241, 0.45);

            --badge-violet-bg: rgba(124, 58, 237, 0.22);
            --badge-violet-text: #C4B5FD;
            --badge-violet-border: rgba(139, 92, 246, 0.45);

            --badge-emerald-bg: rgba(16, 185, 129, 0.22);
            --badge-emerald-text: #6EE7B7;
            --badge-emerald-border: rgba(16, 185, 129, 0.45);

            --badge-amber-bg: rgba(245, 158, 11, 0.22);
            --badge-amber-text: #FCD34D;
            --badge-amber-border: rgba(245, 158, 11, 0.45);

            --badge-slate-bg: rgba(51, 65, 85, 0.5);
            --badge-slate-text: #CBD5E1;
            --badge-slate-border: rgba(71, 85, 105, 0.5);

            --metric-card-bg: #1E293B;
            --metric-card-border: #334155;

            --form-bg: #1E293B;
            --form-border: #334155;
            --input-label: #E2E8F0;
            --tab-list-bg: #0F172A;
            --tab-active-bg: #1E293B;
            --tab-active-text: #A5B4FC;
            --tab-inactive-text: #94A3B8;

            --res-pos-bg: linear-gradient(135deg, rgba(20, 83, 45, 0.4) 0%, rgba(22, 101, 52, 0.25) 100%);
            --res-pos-border: #15803D;
            --res-pos-title: #86EFAC;
            --res-pos-text: #BBF7D0;

            --res-neg-bg: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
            --res-neg-border: #475569;
            --res-neg-title: #F1F5F9;
            --res-neg-text: #CBD5E1;

            --radio-active-bg: rgba(79, 70, 229, 0.25);
            --radio-active-text: #C7D2FE;
            --radio-active-border: rgba(99, 102, 241, 0.5);
            --radio-hover-bg: #27354A;
            --radio-text: #CBD5E1;
        }
    }

    /* Fallback saat Streamlit force dark mode via selector internal */
    [data-theme="dark"],
    .stApp[data-theme="dark"],
    .stApp[data-test-script-runner="true"]:has([data-testid="stSidebar"][style*="rgb(14, 17, 23)"]),
    .stApp:has([data-testid="stHeader"][style*="rgb(14, 17, 23)"]) {
        --app-bg: #0E1117;
        --sidebar-bg: #161B22;
        --sidebar-border: #30363D;
        --card-bg: #1E293B;
        --card-bg-hover: #243248;
        --card-border: #334155;
        --card-border-hover: #475569;
        --hero-bg: linear-gradient(135deg, #1E1B4B 0%, #1E293B 60%, #0F172A 100%);
        --hero-border: #4338CA;
        --text-main: #F8FAFC;
        --text-sub: #CBD5E1;
        --text-muted: #94A3B8;
        --metric-card-bg: #1E293B;
        --metric-card-border: #334155;
        --form-bg: #1E293B;
        --form-border: #334155;
        --input-label: #E2E8F0;
        --tab-list-bg: #0F172A;
        --tab-active-bg: #1E293B;
        --tab-active-text: #A5B4FC;
        --tab-inactive-text: #94A3B8;
        --res-pos-bg: linear-gradient(135deg, rgba(20, 83, 45, 0.4) 0%, rgba(22, 101, 52, 0.25) 100%);
        --res-pos-border: #15803D;
        --res-pos-title: #86EFAC;
        --res-pos-text: #BBF7D0;
        --res-neg-bg: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        --res-neg-border: #475569;
        --res-neg-title: #F1F5F9;
        --res-neg-text: #CBD5E1;
        --radio-active-bg: rgba(79, 70, 229, 0.25);
        --radio-active-text: #C7D2FE;
        --radio-active-border: rgba(99, 102, 241, 0.5);
        --radio-hover-bg: #27354A;
        --radio-text: #CBD5E1;
    }

    /* ============================================================
       3. GLOBAL RESET & BASE TYPOGRAPHY
       ============================================================ */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-main);
    }

    .stApp {
        background-color: var(--app-bg);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
        max-width: 1200px;
    }

    /* ============================================================
       4. KIRA SIDEBAR & RADIO NAVIGATION
       ============================================================ */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--sidebar-border);
        box-shadow: 1px 0 3px rgba(0, 0, 0, 0.03);
    }

    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-main) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: var(--text-sub) !important;
    }

    /* Navigation Radio Items */
    section[data-testid="stSidebar"] [data-testid="stRadio"] {
        gap: 6px;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
        background: transparent;
        color: var(--radio-text) !important;
        font-weight: 500;
        font-size: 0.92rem;
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid transparent;
        transition: all 0.15s ease;
        cursor: pointer;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: var(--radio-hover-bg);
        color: var(--text-main) !important;
    }

    /* Active Radio Item */
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: var(--radio-active-bg) !important;
        color: var(--radio-active-text) !important;
        font-weight: 700;
        border: 1px solid var(--radio-active-border) !important;
        box-shadow: 0 1px 3px rgba(79, 70, 229, 0.08);
    }

    /* ============================================================
       5. KIRA CARDS & HERO
       ============================================================ */
    .kira-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.25rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        color: var(--text-main);
    }
    .kira-card:hover {
        border-color: var(--card-border-hover);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    }

    .kira-hero {
        background: var(--hero-bg);
        border: 1px solid var(--hero-border);
        border-radius: 20px;
        padding: 2.25rem 2.25rem;
        margin-bottom: 2rem;
        box-shadow: var(--hero-shadow);
        position: relative;
        overflow: hidden;
    }

    /* ============================================================
       6. BADGES & METRIC TILES
       ============================================================ */
    .kira-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.75rem;
    }
    .kira-badge-indigo {
        background: var(--badge-indigo-bg);
        color: var(--badge-indigo-text);
        border: 1px solid var(--badge-indigo-border);
    }
    .kira-badge-violet {
        background: var(--badge-violet-bg);
        color: var(--badge-violet-text);
        border: 1px solid var(--badge-violet-border);
    }
    .kira-badge-emerald {
        background: var(--badge-emerald-bg);
        color: var(--badge-emerald-text);
        border: 1px solid var(--badge-emerald-border);
    }
    .kira-badge-amber {
        background: var(--badge-amber-bg);
        color: var(--badge-amber-text);
        border: 1px solid var(--badge-amber-border);
    }
    .kira-badge-slate {
        background: var(--badge-slate-bg);
        color: var(--badge-slate-text);
        border: 1px solid var(--badge-slate-border);
    }

    /* Metric Display Tile */
    .kira-metric-tile {
        background: var(--metric-card-bg);
        border: 1px solid var(--metric-card-border);
        border-radius: 16px;
        padding: 1.25rem 1.35rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .kira-metric-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.08);
        border-color: var(--accent-indigo);
    }
    .kira-metric-tile::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--metric-border-top);
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
    }
    .kira-metric-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--text-muted);
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
        color: var(--text-main);
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
        background: var(--res-pos-bg);
        border: 2px solid var(--res-pos-border);
        border-radius: 20px;
        padding: 1.75rem;
        color: var(--res-pos-title);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.08);
    }
    .kira-result-card-negative {
        background: var(--res-neg-bg);
        border: 2px solid var(--res-neg-border);
        border-radius: 20px;
        padding: 1.75rem;
        color: var(--res-neg-title);
        box-shadow: 0 6px 20px rgba(100, 116, 139, 0.06);
    }

    /* ============================================================
       7. BUTTONS, TABS & FORMS
       ============================================================ */
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
        background: var(--card-bg) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: var(--card-bg-hover) !important;
        border-color: var(--card-border-hover) !important;
        color: var(--accent-indigo) !important;
        transform: translateY(-1px) !important;
    }

    /* Tabs Styling - Pill Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--tab-list-bg);
        border-radius: 14px;
        padding: 6px;
        gap: 6px;
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        -webkit-overflow-scrolling: touch;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.88rem;
        color: var(--tab-inactive-text);
        border: none;
        background: transparent;
        white-space: nowrap;
        transition: all 0.15s ease;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--tab-active-bg) !important;
        color: var(--tab-active-text) !important;
        font-weight: 700;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }

    /* Form Container */
    div[data-testid="stForm"] {
        border: 1px solid var(--form-border);
        border-radius: 18px;
        background: var(--form-bg);
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }

    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        color: var(--input-label) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4F46E5 0%, #8B5CF6 100%);
        border-radius: 9999px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        border-radius: 12px;
        font-weight: 600;
        color: var(--text-main) !important;
    }

    /* Alert Boxes (Info, Success) */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid var(--card-border);
    }

    /* Responsive Dataframe */
    div[data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
    }

    /* Responsive Images */
    div[data-testid="stImage"] img {
        max-width: 100% !important;
        height: auto !important;
        border-radius: 14px;
        border: 1px solid var(--card-border);
    }

    /* ============================================================
       8. RESPONSIVE MEDIA QUERIES (TABLET & MOBILE)
       ============================================================ */

    /* Tablet (769px - 1024px) */
    @media (min-width: 769px) and (max-width: 1024px) {
        .block-container {
            padding-top: 1.25rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
        .kira-hero {
            padding: 1.75rem 1.5rem;
        }
        /* 4-column KPI cards wrap to 2x2 grid */
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="column"]:nth-child(4)) {
            flex-wrap: wrap !important;
            gap: 12px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="column"]:nth-child(4)) > div[data-testid="column"] {
            width: calc(50% - 8px) !important;
            min-width: calc(50% - 8px) !important;
            flex: 1 1 calc(50% - 8px) !important;
        }
    }

    /* Mobile (<= 768px) */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-bottom: 2.5rem !important;
        }
        .kira-hero {
            padding: 1.25rem 1rem !important;
            border-radius: 16px !important;
            margin-bottom: 1.25rem !important;
        }
        .kira-hero h1 {
            font-size: 1.55rem !important;
            line-height: 1.25 !important;
        }
        .kira-hero p {
            font-size: 0.92rem !important;
        }
        .kira-card {
            padding: 1.15rem 1rem !important;
            border-radius: 16px !important;
            margin-bottom: 1rem !important;
        }
        .kira-metric-tile {
            padding: 1rem 1.1rem !important;
        }
        .kira-metric-value {
            font-size: 1.55rem !important;
        }

        /* Stack all columns vertically on mobile to prevent crushing */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 12px !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }

        /* Buttons on mobile */
        div.stButton > button {
            width: 100% !important;
        }
    }
    </style>
    """


