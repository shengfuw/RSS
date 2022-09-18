import argparse
import csv
import itertools
import multiprocessing
import numpy as np
import os
import pandas as pd

from main import *
from args import ArgsConfig
from plot import PlotLinesHandler
from plot_scatter import plot_scatter_pop, plot_scatter_turn

if __name__ == "__main__":
    args_config = ArgsConfig()
    args = args_config.get_args()

    # figure 2 single trial
    m = Market(args)
    f = m.firms[0]
    c = m.cons[0]
    print(f, c)
    m.simulate_step()
    print(f, c)