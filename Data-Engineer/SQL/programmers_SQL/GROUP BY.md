```python
#  고양이와 개는 몇 마리 있을까

SELECT ANIMAL_TYPE, count(*) 
FROM ANIMAL_INS
GROUP BY ANIMAL_TYPE
ORDER BY ANIMAL_TYPE

# --------------------------------------------------------------------------

# 동명 동물 수 찾기
SELECT NAME, COUNT(NAME) COUNT
FROM ANIMAL_INS
GROUP BY NAME HAVING COUNT(NAME) >= 2
ORDER BY DESC

# --------------------------------------------------------------------------

# 입양 시각 구하기(1)
SELECT HOUR(DATETIME) HOUR, COUNT(*) COUNT
FROM ANIMAL_OUTS
WHERE HOUR(DATETIME) BETWEEN 9 AND 19
GROUP BY HOUR(DATETIME)
ORDER BY HOUR(DATETIME)

# --------------------------------------------------------------------------

# 입양 시각 구하기(2)
WITH RECURSIVE TIME_H AS (        # 재귀 쿼리 세팅
    select 0 as HOUR                     # 초기값 설정
    UNION ALL                             # 위 쿼리와 아래 쿼리의 값을 연산
    select HOUR+1                        
    FROM TIME_H                          
    WHERE HOUR < 23                  # HOUR가 23가지만 실행한다.
)

SELECT TIME_H.HOUR, COUNT(HOUR(OUTS.DATETIME)) COUNT
FROM TIME_H
LEFT JOIN ANIMAL_OUTS AS OUTS
ON
TIME_H.HOUR = HOUR(OUTS.DATETIME)
GROUP BY TIME_H.HOUR 
ORDER BY TIME_H.HOUR ASC

```