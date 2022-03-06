# 도전 1
def solution(n):
    answer = 0
    ary = [i for i in range(2,n+1)]
    num = [2,3,5,7]
    tmp = []
    for i in ary:
        if i in num or i % 2 != 0 and i % 3 != 0 and i % 5 != 0 and i % 7 != 0 :
            tmp.append(i)
    for i in range(len(tmp)):
        c = 0
        for j in range(1,tmp[i]+1):
            if c >= 3 : break
            elif tmp[i] % j == 0 : c += 1
        if c == 2 :
            answer += 1
    return answer


# 도전 2
def solution(n): 
    num_list = [i for i in range(2,n+1)]
    num_rm = []
    i = 2

    while i * i < n:
        j = 2
        while i*j <= n :
            if (i*j) in num_list :
                num_rm.append(i * j)
            j += 1
        i = num_list[num_list.index(i)+1]        
    return len(num_list)-len(list(set(num_rm)))


# 도전 3
def solution(n):
    answer = 0
    num_list = list(range(2,n+1))
    
    for i in range(2,n+1):
        rn = int( i ** (1/2) )
        tmp = [] # 루트를 씌운 수 이하의 소수를 담는 변수
        if rn == 1 :
            answer += 1
        else : # 루트를 씌운 수 이하의 소수를 찾기
            for j in range(2, rn+1): 
                c = 0
                for k in range(1,j+1):
                    if j % k == 0 : c += 1
                    if c > 2 : break
                if c == 2 : 
                    tmp.append(j)
            # 확인
            chk = 0
            for check in tmp:
                if i % check == 0 : chk += 1
            if chk == 0 : answer += 1
    
    return answer

n = 5
print(solution(n))
