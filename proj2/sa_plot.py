import matplotlib.pyplot as plt

def create_sa_plot(costs_list, iterations_list):
    # x-axis iterations
    x = iterations_list
    # y-axis costs
    y = costs_list

    # plotting points as a scatter plot
    plt.scatter(x, y, label="Costs", color="red",
                marker=".", s=30)

    # x-axis label
    plt.xlabel('Iterations')
    # frequency label
    plt.ylabel('Costs')
    # plot title
    plt.title('Simulated Annealing Plot')
    # showing legend
    plt.legend()

    # function to show the plot
    plt.show()