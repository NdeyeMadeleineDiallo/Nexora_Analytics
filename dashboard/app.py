import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================
# CONFIGURATION GÉNÉRALE
# ============================================

st.set_page_config(
    page_title="Nexora Analytics",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]

SEGMENTS_PATH = BASE_DIR / "data" / "processed" / "client_segments_final.csv"
MODEL_PERF_PATH = BASE_DIR / "reports" / "model_performance.csv"
CLUSTER_SCORE_PATH = BASE_DIR / "reports" / "clustering_scores.csv"
LOGO_PATH = BASE_DIR / "dashboard" / "assets" / "nexora_logo.svg"

# ============================================
# STYLE CSS
# ============================================

st.markdown("""
<style>
    .main {
        background-color: #F8FAFC;
    }

    .title-box {
        background: linear-gradient(135deg, #0F172A 0%, #111827 100%);
        padding: 30px;
        border-radius: 22px;
        border-bottom: 8px solid #06B6D4;
        box-shadow: 0 10px 30px rgba(15,23,42,0.25);
        margin-bottom: 25px;
    }

    .title-box h1 {
        color: white;
        font-size: 42px;
        margin: 0;
        font-weight: 800;
    }

    .title-box p {
        color: #CBD5E1;
        font-size: 18px;
        margin-top: 10px;
    }

    .section-box {
        display: inline-block;
        border-left: 5px solid #06B6D4;
        background: #ECFEFF;
        padding: 10px 14px;
        border-radius: 10px;
        font-family: Segoe UI;
        margin-top: 18px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(15,23,42,0.06);
    }

    .section-box h3 {
        margin: 0;
        color: #0F172A;
        font-size: 18px;
        font-weight: 700;
    }

    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(15,23,42,0.08);
        border-left: 6px solid #7C3AED;
    }

    .metric-card h4 {
        color: #64748B;
        margin: 0;
        font-size: 15px;
    }

    .metric-card h2 {
        color: #0F172A;
        margin-top: 8px;
        font-size: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=320)

st.markdown("""
<div class="title-box">
    <h1>Nexora Analytics</h1>
    <p>Dashboard IA — Détection de fraude bancaire & Segmentation intelligente des clients</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# CHARGEMENT DES DONNÉES
# ============================================

@st.cache_data
def load_data():
    segments = pd.read_csv(SEGMENTS_PATH) if SEGMENTS_PATH.exists() else pd.DataFrame()
    model_perf = pd.read_csv(MODEL_PERF_PATH) if MODEL_PERF_PATH.exists() else pd.DataFrame()
    cluster_scores = pd.read_csv(CLUSTER_SCORE_PATH) if CLUSTER_SCORE_PATH.exists() else pd.DataFrame()
    return segments, model_perf, cluster_scores

segments, model_perf, cluster_scores = load_data()

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("Nexora Analytics")
st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Choisir une section",
    [
        "Vue d’ensemble",
        "Détection de fraude",
        "Segmentation client",
        "Évaluation clustering"
    ]
)

# ============================================
# PAGE 1 — VUE D’ENSEMBLE
# ============================================

if page == "Vue d’ensemble":

    st.markdown("""
    <div class="section-box">
        <h3>Vue d’ensemble du projet</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Clients analysés</h4>
            <h2>{len(segments) if not segments.empty else 0}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        nb_segments = segments["Segment_Client"].nunique() if "Segment_Client" in segments.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <h4>Segments clients</h4>
            <h2>{nb_segments}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        nb_models = len(model_perf) if not model_perf.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h4>Modèles fraude testés</h4>
            <h2>{nb_models}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    if not segments.empty and "Segment_Client" in segments.columns:
        fig = px.pie(
            segments,
            names="Segment_Client",
            hole=0.55,
            title="Répartition des segments clients",
            color_discrete_sequence=[
                "#06B6D4",
                "#7C3AED",
                "#0F172A",
                "#94A3B8",
                "#CBD5E1"
            ]
        )

        fig.update_layout(
            template="plotly_white",
            height=600,
            title_x=0.5
        )

        st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 2 — DÉTECTION DE FRAUDE
# ============================================

elif page == "Détection de fraude":

    st.markdown("""
    <div class="section-box">
        <h3>Performance des modèles de fraude</h3>
    </div>
    """, unsafe_allow_html=True)

    if model_perf.empty:
        st.warning("Le fichier model_performance.csv est introuvable dans reports/.")
    else:
        st.dataframe(model_perf, use_container_width=True)

        fig = px.bar(
            model_perf,
            x="Modèle",
            y="F1-Score",
            color="F1-Score",
            text="F1-Score",
            color_continuous_scale=[
                "#06B6D4",
                "#7C3AED",
                "#0F172A"
            ],
            title="Comparaison des modèles selon le F1-Score"
        )

        fig.update_traces(
            texttemplate="%{text:.3f}",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_white",
            height=600,
            title_x=0.5,
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 3 — SEGMENTATION CLIENT
# ============================================

elif page == "Segmentation client":

    st.markdown("""
    <div class="section-box">
        <h3>Analyse des segments clients</h3>
    </div>
    """, unsafe_allow_html=True)

    if segments.empty:
        st.warning("Le fichier client_segments_final.csv est introuvable dans data/processed/.")
    else:
        segment_filter = st.multiselect(
            "Filtrer par segment",
            options=segments["Segment_Client"].unique(),
            default=list(segments["Segment_Client"].unique())
        )

        filtered_segments = segments[
            segments["Segment_Client"].isin(segment_filter)
        ]

        st.dataframe(
            filtered_segments.head(100),
            use_container_width=True
        )

        if "Income" in filtered_segments.columns:
            fig_income = px.box(
                filtered_segments,
                x="Segment_Client",
                y="Income",
                color="Segment_Client",
                title="Distribution des revenus par segment",
                color_discrete_sequence=[
                    "#06B6D4",
                    "#7C3AED",
                    "#0F172A",
                    "#94A3B8",
                    "#CBD5E1"
                ]
            )

            fig_income.update_layout(
                template="plotly_white",
                height=600,
                title_x=0.5
            )

            st.plotly_chart(fig_income, use_container_width=True)

        spending_cols = [
            "MntWines",
            "MntMeatProducts",
            "MntGoldProds"
        ]

        available_spending = [
            col for col in spending_cols
            if col in filtered_segments.columns
        ]

        if available_spending:
            spending_profile = (
                filtered_segments
                .groupby("Segment_Client")[available_spending]
                .mean()
                .reset_index()
            )

            fig_spending = px.bar(
                spending_profile,
                x="Segment_Client",
                y=available_spending,
                barmode="group",
                title="Dépenses moyennes par segment"
            )

            fig_spending.update_layout(
                template="plotly_white",
                height=650,
                title_x=0.5
            )

            st.plotly_chart(fig_spending, use_container_width=True)

# ============================================
# PAGE 4 — ÉVALUATION CLUSTERING
# ============================================

elif page == "Évaluation clustering":

    st.markdown("""
    <div class="section-box">
        <h3>Évaluation des modèles de clustering</h3>
    </div>
    """, unsafe_allow_html=True)

    if cluster_scores.empty:
        st.warning("Le fichier clustering_scores.csv est introuvable dans reports/.")
    else:
        st.dataframe(cluster_scores, use_container_width=True)

        fig = px.bar(
            cluster_scores,
            x="Modèle",
            y="Silhouette Score",
            color="Silhouette Score",
            text="Silhouette Score",
            color_continuous_scale=[
                "#06B6D4",
                "#7C3AED",
                "#0F172A"
            ],
            title="Comparaison des modèles de clustering"
        )

        fig.update_traces(
            texttemplate="%{text:.3f}",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_white",
            height=600,
            title_x=0.5,
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)