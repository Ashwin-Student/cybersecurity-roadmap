skill_req={'PYTHON','SQL','AWS','JAVA'}
candidate_skills=set()


no = int(input("ENter the no of skills you have:"))
for i in range(1,no+1):
    skill=input("Enter the skill you have:").strip().upper()
    candidate_skills.add(skill)

if  skill_req.issubset(candidate_skills):
    print("Candidate is Heired")
else:
    print("CAndidate is not heired.")