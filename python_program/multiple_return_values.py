def evaluate_performance(marks):
    sum1=0
    avg=0
    c=0
    for i in marks:
        sum1+=i
        c+=1
    avg = sum1 / c
    grad=''
    if avg >= 40:
        grad = 'Pass'
    else:
        grad='Fail'

    return sum1, avg, grad

mark=[89,25,76,45,35,90]
for i in mark:
    print(f"we are returning the sum, avg, grad", evaluate_performance([i]))
