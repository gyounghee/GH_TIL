# DB와 DBMS
* DB(DataBase) - 컴퓨터에 체계적으로 저장한 데이터
* DBMS(DataBase Management System) - 데이터베이스를 관리하는 시스템  
------------------------------------------------------
###  파일 시스템  vs  DB
* 파일 시스템  
  : 원시 데이터 파일을 컴퓸터의 하드 디스크 등에 저장하는 시스템 
  - 중복 데이터가 많이 발생  /  데이터의 일관성이 떨어짐  /  보안, 백업.복구가 불편

* DB  
  : 컴퓨터에 체계적으로 저장한 데이터
  - 파일 시스템의 단점을 보완  /  데이터의 모델링, 무결성, 다수 사용자를 위한 동시성 제어 등을 제공

+) DBMS
  - DB를 여러 개의 파일에 저장하거나, 하나의 DB를 한개의 파일에 저장, 또는 아예 파일 시스템을 이용하지 않고 디스크에 직접 기록하는 긴으을 지원하는 DBMS도 있다.
  - SQLite는 하나의 DB를 한개의 파일에 저장한다.  

-----------------------------------------------------    
### DL(Data Lake), DW(Data Warehouse), DM(Data Mart)
* DL(Data Lake)  
  : 정형 및 비정형(소셜, 센서, 이미지, 동영상 등)의 다양한 형태의 원시 데이터를 모은 저장소의 집합.
* DW(Data Warehouse)  
  : 데이터 분석을 효율적으로 수행하기 위한 OLAP(온라인 분석 처리) DB와 같이, DB로부터 가져온 데이터의 계층을 생성한다.
  - 주제 중심적이고 비휘발성의 특징을 갖는다.
* DM(Data Mart)  
  : 특정 부서의 의사 결정 지원을 목적으로 하는 부서별 또는 부분별 DW, 분석요건을 중심으로 한 요약 데이터로 구성됨      
-----------------------------------------------------    
### DB의 종류 
- DB는 데이터를 바라보는 관점에 따라 관계형 DB, 계층형 DB, 그래프 DB 등으로 나눌 수 있다.  

.  
#### * 관계형 DB (Relational Database) 
  : 관계형 DB는 데이터를 `관계`로 나타낸다.
  - 일반적으로 DBMS라고하면 RDBMS(Relational DBMS)를 말하며, 오라클 데이터베이스 서버, 마이크로소프트 SQL서버, MySQL과 MariaDB, (PostgreSQL) 등이 이에 해당
  - SQLite도 RDBMS

* SQLite   
  - 가장 널리 사용되는 DB엔진으로 임베디드 디바이스, 사물 인터넷, 데이터 분석, 작은 규모의 웹 사이트에 사용하기 적합하다.
  - SQLite는 임베디드 SQL DB엔진으로, 독립적인 서버 프로세스를 갖지 않는다.
  - 설치 과정이 없고, 설정 파일도 존재하지 않는다.
  - Table, Index, Trigger, View등을 포함한 완전한 db가 디스크 상에 단 하나의 파일로 존재한다.
  - 퍼블릭 도메인으로서 개인적 또는 상업적 목적으로 사용할 수 있다.

    
##### → 관계형 DB에서는 데이터를 `관계`로 나타내며, 이는 `table`로 구현됨
- relation(관계) = table(테이블)
- tuple(튜플) = row(행) = record(레코드)
- attribute(속성) = column(열) = field(필드)

.  
#### 계층형 DB (Hierachical Database)
: 계층형 DB는 데이터를 계층적인 `트리(tree)`로 표현
- 데이터는 레코드(record)로 저장되며, 레코드들은 링크(link)를 통해 연결된다. 
- 레코드(record) : 필드(field)들의 모임
- 필드(field)는 단일 값을 갖는다.

.
#### 그래프 DB (Graph Database)  
: 그래프 DB는 데이터를 `그래프 형태`로 표현한다.

------------------------------------------------------  
### SQL (Structured Query Language)
: SQL은 RDBMS의 데이터를 다루기 위해 사용하는 언어
- DML(Data Manipulation Language, 데이터 조작 언어)  
  : DML은 데이터를 추가, 삭제, 갱신, 조회 하는데 사용한다.
  - `INSERT`,`DELETE`,`UPDATE`,`SELECT`
- DDL(Data Definition Language, 데이터 정의 언어)  
  : DDL은 table등을 생성, 변경, 제거하는데 사용
  - `CREATE`,`ALTER`,`DROP`,`TRUNCATE`
  - SQLite에는 `TRUNCATE`문이 없다.