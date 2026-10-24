from datetime import datetime

days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

day_name = datetime.now().strftime("%A").lower()

for d in days:
    if d == day_name:
        if d == 'saturday' or d == 'sunday':
            print("its an weekend.")
        else:
            print("its an week day.")
        break
