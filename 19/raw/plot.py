import itertools
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
import numpy as np
import os
import seaborn as sns

sns.set()
sns.set_style("darkgrid", {"grid.linestyle": ":"})

class PlotLinesHandler:
    _ids = itertools.count(0)

    def __init__(self, xlabel, ylabel, ylabel_show,
        x_lim=None, y_lim=None, figure_size=(18, 5),
        output_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgfiles")) -> None:
        
        self.id = next(self._ids)

        self.output_dir = output_dir
        self.title = "{}-{}".format(ylabel, xlabel)
        self.legend_list = list()

        plt.figure(self.id, figsize=figure_size, dpi=160)
        # plt.title("{} - {}".format(ylabel_show, xlabel))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel_show)

        ax = plt.gca()
        if x_lim is not None:
            ax.set_xlim([0, x_lim])
            plt.xticks(np.arange(0, x_lim-15+1, step=20))
            # ax.xaxis.set_major_locator(LinearLocator(int(x_lim/20)+1))
            # ax.xaxis.set_major_formatter('{x:0.0f}')
        if y_lim is not None:
            ax.set_ylim([0, y_lim])
            plt.yticks(np.arange(0, y_lim-5+1, step=10))
            # ax.yaxis.set_major_locator(LinearLocator(int(y_lim/10)+1))
            # ax.yaxis.set_major_formatter('{x:0.0f}')

    def plot_line(self, data, linewidth=1, color="", alpha=1.0):
        plt.figure(self.id)
        if color:
            plt.plot(np.arange(data.shape[-1]), data*100,
                linewidth=linewidth, color=color, alpha=alpha)
        else:
            plt.plot(np.arange(data.shape[-1]), data*100, linewidth=linewidth)
    
    def plot_changes(self, inno_id_list, data, line_width=1, color=""):
        plt.figure(self.id)

        last_inno = inno_id_list[0]
        for step in range(1, len(inno_id_list)):
            if inno_id_list[step] != last_inno:
                if color:
                    plt.axvline(x=step, ymin=0, ymax=1, linewidth=line_width, color=color)
                else:
                    plt.axvline(x=step, ymin=0, ymax=1, linewidth=line_width)
                ax = plt.gca()
                ax.text(step+1, data[step]*100-5, "inv "+str(inno_id_list[step]),
                        ha="center", va="center", fontsize=10)
                last_inno = inno_id_list[step]

    def save_fig(self, title_param=""):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        plt.figure(self.id)
        fn = "_".join([self.title, title_param]) + ".png"
        
        plt.legend([title_param.split("_")[-1]])
        plt.subplots_adjust(left=0.05, bottom=0.15, right=0.95, top=0.85)
        plt.savefig(os.path.join(self.output_dir, fn))
        print("fig save to {}".format(os.path.join(self.output_dir, fn)))
