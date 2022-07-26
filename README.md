# KNUeats
#### 경북대 주변에 있는 맛집을 알려주는 어플 서비스 입니다.
## Member 
| [<img src="https://avatars.githubusercontent.com/u/63745627?v=4" width="100px">](https://github.com/kasterra) | [<img src="https://github.com/JangYunSeong.png" width="100px">](https://github.com/JangYunSeong) |
| :--------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------: |
|                          [오영선](https://github.com/oyoungsun)                           |                            [장윤성](https://github.com/JangYunSeong)                             |
## Stack
<img src="https://img.shields.io/badge/java-007396?style=for-the-badge&logo=java&logoColor=white"> <img src="https://img.shields.io/badge/spring-6DB33F?style=for-the-badge&logo=spring&logoColor=white">
<img src="https://img.shields.io/badge/springboot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">
<img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white">


## API Docs

### Schema
```
restaurant(1)
{
	id : INT(primary key,not null,auto increment)
	name : VARCHAR(not null)
	description : VARCHAR
	tel : VARCHAR
	address : VARCHAR(not null)
	lat : VARCHAR(not null)
	lon : VARCHAR(not null)
	category : VARCHAR(not null)
	location : VARCHAR(null) 
	menu : VARCHAR(null) // 임시 저장
	score : FLOAT(0.0)
	review : INT(0)
}

menu(N)
{
	id : INT(not null,auto increment)
	restaurant_id : INT(foreign key-id)
	name : VARCHAR(not null)
	price : VARCHAR(not null) // ex) "12,000원"
}
```
## POST
### 가게 등록
  **Request Parameters**

    ```
    { // restaurant
    	name : String,
    	description : String,  //null 가능
    	tel : String, //null 가능
    	address : String , //null 가능
            menu : Menu[],
    	category : String, // tag enum
    }	
    
    사용 예
    request type : 
    {
     	"name": "찜닭집",
    	"description": "설명",
      	"tel": "053-666-6666",
    	"address" : "대구 북구 산격로 80",
      	"menu": [
    		    {
    			"name":"찜닭",
    			"price":"15,000원"	
    		    }
    		],
      	"category" : "한식",
      	"location" : "북문" // 북문/동문/쪽문&서문
    }
    ```
    **Responses**

    Code: 200 Successful Response
    
### 가게 리뷰 등록

  https://knueat.herokuapp.com/{id}/score
  
  **Request Parameters**
  ```
  {
  	"score" : float(0~5)
  }
  ```
  **response**
  Code: 200 Successful Response

## GET
### 음식 카테고리별 조회

  https://knueat.herokuapp.com/category/{category}

  ### Category : STRING

    - 한식, 분식, 양식, 일식, 카페/디저트, 중식, 아시안, 술집, 기타

  ### return type :

    ```
    ex) https://knueat.herokuapp.com/category/중식
    [
        {
            "id": -,
            "name": "케이푸드스토리",
            "description": "\n",
            "tel": "000-000-0000",
            "address": "-",
            "lat": -,
            "lon": -,
            "location": "쪽문&서문",
            "category": "중식",
            "menu": null,
            "score": 0.0,
            "review": 0
        },
        {
            "id": -,
            "name": "만리향",
            "description": "\n",
            "tel": "000-000-0000",
            "address": "-",
            "lat": -,
            "lon": -,
            "location": "쪽문&서문",
            "category": "중식",
            "menu": null,
            "score": 97.06,
            "review": 23
        }
    ]
    ```

### 가게 ID로 조회

  https://knueat.herokuapp.com/{id}

  ### return type :

    ```
    예) : [https://knueat.herokuapp.com](https://knueat.herokuapp.com/)/{id}
    {	
    	"id": -,
        "name": "배스킨라빈스대구경대북문점",
        "description": "영업시간/매일 10:00 - 23:00\n",
        "tel": "-",
        "address": "-,
        "lat": 35.892834,
        "lon": 128.60918,
        "location": "북문",
        "menu": [
            {
                "id": -,
                "restaurantId": -,
                "name": "파인트",Strn
                "price": "8,900원"
            },
            {
                "id": -,
                "restaurantId": -,
                "name": "쿼터",
                "price": "17,000원"
            },
            {
                "id": -,
                "restaurantId": -,
                "name": "패밀리",
                "price": "24,000원"
            },
            {
                "id": -,
                "restaurantId": -,
                "name": "하프갤론",
                "price": "29,000원"
            }
        ],
        "category": "카페/디저트",
        "score": 4144.9,
        "review": 905
    }
    ```

### 메뉴, 가게 이름 검색으로 조회(like)

  https://knueat.herokuapp.com/search?word=value

  **Request Parameters : word=value**

  ### return type :

    ```
    ex} https://knueat.herokuapp.com/search?word=떡볶이
    [
            {
            "id": -,
            "name": "북문골목떡볶이",
            "description": "평일 10:30 - 24:00\n",
            "tel": "-",
            "address": "-",
            "lat": 35.893433,
            "lon": 128.60977,
            "location": "북문",
            "category": "분식",
            "score": 345.6,
            "review": 80
        },
        {
            "id": -,
            "name": "착한떡볶이",
            "description": "\n",
            "tel": "-",
            "address": "-",
            "lat": -,
            "lon": -,
            "location": "쪽문&서문",
            "category": "분식",
            "score": 0.0,
            "review": 4
        },
        {
            "id": -,
            "name": "선택떡볶이",
            "description": "\n",
            "tel": "-",
            "address": "-",
            "lat": -,
            "lon": -,
            "location": "동문",
            "category": "분식",
            "score": 0.0,
            "review": 17
        }
    ]
    ```

### 학교 문 별 조회

  https://knueat.herokuapp.com/location/{location}

  ### {location} : STRING

    - 북문/동문/쪽문/서문

  ### return type :
	```
	ex) https://knueat.herokuapp.com/eats/location/북문

	[
	    {
		"id": -,
		"name": "배스킨라빈스대구경대북문점",
		"description": "영업시간/매일 10:00 - 23:00\n",
		"tel": "-",
            	"address": "-",
            	"lat": -,
            	"lon": -,
		"location": "북문",
		"category": "카페/디저트",
		"score": 4144.9,
		"review": 905
	    },
	    {
		"id": -,
		"name": "마사",
		"description": "가게에 대한 상세정보가 없습니다.",
		"tel": "-",
            	"address": "-",
            	"lat": -,
            	"lon": -,
		"location": "북문",
		"category": "일식",
		"score": 3582.08,
		"review": 772
	    },
	...
	]
	```
