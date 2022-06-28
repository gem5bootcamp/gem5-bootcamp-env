# https://seaborn.pydata.org/examples/index.html
import seaborn as sns

if __name__ == "__main__":
    x = [k/2 for k in range(8)]
    y = [j - j**3/6 + j**5/120 for j in x]

    plot_1 = sns.barplot(x=x, y=y)
    fig = plot_1.get_figure()
    fig.savefig("example_plot.png")