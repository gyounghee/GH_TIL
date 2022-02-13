###  ------------------------------ 2.2.2 첫 스파크 코드 예제 --------------------------------
```
# spark API를 통해 LICENSE파일을 읽어들이고
licLines = sc.textFile("/usr/local/spark/LICENSE")
# licLines의 요소의 개수(즉, 줄 수) count
lineCnt = licLines.count()  

# licLines에서 BSD라는 문자열이 등장한 line만 필터링하여  bsdLines에 저장
bsdLines = licLines.filter(lambda line: "BSD" in line)
# bsdLines의 요소의 개수(즉, 줄 수) count
bsdLines.count()

# 
from __future__ import print_function

# foreach문은 python의 for문과 유사
# bsdLines의 요소들을 한줄씩 출력
bsdLines.foreach(lambda bLine: print(bLine))

# BSD문자열이 포함된 line만 리턴하는 함수 생성
def isBSD(line):
    return "BSD" in line

# 위에서 만든 isBSD 함수를 통해 필터링
bsdLines1 = licLines.filter(isBSD)
bsdLines1.count()   # 줄 수 count
bsdLines.foreach(lambda bLine: print(bLine))  # bsdLines의 요소 한 줄 씩 줄력
```
.
###  ------------------------------ 2.2.3 RDD의 개념 --------------------------------
* `licLines`와 `bsdLines`는 **`RDD`**라는 스파크 전용 분산 컬렉션

## **RDD**     
: 스파크의 기본 추상화 객체
  - RDD는 데이터를 조작할 수 있는 **`다양한 변환연산자를 제공`**하며,
  - **`변환 연산자`**는 항상 새로운 **`RDD 객체 
  생성`**      
  - - 스파크에 내장된 장애 복구 메커니즘은 RDD에 복원성 부여 ( 스파크는 노드에 장애가 발생해도 유실된 RDD를 원래대로 복구가능 )

> < **RDD의 목적** >   
  - 분산 컬렉션의 성질과 장애 내성을 추상화하고 직관적인 방식으로 대규모 데이터셋에 병렬 연산을 수행할 수 있도록 지원하는 것

>  < **RDD의 특성** >
>  1. 불변성 : 읽기 전용
>  2. 복원성 : 장애 내성
    - RDD는 데이터셋 자체를 중복 저장하지 않음. 대신 데이터셋을 만드는 데 사용된 변환 연산자의 로그 (데이터셋을 어떻게 만들었는지)를 남기는 방식으로 장애 내성을 제공   
      +)  RDD 계보 : RDD에 적용된 변환 연산자와 그 적용 순서
>  3. 분산 : 노드 한 개 이상에 저장된 데이터셋


* RDD의 기본 `행동 연산자` 및 `변환 연산자`


## **RDD의 기본 행동 연산자 및 변환 연산자**
* 변환 연산자  
: RDD의 데이터를 조작해 `새로운 RDD 생성`  
ex) filter, map함수 등

* 행동 연산자  
: 연산자를 호출한 프로그램으로 `계산 결과를 반환`하거나 RDD요소에 `특정 작업을 수행`하려고 실제 계산을 시작하는 역할  
ex) count, foreach 등    
.

###  ------------------------------ 2.3.1 map 변환 연산자 --------------------------------
.
: RDD의 모든 요소에 임의의 함수를 적용할 수 있는 변환연산자
- filter와는 달리 반환하는 호출된 RDD의 타입과 map함수가 반환하는 RDD의 타입이 같을 수도, 다를 수도 있다.   

```
# numbers는 sc(SparkContext)의 paralleize메서드를 통해 Seq객체를 받아 이 Seq 객체의 요소로 구성된 새로운 RDD를 만듦
# 여기서 Seq객체의 요소는 여러 스파크 실행자(executor)로 분산된다.
# range메서드의 인수로 전달된 10 to 50 by 10은 python의 특유의 표현식 , Seq 인터페이스를 구현한  Range 클래스 객체 생성
numbers = sc.parallelize(range(10, 51, 10))

# numbers 요소 한 줄 씩 출력
numbers.foreach(lambda x: print(x))

# numbers의 요소를 제곱하는 map함수를 적용하여 numbersSquared 변수에 저장
numbersSquared = numbers.map(lambda num: num * num)

numbersSquared.foreach(lambda x: print(x))   #  한 줄 씩 출력

# numbersSquared의 요소를 문자열로 변환 후 문자열을 뒤집는 map함수 적용하여 reversed에 저장
reversed = numbersSquared.map(lambda x: str(x)[::-1])
reversed.foreach(lambda x: print(x))   # 한 줄 씩 출력

```  
.
###  ------------------------------ 2.3.2 distinct와 flatMap 변환 연산자 --------------------------------

```
# --------------------------- terminal 하나 더 open ---------------------------
# 임의로 고객 ID를 입력하여 샘플 파일 준비
echo "15,16,20,20
77,80,94
94,98,16,31
31,15,20" > ~/client-ids.log
# 물결표(~)는 리눅스의 사용자 홈 directory를 참조함  → 즉, 입력 내용을 사용자의 홈 directory(/home/spark)에 client-ids.loc 파일로 생성하겠다는 의미

# --------------------------- 원래 terminal ---------------------------

# 임의로 작성한 파일을 불러와서 RDD 생성
lines = sc.textFile("/home/spark/client-ids.log")

# lines에서 각 라인의 요소를 ,기준으로 나눈 후 idStr에 저장
idsStr = lines.map(lambda line: line.split(","))
idsStr.foreach(lambda x: print(x))   # 한 줄 씩 출력

idsStr.first()   # idsStr의 첫  요소 (여기는 line별로 구분되어 있기 때문에 첫 라인이 첫 요소가 된다.)

# collect 행동연산자 
# 새로운 배열을 생성하고, RDD의 모든 요소를 배열에 모아 스파크셸로 반환
idsStr.collect()  
```  
.
> * flatMap  
 : 변환 연산자가 반환한 여러 배열의 모든 요소를 단일 배열로 통합하려는 상황에는 flatMap이 적합
 - 주어진 함수를 RDD의 모든 요소에 적용(map과 동일)
 - 익명 함수가 반환한 배열의 중첩 구조를 한 단계 제거하고 모든 배열이 요소를 단일 컬렉션으로 병합

```
# faltMap을 통해 lines RDD를 ','기준으로 분할하여 ids에 저장
ids = lines.flatMap(lambda x: x.split(","))

ids.collect()  # ids의 요소를 하나의 새로운 배열에 모아서 스파크셸로 반환  

ids.first()  # ids는 2차원의 lines RDD를 1차원 배열로 반환한 것이기 떄문에 첫 요소는 '15'가 되는 것

# collect 행동연산자를 사용하여 ids를 하나의 배열로 모은 후 배열 내의 요소들을 ';'를 구분자로 하여 합침
"; ".join(ids.collect())  

# ids요소들을 int형태로 반환
intIds = ids.map(lambda x: int(x))
intIds.collect()

# distinct 메서드  →  중복 요소를 제거
uniqueIds = intIds.distinct()
uniqueIds.collect()

# finalCount에 중복 요소 제거한 ids의 개수를 저장
finalCount  = uniqueIds.count()
finalCount

# transactionCount에 중복요소를 제거하지 않은 ids의 개수 저장
transactionCount = ids.count()
transactionCount
```
.
###  ------------------------------ 2.3.3 sample, take, takeSample 연산으로  일부 요소 가져오기 --------------------------------
> 1. **sample** 
 - 호출된 RDD에서 무작위로 요소를 뽑아 새로운 RDD를 만드는 변환연산자
 - 
2. **takeSample**
  - (collect와 유사하게) 배열을 반환하는 행동연산자
  - 두 번째 인자가 **`샘플링 결과로 반환될 요소의 개수를 지정`**하는 정수형 변수    
    *( 즉, 요소 개수의 기댓값이 아닌 항상 정확한 개수(num 인자)로 샘플링 )* 
  - 하지만, 결과 값이 RDD가 아닌 리스트나 배열이기 때문에 메모리에 주의해야 함 
  - 크기를 정해놓고 샘플을 추출하고자 한다면 takeSample() 메서드가 적합하고 메모리를 생각해서 작은 값을 추출할 때 사용하는 것이 좋음
3. **take**
  - 데이터의 하위 집합을 가져올 수 있는 행동 연산자 중 하나
  - 지정된 개수의 요소를 모을 때까지 RDD의 파티션을 하나씩 처리해 결과를 반환한다.  
    *( take 메서드의 결과는 단일 머신에 전송되므로 인자에 너무 큰 수를 지정해서는 안됨 )*

+) 파티션    
: 클러스터의 여러 노드에 저장된 데이터의 일부분

```
# ---------------- sample ----------------
# uniqueIds의 데이터를 비복원 추출을 하는데, seed는 (0.3)지정 
# seed는 컴퓨터가 난수를 일정하게 생성하지 않도록 변화를 주는 값.
s = uniqueIds.sample(False, 0.3)
s.count()
s.collect()

# uniqueIds의 데이터 중  50%(0.5) 샘플링. 중복 가능(True)
swr = uniqueIds.sample(True, 0.5)
swr.count()
swr.collect()


# -------------- takeSample --------------
# uniqueIds의 데이터 중 앞에서부터 5(5)개 샘플 추출, 비복원(False) 방식
taken = uniqueIds.takeSample(False, 5)
uniqueIds.take(5)  # 그중 3개를 가져와라
```

###  ------------------------------ 2.4 Double RDD 전용 함수 --------------------------------
* Double 객체만 사용해 RDD를 구성하면 암시적 변환이라는 것을 이용해서 몇가지 추가 함수를 사용 가능
 - 암시적 변환으로는 double RDD 함수를 사용할 수 있으며, RDD 요소의 전체 합계, 표준편차, 분산, 히스토그램을 계산할 수 있다

+) 암시적 변환이란?  
: 

```
### 2.4.1
# intIds RDD는 INT객체로 구성되지만,
# Dovle 객체로 자동 변환되므로 double RDD 함수가 암시적으로 적용됨

intIds.mean()   # 평균 
intIds.sum()    # 합계 
 
intIds.variance()  # 분산 
intIds.stdev()     # 표준편차

### 2.4.2    → 일단 그냥 넘어감 (나중에 필요하면 공부)
intIds.histogram([1.0, 50.0, 100.0])
intIds.histogram(3)

```

