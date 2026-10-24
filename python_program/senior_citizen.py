def is_senior_citizen(age):
    if age > 60:
      return  True
    else:
        return False

age_list=[43,12,19,66,89,24,69,36]

senior_list = list(filter(is_senior_citizen, age_list))
print(senior_list)