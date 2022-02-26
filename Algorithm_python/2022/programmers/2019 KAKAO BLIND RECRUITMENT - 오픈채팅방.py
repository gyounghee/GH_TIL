def solution(record):
    answer = []
    nickname_dict = {}
    for words in record:
        word = words.split()
        if word[0] == "Enter" : 
            answer.append(f'{word[1]}님이 들어왔습니다.')
            nickname_dict[word[1]] = word[2]
        elif word[0] == "Leave" :
            answer.append(f'{word[1]}님이 나갔습니다.')
        elif word[0] == "Change" :    
            nickname_dict[word[1]] = word[2]
            
    for i in range(len(answer)) :
        for key, value in nickname_dict.items() :
            answer[i] = answer[i].replace(f"{key}",f"{value}")
            
    return answer

# TEST CASE Ⅰ
# 결과값 → ["Prodo님이 들어왔습니다.", "Ryan님이 들어왔습니다.", "Prodo님이 나갔습니다.", "Prodo님이 들어왔습니다."]
record = ["Enter uid1234 Muzi", "Enter uid4567 Prodo","Leave uid1234","Enter uid1234 Prodo","Change uid4567 Ryan"]
print(solution(record))
