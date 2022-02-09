```
# putty open한 후 login
lab24  # Terminal 접속 ID(Putty)

conda info --envs   # 가상환경 목록 검색
conda activate python3  #  가상환경 python3으로 실행

# putty에서 jupyter notebook사용을 위한 명령어 
nohup jupyter-notebook --ip=0.0.0.0 --no-browser --port=8924 &  # --port=포트번호  → 포트번호는 본인이 부여받은 port번호 사용

# 웹 브라우저에서 jupyter notebook 실행
http://18.182.177.124:8924/

# password
# multi1234!  로 jupyter notebook 로그인
```
# ----------------------------------------------------
```
# jupyter notebook에서 가상 환경 생성 방법
# New > Terminal  

# python version 확인
python --version   # 3.8.0

# 가상환경 생성  → 이미 생성시 안해도 됨
conda create -n GH python=3.8.0 jupyter tenserflow 
# Proceed ([y]/n) ? 나오면 y
```
```
# 데이터 처리를 위한 Spark 사용
## **1. scala**
# 스파크 설치위치  → Spark_Home = /opt/spark
cd /opt/spark/
# spark-shell 실행 명령어
./bin/spark-shell

# **2. pyspark 실행** 
# pyspark 실행 명령어
pyspark
```