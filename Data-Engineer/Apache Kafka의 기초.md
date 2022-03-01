## Apache Kafka
- Source Application과 Target Application의 커플링을 약하게 하기 위해 나옴
- 카프카는 아주 유연한 큐 역할을 함
- 데이터의 흐름에 있어서 Kafka는 fault tolerant 즉, 고가용성으로 서버가 이슈가 생기거나, 랙(전원)이 내려간다던가 하는 상황에서도 데이터를 손실없이 복구 가능
- 낮은 지연과 높은 처리량을 통해서 아주 효과적으로 데이터를 매우 많이 처리할 수 있음

--------------------------------------------------------------------------------

## Kafka Topic
: Kafka에는 다양한 데이터가 들어갈 수 있는데 그 데이터가 들어갈 수 있는 공간을 **`토픽`**이라고 함
- Kafka에서는 여러 개의 토픽 생성 가능
- DB의 `table`이나 filesystem의 `폴더`와 유사한 성질을 가짐
- 프로듀서는 토픽에 데이터를 넣을 수 있고, Consumer는 데이터를 가져가게 됨
- 토픽은 목적에 따라 `클릭로그, send sms, location log 등`과 같이 무슨 이름을 지정해주는 것이 가능하며, 데이터를 담는지에 대해 명확히 명시함에 따라 유지보수 시 편리하게 관리가 가능함

### Kafka Topic 내부
- 하나의 토픽은 여러 개의 partition으로 구성될 수 있음
- 첫번쨰 partition 번호는 0번부터 시작하며, 하나의 partition은 큐와 같이 내부에 데이터가 partition 끝에서부터 쌓이게 되고, 해당 토픽에 카프카 Consumer가 붙게 되면 데이터를 가장 오래된 순서대로 가져가게 되고 더이상 데이터가 들어오지 않으면 Consumer는 또 다른 데이터가 들어올 때까지 기다림

> * **partition이 하나인 경우**
  - Consumer가 토픽 내부의 partition에서 record(데이터)들을 가져가도 데이터는 삭제되지 않고 partition에 그대로 남음
  - 만약 새로운 Consumer가 붙을 시 다시 0번부터 가져가서 사용이 가능함 **<< 이때, Consumer그룹이 달라야하며, auto.offset.reset = earliest 로 세팅되어 있어야 함 >>**
  - 이처럼 사용할 경우 동일 데이터에 대해서 두번 처리가 가능한데 이는 Kafka를 사용하는 중요한 이유이기도 하다.

> * **partition이 두개 이상인 경우**
  - 프로듀서가 데이터를 보낼 떄 키를 지정할 수 있음
    - 만약 키가 Null 즉, 키를 지정하지 않고 기본 파티셔너 설정을 사용하는 경우 RR(Round Robin)으로 partition이 지정됨
    - 반면 키가 있고, 기본 파티셔너를 사용할 경우, 키의 해시(hash)값을 구하고, 특정 partition에 할당됨
  - **!! partition은 다시 줄일 수 없기 때문에 partition을 늘리는 것은 매우 조심해야함 !!**
     - partition을 늘리는 이유 : partition을 늘리면 Counsumer의 개수를 늘려서 데이터 처리를 분산시킬 수 있음
  - 데이터가 늘어나면 언제 삭제가 될까??
    - 삭제되는 타이밍은 옵션에 따라 다르다. 
      1. 레코드가 저장되는 최대 시간과 크기 지정 가능
        - 일정한 기간 혹은 용량동안 데이터를 저장할 수 있게 되며, 적절하게 데이터가 삭제될 수 있도록 설정 가능

--------------------------------------------------------------------------------

## Kafka의 핵심요소 - broker, replication, ISR
: 이들은 Kafka 운영에 있어서 매우 중요한 역할을 함

1. broker
: Kafka가 설치되어 있는 서버 단위
  - 보통 3개 이상의 broker로 구성하여 사용하는 것을 권장
  - partition이 1개, replicatin이 1인 topic이 존재하고 broker가 3대라면, broker 3대 중 1대에 해당 topic의 정보(데이터)가 저장됨


2. replication (복제)
: replication은 partition의 복제를 뜻함
  - 복제는 Kafka 아키텍쳐의 핵심

  - 만약 replication이 1이라면 partition이 1개만 존재한다는 것이고, replication이 3라면 partition은 원본(Leader partition) 1개와 복제본(Follower partition) 2개로 총 3개가 존재한다는 뜻이다
    - 다만 broker개수에 따라서 replication 개수가 제한됨 **(broker 개수가 3이면 replication은 4가 될 수 없음)**

  - 사용 목적 : 클러스터에서 서버에 장애가 생길 때 Kafka의 가용성을 보장하는 가장 좋은 방법 (고가용성을 위해 사용됨)
    - 만약 broker가 3개인 Kafka에서 replication이 1이고 partition이 1인 topic이
존재하는 경우, 갑자기 broker가 사용이 불가하게 되면 더 이상 해당 partition은 복구가 불가능하다.
    - 하지만 replication이 2인 경우, broker 1개가 죽더라고 복제본(Follower partition)이 존재하므로 복제본은 복구가 가능하며, 나머지 1개가 남은 Follower partition이 Leader partition 역할을 승계하게 됨

  - replication 개수가 많아지면 broker의 리소스 사용량도 늘어나게 됨. 따라서 Kafka에 들어오는 데이터 양과 retention date(저장시간)을 잘 생각해서 replication 개수를 정하는 것이 좋음
    - 3개 이상의 broker를 사용할 때 replication은 3을 추천

3. ISR (In Sync Replica)
: `Leader partition(원본 partition)과 Follower partition(복제본 partition)을 합친 것`을 `ISR`이라고 함

* Leader partition & Follower partition의 역할
- 프로듀서는 topic의 partitino에 데이터를 전달함
  1. Leader partition
  : 프로듀서가 topic의 partition에 데이터를 전달할 때 전달받는 주체 
    - 프로듀서에는 `ack라는 상세옵션`이 있으며, 이를 통해 `고가용성을 유지`할 수 있음 (이 옵션은 partition의 replication과 관련있음)
    - ack는 0, 1, all 옵션 3개 중 하나를 골라 사용 가능
      - 0인 경우,  Leader partition에 데이터를 전송하고 응답값은 받지 않음
        - 때문에 Leader partition에 데이터가 정상적으로 전송됐는지 나머지 partition에 정상적으로 복제되었는지 알 수 없고 보장도 불가능
        - 속도는 빠르지만 데이터 유실 가능성 있음
      - 1인 경우, Leader partition에 데이터를 전송하고 Leader partition이 데이터를 정상적으로 받았는지 응답값을 받음, But 나머지 partition에 복제되었는지는 알 수 없음
        - 만약 Leader partition이 데이터를 받은 즉시 broker에 장애가 난다면 나머지 partition에 데이터가 미처 전송되지 못한 상태이므로 ack 0 옵션과 같이 데이터 유실 가능성이 있음
      - all인 경우, Leader partition에 데이터를 보낸 후 Follower partition에도 데이터가 저장되는 것을 확인하는 절차를 거침
        - ack all옵션을 사용할 경우 데이터 유실은 없지만 0,1에 비해 확인하는 부분이 많기 때문에 속도가 현저히 느림

--------------------------------------------------------------------------------

프로듀서가 데이터를 보내면 무조건 파티셔너를 통해서 broker로 전송됨

## 프로듀서의 파티셔너
: 파티셔너는 데이터를 토픽의 어떤 파티션에 넣을지 결정하는 역할을 함

- 레코드에 포함된 메시지 키 또는 메시지 값에 따라서 파티션의 위치가 결정됨 
  - 프로듀서를 사용할 때 파티셔너를 따로 설정하지 않는다면 `UniformStickyPartitiner`로 설정이 됨
    - 이 파티셔너는 메시지 키가 있을 때 없을 때 다르게 동작하게 됨
    1. 메시지 키가 있는 경우
      - 파티셔너에 의해서 특정한 해쉬값이 생성되는데, 이를 기준으로 어느 partition으로 들어갈지 정해지게 됨
      - 토픽에 파티션이 2개 있는 경우, 동일한 메시지 키를 가진 레코드는 동일한 해쉬값을 만들기 때문에 항상 동일한 파티션에 들어감을 보장함. 때문에 순서를 지켜서 데이터를 처리할 수 있음 **(partition 한개의 내부에서는 Queue처럼 동작하기 때문)**
    2. 메시지 키가 없는 경우 
      - RR(Round Robin)으로 partition에 들어가게 되며, 전통적인 RR과는 약간 다르게 동작함
      - UniformStickyPartitiner는 프로듀서에서 배치로 모을 수 있는 최대한의 레코드들을 모아서 partition으로 데이터를 보내게 되며, 배치단위로 데이터를 보낼 때 partition의 RR방식으로 돌아가면서 데이터를 넣게 됨    
      → 즉, 메시지 키가 없는 레코드들은 파티션에 적절히 분배됨


* Kafka에서는 직접 파티셔너를 만들 수 있도록 Partitioner interface 제공
  - 기본 파티셔너가 아닌 직접 개발한 파티셔너도 프로듀서에서 설정 가능 
  - partitioner interface를 이용하여 커스텀 파티셔너 클래스를 만들면 메시지 키 또는 메시지 값 또는 토픽 이름에 따라서 어느 파티션에 데이터를 보낼 것인지 정할 수 있다.
  - ex) VIP고객을 위해 VIP고객의 데이터를 조금 더 빠른 처리를 하고자 하는 경우
    - 기본적으로 10개의 파티션이 있다고 가정할 때 커스텀 파티셔너를 만들어 8개 파티션에는 VIP고객의 데이터 , 2개는 일반 고객의 데이터를 넣어 개발가능
   

--------------------------------------------------------------------------------

## Kafka Consumer lag
: Kafka를 운영함에 있어서 매우 중요한 모니터링 지표 중 하나로, **`토픽의 가장 최신 offset과 Consumer offset간의 차이`**이다 
- 프로듀서가 데이터를 넣어주는 속도가 컨슈머가 데이터를 가져가는 속도보다 빠르게 되면 **`프로듀서가 넣은 데이터의 offset`과 `컨슈머가 가져간 데이터의 offset`간의 차이가 발생하게 되는데 이를 `Consumer lag`**이라고 함
- lag은 적을수도 많을수도 있으며, lag의 숫자를 통해 현재 해당 토픽에 대해 파이프라인으로 연계되어있는 프로듀서와 컨슈머의 상태에 대해 유추가 가능
  - 주로 Consumer의 상태에 대해 볼 때 사용
- lag은 각 파티션의 offset 기준으로 프로듀서가 넣은 데이터의 offset과 컨슈머가 가져가는 데이터의 offset의 차이를 기반으로 함
  - 때문에 토픽에 여러 partition이 존재할 경우 **lag은 여러 개가 존재할 수 있음**
- 한개의 토픽과 Consumer 그룹에 대해 lag이 여러 개 존재할 수 있을 때, 그 중 높은 숫자의 lag을 `records-lag-max`라고 부름

--------------------------------------------------------------------------------

* Kafka-client 라이브러리를 사용해서 Java 또는 scala와 같은 언어를 통해 KafkaConsumer를 구현할 수 있음
  - 이때 구현한 KafkaConsumer 객체를 통해 현재 lag 정보를 가져올 수 있음
    - lag을 실시간으로 모니터링 하고 싶다면 데이터를 Elasticsearch나 InfluxDB와 같은 저장소에 넣은 뒤, Grafana 대시보드를 통해 확인할 수도 있음 
    - 하지만, Consumer 단위에서 lag을 모니터링하는 것은 매우 위험하고 운영요소가 많이 들어감
      - Consumer 로직단에서 lag을 수집하는 것은 Consumer 상태에 디펜던시가 걸리기 때문
      - Consumer가 비정상적으로 종료되게 되면 더 이상 컨슈머는 lag 정보를 보낼 수 없기 떄문에 lag 측정 불가능 
      - 추가적으로 Consumer가 개발될 때마다 해당 Consumer에 lag 정보를 특정 저장소에 저장할 수 있도록 로직을 개발해야 함
      - 만약 Consumer lag을 수집할 수 없는 Consumer라면 lag을 모니터링 할 수 없으므로 운영이 매우 까다로워지게 됨
    - **위와 같은 이유들로 linkedin에서는 Apache Kafka와 함께 Kafka Consumer lag을 효과적으로 모니터링 할 수 있도록 Burrow를 만듦**
      - Burrow는 오픈소스로서 Golang으로 작성되었고 GitHub에 올라가있음 (지속적으로 관리되고 있음)

## Burrow → Kafka Consumer Lag 모니터링 필수요소
: Burrow는 Consumer lag 모니터링을 도와주는 독립적인 Application 

* Burrow의 3가지 특징
  1. 멀티 카프카 클러스터 지원    
    - 카프카 클러스터가 여러 개더라도 Burrow application 1개만 실행해서 연동한다면 카프카 클러스터들에 붙은 컨슈머의 lag을 모두 모니터링할 수 있음
  2. Sliding window를 통한 Consumer의 status 확인   
    - Burrow에는 sliding window를 통해서 Consumer의 status를 'ERROR', 'WARNING', 'OK'로 표현할 수 있도록 함
      - 데이터 양이 일시적으로 많아지면서 consumer offset이 증가되고 있으면 'WARNING'으로 정의
      - 데이터 양이 많아지는데 consumer가 데이터를 가져가지 않으면 'ERROR'로 정의하여 실제로 Consuner가 문제가 있는지 여부를 알 수 있음
    - 이렇게 status를 기반으로 효과적인 운영에 참고할 수 있음

  3. HTTP api제공   
    - 위와 같은 정보들을 Burrow가 정의한 HTTP api를 통해 조회할 수 있게 하였음
    - HTTP api를 호출하여 response받은 데이터를 시계열 DB와 같은 곳에 저장하는 application을 만들어서 활용 가능


--------------------------------------------------------------------------------

## Kafka, rabbitMQ, redis queue 플랫폼들의 차이점
**메시징 플랫폼은 두 가지로 나뉜다**
  1. **메시지 브로커**
    - 메시지 브로커는 이벤트 브로커 역할을 할 수 없음
    - 많은 대기업들에서 대규모 메시지 기반 미들웨어 아키텍처에서 사용되어 왔다
      - 미들웨어 : 서비스하는 애플리케이션들을 보다 효율적으로 아키텍처들을 연결하는 요소들로 작동하는 소프트웨어 
      - ex) 메시징 플랫폼, 인증 플랫폼, 데이터베이스 등이 미들웨어
      - 메시지 브로커에 있는 큐에 데이터를 보내고 받는 프로듀서와 Consumer를 통해 메시지를 통신하고 네트워크를 맺는 용도로 사용해왔음
    - **메시지 브로커의 특징**
      1. 메시지를 받아서 적절히 처리하고나면 즉시 또는 짧은 시간 내에 삭제되는 구조     
        **→ 메시지 브로커는 데이터를 보내고, 처리하고 삭제함**
    - ex) redis queue, rabbitMQ
        
    

  2. **이벤트 브로커**
    - 이벤트 브로커는 메시지 브로커 역할을 할 수 있음
    - 이벤트 브로커는 서비스에서 나오는 이벤트를 마치 DB에 저장하듯이 이벤트 브로커의 큐에 저장하는데 이렇게함으로서 얻는 이점이 있음
      1. 딱 한 번 일어난 이벤트 데이터를 브로커에 저장하므로서 단일 진실 공급원으로 사용할 수 있고
      2. 장애가 발생했을 때 장애가 일어난 지점부터 재처리할 수 있음
      3. 많은 양의 실시간 스트림 데이터를 효과적으로 처리할 수 있음 
    - 이벤트 브로커의 특징
      1.  이벤트 또는 메시지라고도 불리는 이 레코드 이 장부를 딱 하나만 보관하고 인덱스를 통해 개별 엑세스를 관리함
      2. 업무상 필요한 시간동안 이벤트를 보존할 수 있음
    - ex) Kafka, AWS의 키네시스
    - 이벤트 브로커로 클러스터를 구축하면 이벤트 기반 마이크로 서비스 아키텍처로 발전하는데 중요한 역할을 하며 메시지 브로커로서도 사용할 수 있음

