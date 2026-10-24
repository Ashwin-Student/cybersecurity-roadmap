for i in range (1850, 2027):

  if i % 4 == 0:
    if i % 100 == 0 :
        if i % 400 == 0:
            print(f"{i}it is an leap year")
        else:
            print(f"{i}it is not an leap year ")
    else:
        print(f"{i}it is an leap year")
  else:
    print(f"{i}year is not an leap year")