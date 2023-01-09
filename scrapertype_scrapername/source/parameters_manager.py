import numpy as np
import pandas as pd


def create_or_get_all_params_list(parquet_dir=None):
    full_dataframe = pd.read_parquet(parquet_dir, engine='fastparquet')
    params_to_return = full_dataframe.reset_index().to_dict('records')
    params_to_return = list(params_to_return)
    return params_to_return


def parameters_organizer(parameter_list, max_workers=4, worker_number=0, is_testing=False):
    """
    Gerencia os parâmetros de busca de acordo com o worker atual.
    :param is_testing:
    :param parameter_list: Lista completa de parâmetros.
    :param max_workers: Número máximo de workers do pipeline
    :param worker_number: Número do worker atual que passará por esta função.
    """
    if not worker_number or is_testing:
        pass
    else:
        param_list = parameter_list

        for i in range(max_workers):
            if worker_number == i + 1:
                parameter_list = groups_of_lists_division(parameter_list=param_list,
                                                          max_workers_number=max_workers)[i]

    return parameter_list


def groups_of_lists_division(parameter_list, max_workers_number=4):
    try:
        max_workers_number = int(max_workers_number)
    except:
        pass
    all_lists = []
    values_to_return = np.array_split(parameter_list, max_workers_number)
    for array in values_to_return:
        all_lists.append(list(array))
    return all_lists
