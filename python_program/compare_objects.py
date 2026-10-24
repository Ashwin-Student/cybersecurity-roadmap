class Students:
    def __init__(self, name, total_marks):
        self.name=name
        self.total_marks = total_marks


s1=Students('wbgf',712)
s2=Students('feug',641)

if s1.total_marks > s2.total_marks:
    print(s1.name)
else:
    print(s2.name)