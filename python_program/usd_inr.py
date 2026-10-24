def convert_usd_to_inr(amount):
    value= amount * 83
    return value


d_amount = [124,55,126,236,523]

usd_inr = list(map(convert_usd_to_inr,d_amount))
print(usd_inr)