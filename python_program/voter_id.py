voter_id=set()

while (True):
    id=input("Enter an voter id:")
    if id == 'exit':
        break
    else:
        if id not in voter_id:
            voter_id.add(id)

if len(voter_id) >= 5:
    print(voter_id)
    print("High Turnout")
else:
    print("Low Turnout")


