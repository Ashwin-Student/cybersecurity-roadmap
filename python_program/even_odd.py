def square(s):
    sq = s * s
    return sq
def is_even(n):
    return n % 2 == 0

list1=[1,2,6,8,5,7,9,11,16,17]
even_list=list(filter(is_even, list1))

sq_list=list(map(square, even_list))
print(sq_list)