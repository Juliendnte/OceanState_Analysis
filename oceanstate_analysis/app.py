import streamlit as st
import pandas as pd
import sys
import os

# Ajouter le chemin vers le module analysis ET reports
sys.path.append(os.path.join(os.path.dirname(__file__), 'oceanstate_analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'oceanstate_analysis', 'reports'))

# Configuration de la page
st.set_page_config(
    page_title="OceanState Analysis",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🌊 Analyse de l'État de l'Océan")
st.markdown("*Une exploration des transformations océaniques et de leurs interconnexions*")
st.markdown("---")

# Sidebar pour navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.selectbox(
    "Choisir une section",
    ["🏠 Accueil", "📊 Projet & Analyses", "📚 Documentation"]
)

# ===== ONGLET ACCUEIL =====
if page == "🏠 Accueil":
    st.header("🌊 Bienvenue dans l'analyse de l'état de l'océan")

    # Introduction
    st.subheader("📖 Introduction")
    st.markdown("""
    Les océans couvrent plus de 70% de la surface de notre planète et jouent un rôle crucial dans la régulation 
    du climat mondial. Cependant, ils subissent des transformations profondes dues aux activités humaines.
    
    Cette application présente une analyse complète des évolutions océaniques à travers différents indicateurs 
    interconnectés, suivant une trame narrative structurée.
    """)

    # Problématique
    st.subheader("❓ Problématique")
    st.markdown("""
    **Comment l'activité humaine transforme-t-elle nos océans et quelles sont les interconnexions 
    entre ces différentes transformations ?**
    
    Notre analyse explore deux axes majeurs :
    - 🌡️ **Le réchauffement climatique** et ses conséquences sur les océans
    - 🏭 **La pollution plastique** et l'acidification des eaux
    """)

    # Plan de l'étude
    st.subheader("🗺️ Plan de l'étude")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🌡️ Axe 1 : Réchauffement climatique
        **Réalisé par Sophie**
        
        1. 📈 Réchauffement climatique global ✅
        2. 🌊 Hausse de la température des océans ✅
        3. ⬇️ Conséquences : Fonte des glaces ✅
        4. 🌊 Impact : Montée du niveau des eaux ✅
        5. 🗺️ Ciblage géographique des zones impactées 🔄
        """)

    with col2:
        st.markdown("""
        ### 🏭 Axe 2 : Pollution et acidification
        **Réalisé par Julien**
        
        1. 🏭 Pollution des océans et des terres (plastique) ✅
        2. 💨 Augmentation des émissions de CO2 ✅
        3. ⬇️ Conséquences : Acidification des eaux océaniques ✅
        4. 🐠 Impact : Dégâts sur les espèces marines 🔄
        5. 🔗 Conclusion : Liens entre pollution et climat ✅
        """)

    # Méthodologie
    st.subheader("🔬 Méthodologie")
    st.markdown("""
    Notre approche s'articule autour de :
    - **Collecte de données** provenant de sources fiables (NASA, Our World in Data, EPA, Kaggle)
    - **Analyses temporelles** pour identifier les tendances à long terme
    - **Corrélations statistiques** pour mettre en évidence les interconnexions
    - **Visualisations interactives** pour faciliter la compréhension des phénomènes
    """)


# ===== ONGLET PROJET & ANALYSES =====
elif page == "📊 Projet & Analyses":
    st.header("📊 Analyses et Visualisations")
    st.markdown("*Suivez notre trame narrative à travers les données*")

    # Import des fonctions de rapport
    try:
        from reports import (
            report_acidification,
            report_heat,
            report_glaciermelting_sealevel_correlation,
            report_glaciermelting,
            report_sealevel,
            report_acidification_co2_correlation,
            report_plastic_evolution,
            report_plastic_waste_countries,
            report_plastic_production_global,
            report_plastic_ocean_distribution,
            report_plastic_co2_correlation,
            report_glacier_heat_correlation,
            display_correlation_metrics,
            create_summary_stats,
            report_acidification_redlist_correlation,
            report_redlist
        )
        reports_available = True
        st.success("✅ Module de rapports chargé avec succès")
    except ImportError as e:
        st.error(f"❌ Impossible d'importer les fonctions de rapport : {e}")
        reports_available = False

    # Sous-navigation pour les analyses
    analysis_type = st.selectbox(
        "Choisir une analyse",
        [
            "🌡️ Réchauffement Climatique (Axe Sophie)",
            "🏭 Pollution et Acidification (Axe Julien)",
            "🔗 Interconnexions et Corrélations"
        ]
    )

    # ===== AXE SOPHIE : RÉCHAUFFEMENT CLIMATIQUE =====
    if analysis_type == "🌡️ Réchauffement Climatique (Axe Sophie)":
        st.subheader("🌡️ Axe 1 : Réchauffement climatique et ses conséquences")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Réchauffement global",
            "🌊 Température océanique",
            "🧊 Fonte des glaces",
            "📏 Montée des eaux"
        ])

        with tab1:
            st.markdown("### 📈 Réchauffement climatique global")

            st.markdown("""
            Cette section analyse l'évolution du réchauffement climatique global et ses impacts.
            """)

        with tab2:
            st.markdown("### 🌊 Hausse de la température des océans")


            if reports_available:
                if st.button("🌡️ Générer le rapport de chaleur océanique", key="ocean_heat"):
                    try:
                        with st.spinner("Génération du rapport de chaleur océanique..."):
                            df, fig = report_heat()

                            # CORRECTION : Utiliser plotly_chart au lieu de pyplot
                            st.plotly_chart(fig, use_container_width=True)

                            # Statistiques de température
                            st.subheader("📊 Statistiques de chaleur océanique")
                            col1, col2, col3 = st.columns(3)

                            # Adaptez ces colonnes selon vos données réelles
                            temp_col = [col for col in df.columns if
                                        'heat' in col.lower() or 'temp' in col.lower() or 'OHC' in col][0] if any(
                                'heat' in col.lower() or 'temp' in col.lower() or 'OHC' in col for col in
                                df.columns) else df.columns[1]

                            with col1:
                                st.metric("🌡️ Minimum", f"{df[temp_col].min():.2f}")
                            with col2:
                                st.metric("🌡️ Maximum", f"{df[temp_col].max():.2f}")
                            with col3:
                                st.metric("🌡️ Moyenne", f"{df[temp_col].mean():.2f}")

                            # Tendance
                            trend = df[temp_col].iloc[-1] - df[temp_col].iloc[0]
                            trend_color = "🔴" if trend > 0 else "🔵"
                            st.info(f"{trend_color} **Tendance :** {trend:+.2f} unités sur la période")

                            with st.expander("📋 Données détaillées"):
                                st.dataframe(df)

                    except Exception as e:
                        st.error(f"❌ Erreur : {e}")
                        import traceback

                        st.code(traceback.format_exc())

        with tab3:
            st.markdown("### 🧊 Fonte des glaces")



            if reports_available:
                # Deux options pour les glaciers
                glacier_option = st.radio(
                    "Choisir l'analyse des glaciers",
                    ["🧊 Évolution de la fonte", "🔗 Corrélation Glaciers ↔ Chaleur", "🌊 Corrélation Glaciers ↔ Niveau des mers"],
                    key="glacier_option"
                )

                if glacier_option == "🧊 Évolution de la fonte":
                    if st.button("🧊 Générer rapport fonte des glaces", key="glaciers_alone"):
                        try:
                            with st.spinner("Génération du rapport de fonte des glaces..."):
                                df, fig = report_glaciermelting()
                                st.pyplot(fig)

                                # Statistiques glaciers
                                st.subheader("🧊 Statistiques de fonte")
                                glacier_col = [col for col in df.columns if 'mass' in col.lower() or 'glacier' in col.lower()][0] if any('mass' in col.lower() or 'glacier' in col.lower() for col in df.columns) else df.columns[1]

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("❄️ Masse initiale", f"{df[glacier_col].iloc[0]:.1f}")
                                with col2:
                                    st.metric("❄️ Masse actuelle", f"{df[glacier_col].iloc[-1]:.1f}")
                                with col3:
                                    loss = df[glacier_col].iloc[0] - df[glacier_col].iloc[-1]
                                    st.metric("📉 Perte totale", f"{loss:.1f}")

                                with st.expander("📋 Données glaciers"):
                                    st.dataframe(df)

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

                elif glacier_option == "🔗 Corrélation Glaciers ↔ Chaleur":
                    if st.button("🔗 Générer corrélation Glaciers-Chaleur", key="glaciers_heat"):
                        try:
                            with st.spinner("Analyse corrélation Glaciers-Chaleur..."):
                                df, fig, correlation = report_glacier_heat_correlation()

                                if fig is not None:
                                    st.plotly_chart(fig, use_container_width=True)

                                    # Métriques de corrélation
                                    st.subheader("📊 Analyse de corrélation")
                                    display_correlation_metrics(correlation, "Glaciers vs Chaleur océanique")

                                    # Interprétation
                                    st.markdown("""
                                    **🎯 Interprétation :**
                                    - Une corrélation négative indique que l'augmentation de la chaleur océanique 
                                      correspond à une diminution de la masse glaciaire
                                    - Cette relation confirme l'impact direct du réchauffement des océans 
                                      sur la fonte des glaciers
                                    """)

                                    with st.expander("📋 Données détaillées"):
                                        st.dataframe(df)

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

                else:  # Corrélation Glaciers ↔ Niveau des mers
                    if st.button("🌊 Générer corrélation Glaciers-Niveau mers", key="glaciers_sealevel"):
                        try:
                            with st.spinner("Analyse corrélation Glaciers-Niveau des mers..."):
                                df, fig, correlation = report_glaciermelting_sealevel_correlation()
                                st.pyplot(fig)

                                # Métriques de corrélation
                                st.subheader("📊 Analyse de corrélation")
                                display_correlation_metrics(correlation, "Glaciers vs Niveau des mers")

                                # Interprétation
                                st.markdown("""
                                **🎯 Interprétation :**
                                - Une corrélation négative indique que la fonte des glaciers (diminution de masse) 
                                  correspond à une élévation du niveau des mers
                                - Cette relation illustre la contribution directe de la fonte glaciaire 
                                  à l'élévation du niveau des océans
                                """)

                                with st.expander("📋 Données détaillées"):
                                    st.dataframe(df)

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

        with tab4:
            st.markdown("### 📏 Montée du niveau des eaux")

            if reports_available:

                if st.button("🌊 Générer rapport niveau des mers", key="sealevel"):
                    try:
                        with st.spinner("Génération du rapport niveau des mers..."):
                            df, fig = report_sealevel()

                            # CORRECTION : Utiliser plotly_chart au lieu de pyplot
                            st.plotly_chart(fig, use_container_width=True)

                            # Statistiques niveau des mers
                            st.subheader("🌊 Statistiques niveau des mers")
                            sea_col = [col for col in df.columns if
                                       'level' in col.lower() or 'sea' in col.lower() or 'average' in col.lower()][
                                0] if any(
                                'level' in col.lower() or 'sea' in col.lower() or 'average' in col.lower() for col in
                                df.columns) else df.columns[1]

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("🌊 Niveau initial", f"{df[sea_col].iloc[0]:.2f} mm")
                            with col2:
                                st.metric("🌊 Niveau actuel", f"{df[sea_col].iloc[-1]:.2f} mm")
                            with col3:
                                rise = df[sea_col].iloc[-1] - df[sea_col].iloc[0]
                                st.metric("📈 Élévation totale", f"{rise:.2f} mm")

                            # Tendance et prédiction
                            annual_rise = rise / len(df)
                            st.info(f"📊 **Élévation moyenne annuelle :** {annual_rise:.2f} mm/an")

                            with st.expander("📋 Données niveau des mers"):
                                st.dataframe(df)

                    except Exception as e:
                        st.error(f"❌ Erreur : {e}")
                        import traceback

                        st.code(traceback.format_exc())


    # ===== AXE JULIEN : POLLUTION ET ACIDIFICATION =====
    elif analysis_type == "🏭 Pollution et Acidification (Axe Julien)":
        st.subheader("🏭 Axe 2 : Pollution et acidification des océans")

        tab1, tab2, tab3, tab4 = st.tabs([
            "🏭 Pollution plastique",
            "💨 Émissions CO2",
            "⚗️ Acidification",
            "🐠 Impact biodiversité"
        ])

        with tab1:
            st.markdown("### 🏭 Pollution des océans (plastique)")

            if reports_available:
                # Sous-onglets pour les différents aspects du plastique
                plastic_tab1, plastic_tab2, plastic_tab3, plastic_tab4 = st.tabs([
                    "📈 Évolution Micro/Macro",
                    "🌍 Déchets par pays",
                    "🏭 Production mondiale",
                    "🌊 Répartition océanique"
                ])

                with plastic_tab1:
                    if st.button("📊 Générer rapport Micro/Macroplastiques", key="micro_macro"):
                        try:
                            with st.spinner("Génération du rapport plastiques..."):
                                df, fig = report_plastic_evolution()
                                st.pyplot(fig)

                                # Statistiques plastiques
                                st.subheader("📊 Statistiques plastiques")
                                col1, col2 = st.columns(2)

                                with col1:
                                    if 'microplastics' in df.columns:
                                        st.metric("🔬 Microplastiques max", f"{df['microplastics'].max():,.0f}")

                                with col2:
                                    if 'macroplastics' in df.columns:
                                        st.metric("🗑️ Macroplastiques max", f"{df['macroplastics'].max():,.0f}")

                                with st.expander("📋 Données micro/macroplastiques"):
                                    st.dataframe(df.head(10))

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

                with plastic_tab2:
                    if st.button("🌍 Générer rapport déchets par pays", key="waste_countries"):
                        try:
                            with st.spinner("Génération du rapport par pays..."):
                                df, fig = report_plastic_waste_countries()
                                st.pyplot(fig)

                                # Statistiques des top pays
                                latest_year = df['Year'].max()
                                top_stats = df[df['Year'] == latest_year].nlargest(
                                    5, 'Imports of plastic waste via all modes of transport')

                                st.subheader(f"🏆 Top 5 pays en {latest_year}")
                                for i, row in top_stats.iterrows():
                                    st.metric(
                                        row['Entity'],
                                        f"{row['Imports of plastic waste via all modes of transport']:,.0f} tonnes"
                                    )

                                with st.expander("📋 Données par pays"):
                                    st.dataframe(top_stats)

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

                with plastic_tab3:
                    if st.button("🏭 Générer rapport production mondiale", key="production"):
                        try:
                            with st.spinner("Génération du rapport de production..."):
                                df, fig = report_plastic_production_global()
                                st.pyplot(fig)

                                # Métriques de production
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("📈 Production 1950", f"{df['plastic_production'].iloc[0]:,.0f}")
                                with col2:
                                    st.metric("📈 Production récente", f"{df['plastic_production'].iloc[-1]:,.0f}")
                                with col3:
                                    growth = ((df['plastic_production'].iloc[-1] / df['plastic_production'].iloc[0]) - 1) * 100
                                    st.metric("📊 Croissance", f"{growth:,.1f}%")

                                # Tendance annuelle
                                annual_growth = (df['plastic_production'].iloc[-1] / df['plastic_production'].iloc[0]) ** (1/(len(df)-1)) - 1
                                st.info(f"📈 **Croissance annuelle moyenne :** {annual_growth*100:.1f}%")

                                with st.expander("📋 Données production"):
                                    st.dataframe(df)

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

                with plastic_tab4:
                    if st.button("🌊 Générer rapport répartition océanique", key="ocean_distrib"):
                        try:
                            with st.spinner("Génération du camembert..."):
                                df, fig = report_plastic_ocean_distribution()
                                st.pyplot(fig)

                                # Top 5 pollueurs
                                top_5 = df.nlargest(5, 'Share of global plastics emitted to ocean')
                                st.subheader("🔴 Top 5 pollueurs océaniques")
                                st.dataframe(top_5[['Entity', 'Share of global plastics emitted to ocean']])

                                # Statistiques pollution
                                total_pollution = df['Share of global plastics emitted to ocean'].sum()
                                top_10_pollution = df.nlargest(10, 'Share of global plastics emitted to ocean')['Share of global plastics emitted to ocean'].sum()

                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("🏆 Top pays", f"{top_5.iloc[0]['Entity']}")
                                with col2:
                                    st.metric("📊 Part top 10", f"{top_10_pollution:.1f}%")

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

        with tab2:
            st.markdown("### 💨 Augmentation du CO2")

            if reports_available:
                if st.button("📊 Générer corrélation CO2 ↔ Production plastique", key="co2_plastic"):
                    try:
                        with st.spinner("Analyse de corrélation CO2-Plastique..."):
                            df, fig, correlation = report_plastic_co2_correlation()
                            st.pyplot(fig)

                            # Métriques de corrélation
                            st.subheader("📊 Analyse statistique")
                            display_correlation_metrics(correlation, "CO2 vs Production Plastique")

                            # Interprétation
                            st.markdown("""
                            **🎯 Interprétation :**
                            - Une forte corrélation positive indique que l'augmentation des émissions CO2 
                              suit l'augmentation de la production plastique
                            - Cette relation illustre le lien entre industrialisation et pollution atmosphérique
                            - Les deux phénomènes partagent les mêmes causes : combustion d'énergies fossiles
                            """)

                            # Résumé des données
                            with st.expander("📋 Résumé des données"):
                                stats_config = {
                                    'emissions_total': {'name': 'Émissions CO2', 'decimals': 0},
                                    'plastic_production': {'name': 'Production Plastique', 'decimals': 0}
                                }
                                summary = create_summary_stats(df, stats_config)
                                st.dataframe(summary)

                            # Période d'analyse
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(f"📅 **Période :** {df['Year'].min()} - {df['Year'].max()}")
                            with col2:
                                st.info(f"📊 **Années analysées :** {len(df)}")

                    except Exception as e:
                        st.error(f"❌ Erreur : {e}")
                        import traceback
                        st.code(traceback.format_exc())

        with tab3:
            st.markdown("### ⚗️ Acidification des eaux")


            if reports_available:
                # Deux options : acidification seule ou avec CO2
                acid_option = st.radio(
                    "Choisir l'analyse",
                    ["📈 Évolution pH seule", "🔗 Corrélation pH ↔ CO2"],
                    key="acid_option"
                )

                if acid_option == "📈 Évolution pH seule":
                    if st.button("📊 Générer rapport acidification", key="acidification"):
                        try:
                            with st.spinner("Génération du rapport d'acidification..."):
                                df, fig = report_acidification()
                                st.pyplot(fig)

                                # Statistiques pH
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("🔴 pH minimum", f"{df['Ocean_acidification(in_PH)'].min():.3f}")
                                with col2:
                                    st.metric("🟢 pH maximum", f"{df['Ocean_acidification(in_PH)'].max():.3f}")
                                with col3:
                                    st.metric("📊 pH moyen", f"{df['Ocean_acidification(in_PH)'].mean():.3f}")

                                # Tendance et alertes
                                trend = df['Ocean_acidification(in_PH)'].iloc[-1] - df['Ocean_acidification(in_PH)'].iloc[0]
                                trend_color = "🔴" if trend < 0 else "🟢"
                                st.info(f"{trend_color} **Tendance globale :** {trend:+.3f} unités pH sur la période")

                                # Alerte acidification
                                if trend < -0.1:
                                    st.error("⚠️ **ALERTE :** Acidification significative détectée ! (baisse > 0.1 pH)")
                                elif trend < 0:
                                    st.warning("⚡ **ATTENTION :** Tendance à l'acidification détectée")

                                with st.expander("📋 Données pH"):
                                    st.dataframe(df)

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

                else:  # Corrélation pH ↔ CO2
                    if st.button("🔗 Générer corrélation pH ↔ CO2", key="acid_co2"):
                        try:
                            with st.spinner("Analyse corrélation Acidification-CO2..."):
                                df, fig, correlation = report_acidification_co2_correlation()
                                st.pyplot(fig)

                                # Métriques de corrélation
                                st.subheader("📊 Analyse de corrélation critique")
                                display_correlation_metrics(correlation, "CO2 vs Acidification")

                                # Interprétation détaillée
                                st.markdown("""
                                **🎯 Interprétation scientifique :**
                                - Une corrélation négative forte indique que l'augmentation du CO2 atmosphérique 
                                  correspond à une diminution du pH océanique (acidification)
                                - **Mécanisme :** CO2 + H2O → H2CO3 → H+ + HCO3- (baisse du pH)
                                - Cette relation confirme le lien direct entre émissions anthropiques 
                                  et dégradation chimique des océans
                                - **Seuil critique :** pH < 7.8 représente un danger pour les écosystèmes marins
                                """)

                                # Données période et alertes
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.info(f"📅 **Période analysée :** {df['year'].min()} - {df['year'].max()}")
                                with col2:
                                    st.info(f"📊 **Observations :** {len(df)} années")

                                # Projection et alerte
                                current_ph = df['Ocean_acidification(in_PH)'].iloc[-1]
                                if current_ph < 7.9:
                                    st.error(f"🚨 **ALERTE CRITIQUE :** pH actuel ({current_ph:.3f}) approche du seuil critique !")
                                elif current_ph < 8.0:
                                    st.warning(f"⚠️ **SURVEILLANCE :** pH actuel ({current_ph:.3f}) nécessite une surveillance")

                                with st.expander("📋 Données corrélation CO2-pH"):
                                    st.dataframe(df)

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback
                            st.code(traceback.format_exc())

        with tab4:
            st.markdown("### 🐠 Impact sur la biodiversité marine")

            if reports_available:
                # Sous-onglets pour la biodiversité
                bio_option = st.radio(
                    "Choisir l'analyse biodiversité",
                    ["📊 Distribution Liste Rouge", "🔗 Corrélation Acidification ↔ Biodiversité"],
                    key="bio_option"
                )

                if bio_option == "📊 Distribution Liste Rouge":
                    if st.button("🐠 Générer rapport Liste Rouge", key="red_list"):
                        try:
                            with st.spinner("Génération du rapport Liste Rouge..."):
                                df, fig = report_redlist()
                                st.pyplot(fig)

                                # Statistiques biodiversité
                                st.subheader("🐠 Statistiques de biodiversité")
                                latest_year = df['Year'].max()
                                latest_data = df[df['Year'] == latest_year]

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("📅 Année analysée", latest_year)
                                with col2:
                                    st.metric("🌍 Nombre d'entités", len(latest_data))
                                with col3:
                                    avg_index = latest_data['_15_5_1__er_rsk_lst'].mean()
                                    st.metric("📊 Index moyen", f"{avg_index:.3f}")

                                # Analyse de l'état de la biodiversité
                                if avg_index < 0.7:
                                    st.error("🚨 **ALERTE CRITIQUE :** Index biodiversité très faible !")
                                elif avg_index < 0.8:
                                    st.warning("⚠️ **PRÉOCCUPANT :** Déclin notable de la biodiversité")
                                else:
                                    st.success("✅ **ACCEPTABLE :** État de la biodiversité stable")

                                # Distribution des pays
                                st.subheader("🌍 Répartition par niveau de risque")


                                # Catégorisation
                                def categorize_risk(index_val):
                                    if index_val < 0.6:
                                        return "🔴 Critique"
                                    elif index_val < 0.7:
                                        return "🟠 Élevé"
                                    elif index_val < 0.8:
                                        return "🟡 Modéré"
                                    else:
                                        return "🟢 Faible"


                                latest_data['Niveau_Risque'] = latest_data['_15_5_1__er_rsk_lst'].apply(categorize_risk)
                                risk_counts = latest_data['Niveau_Risque'].value_counts()

                                for risk, count in risk_counts.items():
                                    st.metric(risk, f"{count} pays/entités")

                                with st.expander("📋 Données Liste Rouge détaillées"):
                                    st.dataframe(
                                        latest_data[['Entity', '_15_5_1__er_rsk_lst', 'Niveau_Risque']].sort_values(
                                            '_15_5_1__er_rsk_lst'))

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback

                            st.code(traceback.format_exc())

                else:  # Corrélation Acidification ↔ Biodiversité
                    if st.button("🔗 Générer corrélation Acidification ↔ Biodiversité", key="acid_biodiversity"):
                        try:
                            with st.spinner("Analyse corrélation Acidification-Biodiversité..."):
                                df, fig, correlation = report_acidification_redlist_correlation()
                                st.pyplot(fig)

                                # Métriques de corrélation
                                st.subheader("📊 Analyse de corrélation écologique")
                                display_correlation_metrics(correlation, "Acidification vs Biodiversité")

                                # Interprétation écologique détaillée
                                st.markdown("""
                                **🎯 Interprétation écologique :**
                                - Une corrélation positive indique que la baisse du pH (acidification) 
                                  correspond à une augmentation de l'index Liste Rouge (plus d'espèces menacées)
                                - **Mécanisme biologique :** L'acidification perturbe la formation des coquilles 
                                  et squelettes calcaires (coraux, mollusques, crustacés)
                                - **Impact en chaîne :** La dégradation des écosystèmes calcaires affecte 
                                  toute la chaîne alimentaire marine
                                - **Seuils critiques :** pH < 7.8 = stress majeur pour les organismes calcifiants
                                """)

                                # Analyse des tendances temporelles
                                st.subheader("📈 Tendances temporelles")

                                # Calcul des tendances
                                ph_trend = df['Ocean_acidification(in_PH)'].iloc[-1] - \
                                           df['Ocean_acidification(in_PH)'].iloc[0]
                                bio_trend = df['red_list_index'].iloc[-1] - df['red_list_index'].iloc[0]

                                col1, col2 = st.columns(2)
                                with col1:
                                    trend_ph_color = "🔴" if ph_trend < 0 else "🟢"
                                    st.metric(
                                        f"{trend_ph_color} Évolution pH",
                                        f"{ph_trend:+.3f}",
                                        help="Variation du pH sur la période étudiée"
                                    )
                                with col2:
                                    trend_bio_color = "🔴" if bio_trend > 0 else "🟢"  # Plus d'index = plus de menaces
                                    st.metric(
                                        f"{trend_bio_color} Évolution biodiversité",
                                        f"{bio_trend:+.3f}",
                                        help="Variation de l'index Liste Rouge (+ = plus de menaces)"
                                    )

                                # Alertes combinées
                                if ph_trend < -0.05 and bio_trend > 0.05:
                                    st.error(
                                        "🚨 **DOUBLE ALERTE :** Acidification ET dégradation biodiversité détectées !")
                                elif ph_trend < -0.02:
                                    st.warning(
                                        "⚠️ **SURVEILLANCE :** Acidification en cours, impact sur biodiversité possible")

                                # Prédictions et scénarios
                                st.subheader("🔮 Implications futures")

                                current_ph = df['Ocean_acidification(in_PH)'].iloc[-1]
                                current_bio = df['red_list_index'].iloc[-1]

                                st.info(f"""
                                **📊 État actuel :**
                                - pH océanique : {current_ph:.3f}
                                - Index biodiversité : {current_bio:.3f}

                                **🎯 Scénarios :**
                                - Si pH continue de baisser → Aggravation des menaces sur espèces calcifiantes
                                - Récifs coralliens particulièrement vulnérables (pH optimal > 8.1)
                                - Impact cascadant sur pêcheries et écosystèmes côtiers
                                """)

                                # Données détaillées
                                with st.expander("📋 Données corrélation Acidification-Biodiversité"):
                                    # Ajout de colonnes calculées pour l'analyse
                                    df_display = df.copy()
                                    df_display['Acidification_Niveau'] = df_display['Ocean_acidification(in_PH)'].apply(
                                        lambda
                                            x: "🔴 Critique" if x < 7.9 else "🟠 Préoccupant" if x < 8.0 else "🟡 Surveillance" if x < 8.1 else "🟢 Normal"
                                    )
                                    df_display['Biodiversite_Niveau'] = df_display['red_list_index'].apply(
                                        lambda
                                            x: "🔴 Très menacé" if x > 0.8 else "🟠 Menacé" if x > 0.6 else "🟡 Vulnérable" if x > 0.4 else "🟢 Stable"
                                    )

                                    st.dataframe(df_display[['year', 'Ocean_acidification(in_PH)', 'red_list_index',
                                                             'Acidification_Niveau', 'Biodiversite_Niveau']])

                                # Période d'analyse
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.info(f"📅 **Période analysée :** {df['year'].min()} - {df['year'].max()}")
                                with col2:
                                    st.info(f"📊 **Années de données :** {len(df)}")

                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                            import traceback

                            st.code(traceback.format_exc())


    # ===== INTERCONNEXIONS =====
    else:  # Interconnexions et Corrélations
        st.subheader("🔗 Interconnexions et Corrélations")
        st.markdown("*Synthèse des relations entre tous les phénomènes océaniques*")

        if reports_available:
            st.success("✅ **Toutes les analyses de corrélation sont opérationnelles !**")

            # Vue d'ensemble des corrélations
            st.markdown("""
            ### 📊 Résumé des analyses disponibles :
            
            **🌡️ Axe Climatique (Sophie) :**
            - ✅ Chaleur océanique → Évolution temporelle
            - ✅ Fonte des glaciers → Évolution temporelle  
            - ✅ Niveau des mers → Évolution temporelle
            - ✅ **Corrélation :** Glaciers ↔ Chaleur océanique
            - ✅ **Corrélation :** Glaciers ↔ Niveau des mers
            
            **🏭 Axe Pollution (Julien) :**
            - ✅ Plastiques (micro/macro) → Évolution temporelle
            - ✅ Production plastique → Évolution mondiale  
            - ✅ Pollution océanique → Répartition par pays
            - ✅ Acidification → Évolution pH
            - ✅ **Corrélation :** CO2 ↔ Production plastique
            - ✅ **Corrélation :** CO2 ↔ Acidification océanique
            
            **🔗 Interconnexions transversales :**
            - ✅ Lien industrialisation → pollution multiple (plastique + CO2)
            - ✅ Lien émissions → acidification (impact chimique)
            - ✅ Lien réchauffement → fonte → élévation (chaîne climatique)
            """)

            # Panel de contrôle pour corrélations rapides
            st.subheader("🎛️ Panel de contrôle - Corrélations rapides")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🌡️ Corrélations Climatiques")
                if st.button("🧊 Glaciers ↔ Chaleur", key="quick_glacier_heat"):
                    try:
                        df, fig, corr = report_glacier_heat_correlation()
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                            display_correlation_metrics(corr, "Glaciers-Chaleur")
                    except Exception as e:
                        st.error(f"❌ {e}")

                if st.button("🌊 Glaciers ↔ Niveau mers", key="quick_glacier_sea"):
                    try:
                        df, fig, corr = report_glaciermelting_sealevel_correlation()
                        st.pyplot(fig)
                        display_correlation_metrics(corr, "Glaciers-Niveau")
                    except Exception as e:
                        st.error(f"❌ {e}")

            with col2:
                st.markdown("#### 🏭 Corrélations Pollution")
                if st.button("💨 CO2 ↔ Plastique", key="quick_co2_plastic"):
                    try:
                        df, fig, corr = report_plastic_co2_correlation()
                        st.pyplot(fig)
                        display_correlation_metrics(corr, "CO2-Plastique")
                    except Exception as e:
                        st.error(f"❌ {e}")

                if st.button("⚗️ CO2 ↔ Acidification", key="quick_co2_acid"):
                    try:
                        df, fig, corr = report_acidification_co2_correlation()
                        st.pyplot(fig)
                        display_correlation_metrics(corr, "CO2-Acidification")
                    except Exception as e:
                        st.error(f"❌ {e}")

            # Synthèse narrative
            st.subheader("📖 Synthèse narrative")
            st.markdown("""
            **🎯 Message central :** Les océans sont au cœur d'un système d'interconnexions complexes 
            où réchauffement climatique et pollution industrielle se renforcent mutuellement.
            
            **🔗 Chaînes causales identifiées :**
            
            1. **Chaîne climatique :** CO2 → Réchauffement → Chaleur océanique → Fonte glaciers → Élévation niveau
            2. **Chaîne chimique :** CO2 → Acidification → Dégradation écosystèmes marins
            3. **Chaîne industrielle :** Industrialisation → (CO2 + Plastiques) → Pollution multiple
            
            **⚠️ Effets de synergie :** Les phénomènes ne sont pas isolés mais s'amplifient mutuellement, 
            créant un cercle vicieux de dégradation océanique.
            """)

        else:
            st.error("❌ Module de rapports non disponible - Impossible d'afficher les interconnexions")

# ===== ONGLET DOCUMENTATION =====
else:  # Documentation
    st.header("📚 Documentation et Sources")
    st.markdown("*Accès à toutes les sources de données et documentation technique*")

    # Sous-sections documentation
    doc_section = st.selectbox(
        "Choisir une section",
        ["📊 Sources des données", "🔧 Documentation technique", "📖 Ressources additionnelles"]
    )

    if doc_section == "📊 Sources des données":
        st.subheader("📊 Sources des données utilisées")
        st.markdown("*Toutes les sources sont fiables et vérifiables*")

        # Données de pollution/plastique
        with st.expander("🏭 **Données sur la pollution plastique**"):
            st.markdown("""
            ### Microplastiques
            - **Source :** [Our World in Data - Microplastiques](https://ourworldindata.org/grapher/microplastics-in-ocean?time=1950..2050&tab=line)
            - **Description :** Évolution des microplastiques océaniques (1950-2050)
            - **Format :** Données temporelles par entité géographique

            ### Macroplastiques  
            - **Source :** [Our World in Data - Macroplastiques](https://ourworldindata.org/grapher/macroplastics-in-ocean)
            - **Description :** Accumulation des macroplastiques dans l'océan

            ### Déchets plastiques océaniques
            - **Source :** [Our World in Data - Déchets plastiques](https://ourworldindata.org/grapher/share-of-global-plastic-waste-emitted-to-the-ocean)
            - **Description :** Part mondiale des déchets plastiques émis dans l'océan

            ### Production plastique mondiale
            - **Source :** [Our World in Data - Production](https://ourworldindata.org/grapher/global-plastics-production)
            - **Description :** Production mondiale de plastiques

            ### Import de déchets plastiques
            - **Source :** [Our World in Data - Explorer](https://ourworldindata.org/explorers/plastic-pollution)
            - **Description :** Analyse des flux d'import de déchets plastiques
            """)

        # Données climatiques
        with st.expander("🌡️ **Données climatiques et océaniques**"):
            st.markdown("""
            ### Réchauffement océanique
            - **Source :** [NASA - Ocean Warming](https://www.nasa.gov/wp-content/uploads/2023/06/oceanwarmingannualclassroomdatasheet.pdf)
            - **Description :** Données annuelles de réchauffement des océans
            - **Organisme :** NASA

            ### Acidification océanique
            - **Source :** [Kaggle - Ocean Acidification](https://www.kaggle.com/datasets/jayasurya666/global-ocean-acidification-trends-and-impacts)
            - **Description :** Tendances mondiales d'acidification et impacts

            ### Niveau des océans
            - **Source :** [Our World in Data - Niveau des mers](https://ourworldindata.org/grapher/sea-level)
            - **Description :** Évolution du niveau des océans

            ### Chaleur océanique
            - **Source :** [Our World in Data - Chaleur océan](https://ourworldindata.org/grapher/ocean-heat-top-2000m)
            - **Description :** Contenu de chaleur océanique (0-2000m)

            ### Fonte des glaciers
            - **Source :** [EPA - Glacier Melting](https://www.epa.gov/system/files/documents/2024-05/glaciers_documentation.pdf)
            - **Description :** Documentation sur la fonte des glaciers
            - **Organisme :** EPA (Environmental Protection Agency)
            """)

        # Données biodiversité
        with st.expander("🐠 **Données sur la biodiversité**"):
            st.markdown("""
            ### Index Liste Rouge
            - **Source :** [Our World in Data - Red List Index](https://ourworldindata.org/grapher/red-list-index)
            - **Description :** Index de la Liste Rouge des espèces menacées
            - **Utilité :** Mesure de l'évolution de la biodiversité marine
            """)

    elif doc_section == "🔧 Documentation technique":
        st.subheader("🔧 Documentation technique")

        with st.expander("📁 **Structure du projet**"):
            st.code("""
            OceanState_Analysis/
            ├── app.py                          # Application Streamlit principale
            ├── oceanstate_analysis/           # Module d'analyse
            │   ├── analysis/
            │   │   ├── plots.py               # Fonctions de visualisation
            │   │   ├── preprocessing.py       # Préparation des données
            │   │   └── utils.py               # Utilitaires
            │   ├── reports/                   # Module de rapports
            │   │   ├── __init__.py           # Exports des fonctions
            │   │   └── reports.py            # Fonctions de génération
            │   ├── data/                      # Données du projet
            │   │   ├── raw/                   # Données brutes
            │   │   ├── processed/             # Données traitées
            │   │   └── external/              # Données externes
            │   └── docs/                      # Documentation
            └── requirements.txt               # Dépendances Python
            """)

        with st.expander("📦 **Fonctions de rapport disponibles**"):
            st.markdown("""
            ### 🌡️ Axe Climatique (Sophie)
            - `report_heat()` - Évolution chaleur océanique
            - `report_glaciermelting()` - Fonte des glaciers
            - `report_sealevel()` - Niveau des mers
            - `report_glacier_heat_correlation()` - Corrélation glaciers-chaleur
            - `report_glaciermelting_sealevel_correlation()` - Corrélation glaciers-niveau

            ### 🏭 Axe Pollution (Julien)
            - `report_acidification()` - Évolution pH océanique
            - `report_plastic_evolution()` - Micro/macroplastiques
            - `report_plastic_waste_countries()` - Déchets par pays
            - `report_plastic_production_global()` - Production mondiale
            - `report_plastic_ocean_distribution()` - Répartition océanique
            - `report_plastic_co2_correlation()` - Corrélation CO2-plastique
            - `report_acidification_co2_correlation()` - Corrélation CO2-acidification

            ### 🔧 Utilitaires
            - `display_correlation_metrics()` - Affichage métriques corrélation
            - `create_summary_stats()` - Statistiques résumé
            """)

        with st.expander("⚙️ **Installation et utilisation**"):
            st.markdown("""
            ### Installation
            ```bash
            pip install -r requirements.txt
            ```

            ### Lancement de l'application
            ```bash
            streamlit run app.py
            ```

            ### Utilisation
            1. Naviguer via le menu latéral
            2. Sélectionner l'axe d'analyse (Sophie/Julien/Interconnexions)
            3. Cliquer sur les boutons pour générer les rapports
            4. Explorer les visualisations et corrélations
            """)

    else:  # Ressources additionnelles
        st.subheader("📖 Ressources additionnelles")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 🔗 Liens utiles
            - [Our World in Data](https://ourworldindata.org/) - Données mondiales
            - [NASA Climate](https://climate.nasa.gov/) - Données climatiques NASA
            - [EPA](https://www.epa.gov/) - Agence protection environnement US
            - [Streamlit Documentation](https://docs.streamlit.io/) - Documentation Streamlit

            ### 📚 Références scientifiques
            - IPCC Reports on Ocean and Climate
            - Marine Pollution Research Papers
            - Ocean Acidification Studies
            """)

        with col2:
            st.markdown("""
            ### 👥 Équipe projet
            **Julien Dante**
            - Repository GitHub et architecture
            - Configuration GitFlow
            - Trame narrative
            - Axe pollution et acidification

            **Sophie Aholou** 
            - Gestion de projet
            - Axe réchauffement climatique
            - Analyse des données

            ### 📞 Contact
            *Projet académique - Data Visualisation*
            """)

        # Note de version et statut
        st.markdown("---")
        st.info("""
        📋 **Statut du projet :** Application complètement opérationnelle

        ✅ **Dernière mise à jour :** Intégration complète de tous les graphiques et corrélations

        🎯 **Fonctionnalités :** 14 types de rapports + corrélations + métriques interactives
        """)

# Footer
st.markdown("---")
st.markdown("*🌊 Application développée pour l'analyse de l'état de l'océan - Projet Data Visualisation*")
st.markdown("*🚀 Version complète avec toutes les visualisations intégrées*")