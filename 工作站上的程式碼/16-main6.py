import csv
from model import *

if __name__ == '__main__':
    random.seed(123)
    np.random.seed(123)

    Mylattice = lattice(500, 'Schelling', 0.4)
    log = []
    round_num = 10**6
    for round in range(round_num):
        Mylattice.one_round()
        log.append(Mylattice.get_dissimilarity())
        if round % 10**5 == 0:
            print(round, end=" ")

    # Save data
    data_file_path = 'data6.csv'
    with open(data_file_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(log)

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(9, 6))

    ax.set_xlim([0, 10**6])
    ax.set_ylim([0, 0.4])
    plt.plot(log, label="Threshold = 0.4")

    ax.set_xlabel("ticks (in 10000)", fontsize=12)
    ax.set_ylabel("Dissimilarity", rotation=90, y=0.5, fontsize=12)
    ax.set_yticks(np.arange(0, 0.41, step=0.04))
    ax.set_xticks(np.arange(0, 10**6+1, step=10**5))
    ax.xaxis.set_major_formatter(lambda x, pos: f'{x/10000:.2f}'.rstrip('0').rstrip('.'))
    ax.yaxis.set_major_formatter(lambda y, pos: f'{y:.2f}'.strip('0') if y != 0 else '0')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    fig.set_facecolor('white')
    plt.legend()
    plt.savefig('FIG7-2.jpg')

    print("\n Finished!")