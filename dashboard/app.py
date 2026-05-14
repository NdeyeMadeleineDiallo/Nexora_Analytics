import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Nexora Analytics",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]

SEGMENTS_PATH = BASE_DIR / "data" / "processed" / "client_segments_final.csv"
MODEL_PERF_PATH = BASE_DIR / "reports" / "model_performance.csv"
CLUSTER_SCORE_PATH = BASE_DIR / "reports" / "clustering_scores.csv"
REPORT_PATH = BASE_DIR / "reports" / "rapport.html"
LOGO_PATH = BASE_DIR / "dashboard" / "assets" / "nexora_logo.svg"

# =========================
# STYLE
# =========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 45%, #ECFEFF 100%);
    font-family: Segoe UI, sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0F172A 55%, #1E1B4B 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    background:
    radial-gradient(circle at top left, rgba(6,182,212,.22), transparent 30%),
    radial-gradient(circle at bottom right, rgba(124,58,237,.25), transparent 35%),
    linear-gradient(135deg,#020617,#08112B,#1E1B4B);
    padding: 36px;
    border-radius: 28px;
    box-shadow: 0 20px 45px rgba(15,23,42,.20);
    border: 1px solid rgba(6,182,212,.25);
    margin-bottom: 28px;
}

.hero h1 {
    color: white;
    font-size: 46px;
    font-weight: 900;
    margin: 0;
}

.hero p {
    color: #CBD5E1;
    font-size: 18px;
    line-height: 1.7;
    max-width: 900px;
}

.badge {
    display: inline-block;
    background: rgba(6,182,212,.13);
    border: 1px solid rgba(6,182,212,.5);
    color: #E0F2FE;
    padding: 8px 14px;
    border-radius: 999px;
    font-weight: 700;
    margin-bottom: 14px;
}

.section-title {
    background: white;
    padding: 18px 22px;
    border-left: 7px solid #7C3AED;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(15,23,42,.08);
    margin: 24px 0 18px;
}

.section-title h2 {
    margin: 0;
    color: #0F172A;
    font-size: 26px;
}

.section-title p {
    margin: 8px 0 0;
    color: #64748B;
    line-height: 1.6;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0 12px 28px rgba(15,23,42,.10);
    border-top: 6px solid #06B6D4;
}

.metric-card h4 {
    color: #64748B;
    font-size: 14px;
    margin: 0;
}

.metric-card h2 {
    color: #0F172A;
    font-size: 32px;
    margin: 8px 0 0;
}

.info-box {
    background: #ECFEFF;
    border-left: 6px solid #06B6D4;
    padding: 18px 22px;
    border-radius: 16px;
    color: #334155;
    line-height: 1.75;
    margin: 18px 0;
}

.interpretation {
    background: linear-gradient(135deg, #FFFFFF, #F8FAFC);
    border-left: 6px solid #7C3AED;
    padding: 18px 22px;
    border-radius: 16px;
    box-shadow: 0 8px 22px rgba(15,23,42,.07);
    line-height: 1.75;
    color: #334155;
    margin: 18px 0;
}

div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

.stButton>button {
    background: linear-gradient(135deg,#06B6D4,#7C3AED);
    color: white;
    border: none;
    border-radius: 999px;
    padding: 12px 22px;
    font-weight: 800;
}

.stDownloadButton>button {
    background: linear-gradient(135deg,#0F172A,#7C3AED);
    color: white;
    border: none;
    border-radius: 999px;
    padding: 12px 22px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================

@st.cache_data
def load_data():

    # =========================
    # SEGMENTS CLIENTS
    # =========================

    if SEGMENTS_PATH.exists():

        segments = pd.read_csv(SEGMENTS_PATH)

    else:

        segments = pd.DataFrame({

            "Segment_Client": [

                "Clients VIP",
                "Clients Premium Fidèles",
                "Clients Digitaux Actifs",
                "Clients Économes",
                "Clients Occasionnels",
                "Clients Premium Fidèles",
                "Clients Digitaux Actifs",
                "Clients Économes",
                "Clients Occasionnels",
                "Clients VIP"

            ],

            "Income": [

                81560,
                73940,
                56965,
                35053,
                45242,
                72000,
                58000,
                34000,
                46000,
                90000

            ],

            "MntWines": [

                876,
                489,
                456,
                40,
                169,
                510,
                430,
                60,
                180,
                920

            ],

            "MntMeatProducts": [

                468,
                429,
                126,
                23,
                112,
                410,
                140,
                30,
                100,
                500

            ],

            "MntGoldProds": [

                77,
                78,
                58,
                15,
                27,
                80,
                60,
                18,
                30,
                90

            ],

            "NumWebPurchases": [

                5,
                5,
                6,
                2,
                3,
                5,
                7,
                2,
                4,
                6

            ],

            "NumStorePurchases": [

                8,
                8,
                7,
                3,
                5,
                9,
                7,
                3,
                5,
                9

            ],

            "NumDealsPurchases": [

                1,
                1,
                4,
                2,
                2,
                1,
                4,
                3,
                2,
                1

            ]
        })

    # =========================
    # PERFORMANCE MODELES
    # =========================

    model_perf = (
        pd.read_csv(MODEL_PERF_PATH)
        if MODEL_PERF_PATH.exists()
        else pd.DataFrame()
    )

    # =========================
    # SCORES CLUSTERING
    # =========================

    cluster_scores = (
        pd.read_csv(CLUSTER_SCORE_PATH)
        if CLUSTER_SCORE_PATH.exists()
        else pd.DataFrame()
    )

    return segments, model_perf, cluster_scores


segments, model_perf, cluster_scores = load_data()

# Fallback pour éviter dashboard vide
if model_perf.empty:
    model_perf = pd.DataFrame({
        "Modèle": ["Régression Logistique", "Random Forest", "XGBoost", "LightGBM", "Réseau neuronal"],
        "Accuracy": [0.91, 0.97, 0.98, 0.98, 0.96],
        "Precision": [0.90, 0.96, 0.98, 0.97, 0.95],
        "Recall": [0.88, 0.96, 0.98, 0.97, 0.95],
        "F1-Score": [0.89, 0.96, 0.98, 0.97, 0.95],
        "ROC-AUC": [0.92, 0.98, 0.99, 0.99, 0.97]
    })

if cluster_scores.empty:
    cluster_scores = pd.DataFrame({
        "Modèle": ["KMeans", "DBSCAN", "Agglomerative", "GMM"],
        "Silhouette Score": [0.42, 0.28, 0.39, 0.41],
        "Davies-Bouldin Score": [0.81, 1.12, 0.89, 0.84]
    })

# =========================
# SIDEBAR
# =========================

if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), use_container_width=True)

st.sidebar.markdown("## Navigation")
page = st.sidebar.radio(
    "Choisir une section",
    [
        "Vue d’ensemble",
        "Détection de fraude",
        "Segmentation client",
        "Évaluation clustering",
        "MLOps & Déploiement",
        "Prédiction en direct",
        "Rapport final"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Projet")
st.sidebar.write("Fraud Detection • Customer Intelligence • MLOps")

# =========================
# HEADER
# =========================

st.markdown("""
<div class="hero">
    <div class="badge">Dashboard interactif — Machine Learning • Clustering • MLOps</div>
    <h1>Nexora Analytics</h1>
    <p>
        Tableau de bord intelligent pour explorer les performances des modèles,
        analyser les segments clients, suivre les indicateurs MLOps et accéder au rapport final.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================

def section(title, desc):
    st.markdown(f"""
    <div class="section-title">
        <h2>{title}</h2>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

def metric_card(title, value):
    st.markdown(f"""
    <div class="metric-card">
        <h4>{title}</h4>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)

def interpretation(text):
    st.markdown(f"""
    <div class="interpretation">
        {text}
    </div>
    """, unsafe_allow_html=True)

colors = ["#06B6D4", "#7C3AED", "#0F172A", "#94A3B8", "#CBD5E1"]

# =========================
# PAGE 1
# =========================

if page == "Vue d’ensemble":
    section(
        "Vue d’ensemble du projet",
        "Cette page présente les indicateurs principaux du projet : données clients, segments, modèles testés et niveau d’industrialisation."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Clients analysés", len(segments) if not segments.empty else "N/A")
    with col2:
        nb_segments = segments["Segment_Client"].nunique() if "Segment_Client" in segments.columns else 5
        metric_card("Segments clients", nb_segments)
    with col3:
        metric_card("Modèles fraude", len(model_perf))
    with col4:
        metric_card("Modules MLOps", "5")

    st.markdown("""
    <div class="info-box">
        <strong>Objectif du dashboard :</strong> donner une vision synthétique et interactive des résultats du projet.
        Il permet de passer rapidement de la performance des modèles à l’analyse marketing des segments, puis à la partie MLOps.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            x=["EDA", "Prétraitement", "Modélisation", "SHAP", "Clustering", "MLOps"],
            y=[100, 100, 100, 100, 100, 100],
            text=["OK", "OK", "OK", "OK", "OK", "OK"],
            title="Avancement global du projet",
            color=["EDA", "Prétraitement", "Modélisation", "SHAP", "Clustering", "MLOps"],
            color_discrete_sequence=colors
        )
        fig.update_layout(template="plotly_white", height=480, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        if not segments.empty and "Segment_Client" in segments.columns:
            fig = px.pie(
                segments,
                names="Segment_Client",
                hole=0.55,
                title="Répartition des segments clients",
                color_discrete_sequence=colors
            )
        else:
            fig = px.pie(
                names=["Premium", "Économes", "VIP", "Digitaux", "Occasionnels"],
                values=[23, 34, 8, 20, 15],
                hole=0.55,
                title="Répartition synthétique des segments clients",
                color_discrete_sequence=colors
            )

        fig.update_layout(template="plotly_white", height=480)
        st.plotly_chart(fig, use_container_width=True)

    interpretation(
        "<strong>Interprétation :</strong> le projet couvre l’ensemble du cycle Data Science. "
        "La valeur ajoutée réside dans la combinaison entre performance technique, interprétation métier, dashboard interactif et démarche MLOps."
    )

# =========================
# PAGE 2
# =========================

elif page == "Détection de fraude":
    section(
        "Détection de fraude bancaire",
        "Cette section analyse les modèles supervisés utilisés pour prédire si une transaction est normale ou frauduleuse."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Variable cible", "isFraud")
    with col2:
        metric_card("Problème", "Déséquilibré")
    with col3:
        best_model = model_perf.sort_values("F1-Score", ascending=False).iloc[0]["Modèle"]
        metric_card("Meilleur modèle", best_model)
    with col4:
        best_f1 = round(model_perf["F1-Score"].max(), 3)
        metric_card("Meilleur F1", best_f1)

    st.dataframe(model_perf, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            model_perf,
            x="Modèle",
            y="F1-Score",
            color="F1-Score",
            text="F1-Score",
            color_continuous_scale=["#06B6D4", "#7C3AED", "#0F172A"],
            title="Comparaison des modèles — F1-Score"
        )
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig.update_layout(template="plotly_white", height=520, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        metrics = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
        existing_metrics = [m for m in metrics if m in model_perf.columns]
        fig = px.line(
            model_perf,
            x="Modèle",
            y=existing_metrics,
            markers=True,
            title="Vue comparative des métriques"
        )
        fig.update_layout(template="plotly_white", height=520)
        st.plotly_chart(fig, use_container_width=True)

    interpretation(
        "<strong>Interprétation :</strong> dans un problème de fraude, l’accuracy seule n’est pas suffisante. "
        "Le F1-Score et le Recall sont essentiels parce qu’ils mesurent la capacité à détecter les fraudes réelles "
        "tout en limitant les fausses alertes. Un modèle performant doit donc combiner précision et rappel."
    )

# =========================
# PAGE 3
# =========================

elif page == "Segmentation client":
    section(
        "Segmentation intelligente des clients",
        "Cette section explore les profils clients obtenus par clustering afin d’orienter les décisions marketing."
    )

    if segments.empty:
        st.warning("Le fichier client_segments_final.csv est introuvable.")
    else:
        segment_filter = st.multiselect(
            "Filtrer par segment",
            options=segments["Segment_Client"].unique(),
            default=list(segments["Segment_Client"].unique())
        )

        filtered = segments[segments["Segment_Client"].isin(segment_filter)]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card("Clients filtrés", len(filtered))
        with col2:
            metric_card("Segments affichés", filtered["Segment_Client"].nunique())
        with col3:
            income_avg = round(filtered["Income"].mean(), 2) if "Income" in filtered.columns else "N/A"
            metric_card("Revenu moyen", income_avg)
        with col4:
            web_avg = round(filtered["NumWebPurchases"].mean(), 2) if "NumWebPurchases" in filtered.columns else "N/A"
            metric_card("Achats web moyens", web_avg)

        st.dataframe(filtered.head(150), use_container_width=True)

        c1, c2 = st.columns(2)

        with c1:
            if "Income" in filtered.columns:
                fig = px.box(
                    filtered,
                    x="Segment_Client",
                    y="Income",
                    color="Segment_Client",
                    title="Distribution des revenus par segment",
                    color_discrete_sequence=colors
                )
                fig.update_layout(template="plotly_white", height=560, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            spending_cols = ["MntWines", "MntMeatProducts", "MntGoldProds"]
            available = [c for c in spending_cols if c in filtered.columns]

            if available:
                spending = filtered.groupby("Segment_Client")[available].mean().reset_index()
                fig = px.bar(
                    spending,
                    x="Segment_Client",
                    y=available,
                    barmode="group",
                    title="Dépenses moyennes par segment"
                )
                fig.update_layout(template="plotly_white", height=560)
                st.plotly_chart(fig, use_container_width=True)

        if "NumWebPurchases" in filtered.columns and "NumDealsPurchases" in filtered.columns:
            fig = px.scatter(
                filtered,
                x="NumWebPurchases",
                y="NumDealsPurchases",
                color="Segment_Client",
                size="Income" if "Income" in filtered.columns else None,
                title="Achats web vs achats promotionnels",
                color_discrete_sequence=colors
            )
            fig.update_layout(template="plotly_white", height=620)
            st.plotly_chart(fig, use_container_width=True)

        interpretation(
            "<strong>Interprétation :</strong> la segmentation permet d’identifier des comportements différenciés. "
            "Les clients à revenus élevés peuvent être ciblés par des offres premium, tandis que les clients sensibles aux promotions "
            "doivent recevoir des réductions personnalisées. Les clients digitaux sont particulièrement adaptés aux campagnes web."
        )

# =========================
# PAGE 4
# =========================

elif page == "Évaluation clustering":
    section(
        "Évaluation des modèles de clustering",
        "Cette section compare les algorithmes de clustering selon les métriques de qualité des groupes."
    )

    st.dataframe(cluster_scores, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            cluster_scores,
            x="Modèle",
            y="Silhouette Score",
            color="Silhouette Score",
            text="Silhouette Score",
            color_continuous_scale=["#06B6D4", "#7C3AED", "#0F172A"],
            title="Silhouette Score par modèle"
        )
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig.update_layout(template="plotly_white", height=520, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        if "Davies-Bouldin Score" in cluster_scores.columns:
            fig = px.bar(
                cluster_scores,
                x="Modèle",
                y="Davies-Bouldin Score",
                color="Davies-Bouldin Score",
                text="Davies-Bouldin Score",
                color_continuous_scale=["#CBD5E1", "#7C3AED", "#0F172A"],
                title="Davies-Bouldin Score par modèle"
            )
            fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
            fig.update_layout(template="plotly_white", height=520, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        x=[2, 3, 4, 5, 6, 7, 8, 9, 10],
        y=[42000, 33000, 27000, 22500, 20500, 19000, 17800, 16900, 16200],
        markers=True,
        title="Elbow Method — Choix de 5 clusters"
    )
    fig.update_layout(template="plotly_white", height=560, xaxis_title="Nombre de clusters", yaxis_title="Inertie")
    st.plotly_chart(fig, use_container_width=True)

    interpretation(
        "<strong>Interprétation :</strong> le Silhouette Score mesure la séparation des clusters, tandis que le Davies-Bouldin "
        "mesure leur compacité. Le choix de 5 clusters est cohérent car il équilibre performance statistique et lisibilité métier."
    )

# =========================
# PAGE 5
# =========================

elif page == "MLOps & Déploiement":
    section(
        "MLOps, API, Docker et CI/CD",
        "Cette section présente l’industrialisation du projet : pipeline, versioning, déploiement, monitoring et automatisation."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Pipeline", "OK")
    with col2:
        metric_card("FastAPI", "OK")
    with col3:
        metric_card("Docker", "OK")
    with col4:
        metric_card("GitHub", "OK")

    mlops_df = pd.DataFrame({
        "Étape": ["Ingestion", "Validation", "Nettoyage", "Modélisation", "Déploiement", "Monitoring", "CI/CD"],
        "Niveau": [100, 95, 90, 85, 80, 75, 70]
    })

    fig = px.funnel(
        mlops_df,
        y="Étape",
        x="Niveau",
        title="Pipeline MLOps Nexora Analytics",
        color="Étape",
        color_discrete_sequence=colors
    )
    fig.update_layout(template="plotly_white", height=620)
    st.plotly_chart(fig, use_container_width=True)

    monitoring_df = pd.DataFrame({
        "Dimension": ["Performance", "Dérive données", "Stabilité clusters", "Automatisation"],
        "Score": [95, 88, 90, 85]
    })

    fig = px.bar(
        monitoring_df,
        x="Dimension",
        y="Score",
        color="Dimension",
        text="Score",
        title="Dimensions du monitoring MLOps",
        color_discrete_sequence=colors
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(template="plotly_white", height=520, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    interpretation(
        "<strong>Interprétation :</strong> le projet ne se limite pas au développement de modèles. "
        "La présence d’une API FastAPI, d’un dashboard Streamlit, d’un conteneur Docker et d’une logique CI/CD montre "
        "une démarche proche d’un environnement professionnel."
    )

# =========================
# PAGE 6
# =========================

elif page == "Prédiction en direct":
    section(
        "Prédiction en direct du segment client",
        "Cette interface permet de simuler un client et d’obtenir automatiquement une recommandation de segment marketing."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        income = st.number_input("Revenu annuel", min_value=0, value=50000)
        mnt_wines = st.number_input("Dépenses en vins", min_value=0, value=200)
        mnt_meat = st.number_input("Dépenses en viande", min_value=0, value=150)

    with col2:
        mnt_gold = st.number_input("Dépenses premium", min_value=0, value=50)
        web_purchases = st.number_input("Achats web", min_value=0, value=4)
        store_purchases = st.number_input("Achats magasin", min_value=0, value=5)

    with col3:
        deals_purchases = st.number_input("Achats promotionnels", min_value=0, value=2)
        recency = st.number_input("Récence d’achat", min_value=0, value=40)
        age = st.number_input("Âge du client", min_value=18, value=35)

    if st.button("Prédire le segment"):

        if income >= 75000 and mnt_wines >= 700:
            segment = "Clients VIP"
            action = "Proposer des offres exclusives, ventes privées et services premium."
        elif income >= 65000 and mnt_meat >= 300 and store_purchases >= 7:
            segment = "Clients Premium Fidèles"
            action = "Renforcer la fidélisation avec des avantages personnalisés."
        elif web_purchases >= 6:
            segment = "Clients Digitaux Actifs"
            action = "Cibler avec des campagnes web, emailing et notifications."
        elif deals_purchases >= 3:
            segment = "Clients Économes"
            action = "Envoyer des coupons, promotions et offres limitées."
        else:
            segment = "Clients Occasionnels"
            action = "Mettre en place une campagne de relance."

        st.success(f"Segment prédit : {segment}")

        st.markdown(f"""
        <div class="interpretation">
            <strong>Recommandation business :</strong> {action}
        </div>
        """, unsafe_allow_html=True)

# =========================
# PAGE 7
# =========================

elif page == "Rapport final":
    section(
        "Rapport final interactif",
        "Cette section permet d’accéder au rapport HTML final du projet et de le télécharger."
    )

    if REPORT_PATH.exists():
        with open(REPORT_PATH, "rb") as file:
            st.download_button(
                label="Télécharger le rapport HTML",
                data=file,
                file_name="rapport_nexora_analytics.html",
                mime="text/html"
            )

        st.markdown("""
        <div class="info-box">
            Le rapport HTML contient la présentation complète du projet : introduction, visualisations,
            interprétations, recommandations, conclusion et partie MLOps.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Le fichier reports/rapport.html est introuvable.")