import matplotlib.pyplot as plt
import numpy as np

from ab_testing.constants import Blue, Red
from ab_testing.testers.tester import Tester


def plot_dist(
    ax,
    x: np.array, y: np.array,
    mean: float, margin: float,
    color: dict):
    
    plot = ax.plot(x, y, c=color['plot'], alpha=1)
    ax.axvline(x=mean, c=color['mean'], linestyle='--')
    if margin:
        ax.axvline(x=mean - margin, c=color['margin'], alpha=0.5, linestyle='--')
        ax.axvline(x=mean + margin, c=color['margin'], alpha=0.5, linestyle='--')
    return plot[0]


def plot_power(ax, x, y, color, threshold):
    ax.fill_between(x, 0, y, color=color, alpha=0.5, where=(x > threshold))


def plot(
    tester: Tester, margin: float, name: str,
    c: int = 12, q: int = 1000, figsize: tuple = (15, 6)):

    _, ax = plt.subplots(figsize=figsize)
    
    x_null = np.linspace(
        tester.mean_null - (c * tester.stdev_null),
        tester.mean_null + (c * tester.stdev_null),
        q)
    y_null = tester.distribution_null.pdf(x_null)

    x_alt = np.linspace(
        tester.mean_alt - (c * tester.stdev_alt),
        tester.mean_alt + (c * tester.stdev_alt),
        q)
    y_alt = tester.distribution_alt.pdf(x_alt)

    p0 = plot_dist(ax, x_null, y_null, tester.mean_null, margin, Blue)    
    # pA = plot_dist(ax, x_alt, y_alt, tester.mean_alt, margin, Red)
    pA = plot_dist(ax, x_alt, y_alt, tester.mean_alt, None, Red)

    threshold = tester.mean_null + margin
    plot_power(ax, x_null, y_null, Blue['area'], threshold)
    plot_power(ax, x_alt, y_alt, Red['area'], threshold)
    
    txt_x = x_null.min()
    txt_y = y_null.max()
    power = 1 - tester.distribution_alt.cdf(margin)
    ax.text(txt_x, txt_y, f"Power = {power:.4f}")
    
    ax.legend([p0, pA], ['NULL', 'Alternative'])
    ax.set_title(name)
    ax.set_xlabel('difference')
    ax.set_ylabel('PDF')
