### 개념
    * REST (Representational State Transfer)   
        - 클라이언트 ↔ 서버의 통신방식   
        - URI와 HTTP를 이용한, 통신 목적의 아키텍처 스타일(유형)   
            +) URI(Uniform Resource Identifier)    
                : 문서, 그림, 영상 등의 자원 식별용 이름(경로)    
            +) 아키텍처 스타일 : 아키텍처(구조)의 종류(유형, 스타일, 타입)
                ex) 클라이언트/서버,  저장소,  파이프/필터,   REST
        - REST는 아키텍처 제작 시 사용되는 가이드 정도의 의미로 사용되며 명확히 준수해야할 표준은 없다

    * RESTful
        - REST가 적용된 시스템

    * REST API
        - REST가 적용된 API

    * RESTful
        - REST API를 제공하는 시스템


### REST의 6가지 조건
    * REST는 6가지 조건을 만족해야 함
        1. 일관된 인터페이스
            - URI 사용, HTTP 메소드 사용, RPC 미호출 등의 `지정된 인터페이스`를 준수
        2. 클라이언트/서버 (Client-Server)
            - 클라이언트는 서버에 `요청(request) 메세지`를 전송하고
            - 서버는 요청에 대한 `응답(response) 메세지`를 전송한다
        3. 비연결성(Statelessness)
            - 세션 등 `이전 상황(문맥)` 없이도 통신할 수 있다
        4. 캐시 가능 (Cacheable)
            - 서버의 응답 메세지는 `캐싱(저장 후 재사용)`될 수 있다.
        5. 계층화된 시스템 (Layered system)
            - 계층별로 기능이 분리된다.
            - 그러므로 중간 계층의 기능(로드 밸런싱, 서버증설, 인증 스스템 도입 등)이 변경되어도 통신에 영향을 주지 않는다.
        6. 주문형 코드(code on demand) (선택)
            - 손쉬운 데이터 처리를 위해 서버는 클라이언트에서 실행될 스크립트를 전송할 수 있다.


### REST API 만들기
    * API는 기본적인 CRUD를 위해 사용됨
    * API가 필요한 URL을 만들 때 
        - 표준을 만드는 것이 중요!!! (명확한 패턴)
        - URL에서는 동사를 사용하지 않는다. (명사만 사용)
        - 동사를 쓰는 대신에 HTTP methods를 사용하여 인터랙션 
            - HTTP methods : GET(읽기), POST(생성), PUT(업데이트), DELETE(삭제)
        - **`HTTP methods + 명사`** 방식을 사용 