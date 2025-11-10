import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_ph_evolution(df):
    plt.figure(figsize=(12, 6))
    plt.plot(pd.to_datetime(df['Date']), df['pH yearly average'], label='pH moyen annuel')
    plt.plot(pd.to_datetime(df['Date']), df['pH'], label='pH')
    plt.title("Évolution du pH de l'eau de mer")
    plt.xlabel("Date")
    plt.ylabel("pH")
    plt.legend()
    plt.grid(True)
    plt.show()

    return plt

def plot_plastic_accumulation(df):
    """Crée un graphique de l'accumulation des microplastiques."""
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='year', y='amount', hue='Entity')
    plt.title("Accumulation des microplastiques dans l'océan")
    plt.xlabel("Année")
    plt.ylabel("Quantité accumulée")
    return plt