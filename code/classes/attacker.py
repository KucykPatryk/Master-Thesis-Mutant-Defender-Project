from subprocess import run

from .mutation_set import MutationSet
from .mutation_set import MutationSubset

from csv import DictReader

from classes.vwwrapper import VWWrapper


class Attacker:
    """ The Attacker agent"""
    def __init__(self, mode, pick_limit, subset_size):
        self.mutants_list = self.read_mutants()
        self.m_set = MutationSet(self.mutants_list, len(self.mutants_list))
        self.m_subset = self.new_subset(self.m_set, subset_size)
        self.won = 0  # Times won against defender
        self.lost = 0  # Times lost against defender
        self.last_winner = False  # True if won in last round
        self.pick_limit = pick_limit
        # Create the mutant Vowpal Wabbit model
        # self.vw_mutant = VWWrapper(
        #     '--quiet --cb_explore_adf --epsilon=0.1',
        #     '/home/kucyk-p/UiO/Master_Thesis/vowpal_wabbit/build/vowpalwabbit/vw')

        # This variable decides the agent mode. Currently "random" is supported
        self.agent_mode = mode
        self.features = ''

    @staticmethod
    def generate_mutants():
        """ Generate mutants with context and log files """
        run(['./' + 'run_mutant_generation.sh'], cwd='../generation/')

    @staticmethod
    def read_mutants():
        """ Read mutants from file and saves as a list """
        with open('../generation/mutants.log') as f:
            mutants_list = f.read().splitlines()

        return mutants_list

    def new_subset(self, set, size):
        m_subset = MutationSubset(set.create_random_subset(size),
                                  len(self.mutants_list), size)
        return m_subset

    def win(self):
        """ Add a win """
        self.won += 1
        self.last_winner = True

    def lose(self):
        """ Add a loss """
        self.lost += 1
        self.last_winner = False

    def update(self, won, summary, ids, kill_ratio):
        """ Update values after a round """
        if won:
            self.win()
        else:
            self.lose()

        self.m_subset.update_survived_killed(summary[3], summary[2])
        self.m_set.update_mutants(ids, kill_ratio, self.m_subset.mutants_ids)

    def update_wis(self, subset_ids):
        """ Update was in subset count """
        self.m_set.update_wis(subset_ids)

    @staticmethod
    def produce_mutants_features(ids, mc_dict):
        """ Produces mutants features string
        :param ids: mutant ids as list
        :param mc_dict: dictionary created from mutation.context file
        :return: dictionary created from mutation.context file
        """
        mf = ''
        for row in mc_dict:
            if row['mutantNo'] in ids:
                # mf += row['mutantNo'] + '| '
                mf += '| '
                mf += row['mutationOperatorGroup'] + ':1.0 '
                index = row['mutationOperator'].index(':')
                if row['mutationOperator'][0] == '<':  # Remove < signs
                    mf += row['mutationOperator'][1:index - 1] + row['mutationOperator'][index + 2:-1] + ':1 '
                else:
                    mf += row['mutationOperator'][:index] + row['mutationOperator'][index + 1:] + ':1.0 '
                mf += row['nodeTypeBasic'] + ':1.0 '
                index = row['parentContextDetailed'].index(':')
                mf += row['parentContextDetailed'][:index] + row['parentContextDetailed'][index + 1:] + ':1.0 '
                if ':' in row['parentStmtContextDetailed']:
                    index = row['parentStmtContextDetailed'].index(':')
                    mf += \
                        row['parentStmtContextDetailed'][:index] + row['parentStmtContextDetailed'][
                                                                   index + 1:] + ':1.0 '
                else:
                    mf += row['parentStmtContextDetailed'] + ':1 '
                if row['hasVariableChild'] == '1':
                    mf += 'hasVariableChild' + ':1.0'
                elif row['hasOperatorChild'] == '1':
                    mf += 'hasOperatorChild' + ':1.0'
                elif row['hasLiteralChild'] == '1':
                    mf += 'hasLiteralChild' + ':1.0'
                mf += '\n'
        mf = mf[:-1]
        return mf

    def prepare_for_testing(self):
        """ Prepare agent for the execution """
        if self.agent_mode is 'bandit':
            # Read the mutant context information and store it in a dictionary for each row
            mc = open('../generation/mutants.context')
            mc_dict = DictReader(mc)

            # Mutant features
            self.features = self.produce_mutants_features(self.m_subset.mutants_ids, mc_dict)
            # print(self.features)

            # Prediction
            # TO BE IMPLEMENTED
            # Model selects the mutants
            # m_pred = attacker.vw_mutant.predict(mutants_features)
            # print(m_pred)

            mc.close()

        elif self.agent_mode is 'random':
            # Select from the subsets based on MODEL_PICK_LIMIT parameter
            self.m_subset = self.new_subset(self.m_subset, self.pick_limit)

    def learn(self):
        """ Learn after the tests are run through Major and results are updated """
