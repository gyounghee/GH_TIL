```python
# 최댓값 구하기
SELECT MAX(DATETIME) 시간
FROM ANIMAL_INS

# --------------------------------------------------------------------------
# 최솟값 구하기
SELECT MIN(DATETIME) 시간
FROM ANIMAL_INS

# --------------------------------------------------------------------------
# 동물 수 구하기
SELECT COUNT(*)
FROM ANIMAL_INS

# --------------------------------------------------------------------------
# 중복 제거하기
SELECT count( distinct name)
FROM ANIMAL_INS

```