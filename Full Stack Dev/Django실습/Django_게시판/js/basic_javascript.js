// javascript의 한 줄 주석
/*
    멀티라인 주석
    여러 줄 가능
*/

// javascript는 변수의 정의와 선언이 따로 있다.

// 변수의 선언
var var1;  // var 키워드는 잘 쓰이지 않으며, 사용하지 않는 것이 좋다
let var2;

// 변수의 정의
var2 = 10;
console.log(var2);

// 자료의 타입
console.log(typeof 10);    // 정수 실수 상관없이
console.log(typeof 10.0);  // number 타입
console.log(typeof 'hello');  // 문자열(string) 타입
console.log(typeof true);    // boolean 타입

// python에서 없는 타입
console.log(typeof null);       // object 타입
console.log(typeof undefined);   // undefined 타입
console.log(typeof NaN);       //   -  number 타입
console.log(typeof Infinity);  // 무한 - number 타입

// 연산자
// javascript에서는 몫 연산은 없음
console.log( 2 + 3 );
console.log( 2 - 3 );
console.log( 2 * 3 );
console.log( 2 / 3 );
console.log( 2 % 3 );
console.log( 2 ** 3 );

// 소수점 버리고 정수형만 가져가는 법 - pasrseInt
console.log( parseInt(1234.123) );

// python에 없는 연산자
// 증감연산자
let number = 2;
console.log( ++number );
console.log( --number );

// 비교연산자
// javascript는 비교할 때 타입은 고려하지 않는다.
console.log( 1 == '1' );

// 타입까지 고려하려면 === 를 쓰면 된다.
console.log( 1 === '1' );

// 논리 연산자
// &&(and), ||(or), !(not)
console.log( true && false );
console.log( true || false );
console.log( !true );

// 윤년 구하기
let year = 2000;
if ( (year %4 == 0 ) && (year % 100 != 0) || (year % 400 == 0)){
    console.log( year, '년은 윤년입니다.' )}
else { 
    console.log( year, '년은 평년입니다');}

// 추가적으로 switch-case문이 존재
// 하지만 현대 프로그래밍에서는 거의 안 쓰는 추세


// 배열과 반복
// javascript에서의 배열 = python의 리스트
// 슬라이스나 음수 인데스는 사용하지 x

// let array = [] ; // 빈 배열 객체
// let array = Array();   // Array() 클래스의 생성자를 이용하여 객체 생성

let array = new Array();  // new 연산자를 이용한 Array 객체 생성

array = [1,2,3,4];
console.log( array );
console.log( array[0] );  

// python의 append와 같은 역할으로 "push" 사용
array.push(999);
console.log( array );
console.log( array[4] );

// javascript는 배열을 파이썬의 dict처럼 사용할 수 있다.
// 연관배열이라고 표현
// python의 dict처럼 map타입을 지정 가능....?

let arr = [];
arr['first'] = 10;
console.log( arr );

// for, while, for each
// 파이썬의 for와는 완전 다른 문법 / while의 또 다른 표현이라고 할 수 있음

// 1부터 10까지 반복 - while 사용
let i = 1;
while(i <= 10 ) {
    console.log( i );
    i++;
}

// 1부터 10까지 반복 - for 사용 [초기값; 조건; 증감]  → 을 한줄에 사용
for (let j = 1; j <= 10; j++) {
    console.log( j );
}

// python의 for loop와 동일한 동작을 하는 for each
console.log( array );
for (let x of array){
    console.log( x );
}

// 1부터 n까지 합 구하기
let n = 20;
let total = 0;
for(let i = 1; i <= n; i++){
    total += i
}
console.log( total );

// javascript 함수의 기능은 동일하다
// javascript는 'function' 키워드로 함수를 정ㅇ의

function func(a,b){
    return a+ b;
}

console.log( func(3,5) );

// 가변인자
function add() {
    // 가변인자 객체가 따로 존재
    console.log( arguments );
}

ret = add(1,2,3,4);
console.log (ret);

// 지역변수, 전역변수
let mem = 10;
function func1() {
    let mem = 20;
}
func1();
console.log( mem );

// 디폴트 파라미터
function func2(a, b = 2) {
    console.log(a, b);
}

func2();

// javascript의 class

class Person {
    // 클래스 변수 아님
    // 필드선언을 통해 (public 또는 private(#))
    #name;  // 속성 앞에 #를 붙여서 private선언 - 은닉성 지원
    age;

    // python의 클래스 변수와 같은 기능
    static nation = 'korea'

    // 생성자
    constructor(name, age) {
        // this는 python의 self와 같은 역할
        // 따로 파라미터로 정의하지 않아도 항상 정의되어 있다.
        this.#name = name;
        this.age = age;
    };

    // 정적 메소드
    static staticMethod() {
        console.log( Person.nation );
    }

    //getter
    get name() {
        this.#name;
    }

    //setter
    set name(name) {
        this.#name = name;
    }

    // class 내에서 메소드를 정의할 때는 'function' 키워드는 생략
    info() {
        console.log( this.#name, this.age );
    } 
}

// 객체 생성
object = new Person('장동건',22);
object.info();

// 은닉성
// 외부에서는 접근 불가능
//object.#name = '원빈';
//object.info();


// 정적 변수(static) 변수는 클래스 이름으로 접근 가능
console.log( Person.nation );

// getter와 setter를 사용하는 방법은 python과 동일
object.name = '원빈'
console.log( object.name );
object.info();