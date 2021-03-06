from datamosh.utils import ds_store, cd_up
import os

root = os.path.dirname(os.path.realpath(__file__))
project_root = cd_up(root, 3)

# Slices of DataAudioUnique
unique_audio_folder = os.path.join(project_root, 'DataAudioUnique')
unique_audio_files  = ds_store(os.listdir(unique_audio_folder))

# Full Audio Files
audio_folder = os.path.join(project_root, 'DataAudio')
audio_files  = ds_store(os.listdir(audio_folder))

# Spines
spine_folder = os.path.join(project_root, 'groupings', 'spines')
spine_files  = ds_store(os.listdir(spine_folder))

# Essentia Analysis
essentia_analysis = os.path.join(project_root, 'essentia_analysis')
essentia_json = os.path.join(project_root, 'analysis_data', 'essentia_analysis.json')

# Analysis Data
analysis_data = os.path.join(project_root, 'analysis_data')
