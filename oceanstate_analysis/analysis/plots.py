import seaborn as sns
import matplotlib.pyplot as plt

def plot_ph_evolution(df):
    """Crée un graphique de l'évolution du pH."""
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='date', y='ph')
    plt.title("Évolution du pH de l'eau de mer")
    plt.xlabel("Année")
    plt.ylabel("pH")
    return plt

def plot_plastic_accumulation(df):
    """Crée un graphique de l'accumulation des microplastiques."""
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='year', y='amount', hue='Entity')
    plt.title("Accumulation des microplastiques dans l'océan")
    plt.xlabel("Année")
    plt.ylabel("Quantité accumulée")
    return plt