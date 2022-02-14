```python
==== AWS EC2 에 MYSQL 설정

1. ubuntu 패키지 정보 업데이트
	sudo apt update


2. mysql 설치
apt를 이용하여 mysql 을 설치 

설치 과정에서 y/n를 묻는 문구가 나오면, y 를 입력하여 설치
	sudo apt install mysql-server
--apt-get install mysql-client

3. mysql 설치 확인

--  dkpg --
dpkg는 데비안 패키지 관리 시스템의 기초가 되는 소프트웨어로서, .deb 패키지의 설치, 삭제, 정보 제공을 위해 
사용되는 명령어
dpkg 자체는 APT 등과 같은 고급 도구에 비해 낮은 레벨의 도구이며 복잡한 패키지 관계와 패키지를 원격에서
 받아오는 등의 일을 함. APT도 Ubuntu의 소프트웨어를 관리하기 위해 내부적으로 이 dpkg를 사용
사용 방법
dpkg -l

	dpkg -l | grep mysql-server


4. mysql 실행여부 확인

	sudo netstat -tap | grep mysql


5. mysql 외부 접속 설정

mysql.conf.d 디렉토리로 이동

	cd /etc/mysql/mysql.conf.d
	mysqld.cnf 파일 수정
		-- sudo vi mysqld.cnf
		bind-address를 127.0.0.1 ->0.0.0.0 으로 변경
		-- cat mysqld.cnf
6.mysql 접속


	sudo mysql
	외부 접속 계정 생성 & 권한 부여
		create user '계정이름'@'%' identified by '패스워드';
		grant all privileges on *.* to '계정이름'@'%' with grant option;

7. AWS EC2 인스턴스에 mysql 접속 포트 추가

	네트워크 및 보안
		보안 그룹
			인바운드 규칙 (1/1)
				인바운드 규칙 편집
					규칙추가
						모든규칙
						    MYSQL/Aurora (선택)

8. Mysql에서 접속 확인
mysql workbench를 이용하여 접속확인

Hostname에 public 주소를 입력하고 추가한 user와 비밀번호를 입력하고 test connection을 클릭!



==Mysql 사용
1. mysql 접속
-- $ sudo /usr/bin/mysql -u root -p
--  root로 사용

2. 사용자 정보 확인
mysql> SELECT User, Host, authentication_string FROM mysql.user;

3. TESTDB 라는 데이터 베이스 만들고 확인
# mysql 			            <----  0
mysql> CREATE DATABASE TESTDB;   <----   1
mysql> SHOW DATABASES;              <-----  2

4. TESTDB 데이터베이스를 사용할 계정 testuser 만들고 확인
mysql> CREATE USER 'st01'@'localhost' IDENTIFIED BY 'st01';
mysql> FLUSH PRIVILEGES;
mysql> SELECT User, Host, authentication_string FROM mysql.user;

5. TESTDB 데이터베이스를 사용할 계정 testuser 에 권한 부여
-- mysql> GRANT ALL PRIVILEGES ON my_newdb.st01;
         GRANT ALL PRIVILEGES ON my_newdb TO st01;
mysql> FLUSH PRIVILEGES;
mysql> SHOW GRANTS FOR'testuser'@'localhost';
mysql> SELECT User, Host, authentication_string FROM mysql.user;

Option 1. MySQL 버전 확인
mysql> show variables like "%version%";

Option 2. Mysql 비밀번호 변경 방법
mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('바꿀비번');
또는
-- mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '바꿀비번';

6. database 생성
1)database 생성                                    <------  3
	CREATE DATABASE my_newdb
	DEFAULT CHARACTER SET UTF8
	DEFAULT COLLATE utf8_general_ci;

2)database 연결
connect my_newdb;  
connect TESTDB;                                 <--------   4
show databases;

3) table 생성
                                                      <------------  5
CREATE TABLE `고객` (
`고객번호` varchar(16) NOT NULL,
`이름` varchar(50) NOT NULL,
`비밀번호` varchar(256) NOT NULL,
PRIMARY KEY (`고객번호`)
);
                                                     <----------------6        --desc 주문;      show tables;    show databases;  
CREATE TABLE `주문` (
`주문번호` varchar(16) NOT NULL,
`고객번호` varchar(16) NOT NULL,
`주문일` varchar(8) NOT NULL,
`주문가격` decimal(15,2) NOT NULL,
`배송도시` varchar(256),
`배송완료일` varchar(8),
`결제금액` varchar(8),
`할인금액` decimal(15,2) NOT NULL,
`적립포인트` decimal(15,2) NOT NULL,
PRIMARY KEY (`주문번호`),
FOREIGN KEY (`고객번호`) REFERENCES 고객 (`고객번호`)
);

4) insert table
INSERT INTO `고객` VALUES
('C0006', '홍길동', 'abcd1234'),
('C0007', '양바른', 'ybl1234'),
('C0008', '유코식', 'uu1234'),
('C0009', '김구', 'pass1234'),
('C0010', '신사임당', 'pass1234');


INSERT INTO `주문` (주문번호, 고객번호, 주문일, 주문가격, 할인금액, 적립포인트) VALUES
 ('O1001', 'C0001', '20211201', 10000, 100, 0),
 ('O1002', 'C0001', '20211203', 4500, 45, 0),
 ('O1003', 'C0004', '20211207', 100000, 1000, 0),
 ('O1004', 'C0003', '20211207', 55000, 550, 0),
 ('O1005', 'C0002', '20211217', 85000, 850, 0),
 ('O1006', 'C0002', '20211218', 23000, 230, 0),
 ('O1007', 'C0004', '20211221', 5000, 50, 0),
 ('O1008', 'C0001', '20211222', 8300, 83, 0),
 ('O1009', 'C0002', '20211225', 45000, 450, 0),
 ('O1010', 'C0003', '20211231', 9000, 90, 0);

ALTER TABLE `주문` CHANGE `배송도시` `배송도시코드` INT;

SELECT 고객.고객번호, 고객.이름, 주문.주문번호, 주문.주문일, 주문.주문가격
     FROM 고객, 주문
     WHERE 고객.고객번호 = 주문.고객번호;

SELECT 고객.이름,
(SELECT COUNT(1)
FROM 주문
WHERE 고객.고객번호 = 주문.고객번호) AS 주문횟수
FROM 고객;
```

```python
연결  mysql -u test4 -p     

mysql -r TESTDB4 -p  ?

# 한글 설정 (옵션)
SET FOREIGN_KEY_CHECKS = 0;
ALTER TABLE 테이블명 convert to charset utf8;

# 
이경희 test4 TESTDB4
```