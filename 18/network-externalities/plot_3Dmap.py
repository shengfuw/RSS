import imageio ## to convert to mp4, please also run "pip install imageio-ffmpeg"
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime


class Plot3DArray(object):
    def __init__(self, filename_prefix="", output_dir="giffiles"):
        super().__init__()

        # use the current time as filename if not specified
        if filename_prefix:
            self.filename_prefix = filename_prefix
        else:
            self.filename_prefix = "simulation_{}".format(datetime.datetime.now().strftime('%m_%d_%H_%M'))
        self.output_dir=output_dir

        self.max_digit = 4
        self.plotted_img_paths = []


    def plot_map(self, loc_data, adp, price, ties, period, cmap="magma", figure_size=(9, 9)):
        """
        Param
        - map -> 3d np.array
            an 3d numpy array to plot
        - period -> int
            current timestep t
        - cmap:
            the color set for meshcolor.
            you can choose the one you like at https://matplotlib.org/stable/tutorials/colors/colormaps.html
        """
        title = "Period = {}".format(period)
        output_path = os.path.join(os.getcwd(), self.output_dir, self.filename_prefix)
        filename = "{}_{}.png".format(self.filename_prefix, period)

        adopters_loc = loc_data[(adp == 1.0)]
        adopters_price = price[(adp == 1.0)]
        others_loc = loc_data[(adp == 0.0)]
        others_price = price[(adp == 0.0)]
        _min, _max = np.min(price), np.max(price)

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        ax.scatter(adopters_loc[:, 0], adopters_loc[:, 1], adopters_loc[:, 2],
            c=adopters_price, cmap='Reds', vmin = _min, vmax = _max, marker='^', label="Adopted")
        ax.scatter(others_loc[:, 0], others_loc[:, 1], others_loc[:, 2],
            c=others_price, cmap='Reds', vmin = _min, vmax = _max, marker='o', label="Have not adopted")
        for tie in ties:
            ax.plot(tie[:, 0], tie[:, 1], tie[:, 2], color="lightgray", alpha=0.3, linewidth=0.5)
        ax.legend()
        plt.title(title)
        self.plotted_img_paths.append(self._save_fig(output_path, filename, period))
        plt.close()
    

    def _save_fig(self, output_path, fn, t):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        file_path = os.path.join(output_path, fn)
        plt.savefig(file_path)
        print("|period={}| figrue saved to {}".format((str(t)+' '*self.max_digit)[:self.max_digit], file_path))
        return file_path

    
    def save_gif(self, fps=30, img_dir=""):
        filename = "{}.gif".format(self.filename_prefix)
        file_path = os.path.join(os.getcwd(), self.output_dir, filename)
        
        # img paths
        all_img_paths = self.plotted_img_paths
        if img_dir:
            filename_prefix = os.path.split(img_dir)[-1]
            all_t = sorted([float(os.path.splitext(f)[0].split('_')[-1]) for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))])
            all_img_paths = [os.path.join(img_dir, "{}_{:.3f}.png".format(filename_prefix, t)) for t in all_t]

        images = [imageio.imread(img_path) for img_path in all_img_paths]
        imageio.mimsave(file_path, images, duration=1/fps)
        print("gif saved to {}".format(file_path))

    
    def save_mp4(self, fps=30, img_dir=""):
        filename = "{}.mp4".format(self.filename_prefix)
        file_path = os.path.join(os.getcwd(), self.output_dir, filename)

        # img paths
        all_img_paths = self.plotted_img_paths
        all_img_paths = self.plotted_img_paths
        if img_dir:
            filename_prefix = os.path.split(img_dir)[-1]
            all_t = sorted([float(os.path.splitext(f)[0].split('_')[-1]) for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))])
            all_img_paths = [os.path.join(img_dir, "{}_{:.3f}.png".format(filename_prefix, t)) for t in all_t]
        
        writer = imageio.get_writer(file_path, fps=20)
        for img_path in all_img_paths:
            writer.append_data(imageio.imread(img_path))
        writer.close()
        print("mp4 saved to {}".format(file_path))



if __name__ == "__main__":
    filename_prefix = "expset(a)_eta_0.2_theta_0.56_Gamma_0.019"
    img_dir = os.path.join(os.getcwd(), 'imgfiles', filename_prefix)
    plotter = Plot3DArray(filename_prefix=filename_prefix)
    plotter.save_gif(img_dir=img_dir)
    plotter.save_mp4(img_dir=img_dir)
    

    '''
    # usage example
    t = 60
    lots_of_data = np.random.randint(256, size=(t, 128, 128))
    plotter = Plot2DArray()
    for i in range(t):
        plotter.plot_map(lots_of_data[i], i)
    plotter.save_gif()
    plotter.save_mp4()
    '''
    
