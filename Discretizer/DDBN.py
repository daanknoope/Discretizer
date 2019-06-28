import subprocess
from gobnilp import *
from jkl_serialization import deserialize_jkl, serialize_jkl


class DDBN:

    @staticmethod
    def get_arity(col):
        return len(np.unique(col.values))

    @staticmethod
    def map_variables(variables, mapping):
        return [mapping[var] for var in variables]

    @staticmethod
    def map_variable(variable, mapping):
        return mapping[variable]

    @staticmethod
    def create_tab_from_df(df):
        num_variables = df.shape[1]
        num_rows = df.shape[0]
        arities = [DDBN.get_arity(df.iloc[:, col]) for col in range(num_variables)]
        data = df.to_csv(index=False, header=False, sep=' ')
        dat_string = f'{str(num_variables)}\n{" ".join(map(str, arities))}\n{str(num_rows)}\n{data}'
        return dat_string

    @staticmethod
    def get_raw_jkl(df, ESS=20, paren_lim=6):
        open('dat.tab', 'w').write(DDBN.create_tab_from_df(df))
        command = ["scoring", "dat.tab", str(ESS), str(paren_lim), "noprune", "bdeu", '0']
        out = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        jkl = out.stdout
        print(out.stderr)
        return jkl


    # we assume max 1 layer back
    @staticmethod
    def filter_illegal_parent_sets(jkl, objective, discretization_variables, varmap, unmap, look_back=0):
        fjkl = jkl.copy()

        score_list = []
        for score, parent_list in fjkl[objective]:
            if len(set(parent_list).intersection(
                    set(discretization_variables))) < 2:  # Can only select one discretization variable
                score_list.append((score, parent_list))
        fjkl[objective] = score_list

        # objective cannot be target of node
        for node in fjkl:
            score_list = []
            for score, parent_list in fjkl[node]:
                if look_back:
                    if objective not in parent_list and DDBN.map_variable(DDBN.map_variable(objective, unmap) + "_1",
                                                                     varmap) not in parent_list:
                        score_list.append((score, parent_list))
                else:
                    if objective not in parent_list:
                        score_list.append((score, parent_list))
            fjkl[node] = score_list

        for discretization_var in discretization_variables:  # Discretizatization vars cannot be connected to another
            score_list = []
            for score, parent_list in fjkl[discretization_var]:
                if len(set(parent_list).intersection(set(discretization_variables))) < 1:
                    score_list.append((score, parent_list))
            fjkl[discretization_var] = score_list

        if look_back:
            nodes = set(DDBN.map_variables(fjkl.keys(), unmap))
            prev_tf = set(DDBN.map_variables(filter(lambda x: '_' in x, nodes), varmap))
            current_tf = set(DDBN.map_variables(nodes - prev_tf, varmap))

            # past cannot learn from future
            for node in prev_tf:
                score_list = []
                for score, parent_list in fjkl[node]:
                    if len(set(parent_list).intersection(current_tf)) < 1:
                        score_list.append((score, parent_list))

                fjkl[node] = score_list

            # objective cannot be connected to previous objective
            score_list = []
            for score, parent_list in fjkl[objective]:
                if len(set(parent_list).intersection(DDBN.map_variable(DDBN.map_variable(objective, unmap) + "_1", varmap))) < 1:
                    score_list.append((score, parent_list))
            fjkl[objective] = score_list

        return fjkl

    @staticmethod
    def learn_discretization_DBN(df, objective, discretization_nodes, settings):
        lookback = create_lookback_dataset(df)
        for col in lookback.columns:
            lookback[col] = lookback[col].apply(int)

        variable_map = {k: v for k, v in zip(lookback.columns, map(str, range(len(lookback.columns))))}
        variable_unmap = {k: v for k, v in zip(map(str, range(len(lookback.columns))), lookback.columns)}

        jkl = deserialize_jkl(DDBN.get_raw_jkl(lookback))
        filtered_jkl = DDBN.filter_illegal_parent_sets(jkl, DDBN.map_variable(objective, variable_map), DDBN.map_variables(
            discretization_nodes + [unroll_node(x, 1) for x in discretization_nodes], variable_map), variable_map,
                                                  variable_unmap, look_back=1)

        jkl_string = serialize_jkl(filtered_jkl)
        open('data.jkl', 'w').write(jkl_string)
        open('gobnilp.set', 'w').write(settings)

        proc = subprocess.Popen(['gobnilp', 'data.jkl'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='.')
        proc.wait()
        solution = open('sol.dot', 'r')
        G = parse_gobnilp_structure(solution, lambda x: variable_unmap[x])

        return G
