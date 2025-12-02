import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm


def plot_ph_evolution(df):
    plt.rcParams['figure.figsize'] = (12, 6)
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(df['year'], df['Ocean_acidification(in_PH)'],
            marker='o', linewidth=2, markersize=4, color='steelblue')
    ax.set_title('Évolution de l\'acidification océanique (pH) de 1950 à 2023',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Année')
    ax.set_ylabel('pH océanique')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def plot_plastic_accumulation(df):
    """Crée un graphique de l'accumulation des microplastiques."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='year', y='amount', hue='Entity', ax=ax)
    ax.set_title("Accumulation des microplastiques dans l'océan")
    ax.set_xlabel("Année")
    ax.set_ylabel("Quantité accumulée")
    return fig

def plot_micro_macro_plastic(df):
    plt.rcParams['figure.figsize'] = (12, 8)
    sns.set_style("whitegrid")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Microplastiques
    sns.lineplot(data=df, x='year', y='microplastics',
                 hue='Entity', ax=ax1, marker='o')
    ax1.set_title('Évolution des Microplastiques')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Déchets plastiques mal gérés (tonnes)')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Macroplastiques
    sns.lineplot(data=df, x='year', y='macroplastics',
                 hue='Entity', ax=ax2, marker='s')
    ax2.set_title('Évolution des Macroplastiques')
    ax2.set_xlabel('Année')
    ax2.set_ylabel('Déchets plastiques mal gérés (tonnes)')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

def plot_evolution_emission_plastic(df):
    plt.figure(figsize=(16, 10))

    latest_year = df['Year'].max()
    top_countries = df[df['Year'] == latest_year].nlargest(10, 'Imports of plastic waste via all modes of transport')

    for country in top_countries['Entity'].values:
        country_data = df[df['Entity'] == country]
        plt.plot(country_data['Year'], country_data['Imports of plastic waste via all modes of transport'],
                 marker='o', linewidth=2, label=country)

    plt.title('Évolution des Déchets Plastiques Mal Gérés par Pays (Top 10)', fontsize=16, fontweight='bold')
    plt.xlabel('Année', fontsize=12)
    plt.ylabel('Déchets plastiques mal gérés (tonnes)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_production_plastic(df):
    plt.figure(figsize=(14, 8))

    production_annuelle = df.groupby('Year')['plastic_production'].sum().reset_index()

    plt.plot(production_annuelle['Year'], production_annuelle['plastic_production'],
             marker='o', linewidth=2, markersize=6)
    plt.title('Évolution de la Production Annuelle Mondiale de Plastique', fontsize=16, fontweight='bold')
    plt.xlabel('Année', fontsize=12)
    plt.ylabel('Production', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_repartition_plastic(df):
    plt.figure(figsize=(12, 12))

    top_10_ocean = df.nlargest(15, 'Share of global plastics emitted to ocean')
    autres = df.iloc[15:]['Share of global plastics emitted to ocean'].sum()

    # Données pour le camembert
    labels = list(top_10_ocean['Entity']) + ['Autres pays']
    sizes = list(top_10_ocean['Share of global plastics emitted to ocean']) + [autres]

    # Création du camembert
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Répartition de la Pollution Plastique Maritime par Pays (2019)',
              fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def plot_relation_acidification_co2(df):
    fig, ax1 = plt.subplots(figsize=(18, 10))

    # Calcul de la corrélation
    correlation, p_value = pearsonr(df['emissions_total'], df['Ocean_acidification(in_PH)'])

    # Graphique CO2 (axe gauche)
    color1 = 'darkred'
    ax1.set_xlabel('Année', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Émissions CO2 mondiales (tonnes)', color=color1, fontsize=16, fontweight='bold')
    line1 = ax1.plot(df['year'], df['emissions_total'],
                     color=color1, linewidth=4, marker='o', markersize=6,
                     markerfacecolor='red', markeredgecolor='darkred', markeredgewidth=2,
                     label='Émissions CO2 mondiales', alpha=0.9)
    ax1.tick_params(axis='y', labelcolor=color1, labelsize=14)
    ax1.grid(True, alpha=0.3)

    # Graphique pH (axe droit)
    ax2 = ax1.twinx()
    color2 = 'darkblue'
    ax2.set_ylabel('pH océanique', color=color2, fontsize=16, fontweight='bold')
    line2 = ax2.plot(df['year'], df['Ocean_acidification(in_PH)'],
                     color=color2, linewidth=4, marker='s', markersize=6,
                     markerfacecolor='blue', markeredgecolor='darkblue', markeredgewidth=2,
                     label='pH océanique', alpha=0.9)
    ax2.tick_params(axis='y', labelcolor=color2, labelsize=14)

    # Configuration du titre et des légendes avec la corrélation
    plt.title('Relation Critique : Émissions CO2 vs Acidification Océanique\n' +
              f'Analyse temporelle {df["year"].min()}-{df["year"].max()}\n' +
              f'Corrélation: r = {correlation:.4f} (p-value: {p_value:.2e})',
              fontsize=20, fontweight='bold', pad=25)

    # Légende combinée
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left',
               fontsize=14, framealpha=0.95, fancybox=True, shadow=True)

    # Style amélioré
    ax1.tick_params(axis='x', labelsize=14)
    for spine in ax1.spines.values():
        spine.set_linewidth(2)
    for spine in ax2.spines.values():
        spine.set_linewidth(2)

    plt.tight_layout()
    return fig

def plot_relation_acidification_redlist(df):
    fig, ax1 = plt.subplots(figsize=(15, 10))

    # Calcul de la corrélation
    correlation, p_value = pearsonr(df['Ocean_acidification(in_PH)'], df['red_list_index'])

    # pH océanique (axe de gauche)
    color1 = 'steelblue'
    ax1.set_xlabel('Année', fontsize=14)
    ax1.set_ylabel('pH océanique', color=color1, fontsize=14)
    line1 = ax1.plot(df['year'], df['Ocean_acidification(in_PH)'],
                     'o-', color=color1, linewidth=3, markersize=7, label='pH océanique')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # Index Liste Rouge (axe de droite)
    ax2 = ax1.twinx()
    color2 = 'darkred'
    ax2.set_ylabel('Index Liste Rouge', color=color2, fontsize=14)
    line2 = ax2.plot(df['year'], df['red_list_index'],
                     's-', color=color2, linewidth=3, markersize=7, label='Index Liste Rouge')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Titre avec corrélation
    ax1.set_title('Évolution parallèle: Acidification océanique vs Biodiversité marine\n' +
                  f'Corrélation: r = {correlation:.4f} (p-value: {p_value:.2e})',
                  fontsize=18, fontweight='bold', pad=20)

    # Légende combinée
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right', fontsize=12)

    plt.tight_layout()
    return fig

def plot_relation_glaciermelting_heat(df):
    # Calcul de la corrélation

    fig = go.Figure()

    # Glacier
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Mean cumulative mass balance"],
        name="Masse cumulée glaciers",
        yaxis="y1",
        line=dict(color="blue")
    ))

    # Chaleur océanique
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["ocean_heat_avg"],
        name="Chaleur océanique",
        yaxis="y2",
        line=dict(color="orange")
    ))

    # Layout double axe avec corrélation dans le titre
    fig.update_layout(
        title=f"Lien entre réchauffement des océans et fonte des glaciers",
        xaxis=dict(title="Année"),
        yaxis=dict(title="Masse cumulée des glaciers (mm w.e.)", side="left"),
        yaxis2=dict(title="Chaleur océanique (10^22 J)", overlaying="y", side="right"),
        legend=dict(x=0.05, y=0.95),
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig

def plot_relation_glaciermelting_sealevel(df):
    x = df["sea_level_avg"]
    y = df["Mean cumulative mass balance"]

    # Calculer la régression linéaire

    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()
    y_pred = model.predict(X)

    # Créer le graphique
    fig = go.Figure()

    # Nuage de points (observations réelles)
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        name="Masse des glaciers",
        marker=dict(color="blue")
    ))

    # Ligne de régression (tendance)
    fig.add_trace(go.Scatter(
        x=x,
        y=y_pred,
        mode="lines",
        name="Tendance fonte",
        line=dict(color="red", width=3)
    ))

    # Mettre à jour le layout

    fig.update_layout(
        title="Lien entre fonte des glaciers et montée du niveau de la mer",
        xaxis_title="Niveau moyen de la mer (mm)",
        yaxis_title="Masse cumulée des glaciers (mm w.e.)",
        legend=dict(
            title="Légende",
            x=0.8,
            y=0.95
        )
    )
    # Afficher le graphique
    fig.show()

def plot_relation_plastic_co2(df):
    fig, ax1 = plt.subplots(figsize=(16, 8))

    # Calcul de la corrélation
    correlation, p_value = pearsonr(df['emissions_total'], df['plastic_production'])

    color1 = 'darkred'
    ax1.set_xlabel('Année', fontsize=14)
    ax1.set_ylabel('Émissions CO2 mondiales', color=color1, fontsize=14)
    line1 = ax1.plot(df['Year'], df['emissions_total'],
                     color=color1, linewidth=3, marker='o', markersize=4, label='Émissions CO2')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = 'darkblue'
    ax2.set_ylabel('Production mondiale de plastique', color=color2, fontsize=14)
    line2 = ax2.plot(df['Year'], df['plastic_production'],
                     color=color2, linewidth=3, marker='s', markersize=4, label='Production plastique')
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.title('Évolution Parallèle : Émissions CO2 vs Production de Plastique (1950-2019)\n' +
              f'Corrélation: r = {correlation:.4f} (p-value: {p_value:.2e})',
              fontsize=16, fontweight='bold', pad=20)

    # Légende combinée
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    return fig

def plot_heat(df):
    # Copier pour éviter de modifier df original
    df_anom = df.copy()

    # Choisir une source de référence (ex : NOAA)
    baseline = df_anom[df_anom["Year"] == 1980]["ocean_heat_content_noaa_2000m"].iloc[0]

    # Calcul de l'anomalie
    df_anom["OHC_Anomaly"] = df_anom["ocean_heat_content_noaa_2000m"] - baseline


    # Figure
    fig = px.line(
        df_anom,
        x="Year",
        y="OHC_Anomaly",
        title=f"Anomalie du contenu thermique de l'océan (base : 1980)",
        labels={
            "Year": "Année",
            "OHC_Anomaly": "Anomalie OHC (10^22 Joules)"
        }
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )

    return fig

def plot_sealevel(df):
    df_melted = df.melt(
        id_vars="Day",
        value_vars=[
            "sea_level_church_and_white_2011",
            "sea_level_uhslc",
            "sea_level_average"
        ],
        var_name="Source",
        value_name="Sea_Level"
    )

    # Renommer les sources pour la légende
    name_map = {
        "sea_level_church_and_white_2011": "Church & White (2011)",
        "sea_level_uhslc": "UH Sea Level Center",
        "sea_level_average": "Moyenne"
    }
    df_melted["Source"] = df_melted["Source"].map(name_map)

    # Calcul de la corrélation avec le temps pour la moyenne
    df_avg = df.dropna(subset=["sea_level_average"])

    # Palette de couleurs personnalisée (optionnelle)
    color_map = {
        "Church & White (2011)": "#1f77b4",  # bleu
        "UH Sea Level Center": "#ff7f0e",  # orange
        "Moyenne": "#2ca02c"  # vert
    }

    # Tracer le graphique
    fig = px.line(
        df_melted,
        x="Day",
        y="Sea_Level",
        color="Source",
        color_discrete_map=color_map,
        title=f"Évolution du niveau moyen de la mer (1980–2023)",
        labels={
            "Sea_Level": "Niveau de la mer (mm)",
            "Day": "Année"
        }
    )

    # Mise en forme
    fig.update_layout(
        legend_title_text="Source des données",
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        template="plotly_white"
    )

    return fig

def plot_glaciermelting(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Mean cumulative mass balance"],
        name="Bilan massique",
        mode="lines+markers"
    ))

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Number of observations"],
        name="Nb d'observations",
        mode="lines",
        yaxis="y2"
    ))

    fig.update_layout(
        title=f"Évolution du bilan massique et du nombre d'observations",
        xaxis=dict(title="Année"),
        yaxis=dict(title="Bilan massique"),
        yaxis2=dict(title="Nb observations", overlaying="y", side="right"),
        template="plotly_white"
    )

    return fig

def plot_redlist(df):
    latest_year = df['Year'].max()
    latest_data = df[df['Year'] == latest_year].copy()

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.hist(latest_data['_15_5_1__er_rsk_lst'], bins=20, alpha=0.7, color='forestgreen', edgecolor='black')
    ax.set_title(f'Distribution de l\'Index de la Liste Rouge en {latest_year}',
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Index de la Liste Rouge', fontsize=12)
    ax.set_ylabel('Nombre de pays/entités', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.axvline(latest_data['_15_5_1__er_rsk_lst'].mean(), color='red', linestyle='--',
               label=f'Moyenne: {latest_data["_15_5_1__er_rsk_lst"].mean():.2f}')
    ax.legend()
    plt.tight_layout()
    return fig

def plot_globalwarn(df):
    # Filtrer pour l'entité "World"
    df_world = df[df["Entity"] == "World"]

    # Créer le graphique
    fig = px.line(
        df_world,
        x="Year",
        y="near_surface_temperature_anomaly",
        title="Évolution de la température terrestre - Monde"
    )

    for trace in fig.data:
        trace.name = "Anomalie de température"
        trace.line.color = "#d62728"

        # Mettre à jour layout
    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Anomalie de température (°C)",
        legend_title_text="Mesure",
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )

    return fig

def plot_heat_variation(df):
    df["OHC_avg"] = df[
        ["ocean_heat_content_noaa_2000m",
         "ocean_heat_content_mri_2000m",
         "ocean_heat_content_iap_2000m"]
    ].mean(axis=1)

    df["OHC_change"] = df["OHC_avg"].diff()

    fig = px.line(
        df,
        x="Year",
        y="OHC_change",
        title="Taux de variation annuel du contenu thermique de l’océan",
        labels={"OHC_change": "Variation annuelle (10^22 Joules)", "Year": "Année"}
    )

    return fig