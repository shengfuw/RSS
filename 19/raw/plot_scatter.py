import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.optimize import curve_fit

def poly2(x, a, b, c):
    return a*x**2 + b*x + c

def plot_scatter_pop(alpha_df, beta_df, rnd_seed, n_trail, fig_size=9):
    plt.figure(figsize=(fig_size, fig_size*5.43/7.7), dpi=160)
    plt.xlabel("100-Noise")
    plt.ylabel("Popularity of Leading Innovations among Firms")
    ax = plt.gca()
    ax.set_xlim([0, 100])
    plt.xticks(np.arange(0, 101, step=20))
    ax.set_ylim([35, 85])
    plt.yticks(np.arange(35, 86, step=5))
    
    # scatter with error bar
    point_x = np.arange(0, 101, 10)
    plt.errorbar(x=point_x, y=alpha_df["pop_mean"].to_numpy(), yerr=alpha_df["pop_std"].to_numpy(), 
                 fmt="ks", ecolor="0.8")
    plt.errorbar(x=point_x, y=beta_df["pop_mean"].to_numpy(), yerr=beta_df["pop_std"].to_numpy(), 
                 fmt="kD", ecolor="0.5")
    
    # curve
    line_x = np.arange(0, 101, 1)
    (a, b, c), _ = curve_fit(poly2, point_x, np.array(alpha_df["pop_mean"].to_numpy()))
    plt.plot(line_x, poly2(line_x, a, b, c), "--", color="0.8", lw=5)
    (a, b, c), _ = curve_fit(poly2, point_x, np.array(beta_df["pop_mean"].to_numpy()))
    plt.plot(line_x, poly2(line_x, a, b, c), "-", color="0.5", lw=5)
    plt.legend(["Innovation Merit World", "Consultant Quality World"])

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgfiles")
    fn = "Popularity-Effect_rndSeed_{}_trail_{}_firm.png".format(rnd_seed, n_trail)
    plt.savefig(os.path.join(output_dir, fn))
    print("fig save to {}".format(os.path.join(output_dir, fn)))


def plot_scatter_turn(alpha_df, beta_df, rnd_seed, n_trail, fig_size=9):
    plt.figure(figsize=(fig_size, fig_size*5.43/7.7), dpi=160)
    plt.xlabel("100-Noise")
    plt.ylabel("Innovation Turnover Rate, Firms")
    ax = plt.gca()
    ax.set_xlim([0, 100])
    plt.xticks(np.arange(0, 101, step=20))
    ax.set_ylim([0, 140])
    plt.yticks(np.arange(0, 141, step=20))
    
    # scatter with error bar
    point_x = np.arange(0, 101, 10)
    plt.errorbar(x=point_x, y=alpha_df["turn_mean"].to_numpy(), yerr=alpha_df["turn_std"].to_numpy(), 
                 fmt="ks", ecolor="0.8")
    plt.errorbar(x=point_x, y=beta_df["turn_mean"].to_numpy(), yerr=beta_df["turn_std"].to_numpy(), 
                 fmt="kD", ecolor="0.5")
    
    # curve
    line_x = np.arange(0, 101, 1)
    (a, b, c), _ = curve_fit(poly2, point_x, np.array(alpha_df["turn_mean"].to_numpy()))
    plt.plot(line_x, poly2(line_x, a, b, c), "--", color="0.8", lw=5)
    (a, b, c), _ = curve_fit(poly2, point_x, np.array(beta_df["turn_mean"].to_numpy()))
    plt.plot(line_x, poly2(line_x, a, b, c), "-", color="0.5", lw=5)
    plt.legend(["Innovation Merit World", "Consultant Quality World"])

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgfiles")
    fn = "Turnover-Effect_rndSeed_{}_trail_{}_firm.png".format(rnd_seed, n_trail)
    plt.savefig(os.path.join(output_dir, fn))
    print("fig save to {}".format(os.path.join(output_dir, fn)))


if __name__ == "__main__":
    # read data
    csvfile_name = "alpha_beta_rndSeed_646_trail_1_firm.csv"
    rnd_seed = csvfile_name.split("_")[-4]
    n_trail = csvfile_name.split("_")[-2]
    
    file_df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), csvfile_name))
    alpha_df = file_df[file_df.fix_alpha == 0]
    alpha_df.sort_values(by=["alpha"], ascending=[True],
                         ignore_index=True, inplace=True)
    beta_df = file_df[file_df.fix_alpha == 1]
    beta_df.sort_values(by=["beta"], ascending=[True],
                        ignore_index=True, inplace=True)
    plot_scatter_pop(alpha_df, beta_df, rnd_seed, n_trail)
    plot_scatter_turn(alpha_df, beta_df, rnd_seed, n_trail)




    