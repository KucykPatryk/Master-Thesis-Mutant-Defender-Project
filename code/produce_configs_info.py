import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import os
import dill
import numpy as np

PROGRAM = 'triangle'

if __name__ == "__main__":
    """
    Based on a program crate an array of dictionaries for presenting a table with calculated values on the result data
    for different configurations. Then make another table presenting the configurations' values.
    Write it in the latex format to a file.
    """

    dict_array = []  # Array of table dicts
    configs_array = []  # Array of configs
    folder_names = dict()
    graphs_array_m = []  # Array of exploration data as arrays for mutants
    graphs_array_t = []  # Array of exploration data as arrays for tests
    mutants_tests = []  # Total amount of mutants [0] and tests [1]

    folders = 0
    program_dir = 'results/' + PROGRAM + '/'
    configs_dir = 'results/' + PROGRAM + '-configs/'
    os.makedirs(configs_dir)

    # Loop over the program folder
    i = 1
    for _, dir_names, file_names in os.walk(program_dir):
        #files += len(filenames)
        #folders += len(dir_names)
        if not file_names:
            # Configurations details table
            for c in dir_names:
                folder_names['c' + str(i)] = c
                config_data = c.split('_')
                configs = dict()  # Dictionary showing configs
                configs['Config'] = 'c' + str(i)  # Configuration
                configs['Rounds'] = config_data[1].split(':')[-1]  # Iterations
                configs['MSS'] = config_data[2].split(':')[-1]  # Mutants subset size
                configs['TSS'] = config_data[3].split(':')[-1]  # Tests subset size
                configs['MPLM'] = float(config_data[4].split(':')[-1]) * 100  # Model pick limit multiplier
                configs['WT'] = float(config_data[5].split(':')[-1]) * 100  # Winning threshold
                configs['AM'] = config_data[6].split(':')[-1]  # Attacker Mode
                configs['DM'] = config_data[7].split(':')[-1]  # Defender Mode
                configs['BA'] = config_data[8].split(':')[-1]  # Bandit Algorithm
                configs_array.append(configs)
                i += 1
            i = 1
            continue

        # Load Graphs
        file = open(program_dir + folder_names['c' + str(i)] + '/exploration_mutants_l', 'rb')
        exploration_mutants_l = dill.load(file)
        file.close()
        file = open(program_dir + folder_names['c' + str(i)] + '/exploration_tests_l', 'rb')
        exploration_tests_l = dill.load(file)
        file.close()
        graphs_array_m.append(exploration_mutants_l)
        graphs_array_t.append(exploration_tests_l)
        file = open(program_dir + folder_names['c' + str(i)] + '/total_mutants_tests', 'rb')
        mutants_tests = dill.load(file)
        file.close()

        # Save tables
        table = dict()  # Dictionary for a table
        game_info_df = pd.read_csv(program_dir + folder_names['c' + str(i)] + '/game_info_log.csv')
        tests_info_df = pd.read_csv(program_dir + folder_names['c' + str(i)] + '/tests_info.csv')
        mutants_info_df = pd.read_csv(program_dir + folder_names['c' + str(i)] + '/mutants_info.csv')
        table['C'] = 'c' + str(i)  # Configuration
        i += 1
        table['K Ratio'] = game_info_df['Kill Ratio'].mean() * 100  # avg. kill ratio
        table['Wins'] = (game_info_df['Winner'] == 'Attacker').mean() * 100  # % wins for attacker
        table['R Time'] = game_info_df['Round Time'].mean() # avg. time per round
        tests_info_df['picked_ratio'] = \
            tests_info_df['Times selected by Agent'] / tests_info_df['Times in a Subset']
        table['PT Mean'] = tests_info_df['picked_ratio'].mean() * 100  # mean of tests picked from subset
        table['PT Median'] = tests_info_df['picked_ratio'].median() * 100  # median of tests picked from subset
        mutants_info_df['picked_ratio'] = \
            mutants_info_df['Times selected by Agent'] / mutants_info_df['Times in a Subset']
        table['PM Mean'] = mutants_info_df['picked_ratio'].mean() * 100  # mean of mutants picked from subset
        table['PM Median'] = mutants_info_df['picked_ratio'].median() * 100  # median of mutants picked from subset

        print(table)
        dict_array.append(table)
    print(configs_array)
    #print("{:,} folders".format(folders))

    df = pd.DataFrame.from_records(dict_array)
    df = df.round(2)
    latex_output = df.to_latex(index=False)
    with open(configs_dir + 'configs_' + PROGRAM + '.tex', 'w') as f:
        f.write(latex_output)

    df = pd.DataFrame.from_records(configs_array, columns=['Config', 'Rounds', 'MSS', 'TSS', 'MPLM', 'WT', 'AM', 'DM',
                                'BA'])
    latex_output = df.to_latex(index=False)
    with open(configs_dir + 'configs_x_' + PROGRAM + '.tex', 'w') as f:
        f.write(latex_output)

    # Plot joined graphs
    # For mutants
    fig1, ax = plt.subplots()
    i = 1
    for p_m in graphs_array_m:
        x = np.arange(0, len(p_m), 1)
        x_new = np.linspace(x.min(), x.max())
        y_smooth = spline(x, p_m, x_new)
        ax.plot(x_new, y_smooth, label="c" + str(i))
        i += 1
    # Place a legend above this subplot, expanding itself to fully use the given bounding box.
    plt.legend(bbox_to_anchor=(0., 1.07, 1., .102), loc='lower left',
               ncol=3, mode="expand", borderaxespad=0.)
    ax.set_ylim(0, mutants_tests[0])
    ax.grid()
    ax.set(xlabel='Round', ylabel='Mutants Explored',
           title='Visualisation of mutants explored before selection per round')

    # For tests
    fig2, ax = plt.subplots()
    i = 1
    for p_t in graphs_array_t:
        x = np.arange(0, len(p_t), 1)
        x_new = np.linspace(x.min(), x.max())
        y_smooth = spline(x, p_t, x_new)
        ax.plot(x_new, y_smooth, label="c" + str(i))
        i += 1
    # Place a legend above this subplot, expanding itself to fully use the given bounding box.
    plt.legend(bbox_to_anchor=(0., 1.07, 1., .102), loc='lower left',
               ncol=3, mode="expand", borderaxespad=0.)
    ax.set_ylim(0, mutants_tests[1])
    ax.grid()
    ax.set(xlabel='Round', ylabel='Tests Explored',
           title='Visualisation of tests explored before selection per round')

    fig1.savefig(configs_dir + PROGRAM + '_mutants_explored.png')
    fig2.savefig(configs_dir + PROGRAM + '_tests_explored.png')
    plt.show()
