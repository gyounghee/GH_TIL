def solution(numbers):
    answer = ""
    n = sorted(numbers, key = lambda x : str(x)[0], reverse=True)
    n =list(map(str, n))
    max_n = int(''.join(n))
    
    for _ in range(len(n)):
        n.append(n.pop(0))
        if int(''.join(n)) > max_n : max_n = int(''.join(n))
        
    return max_n


# TEST CASE Ⅰ
numbers = [6, 10, 2]
print(solution(numbers))

# TEST CASE Ⅱ   
numbers = [3, 30, 34, 5, 9]
print(solution(numbers))



