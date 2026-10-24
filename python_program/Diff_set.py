morning = {1,23,4,15,56,26,15,686,21,13,124,14}
evening = {23,56,15,13,54376,2567,437,21,4,26}

only_one = morning ^ evening

for o in only_one:
    if o in morning:
        print(f"{o} is in morning batch")
    else:
        print(f"{o} is in evening batch")