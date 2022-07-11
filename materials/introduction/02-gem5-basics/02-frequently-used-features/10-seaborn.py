# https://seaborn.pydata.org/examples/index.html
import seaborn as sns

if __name__ == "__main__":
    x = [k / 2 for k in range(8)]
    y = [j - j**3 / 6 + j**5 / 120 for j in x]

    plot_1 = sns.barplot(x=x, y=y)
    fig = plot_1.get_figure()
    fig.savefig("example_plot_1.png")

    x = ["A", "B", "C"]
    y = [0.1, 0.2, 0.5]
    plot_2 = sns.barplot(x=x, y=y)
    fig = plot_2.get_figure()
    fig.savefig("example_plot_2.png")
