import pandas as pd
import os

PROGRAM = 'range'

if __name__ == "__main__":
    """
    Based on a program crate an array of dictionaries for presenting a table with calculated values on the result data
    for different configurations. Then make another table presenting the configurations' values.
    Write it in the latex format to a file.
    """

    dict_array = []  # Array of table dicts
    configs_array = []  # Array of configs
    folder_names = dict()

    folders = 0
    program_dir = 'results/' + PROGRAM + '/'

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
    print(configs)
    #print("{:,} folders".format(folders))

    df = pd.DataFrame.from_records(dict_array)
    df = df.round(2)
    latex_output = df.to_latex(index=False)
    with open('results/configs_' + PROGRAM + '.tex', 'w') as f:
        f.write(latex_output)

    df = pd.DataFrame.from_records(configs_array, columns=['Config', 'Rounds', 'MSS', 'TSS', 'MPLM', 'WT', 'AM', 'DM',
                                'BA'])
    latex_output = df.to_latex(index=False)
    with open('results/configs_x_' + PROGRAM + '.tex', 'w') as f:
        f.write(latex_output)


