import urllib.request
import re

import html2markdown as hm

page_list = [
    # 'ABCI', 
    # 'ACE3P',
    # 'BimBim', 
    # 'COMBI', 
    # 'CSTParticleStudio', 'DELPHI', 'Fastion', 'FootprintViewer',
    # 'GdFiDl', 'Guinea-Pig', 'HFSS', 'IBSimu', 'ImpedanceWake2D',
    # 'LHCOnlineModel', 'MadX', 'MapClass', 'MOSES', 'Ninja', 'ONIX',
    # 'PageStore', 'PATH', 'PHOTON', 'Placet', 
    # 'PyECLOUD', 
    # 'PyHEADTAIL',
    # 'PyOptics', 'PyORBIT', 'PyPARIS', 'PyPIC', 'PySSD', 'PyTimber',
    # 'RF-Track', 'SIRE', 'SixTrack', 'SixTrackAndCollimation',
    # 'SUSSIX', 'TRAIN',
    #'HpcCERN', 'CNAFcluster',
    #'LxbatchHTCondor',
    #'AFSDebian',
    'AFSMacOs',
    ]
twiki_root = "https://twiki.cern.ch/twiki/bin/view/ABPComputing/"

for twiki_page in page_list:

    print(twiki_page)
    twikihtml = twiki_root + twiki_page + '?skin=text'
    #twikihtml = twiki_root + twiki_page + '?skin=plain'


    with urllib.request.urlopen(twikihtml) as response:
        html = response.read()

    mkdown = hm.convert(html)

    # Some cleanup
    lines = mkdown.splitlines()
    new_lines = []
    for ll in lines:
        nll = ll
        # Lines that start with too many spaces are wrongly interpreted as code blocks
        if nll.startswith('    '):
            nll = nll[2:]

        # Remove multiple spaces after bullet
        nll = re.sub(r'\*( +)', '* ', nll)

        if nll.startswith(' *'):
            nll = nll[1:]
        
        nll = nll.replace(' * __', '* __')

        nll = re.sub(r'( +)\*', '    -', nll)

        nll = nll.replace(r'\*', '')

        nll = re.sub(r'<a name=(.*)></a>', '', nll)

        match = re.search(r'##(.*)__(.*)__( +)', nll)
        if match is not None:
            nll = f"## {match.group(2)}"

        nll = re.sub(r'<img(.*)TWikiDocGraphics/external-link.gif" width=(.*)/>', '', nll)
                    
        if nll.startswith('-- Main.'):
            nll = ''

        # # Handle things like "*    __Programming Languages used for implementation:__ "
        # match = re.search('(.*)__(.*)__(.*)', nll)
        # if match is not None:
        #     nll = f"### {match.group(2)}"
        
        new_lines.append(nll)

    new_mkdown = '\n'.join(new_lines)

    # with open('raw_'+twiki_page+'.md', 'w') as fid:
    #     fid.write(mkdown)
    with open(twiki_page+'.md', 'w') as fid:
        fid.write(new_mkdown)

