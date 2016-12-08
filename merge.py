import os
import subprocess


def create_lfn_list(j):
    '''
    Takes a job as input and returns two lists. The first list contains the
    lfns of all DiracFiles the job created and the second the grid site they
    are on.
    '''
    lfns = []
    locations = []
    for sj in j.subjobs:
        for df in sj.outputfiles.get(DiracFile):
            lfns.append(df.lfn)
            locations.append(df.locations[0])
    return lfns


def create_txt_for_hadd(j, name):
    '''
    Takes a job and a name as input.
    Creates a txt file called name and adds all DiracFiles the job craeted
    to the file, such that it can be passed to hadd
    '''
    if not name.endswith('.txt'):
        if '.' in name:
            print('Name needs to end in .txt')
            return
        name = name + '.txt'

    lfns, locations = create_lfn_list(j)
    gangascriptdir = os.path.abspath(__file__)
    lfn_urls = subprocess.check_output(
        [
            "lb-run",
            "LHCbDirac",
            "prod",
            "python",
            gangascriptdir + "/get_access_urls.py"
        ] + lfns
    ).split('\n')

    for line in lfn_urls[:]:
        if 'SRM_FILE_UNAVAILABLE' in line:
            print(line)
        if not line.startswith('root://'):
            lfn_urls.remove(line)

    with open(name, 'w') as f:
        for lfn in lfn_urls:
            f.write(lfn + '\n')
    print('Done. Now run')
    print('hadd -ff <taget> @{}'.format(name))
    print('Make sure to have a valid grid token at all time')
