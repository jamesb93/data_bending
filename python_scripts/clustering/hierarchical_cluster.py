import os
from datamosh.utils import read_json, write_json


this_script = os.path.dirname(os.path.realpath(__file__))
level_one_path = os.path.join(this_script, 'outputs', 'AP_UMAP-7-1-ahc_250', 'ahc_250.json')
level_two_path = os.path.join(this_script, 'outputs', 'AP_UMAP-7-1-ahc_500', 'ahc_500.json')
level_three_path = os.path.join(this_script, 'outputs', 'AP_UMAP-7-1-ahc_1600', 'ahc_1600.json')

level_one = read_json(level_one_path)
level_two = read_json(level_two_path)
level_three = read_json(level_three_path)


def find_hierarchy(level_one, level_two, file_out):
    '''
    args:
        level_one:
            the top level dictionary containing clusters
        level_two:
            the next level dictionary containing clusters
        file_out:
            the path of the output file (json)
    '''
    results = {}

    for parent_cluster in level_one:
        parent_entries = level_one[parent_cluster]
        results[parent_cluster] = {}
        t_sim = {}
        for children_cluster in level_two:
            children_entries = level_two[children_cluster]
            share = len(set(children_entries) & set(parent_entries))
            if share != 0:
                t_sim[children_cluster] = share
        results[parent_cluster] = t_sim
        

    write_json(file_out, results)

if __name__ == '__main__':
    find_hierarchy(
        level_one, 
        level_two, 
        os.path.join(this_script, 'one.json'))

    find_hierarchy(
        level_two, 
        level_three, 
        os.path.join(this_script, 'two.json'))