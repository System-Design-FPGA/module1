import os
flag_inplace = True

headers_to_boldify = ['#', "##"]

all_files_in  = 'codes/codes_pages/'
filenames = os.listdir(all_files_in)
file_paths = [f'{all_files_in}/{ff}' for ff in filenames]

for ff in file_paths:

    with open(ff, 'r') as fid:
        lines = fid.readlines()

    for ii, ll in enumerate(lines):
        for hh in headers_to_boldify:
            if ll.startswith(hh+' '):
                title = ll.split(hh+' ', 1)[-1].replace('\n', ' ')
                title = title.lstrip(' *').rstrip(' *')
                newll = f'{hh} **{title}**\n'
                lines[ii] = newll

    if flag_inplace:
        new_ff = ff
    else:
        new_ff = ff.split('.md')[0]+'_test.md'

    with open(new_ff, 'w') as fid:
        fid.writelines(lines)