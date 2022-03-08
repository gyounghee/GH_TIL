> DB 또는 TABLE 보기
- 
```
SHOW DATABASES;
SHOW TABLES;
```

> **DB**
- DB 만들기  
  - `CREATE DATABASE DB명;`
>
> - DB 선택하기  
  - ```
  USE DB명;
  ```
>

> **TABLE**
- TABLE 만들기  
  - 
  ```
  CREATE TABLE TABLE명(
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(20) NOT NULL,
  description TEXT NULL,
  PRIMARY KEY(id)
  );
```
- TABLE 구조 살펴보기
  - ```
  DESC TABLE명
  ```
- TABLE에 값 추가
  - ```
  INSERT INTO TABLE명(title, description, created, author, profile) VALUES ( 'MySQL', 'MySQL is ...', NOW(), 'gyounghee', 'developer' ); 
  ```
- TABLE 내용 조회
  - ```
  SELECT * FROM topic;
  ```
  - 조건에 맞는 내용 조회 ( WHERE )  
  ```
  SELECT * FROM topic WHERE author = 'gyounghee';
  ```
  - 정렬하기 ( ORDER BY 컬럼명 [DESC, ASC] )   
  → 저자가 gyounghee인 컬럼들을 내림차순으로 정렬하여 2건만 조회
  ```
  SELECT * FROM topic 
  WHERE author = 'gyounghee' 
  ORDER BY id DESC
  LIMIT 2;
  ````
  - TABLE 내용 수정 
  ```
  UPDATE topic SET description='Oracle is ...',title='Oracle' 
  WHERE id = 2;
  ```
  - TABLE 내용 삭제
  ```
  DELETE FROM topic WHERE id = 5;
  ```