import random

generate_no = random.randint(1,10000)
attempt=0

print("welsome to the guese game")

while True:
  attempt +=1
  no = int(input("guese an integer no in range of 1 to 10000:"))
  if generate_no != no:
    if no > generate_no:
        print("your guese no is  high, try some lower no")
    else:
        print("your guese no is low, try some higher no")
  else:
    print(f"your guese no is perfectly match, congrates! you done this in {attempt} attempts ")
    break