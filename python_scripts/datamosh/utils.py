import os
import yaml

# JSON importing
try:
    import rapidjson as rj
except ImportError:
    import json as rj

import soundfile as sf
import simpleaudio as sa
from scipy.io import wavfile


def check_make(dir_path):
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        print(f'Directory {dirName} already exists.')

def cd_up(path, num):
    '''
    Given path, traverse num directories up from it
    '''
    t_path = path
    for _ in range(num):
        t_path = os.path.dirname(t_path)
    return t_path

def read_yaml(yaml_file):
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def list_to_coll(list_in, out_file):
    '''
    Turns a list into a coll.

    list: Provide a list to convert
    out_file: a path to a file where the coll will be saved
    '''
    f = open(out_file, 'w+')
    counter = 0
    for item in list_in:
        f.write(f'{counter}, {item};')
        counter += 1
    f.close()

def check_size(path, min_size):
    '''
    Check's the size of a fyle in bytes.
    Returns true if the file has a size.
    Used to avoid empty files.
    '''
    try:
        if os.path.getsize(path) >= min_size and os.path.getsize(path) <= 150000000:
            return True
    except OSError:
        return False

def check_ext(path, extensions):
    '''
    Given a path and a list of legal extensions it either returns false or true.
    '''
    ext = os.path.splitext(path)[1]
    try:
        dummy = extensions.index(ext)
    except ValueError:
        return True
    else:
        return False
    
def wipe_dir(dir):
    '''
    Wipe a directory given a path
    '''
    for file_name in os.listdir(dir):
        os.remove(os.path.join(dir, file_name))

def bytes_to_mb(val):
    '''
    convert bytes to mb
    '''
    return val * 0.000001

def get_path():
    '''
    returns path of script being run
    '''
    return os.path.dirname(os.path.realpath(__file__))

def samps2ms(ms, sr):
    '''
    convert samples to milliseconds given a sampling rate
    '''
    return (ms / sr) * 1000.0

def ms2samps(samples, sr):
    '''
    convert milliseconds to samples given a sample rate
    '''
    return (samples/1000) * sr

def ds_store(list_in):
    '''
    Remove .DS_Store if in a list
    '''
    if '.DS_Store' in list_in:
        list_in.remove('.DS_Store')
    return list_in

def bufspill(audio_file):
    '''
    Reads an audio file and converts its content to a numpy array.

    Args:
        : A path to an audio file.
    Returns:
        A numpy array containing the data as 32 bit floating point numbers.
    '''
    try:
        t_data, _ = sf.read(audio_file)
        return t_data.transpose()
    except:
        print(f'Could not read: {audio_file}')

def write_json(json_file, in_dict):
    '''
    Takes a dictionary and writes it to JSON file.

    Args:
        json_file: A path to where the JSON file will be written.
        in_dict: A dictionary that will be saved as JSON.
    Returns:
        None
    '''
    with open(json_file, 'w+') as fp:
        rj.dump(in_dict, fp, indent=4) 

def read_json(json_file):
    '''
    Takes a JSON file and returns a dictionary

    Args:
        json_file: A path to a JSON file that will be read.
    Returns:
        A python dictionary.
    '''
    with open(json_file, 'r') as fp:
        try:
            data = rj.load(fp)
        except ImportError
        return data

def walkman(audio_path):
    '''
    Play a sound file given a path to a valid piece of audio.
    '''
    wave_obj = sa.WaveObject.from_wave_file(os.path.join(audio_path))
    play_obj = wave_obj.play()
    play_obj.wait_done()

def printp(stringer):
    '''
    A uniform way for printing status updates in scripts
    '''
    print(f'---- {stringer} ----')

def printe(stringer):
    '''
    A uniform way for printing errors in scripts
    '''
    print(f'!!!! {stringer} !!!!')