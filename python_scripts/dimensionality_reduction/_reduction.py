import sys
import os
import umap
import numpy as np
import json

from shutil import copyfile
from datamosh.utils import read_json, write_json, printp, read_yaml, get_path, check_make
from datamosh.variables import project_root, analysis_data
from sklearn import decomposition
from sklearn import manifold
from sklearn.preprocessing import MinMaxScaler, StandardScaler

if len(sys.argv) != 2:
    print('You need to pass a YAML config file as an argument.')
    exit()

this_script = os.path.dirname(os.path.realpath(__file__))

# Configuration
cfg_path = os.path.join(this_script, sys.argv[1])
cfg = read_yaml(cfg_path)
json_out      = cfg['json']
input_data    = cfg['input_data']
pre_reduction = cfg['pre_reduction']
normalisation = cfg['normalisation']
algorithm     = cfg['algorithm']
identifier    = cfg['identifier']
components    = cfg['components']

folder_name = f'{algorithm}_{identifier}'
output_path = os.path.join(this_script, 'outputs', folder_name)
check_make(output_path)
copyfile(cfg_path, os.path.join(output_path, 'configuration.yaml'))

feature = read_json(os.path.join(project_root, input_data))

data = [v for v in feature.values()]
keys = [k for k in feature.keys()]

if normalisation == 'minmax':
    printp('Normalising input data')
    scaler = MinMaxScaler()
if normalisation == 'standardise':
    printp('Standardising input data')
    scaler = StandardScaler()
data = np.array(data)
data = scaler.fit_transform(data)

######### Initial Reduction ##########
if pre_reduction != 0:
    printp('Performing PRE-Reduction')
    pca = decomposition.PCA(n_components=pre_reduction)
    data = pca.fit_transform(data)
elif pre_reduction == 0:
    printp('Skipping PRE-Reduction')

######### Dimensionality Reduction ##########
printp('Performing POST-Reduction')
if algorithm == 'TSNE':
    reduction = manifold.TSNE(n_components=components)
if algorithm == 'ISOMAP':
    reduction = manifold.Isomap(n_components=components)
if algorithm == 'UMAP':
    umap_neighbours = cfg['umap_neighbours']
    umap_mindist    = cfg['umap_mindist']
    reduction = umap.UMAP(n_components=components, n_neighbors=umap_neighbours, min_dist=umap_mindist)
printp('Fitting Transform')
data = reduction.fit_transform(data)

# Normalisation
printp('Normalising for JSON output')
post_normalisation = MinMaxScaler()
data = post_normalisation.fit_transform(data)

out_dict = {}
printp('Outputting JSON')
for key, value in zip(keys, data):  
    out_dict[key] = value.tolist()
write_json(os.path.join('outputs', output_path, json_out), out_dict)