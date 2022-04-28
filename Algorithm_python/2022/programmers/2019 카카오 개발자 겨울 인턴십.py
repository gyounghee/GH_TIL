# 2019 카카오 개발자 겨울 인터십

def solution(s):
    s = ( s.replace('},{','split').replace('{','').replace('}','') ).split('split')
    
    sorted_s = sorted(s, key=len) 
    for n in range(len(sorted_s)):
        sorted_s[n] = sorted_s[n].split(',')
                                              
    num_list = sum(sorted_s,[])               
    num_list = list(dict.fromkeys(num_list))  
    
    answer = list(map(int, num_list))
    return answer


# TEST CASE Ⅰ
s = "{{2},{2,1},{2,1,3},{2,1,3,4}}"
print(solution(s))   # [2, 1, 3, 4]

# TEST CASE Ⅱ
s = "{{1,2,3},{2,1},{1,2,4,3},{2}}"
print(solution(s))   # [2, 1, 3, 4]

# TEST CASE Ⅲ
s = "{{20,111},{111}}"
print(solution(s))   # [111, 20]

# TEST CASE Ⅳ
s = "{{123}}"
print(solution(s))   # [123]

# TEST CASE Ⅴ 
s = "{{4,2,3},{3},{2,3,4,1},{2,3}}"
print(solution(s))   # [3, 2, 4, 1]


## 다른 풀이
def solution(s):
    s = eval(s.replace("{", "[").replace("}", "]"))
    answer = list({num:0 for k in sorted(s, key=lambda x: len(x)) for num in k}.keys())
    return answer

