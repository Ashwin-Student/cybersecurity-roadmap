import os

os.mkdir('Testfolder1')


if os.path.exists('Testfolder1'):

    os.rmdir('Testfolder1')
    print("Folder existed and has been removed.")
else:
    print('not exists')
