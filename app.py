"""
Sunwa-AI (सुनवाई-AI) - Public Grievance Root-Cause & Action Prioritizer
Main Streamlit Application Entry Point.
Provides distinct Administrative Command Center and Citizen Grievance Portal.
Supports full English, Hindi (हिंदी), and Marathi (मराठी) localization.
"""

import streamlit as st
import os

from components.shared_ui import apply_custom_styles, t
from components.admin_dashboard import render_admin_dashboard
from components.citizen_portal import render_citizen_portal
from engine.pipeline import run_full_pipeline

# Configure application layout
st.set_page_config(
    page_title="Sunwa-AI (सुनवाई-AI)",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply accessible high-contrast CSS styling
apply_custom_styles()

# Initialize session state variables
if "language" not in st.session_state:
    st.session_state["language"] = "en"

if "pipeline_data" not in st.session_state:
    st.session_state["pipeline_data"] = None


def get_pipeline_data(force_refresh: bool = False):
    """
    Returns pipeline data from session state, or runs the pipeline
    with informative staged progress indicators if not yet initialized.
    """
    if st.session_state["pipeline_data"] is not None and not force_refresh:
        return st.session_state["pipeline_data"]

    # Render staged progress container
    progress_container = st.empty()
    with progress_container.container():
        st.markdown("### ⚙️ **Sunwa-AI Civic Intelligence Engine**")
        st.caption("Initializing grievance clustering, geospatial resolution, and priority scoring...")
        p_bar = st.progress(0.0)
        p_status = st.empty()

        def update_progress(stage: str, msg: str, pct: float):
            p_bar.progress(pct)
            p_status.markdown(f"**Stage [{stage.upper()}]:** {msg}")

        try:
            complaints, clusters, landmarks, diagnostics = run_full_pipeline(
                enable_llm_fallback=True,
                max_llm_calls=3,
                progress_callback=update_progress
            )
            st.session_state["pipeline_data"] = (complaints, clusters, landmarks, diagnostics)
        except Exception as err:
            st.error(f"❌ Error during pipeline execution: {str(err)}")
            raise err

    # Clear progress elements once processing finishes
    progress_container.empty()
    return st.session_state["pipeline_data"]


# Load or retrieve pipeline data
complaints, clusters, landmarks, diagnostics = get_pipeline_data()

# Sidebar: Branding, Portal Switcher, and Localization
with st.sidebar:
    st.markdown("## 🏛️ **Sunwa-AI**")
    st.markdown("<p style='font-size: 0.85rem; color: #94a3b8; margin-top: -10px;'>सुनवाई-AI Civic Decision Support</p>", unsafe_allow_html=True)

    # Language Switcher
    lang_options = {
        "English": "en",
        "हिंदी (Hindi)": "hi",
        "मराठी (Marathi)": "mr"
    }
    cur_lang_code = st.session_state["language"]
    default_idx = 0
    if cur_lang_code == "hi":
        default_idx = 1
    elif cur_lang_code == "mr":
        default_idx = 2

    sel_lang_label = st.selectbox(
        f"🌐 {t('language_label')}",
        list(lang_options.keys()),
        index=default_idx,
        key="lang_selector"
    )
    new_lang_code = lang_options[sel_lang_label]
    if new_lang_code != st.session_state["language"]:
        st.session_state["language"] = new_lang_code
        st.rerun()

    st.markdown("---")

    # Portal Selector (Supports query param e.g. ?portal=citizen)
    query_params = st.query_params
    default_portal = "admin"
    if query_params.get("portal") == "citizen":
        default_portal = "citizen"

    portal_choice = st.radio(
        t("portal_switch"),
        options=["admin", "citizen"],
        format_func=lambda x: f"🏛️ {t('portal_admin')}" if x == "admin" else f"🗣️ {t('portal_citizen')}",
        index=0 if default_portal == "admin" else 1,
        key="portal_radio"
    )

    admin_view = "overview"
    if portal_choice == "admin":
        st.markdown("---")
        st.markdown("### 📋 Navigation")
        nav_items = {
            "overview": f"🏛️ {t('nav_overview')}",
            "priority_queue": f"⚡ {t('nav_priority_queue')}",
            "evidence_panel": f"📁 {t('nav_evidence_panel')}",
            "incident_map": f"🗺️ {t('nav_incident_map')}",
            "action_center": f"🛠️ {t('nav_action_center')}",
            "alert_queue": f"🔔 {t('nav_alert_queue')}",
            "intervention_tracking": f"📈 {t('nav_intervention_tracking')}",
            "settings": f"⚙️ {t('nav_settings')}"
        }
        selected_nav_label = st.radio(
            "Select Section",
            list(nav_items.values()),
            label_visibility="collapsed"
        )
        # Invert lookup
        for k, v in nav_items.items():
            if v == selected_nav_label:
                admin_view = k
                break

    st.markdown("---")
    if st.button(f"🔄 {t('btn_run_pipeline')}", use_container_width=True):
        st.session_state["pipeline_data"] = None
        st.rerun()

    st.markdown("<div style='margin-top: 30px; font-size: 0.75rem; color: #64748b;'>Sunwa-AI v2.0 • Hackathon PS7 Rebuild<br>Navi Mumbai Municipal Corporation</div>", unsafe_allow_html=True)


# Main Content Area
if portal_choice == "citizen":
    render_citizen_portal()
else:
    render_admin_dashboard(complaints, clusters, landmarks, admin_view)
