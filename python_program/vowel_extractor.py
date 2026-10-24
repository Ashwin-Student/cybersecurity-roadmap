sen = input("Enter an Sentence to check an vowels in it.").lower()
sen_list = list(sen)

vowel=set()

for s in sen_list:
    if s in 'aeiou':
        vowel.add(s)
print(vowel)

