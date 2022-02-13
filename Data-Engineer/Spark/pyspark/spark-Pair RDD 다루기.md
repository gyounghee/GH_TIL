##  ------------------------------ 4.1 Pair RDD 다루기 --------------------------------
* 키-값 쌍
  - 키-값 쌍은 범용적이고 확정성이 뛰어난 데이터 모델
  - 확장성 & 간결성   
  → 기존 키-값 쌍에 새로운 타입의 키와 값을 쉽게 추가할 수 있고, 키-값 쌍을 독립적으로 저장 가능
  - 키와 값에 정수형이나 문자열 등 기본타입도 사용 가능하며, 복잡한 데이터 구조체도 사용 가능하다.
  - 대표적인 키-값 저장소 : 캐싱 시스템, NoSQL DB 등 
  - 키-값 쌍은 `연관배열`이라는 자료 구조를 사용하는데  python에서는 ditionary, scala와 java에서는 map, **`spark에서는 Pair RDD`**라고 한다.

* Pair RDD 
: 키-값 쌍으로 구성된 RDD  

_   
> 1. Pair RDD 생성
- SparkContext의 일부 메서드는 Pair RDD를 기본으로 반환한다.   
ex) 하둡 파일 형식을 로드하는 hadoopFile, sequenceFile 등
- RDD의 keyBy 변환 연산자는 RDD 요소로 키를 생성하는 f함수를 받고, 각 요소를 `(f(요소), 요소)`쌍의 튜플로 매핑한다.
- 2-요소 튜플로 RDD를 구성하면 Pair RDD 함수가 RDD에 자동으로 추가됨 (암시적 변환)  
  → Pair RDD 함수는 PairRDDFunctions클래스에 정의되어 있으며, 2-요소 튜플로 구성된 RDD는 이 클래스의 객체로 암시적으로 변환되는 것   

_  
> 2. 기본 Pair RDD 함수  

```
한 쇼핑 사이트의 마케팅 부서에서 고객에게 선별적으로 사은품을 보내는 행사를 했다.   
마케팅 기획자는 어제 날짜의 구매기록을 읽어 들여 특정 규칙에 따라 사은품을 추가하는 프로그램을 개발해 달라고 요청했다.

** 규칙 ** 
1. 구매 횟수가 가장 많은 고객에게는 곰인형을 보낸다. 
2. 바비 쇼핑몰 놀이 세트를 두 개 이상 구매하면 청구 금액을 5% 할인해준다.  
3. 사전을 다섯 권 이상 구매한 고객에게는 칫솔을 보낸다.
4. 가장 많은 금액을 지출한 고객에게는 커플 잠옷 세트를 보낸다.  
```
```
# 예제 파일을 sc객체의 textFile을 이용해 읽어오면 RDD객체가 생성됨
tranFile = sc.textFile("first-edition/ch04/ch04_data_transactions.txt") 
tranData = tranFile.map(lambda line: line.split("#"))


# ------------------------ 첫 번쨰 조건 ----------------------------
# 1. 구매 횟수가 가장 많은 고객에게 곰인형 증정

# Pair RDD 생성
transByCust = tranData.map(lambda t: (int(t[2]), t))

# Pair RDD의 키 또는 값으로 구성된 새로운 RDD를 가져오려면 keys또는 values의 변환 연산자를 사용
# 고객 ID 목록 중 중복 제거하고 count  ( → 고객은 100명 )
transByCust.keys().distinct().count()

import operator
# 구매 횟수가 가장 많은 고객을 찾기 위해 고객 별로 줄 개수를 셈  (→ 구매 횟수는 총 1000개)
transByCust.countByKey()

# 고객들의 구매 횟수만 나타낸 후 개수 셈 
# → 당연히 총 1000개가 됨
sum(transByCust.countByKey().values())

#  transByCust.countByKey().items() → (키 : 값) 쌍을 튜플로 묶은 것
(cid, purch) = sorted(transByCust.countByKey().items(), key=operator.itemgetter(1))[-1]
complTrans = [["2015-03-30", "11:59 PM", "53", "4", "1", "0.00"]]

# lookup() 행동연산자 
# → 해당 키의 값들을 모두 보여줌
transByCust.lookup(53)

# transByCust들의 각 줄을 ','를 구분자로 하여 합침
for t in transByCust.lookup(53):
    print(", ".join(t))
```
> **mapValues 변환 연산자**
* mapValues 변환 연산자를 사용하면 키를 변경하지 않고, Pair RDD에 포함된 값만 변경할 수 있다.

```
# ------------------------ 두 번째 조건 ----------------------------
# 2. 바비 쇼핑몰 놀이 세트를 두 개 이상 구매하면 청구 금액을 5% 할인

# 바비 쇼핑몰 놀이 세트의 상품 ID( tran[3]) ) → 25  /  구매수량 ( tran[4] )  /  구매금액 ( tran[5] )
# 바비 쇼핑몰 놀이 세트를 2개 이상 구매하는 고객에게 5% 할인해주는 applyDiscount함수 생성
def applyDiscount(tran):
    if(int(tran[3])==25 and float(tran[4])>1):
        tran[5] = str(float(tran[5])*0.95)
    return tran

# mapValues 변환 연산자로 Pair RDD 값 바꾸기
transByCust = transByCust.mapValues(lambda t: applyDiscount(t))
```
> **flatMapValues 변환 연산자**  
: 변환 함수가 반환한 컬렉션 값들을 원래 키와 합쳐 새로운 키-값 쌍으로 생성  
- 변환 함수가 인수로 받은 값의 결과로 빈 컬렉션을 반환하면 해당 키-값 쌍을 결과 Pair RDD에서 제외하고, 
- 반대로 컬렉션에 두 개 이상의 값을 넣어 반환하면 결과 Pair RDD에 이 값들을 추가한다. 
- 입력 Pair RDD값은 결과 Pair RDD 타입이 다를 수 있음
>
>- 각 키 값을 0개 또는 한 개 이상 값으로 매핑하여 RDD에 포함된 요소 개수를 변경
  →  즉, 키에 새로운 값을 추가하거나 키 값을 모두 제거할 수 있음

```
# ------------------------ 세 번째 조건 ----------------------------
# 3. 사전(상품 ID 81번)을 다섯 권 이상 구매한 고객에게 사은품으로 칫솔을 증정하는 즉, 구매 기록 추가하는 함수 생성
def addToothbrush(tran):
    if(int(tran[3]) == 81 and int(tran[4])>4):
        from copy import copy
        cloned = copy(tran)
        cloned[5] = "0.00"     # 무료 증정이니까 구매 금액 0
        cloned[3] = "70"       # 칫솔 상품 ID 70번 
        cloned[4] = "1"        # 구매 수량 1
        return [tran, cloned]   # 원래 요소와 추가한 요소 반환
    else:               # 조건에 맞지 않을 경우
        return [tran]        # 원래 요소만 반환

# flatMapValues 변환 연산자
# flatMapValues에 전달한 lambda 함수는 각 구매기록을 리스트로 매핑
transByCust = transByCust.flatMapValues(lambda t: addToothbrush(t))

# ↑ 위를 실행하고 나면 
# 사전을 다섯 권 이상 구매한 기록은 모두 6개이므로 transByCust RDD의 요소는 총 1006개가 되어야함. 
```
> **reduceByKey 변환 연산자**   
reduceByKey ------- < merge함수 전달 필요 >   
: 각 키의 모든 값을 동일한 타입의 단일 값으로 병합
- 각 키별로 값 하나만 남을 때 까지 merge 함수를 계속 호출
- 따라서 merge함수는 결합 법칙을 만족해야 한다 
- 만족하지 않으면 같은 RDD라도 reduceByKey를 호출할 때마다 결과 값이 달라진다

> **foldByKey 변환연산자** 
- reducByKey와 기능은 같지만 merge 함수의 인자 목록 바로 앞에 zeroValue 인자를 담은 또 다른 인자목록을 추가 로 전달해야한다 
- zeroValue는 반드시 항등원이여야 한다   
  (*덧셈 - 0 / 곱셈 - 1 / 리스트 연산 - Nil 등)*
  - zeroValue는 가장 먼저 func 함수로 전달해 키의 첫 번째 값과 병합하며, 이 결과를 다시 키의 두 번째 값과 병합한다
  - RDD 연산이 병렬로 실행되기 때문에 zeroValue가 여러 번 쓰일 수도 있음

+) pythonRDD보는 법   
**`RDD명.foreach(print)`**

```
# ------------------------ 네 번째 조건 ----------------------------
# 4. 가장 많은 금액을 지출한 고객에게 커플잠옷세트 증정

# amounts에 구매 금액(tran[5]) 뽑아서 새로운 Pair RDD 생성 → (고객ID, 구매금액)
amounts = transByCust.mapValues(lambda t: float(t[5]))
# amounts에 각 고객 ID별로 구매금액 합산
totals = amounts.foldByKey(0, lambda p1, p2: p1 + p2).collect()

# zeroValue가 여러 번 쓰이는 상황 재현  → 100000
# zeroValue(100000달러)가 결과 값에 여러번(RDD의 파티션 개수만큼) 더해진다.
amounts.foldByKey(100000, lambda p1, p2: p1 + p2).collect()

# ID 76번 고객에게 커플 잠옷 세트(상품 ID 63번)를 보내기 위해 암시로 만든 complTrans 배열에 구매기록 추가
complTrans += [["2015-03-30", "11:59 PM", "76", "63", "1", "0.00"]]


# 구매 기록에서 고객 ID를 키로 설정하고 구매 기록의 배열 전체를 값으로 설정하여, transByCust RDD에 추가한 후 결과를 새로운 파일에 저장해야함

# transByCust에 고객 ID를 키로, 구매 기록의 배열 전체를 값으로 설정하여 저장
transByCust = transByCust.union(sc.parallelize(complTrans).map(lambda t: (int(t[2]), t)))

# tarnsByCust의 값을 '#'를 구분자로 하여 합친 후, ch04output-transByCust TextFile로 저장
# ↓↓ 이미 저장되어있을 경우 이상한.. 긴 오류같은게 뜸  ↓↓
transByCust.map(lambda t: "#".join(t[1])).saveAsTextFile("ch04output-transByCust")

# ------------------------------ 업무 끝 ------------------------------
```
> aggregateByKey 
- aggregateByKey는 zeroValue를 받아 RDD 값을 병합한다는 점에서 foldByKey나 reduceByKey와 유사하지만, 값 타입을 바꿀 수 있다는 차이가 있음
- aggregateByKey를 호출하려면 `zeroValue`와 `변환함수`와 `병합함수`를 인수로 전달해야함
  - 변환함수   
    : 임의의 V 타입을 가진 값을 또 다른 U 타입으로 변환 
  - 병합함수   
    : 첫 번째 함수가 변환한 값을 두 개씩 하나로 병합
- aggregateByKey 연산자에 zeroValue 인수만 넣어 호출하면 변환 함수와 병합 함수를 인수로 받는 새로운 함수가 반환됨 → But, 보통 모든 인자를 한번에 전달하여 호출 


```
# 각 고객이 구매한 제품의 목록 확인하기
# tran[3] → 상품 ID 
# zeroValue로 빈 List를 사용했다
# 첫 번째 인자는 RDD의 각 파티션별로 요소를 병합
# 두 번쨰 인자는 여러 파티션의 값을 최종 병합
prods = transByCust.aggregateByKey([], lambda prods, tran: prods + [tran[3]], lambda prods1, prods2: prods1 + prods2)
prods.collect()
```


