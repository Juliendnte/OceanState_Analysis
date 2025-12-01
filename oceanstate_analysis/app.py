import streamlit as st
import pandas as pd
import sys
import os

# Ajouter le chemin vers le module analysis
sys.path.append(os.path.join(os.path.dirname(__file__), 'oceanstate_analysis'))

from analysis.plots import plot_ph_evolution, plot_plastic_accumulation

# Configuration de la page
st.set_page_config(
    page_title="OceanState Analysis",
    page_icon="🌊",
    layout="wide"
)

# Titre principal
st.title("🌊 Analyse de l'État de l'Océan")
st.markdown("---")

# Sidebar pour navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choisir une analyse",
    ["Accueil", "Évolution du pH", "Microplastiques"]
)

if page == "Accueil":
    st.header("Bienvenue dans l'analyse de l'état de l'océan")
    st.markdown("""
    Cette application présente différentes analyses sur l'évolution de l'état de l'océan :
    
    - **Évolution du pH** : Analyse de l'acidification des océans
    - **Microplastiques** : Accumulation des microplastiques dans l'océan
    
    Utilisez le menu latéral pour naviguer entre les différentes analyses.
    """)

elif page == "Évolution du pH":
    st.header("📈 Évolution du pH de l'eau de mer")

    # Upload de fichier ou données d'exemple
    uploaded_file = st.file_uploader(
        "Télécharger vos données pH (CSV)",
        type=['csv'],
        help="Le fichier doit contenir les colonnes : Date, pH, pH yearly average"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Vérifier les colonnes requises
            required_cols = ['Date', 'pH', 'pH yearly average']
            if all(col in df.columns for col in required_cols):
                st.success("Données chargées avec succès!")

                # Afficher un aperçu des données
                with st.expander("Aperçu des données"):
                    st.dataframe(df.head())

                # Créer et afficher le graphique
                fig = plot_ph_evolution(df)
                st.pyplot(fig)

                # Statistiques supplémentaires
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("pH minimum", f"{df['pH'].min():.2f}")
                with col2:
                    st.metric("pH maximum", f"{df['pH'].max():.2f}")
                with col3:
                    st.metric("pH moyen", f"{df['pH'].mean():.2f}")

            else:
                st.error(f"Le fichier doit contenir les colonnes : {', '.join(required_cols)}")

        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
    else:
        st.info("Téléchargez un fichier CSV pour voir l'analyse du pH")

elif page == "Microplastiques":
    st.header("🏭 Accumulation des microplastiques")

    # Upload de fichier ou données d'exemple
    uploaded_file = st.file_uploader(
        "Télécharger vos données microplastiques (CSV)",
        type=['csv'],
        help="Le fichier doit contenir les colonnes : year, amount, Entity"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Vérifier les colonnes requises
            required_cols = ['year', 'amount', 'Entity']
            if all(col in df.columns for col in required_cols):
                st.success("Données chargées avec succès!")

                # Filtres
                col1, col2 = st.columns(2)
                with col1:
                    entities = st.multiselect(
                        "Sélectionner les entités",
                        options=df['Entity'].unique(),
                        default=df['Entity'].unique()[:3]  # Sélectionner les 3 premières par défaut
                    )

                with col2:
                    year_range = st.slider(
                        "Plage d'années",
                        min_value=int(df['year'].min()),
                        max_value=int(df['year'].max()),
                        value=(int(df['year'].min()), int(df['year'].max()))
                    )

                # Filtrer les données
                filtered_df = df[
                    (df['Entity'].isin(entities)) &
                    (df['year'] >= year_range[0]) &
                    (df['year'] <= year_range[1])
                    ]

                if not filtered_df.empty:
                    # Afficher un aperçu des données filtrées
                    with st.expander("Aperçu des données filtrées"):
                        st.dataframe(filtered_df.head())

                    # Créer et afficher le graphique
                    fig = plot_plastic_accumulation(filtered_df)
                    st.pyplot(fig)

                    # Statistiques par entité
                    st.subheader("Statistiques par entité")
                    stats = filtered_df.groupby('Entity')['amount'].agg(['mean', 'max', 'min']).round(2)
                    st.dataframe(stats)

                else:
                    st.warning("Aucune donnée ne correspond aux filtres sélectionnés")

            else:
                st.error(f"Le fichier doit contenir les colonnes : {', '.join(required_cols)}")

        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
    else:
        st.info("Téléchargez un fichier CSV pour voir l'analyse des microplastiques")

# Footer
st.markdown("---")
st.markdown("*Application développée pour l'analyse de l'état de l'océan*")