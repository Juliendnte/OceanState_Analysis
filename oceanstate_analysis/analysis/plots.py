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

