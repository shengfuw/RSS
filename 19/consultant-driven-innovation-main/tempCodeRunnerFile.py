 args.rnd_seed
    # manager = multiprocessing.Manager()
    # log_data = manager.list()

    # args_list = list()
    # for val in range(0, 101, 10):
    #     args_list.append([args, val/100, 0, RANDOM_SEED, log_data, False])
    #     args_list.append([args, 0, val/100, RANDOM_SEED, log_data, True])

    # n_cpus = multiprocessing.cpu_count()
    # print("cpu count: {}".format(n_cpus))
    # pool = multiprocessing.Pool(n_cpus+2)
    # pool.starmap(simulate_trails, args_list)
        
    # # write to csv
    # out_fn = "alpha_beta_rndSeed_{}_trail_{}_firm.csv".format(RANDOM_SEED, args.n_trails)
    # out_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), out_fn)
    # out_file = open(out_file_path, "w", newline="")
    # out_writer = csv.writer(out_file)
    # out_writer.writerow(["alpha", "beta", "turn_mean", "turn_std", "pop_mean", "pop_std", "fix_alpha"])
    # for row in log_data:
    #     out_writer.writerow(row)
    # out_file.close()
    
    # # plot
    # file_df = pd.read_csv(out_file_path)
    # alpha_df = file_df[file_df.fix_alpha == 0]
    # alpha_df.sort_values(by=["alpha"], ascending=[True],
    #                      ignore_index=True, inplace=True)
    # beta_df = file_df[file_df.fix_alpha == 1]
    # beta_df.sort_values(by=["beta"], ascending=[True],
    #                     ignore_index=True, inplace=True)
    # plot_scatter_pop(alpha_df, beta_df, RANDOM_SEED, args.n_trails)
    # plot_scatter_tur