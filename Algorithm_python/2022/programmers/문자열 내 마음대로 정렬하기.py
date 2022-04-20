# 문자열로 구성된 리스트 strings와, 정수 n이 주어졌을 때,
# 각 문자열의 인덱스 n번째 글자를 기준으로 오름차순 정렬하려 합니다.
# 예를 들어 strings가 ["sun", "bed", "car"]이고 n이 1이면 각 단어의 인덱스 1의 문자 "u", "e", "a"로 strings를 정렬

# ** 제한 조건 **
# - strings는 길이 1 이상, 50이하인 배열입니다.
# - strings의 원소는 소문자 알파벳으로 이루어져 있습니다.
# - strings의 원소는 길이 1 이상, 100이하인 문자열입니다.
# - 모든 strings의 원소의 길이는 n보다 큽니다.
# - 인덱스 1의 문자가 같은 문자열이 여럿 일 경우, 사전순으로 앞선 문자열이 앞쪽에 위치합니다.


# 다중 조건 정렬 사용
def solution(strings, n):
    word_list, answer = [], []
    for s in strings:
        word_list.append((s, len(s)))
    answer_list = sorted(word_list, key = lambda x : (x[0][n], x[0])  )
    for a in answer_list:
        answer.append(a[0])
    return answer


# TEST CASE Ⅰ
strings = ["sun", "bed", "car"]
n = 1
print(solution(strings, n))   # ["car", "bed", "sun"]

# TEST CASE Ⅱ
strings = ["abce", "abcd", "cdx"]
n = 2
print(solution(strings, n))   # ["abcd", "abce", "cdx"]



## 다른 풀이
# operator.itemgetter 모듈 사용
#  - sorted와 같은 함수의 key 매개변수에 적용되어 다중 수준의 정렬을 가능하게 해주는 모듈

from operator import itemgetter

def solution(strings, n):
    answer = sorted(sorted(strings, key = itemgetter(n)))
    return answer


## 개념 정리

# 리스트.sort()    vs    sorted(리스트)   의 차이

# 1. 리스트.sort()
#   - 본체의 리스트를 정렬해서 변환
# 2. sorted(리스트)
#   - 본체 리스트는 내버려두고, 정렬한 새로운 리스트 반환
