notes = (1,5,10, 20,50,100,200,500,2000)

notes_rs=int(input("enter the notes rs:"))

if notes_rs in notes:
    print(notes.index(notes_rs))
else:
    print("Notes rs is not valid")