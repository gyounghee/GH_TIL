## 4.3 데이터 조인, 정렬, 그루핑
```python
# 마케팅 기획자가 보고서에 추가해달라고 요청한 데이터이다.

# * 요청사항 *
# - 어제 판매한 상품 이름과 각 상품별 매출액 합계 (알파벳 오름차순으로 정렬할 것)
# - 어제 판매하지 않은 상품 목록
# - 전일 판매 실적 통계 : 각 고객이 구입한 상품의 평균 가격, 최저 가격 및 최고 가격, 구매 금액 합계

# 모든 분석 작업에 스파크 코어 API 사용하여 작업할거임
```

### 4.3.1 데이터 조인
* 4.3 실습 시작 전 필요한 파일 불러오고 가공   

```python
# 전일 구매 기록이 담긴 예제 파일을 불러와 RDD 생성한 후 tranFile에 저장
tranFile = sc.textFile("first-edition/ch04/ch04_data_transactions.txt")

# tranFile의 각 줄을 "#"을 기준으로 나눈 후 tranData에 저장
tranData = tranFile.map(lambda line: line.split("#"))

# tranData를 매핑하여 고객 ID(t[2])를 키로 설정한 Parir RDD 생성한 후 tranByCust에 저장
transByCust = tranData.map(lambda t: (int(t[2]), t))
```

### 4.3.1.1 RDBMS와 유사한 Join 연산자
1. join   
: RDBMS의 내부조인(inner join)과 동일
  - 첫 번째 Pair RDD와 두 번째 Pair RDD에서 키가 동일한 모든 값의 조합이 포함된 Pair RDD[(K, (v,M))] 생성
  - 두 RDD 중 어느 한쪽에만 있는 키의 요소는 결과 RDD에서 제외
2. leftOuterJoin  
: (K , (V, Option(W))) 타입의 Pair RDD 반환
   - 첫 번째 RDD에 있는 요소를 기준으로 Join
    - 첫 번째 RDD에만 있는 키의 요소는 결과 RDD에 (key, (V,None)) 타입으로 저장
    - 두 번째 RDD에만 있는 키의 요소는 결과 RDD에서 제외
3. rightOuterJoin  
: (k, (Option(V), W)) 타입의 Pair RDD 반환
  - 두 번째의 RDD에 있는 요소를 기준으로 Join
    - 첫 번째 RDD에만 있는 키의 요소는 RDD에서 제외
    - 두 번째 RDD에만 있는 키의 요소는 결과 RDD에 (key, (None, W)) 타입으로 저장
4. fullOuterJoin  
: (k, (Option(V), Option(W))) 타입의 Pair RDD 반환
  - 두 RDD 중 어느 한 쪽에만 있는 키의 요소는 결과 RDD에 (key, (v, None)) 또는 (key, (None, w)) 타입으로 저장  

**조인할 두 RDD의 요소 중 키가 중복된 요소는 여러 번 Join**

* 다른 Pair RDD 변환 연산자와 마찬가지로 조인 연산자에 Partitioner 객체나 파티션 개수를 전달할 수 있다.
  - 연산자에 파티션 개수만 지정하면 HashPartitioner를 사용
  - Partitioner를 지정하지 않으면(더하여 파티션 개수도 지정하지 않으면) 스파크는 Join할 두 RDD 중 첫 번째 RDD의 Partitioner를 사용
  - 두 RDD에 Partitioner를 명시적으로 정의하지 않으면 스파크는 새로운 HashPartitioner 생성
    - 이때는 파티션 개수로 spark.default.partitions 매개변수 값을 사용하거나(명시적으로 설정된 경우) 두 RDD의 파티션 개수 중 더 큰 수를 사용 

```python
##  1. 어제 판매한 상품 이름과 각 상품별 매출액 합계(오름차순으로 정렬)

# transByCust를 매핑하여 상품 ID(ct[1][3])를 키로하는 Pair RDD 생성 후 transByProd에 저장
transByProd = transByCust.map(lambda ct: (int(ct[1][3]), ct[1]))

# mapValues 변환연산자를 이용하여 매출 금액의 type을 float으로 변경 후
# reauceByKey 변환 연산자를 이용해 각 상품의 매출금액 합계를 구하여 totalsByProd에 저장 
# reduceByKey는 각 키의 모든 값을 동일한 타입의 단일 값으로 병합하며, 각 키별로 값 하나만 남을 때 까지 merge 함수를 계속 호출 
totalsByProd = transByProd.mapValues(lambda t: float(t[5])).reduceByKey(lambda tot1, tot2: tot1 + tot2)

# textFile로 로드한 상품 파일을 RDD로 생성한 후 
# 매핑을 통해 각 줄 별로 "#"를 기준으로 나눔
# 다시한번 매핑하여 Pair RDD 생성 후 products 변수에 저장
products = sc.textFile("first-edition/ch04/ch04_data_products.txt").map(lambda line: line.split("#")).map(lambda p: (int(p[0]), p))


# ---------------------- join (inner join) --------------------------
# totalsByProd와 products join(결합)하여 totalsAndProds에 저장
# 상품 ID별로 두 쌍(해당 상품의 매출액, 상품 데이터의 문자열 배열)으로 구성된 2-요소 튜플이 만들어진것
totalsAndProds = totalsByProd.join(products)

# totalsAndProds의 첫번쨰 요소 불러오기
totalsAndProds.first()


# ---------------------- leftOuterJoin --------------------------
## 2. 어제 판매하지 않은 상품 목록 

# products를 기준으로 join하여 totalsWithMissingProds에 저장
totalsWithMissingProds = products.leftOuterJoin(totalsByProd)

# 판매하지 않은 상품 목록을 보기 위해 None값을 가진 요소만 남도록 RDD를 필터링 한 후 키와 None객체를 제외한 상품데이터만 가져와야 함
# leftOuterJoin한 totalsWithMissingProds 중에서 필터링하여 두 번쨰 RDD의 요소가 None인 것을 뽑은 후에, 매핑하여 첫 번쨰 RDD의 요소만 missingProds에 저장
missingProds = totalsWithMissingProds.filter(lambda x: x[1][1] is None).map(lambda x: x[1][0])

from __future__ import print_function
# missingProds의 각 줄을 ", "를 구분자로 하여 join후 출력
missingProds.foreach(lambda p: print(", ".join(p)))
```

* subtract  
  - 첫 번쨰 RDD에서 두 번째 RDD의 요소를 제거한 여집합 반환 
  - subtract 메서드는 일반 RDD에서도 사용 가능
  - 전체를 비교하여 제거 여부 판단

* subtractByKey
  - Pair RDD 에서만 사용가능한 메소드
  - 첫 번째 RDD의 키-값 쌍 중에서 두 번째 RDD에 포함되지 않은 키의 요소들로 RDD를 구성하여 반환
  - 첫 번쨰 RDD와 두 번째 RDD는 반드시 같은 타입의 값을 가질 필요 없음


```python
# ------------------------------ 위의 leftOuterJoin 보다 더 간단한 방법 ---------------------------------
# 이 작업에는 subtractByKey가 적절

# rightOuterjoin을 한 결과와 동일
# totalsByKey의 값이 None인 products 요소들로 RDD를 구성하여 반환되는 값을 missingProds에 저장
missingProds = products.subtractByKey(totalsByProd)

# missingProds의 각 줄을 ", "를 구분자로 하여 출력
missingProds.foreach(lambda p: print(", ".join(p[1])))

# 
missing = transByProd.subtractByKey(products)
```

* cogroup 변환연산자로 RDD 조인   
: 여러 RDD 값을 각각 키로 그루핑한 후 키를 기준으로 조인
  - RDD를 최대 3개까지 Join 가능
  - cogroup을 호출한 RDD와 cogroup에 전달된 RDD는 모두 동일한 타입의 키를 가져야 함


```python
# cogroup을 통해 totalsByProd와 products 조인 후 prodTotCogroup에 저장
prodTotCogroup = totalsByProd.cogroup(products)

# prodToCogroup의 값에서 첫 번째 RDD(매출 합계)가 없는 것 줄만 필터링 한 후
# 두 번째 RDD(상품 데이터)의 내용을 ', "를 구분자로 하여  join한 후 출력 
prodTotCogroup.filter(lambda x: len(x[1][0].data) == 0).foreach(lambda x: print(", ".join(x[1][1].data[0])))


# -------------------------------------- +) 어제 판매한 상품 보기 ------------------------------------
# prodTotCogroup에서 매출 합계가 0이상인 것들을 필터링 한 후,
# 상품 데이터 중 상품 ID만 출력
totalsAndProds = prodTotCogroup.filter(lambda x: len(x[1][0].data)>0).map(lambda x: (int(x[1][1].data[0][0]),(x[1][0].data[0], x[1][1].data[0])))
```

* intersection 변환연산자   
: 타입이 동일한 두 RDD에서 양쪽 모두에 포함된 공통 요소(즉, 교집합)을 새로운 RDD로 반환

```python
# 매출 합계 데이터에서는 상품 ID를 매핑하고, 상품 데이터에서는 상품의 ID를 매핑하여 교집합 구하기 
totalsByProd.map(lambda t: t[0]).intersection(products.map(lambda p: p[0]))

rdd1 = sc.parallelize([1,2,3])
rdd2 = sc.parallelize([2,3,4])

# rdd1와 rdd2의 교집합 구해서 하나의 배열로 합치기  → 결과는 [] 
rdd1.intersection(rdd2).collect()
```

* cartesian 변환연산자  
: 두 RDD의 데카르트 곱()을 계산
  - 첫 번째 RDD와 두 번째 RDD의 요소로 만들 수 있는 모든 조합이 (T,U) 쌍 형태로 구성
  - 모든 파티션의 데이터를 결합해야 하므로 대량의 데이터가 네트워크로 전송될 수 밖에 없다.
  - 또한, 결과 RDD에 포함된 요소 개수 또한 지수적으로 증가하므로 무시 못할 정도로 많은 메모리 용량이 필요 

```python
rdd1 = sc.parallelize([7,8,9])   # 7,8,9를 요소로 가지는 RDD 생성
rdd2 = sc.parallelize([1,2,3])   # 1,2,3을 요소로 가지는 RDD 생성
rdd1.cartesian(rdd2).collect()   # catesian 변환연산자를 이용하여 데카르트 곱 수행

# cartesian연산을 한 결과 중에서 rdd2숫자로 rdd1를 나눴을 떄 나누어떨어지는 조합 찾기
rdd1.cartesian(rdd2).filter(lambda el: el[0] % el[1] == 0).collect() 
```

* zip 변환연산자   
  - zip과 zipPartitions의 변환 연산자는 모든 RDD에 사용 가능
  - RDD[T]의 zip 연산자에 RDD[U]를 전달하면 zip 연산자는 두 RDD의 각 요소를 순서대로 짝 지은 새로운 RDD[(T,U)]를 반환
    - 첫 번쨰 쌍은 각 RDD의 첫 번째 요소를 두 번째는 두 번째 요소끼리  ... ~ 조합한 것
  - 스파크의 zip연산자는 두 RDD의 파티션 개수가 다르거나 두 RDD의 모든 파티션이 서로 동일한 개수의 요소를 포함해야 함

```python
rdd1 = sc.parallelize([1,2,3])
rdd2 = sc.parallelize(["n4","n5","n6"])

# 순서에 맞는 요소끼리 zip !! 
rdd1.zip(rdd2).collect()
```

-------------------------------------------------------

### 4.3.2 데이터 정렬
* RDD의 데이터를 정렬하는 데 주로 사용하는 변환 연산자
  1. repartitionAndSortWithPartition
     - 리파티셔닝과 정렬 작업을 동시에 수행
     -  정렬 가능한 클래스를 Pair RDD 키로 사용할 떄만 호출 가능
  2. sortByKey 
    - 키를 기준으로 정렬하는 것 같음 
    - 인자로 ascending = True (또는 False)를 이용하여 오름자순 (또는 내림차순) 설정 가능
    - 정렬 가능한 클래스를 Pair RDD 키로 사용할 떄만 호출 가능
  3. sortBy   
    - 

```python
# totalsAndProds.first()    →    (6, (43252.97, [u'6', u'LEGO Castle', u'4777.51', u'10']))
# totalsAndProds의 값
# t[1]   →    (43252.97, [u'6', u'LEGO Castle', u'4777.51', u'10'])

# 상품 데이터 
# t[1][1]   →   [u'6', u'LEGO Castle', u'4777.51', u'10']

# 상품 ID
# t[1][1][1]   →   LEGO Castle

# totalsAndProds의 값에서 상품데이터의 상품 ID를 기준으로 정렬
sortedProds = totalsAndProds.sortBy(lambda t: t[1][1][1])
sortedProds.collect()
```

--------------------------------------------------------
### 4.3.3 데이터 그루핑
**그루핑(Grouping)**  
: 특정 기준에 따라 단일 컬렉션으로 집계하는 연산
- aggregateByKey, groupByKey(또는 groupBy), combineByKey등의 Pair RDD 변환 연산자를 이용하여 데이터 그루핑

_  
1. groupByKey   
: 동일한 키를 가진 모든 요소를 단일 키-값 쌍으로 모은 Pair RDD 반환
- 각 키의 모든 값을 메모리로 가져오기 때문에 메모리 시소스를 과다하게 사용하지 않도록 주의해야 함
- 모든 값을 한꺼번에 그루핑 할 필요가 없으며, aggregateByKey, reduceByKey, foldByKey를 사용하는 것이 좋음
2. groupBy  
- Pair RDD가 아닌 일반 RDD에서도 사용 가능
- 일반 RDD를 Pair RDD로 변환하고 groupByKey를 호출하는 것과 같은 결과를 만들 수 있음   

=> *groupByKey과 groupBy는 동일한 결과를 반환*

3. combineByKey  
- combineByKey를 호출하려면 3가지 커스텀 함수를 정의하여 전달해야함
  - 두 번째 함수는 Pair RDD에 저장된 값들을 `결합 값으로 병합`
  - 세 번째 함수는 `결합값을 최종 결과로 병합`



```python
# 결합 값을 생성하는 함수
def createComb(t):
    total = float(t[5])   # 구매 금액
    q = int(t[4])         # 구매 수량
    return (total/q, total/q, q, total)  # 낱개가격, 낱개가격, 구매수량, 구매금액

# 결합 값과 값을 병합하는 함수
def mergeVal((mn,mx,c,tot),t):
    total = float(t[5])   # 구매 금액
    q = int(t[4])         # 구매 수량
    return (min(mn,total/q),max(mx,total/q),c+q,tot+total)   # 

# 결합 값을 서로 병합하는 함수 
def mergeComb((mn1,mx1,c1,tot1),(mn2,mx2,c2,tot2)):
    return (min(mn1,mn1),max(mx1,mx2),c1+c2,tot1+tot2)

# conbineByKey를 활용하여 각 고객이 구매한 상품의 최저 가격 최고가격, 총 구매 수량, 총 구매 금액의 튜플로 구성된 RDD 반환 (transByCust RDD의 파티션 개수를 그대로 사용하여 파티셔닝을 유지함)
# mapVlalues 변화연산자를 상요하여 상품의 평균 가격을 튜플에 추가한 후 avgByCust에 저장
avgByCust = transByCust.combineByKey(createComb, mergeVal, mergeComb).mapValues(lambda (mn,mx,cnt,tot): (mn,mx,cnt,tot,tot/cnt))
avgByCust.first()

# x  →  (98, (51227.19, [u'98', u'Gabapentin', u'8763.57', u'5']))

# totalsAndProds의 값만 매핑하고,   
# 그 결과에서 그 값+", "+키를 ', '를구분자로 하여 join하고 그 결과를 "ch04output-totalsPerProd"라는 이름의 TextFile로 저장한다. 
totalsAndProds.map(lambda p: p[1]).map(lambda x: ", ".join(x[1])+", "+str(x[0])).saveAsTextFile("ch04output-totalsPerProd")

# 구분자를 "#'로 하고 출력 형식 지정하여 "ch04output-avgByCust"라는 이름의  textFile로 저장 
avgByCust.map(lambda (pid, (mn, mx, cnt, tot, avg)): "%d#%.2f#%.2f#%d#%.2f#%.2f" % (pid, mn, mx, cnt, tot, avg)).saveAsTextFile("ch04output-avgByCust")

```