import seaborn as sns
import matplotlib.pyplot as plt

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
