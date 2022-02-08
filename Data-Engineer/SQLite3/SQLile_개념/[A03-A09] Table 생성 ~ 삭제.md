## Table 만들기
### DB의 table명을 지을 때 단수형? 복수형?
* 일반적으로 table명을 단수형으로 지을 것을 권장
  - 단순하고 편리하다
  - table간의 관계를 나타내는 table명을 지을 때 자연스럽다
  - 단수/복수의 변환을 고민하지 않아도 된다.
  - ORM(Object Relation Mapping)을 이용할 때 좋다.  

.  
+) 단수형이든 복수형이든 규칙을 정해 일관적으로 사용하는 것이 좋음 

------------------------------------------------------  
### 추가
**(1)**     
`INSERT INTO 테이블명(컬럼1, 컬럼2, 컬럼3)
VALUES(컬럼1값, 컬럼2값, 컬럼3값);`

**(2)**
`INSERT INTO 테이블명 VALUES(컬럼1값, 컬럼2값, 컬럼3값)`  

------------------------------------------------------  
### 삭제
**(1)**  
`DELETE FROM 테이블명;`  
→ 테이블 내의 모든 행 삭제

------------------------------------------------------  
### 갱신
**(1)**  
`UPDATE 테이블명 SET 컬럼명 = 바꿀 값;`

**(2) 조건 달기**
* `UPDATE Person SET Name = '소진' WHERE Name = '박소진';`  
  → Name이 '박소진'인 행의 Name을 '소진'으로 변경

------------------------------------------------------  
### 조회
**(1)**  
`SELECT * FROM 테이블명;`  
→ 모든 테이블 내용 조회

**(2) 조건 달기**
`SELECT * FROM 테이블명 WHERE 조건;`     
* `SELECT * FROM Person WHERE Name = '박소진';`   
  → 이름이 박소진인 행의 모든 내용을 조회
* `SELECT * FORM Person WHERE Birthday IS NOT NULL;`  
  → Birthday가 NULL이 아닌 행의 모든 내용을 조회

**(3) 원하는 순서로 조회하기**
* `SELECT 컬럼명 FROM 테이블명 ORDER BY 컬럼명;`  
  →  defalut값은 오름차순이다.     
   
* `SELECT 컬럼명 FORM 테이블명 ORDER BY 컬럼명 DESC;`  
  → DESC는 내림차순

**(4) LIKE를 이용한 조회**
* `SELECT * FROM Person WHERE Birthday LIKE '1986%'`  
  → Birthday가 1986으로 시작하는 행의 모든 컬럼 조회

------------------------------------------------------  
### 변경사항 저장과 취소
* 변경사항 저장하기
  - `File → Write Changes` 또는 `DB Toolbar의 Write Changes`
  - 지금까지 작업한 내용을 DB파일에 기록
* 변경사항 되돌리기
  - `File → Revert Changes` 또는 `DB Toolbar의 Revert Changes`
  - 마지막 저장한 상태로 되돌림

------------------------------------------------------

## Table 변경
### column 추가
* `ALTER TABLE 테이블명 ADD COLUMN 컬럼명 컬럼타입`  
  ex) `ALTER TABLE Person ADD COLUMN New INTEGER`  
  → 'Person' table에 INT타입의 'NEW'컬럼 추가

--------------------------------------------  
### column명 변경
* `ALTER TABLE 테이블명 RENAME COLUM 기존_컬럼명 TO 바꿀_컬럼명`  
  ex) `ALTER TABLE Person RENAME COLUMN New TO Height`  

--------------------------------------------  
### table drop하기
* `DROP TABLE 테이블명`  
ex) `DROP TALBE Person;`

--------------------------------------------  
### 컬럼 별명
* `SELECT 컬럼1명 AS 컬럼1_별명 FROM 테이블명`  
  ex) `SELECT Name AS "이름", Birthday "생일" FROM Person;`  
  → `AS` 키워드 생략 가능
--------------------------------------------  
.  
## 뷰(View)
: `사용자에게 접근이 허용된 자료만을 제한적으로 보여주기 위해 하나 이상의 기본 테이블로부터 유도된, 이름을 가지는 가상 테이블` 
- View는 저장장치 내에 물리적으로 존재하지 않지만 사용자에게 있는 것처럼 간주된다
- View는 데이터 보정작업, 처리과정 시험 등 임시적인 작업을 위한 용도로 활용된다
3. View는 join문의 사용 최소화로 사용상의 편의성을 최대화한다.

+) 뷰(View)의 특징  
1. 뷰는 기본 테이블로부터 유도된 테이블이기 때문에 기본 테이블과 같은 형태의 구조를 사용하며, 조작도 기본 테이블과 거의 같다.
2. 뷰는 가상 테이블이기 때문에 물리적으로 구현되어 있지 않다.
3. 데이터의 논리적 독립성을 제공할 수 있다.
4. 필요한 데이터만 View로 정의해서 처리할 수 있기 떄문에 관리가 용이하고 명령문이 간단해진다.
5. View를 통해서만 데이터에 접근하게 하면 View에 나타나지 않는 데이터를 안전하게 보호하는 효율적인 기법으로 사용할 수 있다.

--------------------------------------------  
### View 생성
* `CREATE VIEW 생성_할_View명 AS SELECT ~~ FROM 테이블명`   
ex)
```python
CREATE VIEW Birthday AS 
  SELECT Name, 
  Birthday bdate,
  substr(Birthday, 1, 4) YYYY,
  substr(Birthday, 6, 2) MM,
  substr(Birthday, 9, 2) DD
  FROM Person;
```

+) substr()  
: 문자열의 일부를 반환
```python
SELECT
   substr('abcdefg', 3),     -- 셋째 자리부터 끝까지
   substr('abcdefg', 3, 2);  -- 셋째 자리부터 두 글자
```

### View 조회
- 일반 테이블과 같은 방법으로 조회
- `SELECT * FROM View명`

### View 삭제
- `DROP VIEW View명`