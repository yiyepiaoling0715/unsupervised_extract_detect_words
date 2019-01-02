import multiprocessing as mp


def process_deal(func_in, *args, **kwargs):
    # cpu_count=mp.cpu_count()
    process_deal = mp.Process(target=func_in, args=args, kwargs=kwargs)
    return process_deal


def processes_deal(func_in):
    pass


def processes_start(funcs_in):
    for func_iter in funcs_in:
        func_iter.start()


def proccess_join(funcs_in):
    for func_iter in funcs_in:
        func_iter.join()


def split_list_data(list_in):
    cpu_count = mp.cpu_count()
    slice_length = int(len(list_in) / cpu_count)
    slices = [list_in[index * slice_length:min((index + 1) * slice_length, len(list_in))] for index in range(cpu_count)]
    return slices


def split_dict_data(dict_in):
    cpu_count = mp.cpu_count()
    slice_length = int(len(dict_in) / cpu_count)
    keys = list(dict_in.keys())
    slices = [keys[index * slice_length:min((index + 1) * slice_length, len(keys))] for index in range(cpu_count)]
    dict_slices_list = [{key_iter: dict_in[key_iter] for key_iter in slice_group_iter} for slice_group_iter in slices]
    return dict_slices_list
