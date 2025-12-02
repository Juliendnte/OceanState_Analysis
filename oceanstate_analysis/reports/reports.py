"""
Module de rapports pour l'application OceanState Analysis
Contient toutes les fonctions de génération de rapports avec visualisations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr
import plotly.graph_objects as go
import streamlit as st

from analysis.preprocessing import (
    load_and_clean_acid_data,
    load_and_clean_CO2_emission_data,
    load_and_clean_microplastic_data,
    load_and_clean_macroplastic_data,
    load_and_clean_plastic_waste_data,
    load_and_clean_plastic_production_data,
    load_and_clean_plastic_waste_ocean_data,
    load_and_clean_heat_data,
    load_and_clean_sealevel_data,
    load_and_clean_glaciers_data,
    load_and_clean_red_list_index_data,
    load_and_clean_global_warning_data
)

from analysis.plots import (
    plot_ph_evolution,
    plot_plastic_accumulation,
    plot_micro_macro_plastic,
    plot_evolution_emission_plastic,
    plot_production_plastic,
    plot_repartition_plastic,
    plot_relation_acidification_co2,
    plot_relation_acidification_redlist,
    plot_relation_glaciermelting_heat,
    plot_relation_plastic_co2,
    plot_heat,
    plot_sealevel,
    plot_relation_glaciermelting_sealevel,
    plot_glaciermelting,
    plot_redlist,
    plot_globalwarn
)

# Configuration globale des graphiques
plt.rcParams['figure.figsize'] = (14, 8)
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 12

def report_acidification():
    """
    Génère un rapport complet sur l'acidification océanique
    Returns: DataFrame avec les données et figure matplotlib
    """
    df = load_and_clean_acid_data()
    df = df[["year", "Ocean_acidification(in_PH)"]]
    df.dropna(inplace=True)
    return df, plot_ph_evolution(df)

def report_heat():
    df = load_and_clean_heat_data()
    return df, plot_heat(df)

def report_glaciermelting_sealevel_correlation():
    df_glaciers = load_and_clean_glaciers_data()
    df_sea = load_and_clean_sealevel_data()

    # Extraire l'année depuis Day
    df_sea["Year"] = pd.to_datetime(df_sea["Day"]).dt.year

    # Calculer la moyenne des trois mesures du niveau de la mer

    df_sea["sea_level_avg"] = df_sea[[
        "sea_level_church_and_white_2011",
        "sea_level_uhslc",
        "sea_level_average"
    ]].mean(axis=1)

    # Garder uniquement Year et la moyenne
    df_sea = df_sea[["Year", "sea_level_avg"]]

    # Fusionner avec les glaciers sur Year
    df_combined = df_glaciers.merge(df_sea, on="Year", how="inner")
    correlation = pearsonr(df_combined["Mean cumulative mass balance"],
                           df_combined["sea_level_avg"])
    fig = plot_relation_glaciermelting_sealevel(df_combined)
    return df_combined, fig, correlation

def report_glaciermelting():
    df = load_and_clean_glaciers_data()
    fig = plot_glaciermelting(df)
    return df, fig

def report_sealevel():
    df = load_and_clean_sealevel_data()
    fig = plot_sealevel(df)
    return df, fig

def report_redlist():
    df = load_and_clean_red_list_index_data()
    fig = plot_redlist(df)
    return df, fig

def report_acidification_redlist_correlation():
    df_acid = load_and_clean_acid_data()
    df_red_list = load_and_clean_red_list_index_data()
    df_red_global = df_red_list.groupby('Year')['_15_5_1__er_rsk_lst'].mean().reset_index()
    df_red_global.columns = ['year', 'red_list_index']

    # Nettoyage des données d'acidification
    df_acid_clean = df_acid[['year', 'Ocean_acidification(in_PH)']].dropna()
    df_merged = pd.merge(df_acid_clean, df_red_global, on='year', how='inner')
    fig = plot_relation_acidification_redlist(df_merged)
    corr_coef, p_value = pearsonr(df_merged['Ocean_acidification(in_PH)'], df_merged['red_list_index'])
    return df_merged, fig, corr_coef

def report_global_warn():
    df = load_and_clean_global_warning_data()
    fig = plot_globalwarn(df)
    return df, fig

def report_acidification_co2_correlation():
    """
    Génère un rapport sur la corrélation entre CO2 et acidification
    Returns: DataFrame fusionné, figure matplotlib, corrélation
    """
    # Chargement des données
    df_acid = load_and_clean_acid_data()
    df_acid = df_acid[["year", "Ocean_acidification(in_PH)"]]
    df_acid = df_acid.dropna()

    df_co2 = load_and_clean_CO2_emission_data()
    co2_mondial_annuel = df_co2.groupby('Year')['emissions_total'].sum().reset_index()
    co2_mondial_annuel = co2_mondial_annuel.rename(columns={'Year': 'year'})

    # Fusion des datasets
    merged_co2_acid = df_acid.merge(co2_mondial_annuel, on='year', how='inner')

    # Calcul de la corrélation
    correlation = pearsonr(merged_co2_acid['emissions_total'],
                           merged_co2_acid['Ocean_acidification(in_PH)'])

    # Création du graphique double axe
    fig, ax1 = plt.subplots(figsize=(18, 10))

    # Graphique CO2 (axe gauche)
    color1 = 'darkred'
    ax1.set_xlabel('Année', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Émissions CO2 mondiales (tonnes)', color=color1, fontsize=16, fontweight='bold')
    line1 = ax1.plot(merged_co2_acid['year'], merged_co2_acid['emissions_total'],
                     color=color1, linewidth=4, marker='o', markersize=6,
                     markerfacecolor='red', markeredgecolor='darkred', markeredgewidth=2,
                     label='Émissions CO2 mondiales', alpha=0.9)
    ax1.tick_params(axis='y', labelcolor=color1, labelsize=14)
    ax1.grid(True, alpha=0.3)

    # Graphique pH (axe droit)
    ax2 = ax1.twinx()
    color2 = 'darkblue'
    ax2.set_ylabel('pH océanique', color=color2, fontsize=16, fontweight='bold')
    line2 = ax2.plot(merged_co2_acid['year'], merged_co2_acid['Ocean_acidification(in_PH)'],
                     color=color2, linewidth=4, marker='s', markersize=6,
                     markerfacecolor='blue', markeredgecolor='darkblue', markeredgewidth=2,
                     label='pH océanique', alpha=0.9)
    ax2.tick_params(axis='y', labelcolor=color2, labelsize=14)

    # Configuration du titre avec corrélation
    plt.title('Relation Critique : Émissions CO2 vs Acidification Océanique\n' +
              f'Analyse temporelle {merged_co2_acid["year"].min()}-{merged_co2_acid["year"].max()}\n' +
              f'Corrélation: r = {correlation[0]:.4f} (p-value: {correlation[1]:.2e})',
              fontsize=20, fontweight='bold', pad=25)

    # Légende combinée
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
               fontsize=14, framealpha=0.95, fancybox=True, shadow=True)

    plt.tight_layout()

    return merged_co2_acid, fig, correlation

def report_plastic_evolution():
    """
    Génère un rapport sur l'évolution des plastiques (micro/macro)
    Returns: DataFrame fusionné, figure matplotlib
    """
    # Chargement et fusion des données
    df_micro = load_and_clean_microplastic_data()
    df_macro = load_and_clean_macroplastic_data()

    # Suppression des colonnes Code si elles existent
    if 'Code' in df_micro.columns:
        df_micro.drop(columns="Code", inplace=True)
    if 'Code' in df_macro.columns:
        df_macro.drop(columns="Code", inplace=True)

    # Fusion des données
    df_plastics = df_micro.merge(df_macro, on=['Entity', 'year'], how='inner')

    # Création du graphique double
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Microplastiques
    sns.lineplot(data=df_plastics, x='year', y='microplastics',
                 hue='Entity', ax=ax1, marker='o')
    ax1.set_title('Évolution des Microplastiques')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Microplastiques (tonnes)')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Macroplastiques
    sns.lineplot(data=df_plastics, x='year', y='macroplastics',
                 hue='Entity', ax=ax2, marker='s')
    ax2.set_title('Évolution des Macroplastiques')
    ax2.set_xlabel('Année')
    ax2.set_ylabel('Macroplastiques (tonnes)')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()

    return df_plastics, fig

def report_plastic_waste_countries():
    """
    Génère un rapport sur les déchets plastiques par pays (top 10)
    Returns: DataFrame, figure matplotlib
    """
    df_plastic_waste = load_and_clean_plastic_waste_data()

    # Identifier les top 10 pays pour l'année la plus récente
    latest_year = df_plastic_waste['Year'].max()
    top_countries = df_plastic_waste[df_plastic_waste['Year'] == latest_year].nlargest(
        10, 'Imports of plastic waste via all modes of transport')

    # Création du graphique
    fig, ax = plt.subplots(figsize=(16, 10))

    for country in top_countries['Entity'].values:
        country_data = df_plastic_waste[df_plastic_waste['Entity'] == country]
        ax.plot(country_data['Year'],
                country_data['Imports of plastic waste via all modes of transport'],
                marker='o', linewidth=2, label=country)

    ax.set_title('Évolution des Déchets Plastiques Mal Gérés par Pays (Top 10)',
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Année', fontsize=12)
    ax.set_ylabel('Déchets plastiques mal gérés (tonnes)', fontsize=12)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return df_plastic_waste, fig

def report_plastic_production_global():
    """
    Génère un rapport sur la production mondiale de plastique
    Returns: DataFrame agrégé, figure matplotlib
    """
    df_plastic_production = load_and_clean_plastic_production_data()

    # Agrégation par année
    production_annuelle = df_plastic_production.groupby('Year')['plastic_production'].sum().reset_index()

    # Création du graphique
    fig, ax = plt.subplots(figsize=(14, 8))

    ax.plot(production_annuelle['Year'], production_annuelle['plastic_production'],
            marker='o', linewidth=2, markersize=6)
    ax.set_title('Évolution de la Production Annuelle Mondiale de Plastique',
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Année', fontsize=12)
    ax.set_ylabel('Production (tonnes)', fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return production_annuelle, fig

def report_plastic_ocean_distribution():
    """
    Génère un rapport sur la répartition de la pollution plastique maritime
    Returns: DataFrame, figure matplotlib (camembert)
    """
    df_plastic_waste_ocean = load_and_clean_plastic_waste_ocean_data()

    # Top 15 + autres
    top_15_ocean = df_plastic_waste_ocean.nlargest(15, 'Share of global plastics emitted to ocean')
    autres = df_plastic_waste_ocean.iloc[15:]['Share of global plastics emitted to ocean'].sum()

    # Données pour le camembert
    labels = list(top_15_ocean['Entity']) + ['Autres pays']
    sizes = list(top_15_ocean['Share of global plastics emitted to ocean']) + [autres]

    # Création du graphique
    fig, ax = plt.subplots(figsize=(12, 12))

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title('Répartition de la Pollution Plastique Maritime par Pays (2019)',
                 fontsize=16, fontweight='bold')
    ax.axis('equal')
    plt.tight_layout()

    return df_plastic_waste_ocean, fig

def report_plastic_co2_correlation():
    """
    Génère un rapport sur la corrélation entre production plastique et CO2
    Returns: DataFrame fusionné, figure matplotlib, corrélation
    """
    # Chargement des données
    df_co2 = load_and_clean_CO2_emission_data()
    df_plastic_production = load_and_clean_plastic_production_data()

    # Agrégation
    co2_mondial = df_co2.groupby('Year')['emissions_total'].sum().reset_index()
    co2_mondial = co2_mondial[co2_mondial['Year'] >= 1950]

    production_mondiale = df_plastic_production.groupby('Year')['plastic_production'].sum().reset_index()

    # Fusion
    merged_temporal = co2_mondial.merge(production_mondiale, on='Year', how='inner')

    # Calcul de la corrélation
    correlation = pearsonr(merged_temporal['emissions_total'],
                           merged_temporal['plastic_production'])

    # Création du graphique double axe
    fig, ax1 = plt.subplots(figsize=(16, 8))

    color1 = 'darkred'
    ax1.set_xlabel('Année', fontsize=14)
    ax1.set_ylabel('Émissions CO2 mondiales', color=color1, fontsize=14)
    line1 = ax1.plot(merged_temporal['Year'], merged_temporal['emissions_total'],
                     color=color1, linewidth=3, marker='o', markersize=4,
                     label='Émissions CO2')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = 'darkblue'
    ax2.set_ylabel('Production mondiale de plastique', color=color2, fontsize=14)
    line2 = ax2.plot(merged_temporal['Year'], merged_temporal['plastic_production'],
                     color=color2, linewidth=3, marker='s', markersize=4,
                     label='Production plastique')
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.title('Évolution Parallèle : Émissions CO2 vs Production de Plastique (1950-2019)\n' +
              f'Corrélation: r = {correlation[0]:.4f} (p-value: {correlation[1]:.2e})',
              fontsize=16, fontweight='bold', pad=20)

    # Légende combinée
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()

    return merged_temporal, fig, correlation

def report_glacier_heat_correlation():
    """
    Génère un rapport sur la corrélation entre fonte des glaciers et chaleur océanique
    Returns: DataFrame fusionné, figure plotly, corrélation
    """
    try:

        df_heat = load_and_clean_heat_data()
        df_glaciers = load_and_clean_glaciers_data()

        # Calculer la moyenne des trois mesures de chaleur
        df_heat["ocean_heat_avg"] = df_heat[[
            "ocean_heat_content_noaa_2000m",
            "ocean_heat_content_mri_2000m",
            "ocean_heat_content_iap_2000m"
        ]].mean(axis=1)

        # Garder uniquement Year et la moyenne
        df_heat = df_heat[["Year", "ocean_heat_avg"]]

        # Fusionner avec les glaciers sur la colonne Year
        df_combined = pd.merge(df_glaciers, df_heat, on="Year", how="inner")

        # Calcul de la corrélation
        correlation = pearsonr(df_combined["Mean cumulative mass balance"],
                               df_combined["ocean_heat_avg"])

        # Création du graphique Plotly
        fig = go.Figure()

        # Glacier
        fig.add_trace(go.Scatter(
            x=df_combined["Year"],
            y=df_combined["Mean cumulative mass balance"],
            name="Masse cumulée glaciers",
            yaxis="y1",
            line=dict(color="blue")
        ))

        # Chaleur océanique
        fig.add_trace(go.Scatter(
            x=df_combined["Year"],
            y=df_combined["ocean_heat_avg"],
            name="Chaleur océanique",
            yaxis="y2",
            line=dict(color="orange")
        ))

        # Layout double axe
        fig.update_layout(
            title=f"Lien entre réchauffement des océans et fonte des glaciers<br>Corrélation: r = {correlation[0]:.4f} (p-value: {correlation[1]:.2e})",
            xaxis=dict(title="Année"),
            yaxis=dict(title="Masse cumulée des glaciers (mm w.e.)", side="left"),
            yaxis2=dict(title="Chaleur océanique (10^22 J)", overlaying="y", side="right"),
            legend=dict(x=0.05, y=0.95),
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return df_combined, fig, correlation

    except Exception as e:
        st.error(f"Erreur lors du chargement des données glaciers/chaleur: {e}")
        return None, None, None

def display_correlation_metrics(correlation, title="Corrélation"):
    """Affiche les métriques de corrélation dans Streamlit"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📊 Corrélation (r)", f"{correlation[0]:.4f}")

    with col2:
        # Interprétation de la corrélation
        abs_corr = abs(correlation[0])
        if abs_corr > 0.8:
            interpretation = "Très forte"
            color = "🟢"
        elif abs_corr > 0.6:
            interpretation = "Forte"
            color = "🟡"
        elif abs_corr > 0.3:
            interpretation = "Modérée"
            color = "🟠"
        else:
            interpretation = "Faible"
            color = "🔴"

        st.metric(f"{color} Force", interpretation)

    with col3:
        # Significativité statistique
        is_significant = correlation[1] < 0.05
        significance = "Significative" if is_significant else "Non significative"
        sig_color = "✅" if is_significant else "❌"
        st.metric(f"{sig_color} P-value", f"{correlation[1]:.2e}")

def create_summary_stats(df, columns_config):
    """Crée un résumé statistique formaté pour Streamlit"""
    stats_data = []

    for col, config in columns_config.items():
        if col in df.columns:
            stats_data.append({
                'Métrique': config['name'],
                'Minimum': f"{df[col].min():.{config.get('decimals', 2)}f}",
                'Maximum': f"{df[col].max():.{config.get('decimals', 2)}f}",
                'Moyenne': f"{df[col].mean():.{config.get('decimals', 2)}f}",
                'Médiane': f"{df[col].median():.{config.get('decimals', 2)}f}"
            })

    return pd.DataFrame(stats_data)