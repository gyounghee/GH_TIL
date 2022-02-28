## 4.2 데이터 파티셔닝을 이해하고 데이터 셔플링 최소화
* **데이터 파티셔닝**  
: 데이터를 여러 클러스터 노드로 분할하는 메커니즘  
  - 스파크의 성능과 리소스 점유량을 크게 좌우할 수 있는 RDD의 가장 기본적인 개념

* **스파크 클러스터**  
: 병렬 연산이 가능하고 네트워크로 연결된 머신(노드)의 집합

* **RDD의 파티션**  
: RDD 데이터의 일부를 의미  
 ex) 로컬 파일 시스템에 저장된 textFile을 spark에 load하면
  1. 스파크는 파일 내용을 여러 파티션으로 분할하여 클러스터 노드에 고르게 분산 저장하며, 여러 파티션을 하나의 노드에 저장할 수도 있다
  2. 이렇게 분산된 파티션이 모여서 하나의 RDD를 형성      
 ( *RDD의 파티션 목록은 RDD의 partitions 필드로 제공되며, 필드 타입은 Array이므로 partitions.size 필드로 파티션 개수를 알아 낼 수 있다. )*
  - RDD의 파티션 개수는 해당 RDD에 변환 연산을 실행할 테스크 개수와 직결되기 떄문에 매우 중요하다
    - 테스크 개수가 필요 이하로 적으면 클러스터를 충분히 활용할 수 없다. 또한, 각 테스크가 처리할 데이터 분량이 실행자의 메모리 리소스를 초과해 메모리 문제가 발생할 수 있기 때문에, 클러스터의 코어 개수보다 서너배 더 많은 파티션을 사용하는 것이 좋다
    - But, 테스크가 너무 많으면 병목 현상이 발생하므로 비상식적으로 큰 값은 설정 X

--------------------------------------------------------------------------------
## 4.2.1 스파크의 데이터 Partitioner
* **스파크의 데이터 Partitoner**
  - RDD의 각 요소에 파티션 번호를 할당하는 Partitioner 객체가 수행
  - 스파크는 Partitioner의 구현체
    - HashPartitioner와 RangePartitioner를 제공, 사용자 정의 Partitioner를 Pair RDD에 사용할 수 있음
    
1. **HashPartitioner**
  - 스파크의 기본 Partitioner, **파티션 개수를 받는 메서드를 호출**할 떄 사용
  - 각 요소의 해시 코드(Pair RDD는 키의 해시 코드)를 단순한 mod공식(partitionIndex = hashCode % numberOfPartitions)에 대입해 **파티션 번호를 계산**
  - 각 요소의 파티션 번호를 거의 무작위로 결정하기 떄문에 모든 파티션을 정확하게 같은 크기로 분할할 가능성은 낮지만, 대규모 데이터셋을 상대적으로 적은 수의 파티션으로 나누면 대체로 데이터를 고르게 분산시킬 수 있음
  - HashParitioner를 사용할 시 데이터 파티션의 기본 개수는 스파크의 spark.default.parrallelism 환경 매개변수 값으로 결정됨. 이를 지정하지 않으면 스파크는 클러스터의 코어 개수를 대신 사용  
_  
2. **RangePartitioner**  
  - 정렬된 RDD의 데이터를 거의 같은 범위 간격으로 분할 가능
  - RangePartitioner는 대상 RDD에서 샘플링한 데이터를 기반으로 범위 경계를 결정
  But, RangePartitioner를 직접 사용할 일은 많지 않음  
  _  
3. **Pair RDD의 사용자 정의 Partitioner**
  - **Pair RDD에만 쓸 수 있음**, Pair RDD의 변환 연산자를 호출할 때 사용자 정의 Partitioner를 인수로 전달
- 파티션(또는 파티션을 처리하는 테스크)의 데이터를 특정 기준에 따라 **정확하게 배치해야할 경우** 사용자 정의 Partitioner로 Pair RDD 분할 가능  
  ex) 각 테스크가 특정 키-값 쌍 데이터만 처리해야 할 때   
  (특정 데이터가 단일 DB, 단일 DB table, 단일 사용자 등에 속할 때)  
.  
* 대부분의 Pair RDD 변환 연산자는 두 가지 추가 버전 제공
  1.  Int 인수(변경할 파티션 개수)를 추가로 받음
  
  2. 사용할 Partitioner(스파크 지원 Partitioner 또는 사용자 정의 Partitioner)를 추가 인수로 받음  

```pyspark
# HashPartitoner에 파티션 100개 설정
# 1. Int 인수를 추가로 받는 경우
rdd.foldByKey(afunction, 100)  

# 2. 사용할 Partitioner를 추가 인수로 받는 경우
# 사용자 정의 Partitioner를 지정하려면 두 번째 버전 사용
rdd.foldByKey(afunction,new HashPartitioner(100))
```

* mapValues와 flatMapValues를 제외한 Pair RDD의 변환 연산자는 모두 위 두 가지 버전의 메서드를 추가로 제공한다.
  - mapValues와 flatMapValues는 항상 파티셔닝을 보존

* Pair RDD 변환 연산자를 호출할 때 Partitioner를 따로 지정하지 않으면 스파크는 부모 RDD(현재 RDD를 만드는데 사용한 RDD들)에 지정된 파티션 개수 중 가장 큰 수 사용
  - Partitioner를 정의한 부모 RDD가 없다면 spark.default.parallelism 매개변수에 지정된 파티션 개수로 HashPartitioner를 사용

* 기본 HashPartitioner를 그대로 사용하면서 임의의 알고리즘으로 키의 해시 코드만 바꾸어도 Pair RDD 데이터의 파티션 배치를 변경할 수 있음 
  - 이 방법은 구현하기도 더 쉽고, 부주의한 셔플링을 피할 수 있기 때문에 성능도 향상할 수 있음

--------------------------------------------------------------------------------
## 4.2.2 불필요한 셔플링 줄이기
* 셔플링  
: 파티션 간의 물리적인 데이터 이동
  - 새로운 RDD의 파티션을 만들기위해 여러 파티션의 데이터를 합칠 때 발생  

.  
* [ **세 파티션으로 구성된 RDD에 aggregateByKey 변환 연산을 수행할 때 셔플링 과정** ]    
1. aggregateByKey에 전달된 변환 함수는 파티션별로 값을 병합  
  1-2. 중간 파일에는 파티션별로 병합된 값을 저장하며, 이 파일을 셔플링 단계의 입력 데이터로 사용  
2. 병합 함수는 셔플링 단계를 거치며, 여러 파티션의 값을 최종 병합  

+) aggregateByKey에는 변환 함수(값의 타입을 변경)와 병합 함수(두 값을 하나로 합침)를 전달함
  - 변환 함수는 각 파티션의 내부 값들을 병합하며, 병합 함수는 여러 파티션의 값을 최종 병합    
```
prods = transByCust.aggregateByKey([], lambda prods, tran: prods + [tran[3]],
    lambda prods1, prods2: prods1 + prods2)
# 1. RDD1의 파티션별로(파티션 1 ~ 3까지) 각 키 값을 모아서 리스트를 구성
# 2. 스파크는 이 리스트들을 각 노드의 중간 파일에 기록
# 3. 병합 함수를 호출해 여러 파티션에 저장된 리스트들을 각 키별 단일 리스트로 병합
# 4. 기본 Partitioner(즉, HashPartitioner)를 적용하여 각 키를 적절한 파티션에 할당
```      

_    
* 맵 테스크       
: 셔플링 바로 전에 수행한 테스크  
  - 맵 테스크의 결과는 중간 파일에 기록(주로 OS의 파일 시스템 캐시에만 저장), 이후 리듀스 테스크가 이 파일을 읽어 들음  
  - 중간 파일을 디스크에 기록하는 작업도 부담이지만, 셔플링할 데이터를 네트워크로 전송해야 하기 때문에 스파크 잡의 셔플링 횟수를 최소한으로 줄이도록 노력해야함  

_  
* 리듀스 테스크  
: 셔플링 바로 다음에 수행한 테스크

-------------------------------------------------------------------

## 4.2.2.1 셔플링 발생조건 : Partitioner를 명시적으로 변경하는 경우
> * Pair RDD 변환 연산자의 대부분에 사용자 정의 Partitioner를 지정할 수 있고, 사용자 정의 Partitioner를 쓰면 반드시 셔플링이 발생 ( 이전 HashPartitioner와 다른 HashPartitioner를 사용해도 동일 )  
* 스파크는 HashPartitioner 객체가 다르더라도 동일한 파티션 개수를 지정했다면 같다고 간주
  - 즉, 이전에 사용한 HashPartitioner와 **파티션 개수가 다른** HashPartitioner를 변환 연산자에 사용하면 셔플링이 발생
>```python
> # RDD의 원래 파티션 개수(parallelism)가 100개가 아니였다고 가정
> # 파티션의 개수를 100개라고 명시적으로 변경
> rdd.aggregateByKey(zeroValue, seqFunc, comboFunc, 100).collect()
> #in Python there is no version of aggregateByKey with a custom partitioner
```

## 4.2.2.2 셔플링 발생조건 : Partitioner를 제거하는 경우
> * 대표적으로 RDD의 Partitioner를 제거하는 연산자
  - map과 flatMap
  - 이 연산자 자체로는 셔플링이 발생하지 않지만, 연산자의 결과 RDD에 다른 변환 연산자(aggregateByKey나 flodByKey)를 사용하면 Partitioner를 사용했더라도 셔플링 발생

```python
# sc.parralelize() 이용하여 RDD 생성  ( 0~9999 정수 목록으로 RDD 만듦)
rdd = sc.parallelize(range(10000))   
# map 변환을 사용하여 Pair RDD를 생성하고, Partitioner를 제거한 후 또 다른 map으로 키와 값을 서로 바꿈 (셔플링 발생 X )
rdd.map(lambda x: (x, x*x)).map(lambda (x, y): (y, x)).collect()
# 동일한 Pair RDD만든 후, reduceByKey 변환 연산자가 셔플링 유발
rdd.map(lambda x: (x, x*x)).reduceByKey(lambda v1, v2: v1+v2).collect()
```
> * map이나 flatMap 변환 연산자 뒤에 사용하면 셔플링이 발생하는 변환 연산자
  - RDD의 Partitioner를 변경하는 Pair RDD 변환 연산자  
  : aggregateByKey, foldByKey, reduceByKey, groupByKey, join, leftOuterJoin, rightOuterJoin, fullOuterJoin, subtracByKey
  - 일부 RDD 변환 연산자   
  : suubtract, intersenction, groupWith
  - sortByKey 변환 연산자(셔플링이 부조건 발생)
  - partitionBy 또는 shuffle=true로 설정한 coalesce 연산자

## 4.2.2.3 외부 셔플링 서비스로 셔플링 최적화
* `셔플링`을 수행하면 실행자는 다른 실행자의 파일을 읽어 들여야 함 (SPARK의 셔플링은 풀링(Pulling)방식 사용 )
  - 셔플링 도중 일부 실행자에게 장애가 발생할 시 데이터 흐름이 중단됨
    - 해당 실행자가 처리한 데이터를 더 이상 가져올 수 없기 때문

* 반면 `외부 셔플링 서비스`는 실행자가 중간 셔플 파일을 읽을 수 있는 단일 지점을 제공하여 셔플링의 데이터 교환 과정을 최적화할 수 있음
  - spark는 각 워커 노드별로 외부 셔플링 서버를 시작함
  - 외부 셔플링 서비스를 활성화하려면 `spark.shuffle.service.enabled`를 true로 설정하면 됨

## 4.2.2.4 셔플링 관련 매개변수
**spark는 `정렬 기반 셔플링`과 `해시 기반 셔플링` 지원**
  - 셔플링 알고리즘은 `spark.shuffle.manager` 매개변수 값을 `hash` 또는 `sort`로 설정하여 지정
  - `정렬 기반 셔플링`은 파일을 더 적게 생성하고 메모리를 더 효율적으로 사용가능

1. saprk.shuffle.consolidateFiles 매개변수  
: 셔플링 중에 생성된 중간 파일의 통합 여부를 지정   

**집계 연산이나 co-grouping 연산으로 발생하는 셔플링 작업에는 많은 메모리 리소스 필요**
2. spark.shuffle.spill 매개변수  
: 셔플링에 쓸 메모리 리소스의 제한 여부를 지정할 수 있다.
  - 메모리를 제한하면 스파크는 제한 임계치를 초과한 데이터를 디스크로 내보냄
  - 메모리 임계치는 `spark.shuffle.memoryFraction` 매개변수로 지정
    - 메모리 임계치를 너무 높게 하면 메모리 부족 예외 발생할 수 있음
    - 너무 낮게 설정하면 데이터를 자주 내보내므로 균형을 잘 맞추는 것이 중요 ( 보통 기본설정을 사용함 )

3. spark,shuffle.spill.compress 매개변수   
: 디스크로 내보낼 데이터의 압출 여부 지정 가능

4. spark.shuffle.compress : 중간 파일의 압축 여부 지정 (기본값 true)
5. spark.shuffle.spill.batchSize : 데이터를 디스크로 내보낼 때 일괄로 직렬화 또는 역직렬화할 객체 개수 지정 (기본값 1만개)
6. spark.shuffle.service.port : 외부 셔플링 서비스를 활성화할 경우 서비스 서버가 사용할 포트 번호 지정 (기본값 7337 )


## 4.2.3 RDD 파티션 변경
**왜 파티션 변경?**   
**→ 작업 부하를 효율적으로 분산  /  메모리 문제 방지**를 위해 RDD의 파티셔닝을 명시적으로 변경  

* 일부 SPARK 연산자에는 파티션 개수의 기본 값이 너무 작게 설정되어 있는 경우
  - 파티션에 매우 많은 요소를 할당하고, 메모리를 과다하게 점유하여 병렬 처리 기능 저하 

* RDD의 파티션을 변경할 수 있는 변환 연산자
  - `partitionBy`,`coalesce`,`repartition`,`repartitionAndSortWithinPartition`
  1. partitionBy  
    - Pair RDD에서만 사용 가능
    - Partitioner 객체만 인자로 전달 가능
    - 전달된 Partitioner가 기존과 동일하면 파티셔닝을 그대로 보존하며, RDD도 동일하게 유지 , 반면 기존과 다르면 셔플링 작업을 스케쥴링하고 새로운 RDD 생성
  2. coalesce  
    : 파티션 개수를 줄이거나 늘리는데 사용  
    - 두번쨰 인자는 셔플링의 수행여부 지정
      - 파티션 개수를 늘리려면 → shuffle = ture
    - coaalesce 메서드 알고리즘은 새로운 파티션 개수와 동일한 개수의 부모 RDD 파티션을 선정하고 나머지 파티션의 요소를 나누어 선정한 파티션과 병합(coalescce)하는 방식으로 파티션 개수를 줄임
      - 이 과정에서 부모 RDD 파티션의 지역성 정보를 최대한 유지하면서 데이터를 전체 파티션에 고르게 분배하려고 노력
  3. repartition  
    : 단순히 shuffle을 true로 설정하여 coalesce를 호출한 결과를 반환
    - coalesce의 `shuffle인자를 false로 지정`한 경우
      - 셔플링이 발생하지 않는 coalesce 이전의 모든 변환 연산자는 coalesce에 새롭게 지정된 실행자 개수(파티션 개수)를 사용
    - coalesce의 `shuffle인자를 true로 지정`한 경우 
      - coalesce 이전의 변환 연산자들은 원래 파티션 개수를 그대로 사용, coalesce 이후의 연산자들만 새롭게 지정된 파티션 개수로 실행
  4. repartitionAndSortWithinPartition  
    - RDD 파티션을 변경할 수 있으며, 정렬 가능한 RDD(정렬 가능한 키로 구성된 Pair RDD)에서만 사용 가능
    - 새로운 Partitioner객체를 받아 각 파티션 내에서 요소를 정렬
    - 셔플링 항상 수행

## 4.2.4 파티션 단위로 데이터 매핑
**spark에서는 RDD의 전체 데이터 뿐만 아니라 RDD의 각 파티션에 개별적으로 매핑함수를 적용할 수 있음**
- 각 파티션 내에서만 데이터가 매핑되도록 기존 변환 연산자를 최적화해 셔플링 억제 가능
- 파티션 단위로 동작하는 RDD 연산 : mapPartitions, mapPartitionsWithIndex
- 파티션을 요소로 매핑 : glom

1. mapPartitions  
  - 매핑함수를 인수로 받는다는 점에서 map과 동일 
  - mapPartitions의 매핑 함수는 각 파티션의 모든 요소를 반복문으로 처리하고 새로운 RDD 파티션을 생성
2. mapPartitionsWithIndex  
  - mapPartitions과 유사하지만 mapPartitionsWithIndex는 매핑 함수에 파티션 번호가 함께 전달됨
  - 매핑 함수는 이 파티션 번호를 매핑 작업에 활용 가능
3. glom  (파티션의 데이터를 수집)   
: 각 파티션의 모든 요소를 배열 하나로 모으고, 이 배열들을 요소로 포함하는 새로운 RDD를 반환
  - 새로운 RDD에 포함된 요소 개수는 이 RDD의 파티션 개수와 동일
  - glom 연산자는 기존의 Partitioner를 제거 

```python
import random
# 0 ~ 99 중에서 랜덤하게 숫자를 500번 뽑아라
l = [random.randrange(100) for x in range(500)]

# l을 파티션 30개에 분산된 RDD 생성 후 glom 연산자 호출 
rdd = sc.parallelize(l, 30).glom()

# rdd는 각 파티션의 데이터로 구성된 배열임을 알 수 있음
rdd.collect()

# 배열의 객체수가 30개임을 알 수 있음 
rdd.count()
```
