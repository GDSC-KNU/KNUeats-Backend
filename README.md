# KNUeats
### back-end API Docs
[notion] https://www.notion.so/API-Docs-3ffb1f32f7c641a58a42fdc3187c680d

### Schema
```json
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
### /eats
##POST
- 가게 등록

  https://knueat.herokuapp.com/

  **Responses**

  Code: 200 Successful Response

  **Request Parameters**

    ```json
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

##GET
- 음식 카테고리별 조회

  https://knueat.herokuapp.com/category/{category}

  ### Category : STRING

    - 한식, 분식, 양식, 일식, 카페/디저트, 중식, 아시안, 술집, 기타

  ### return type :

    ```json
    ex) https://knueat.herokuapp.com/category/중식
    [
        {
            "id": 40,
            "name": "케이푸드스토리",
            "description": "\n",
            "tel": "053-944-7853",
            "address": "대구광역시 북구 대현로9길 51-4 ",
            "lat": 35.888134,
            "lon": 128.6035,
            "location": "쪽문&서문",
            "category": "중식",
            "menu": null,
            "score": 0.0,
            "review": 0
        },
        {
            "id": 49,
            "name": "만리향",
            "description": "\n",
            "tel": "053-954-3453",
            "address": "대구광역시 북구 대학로 133 ",
            "lat": 35.896133,
            "lon": 128.61296,
            "location": "북문",
            "category": "중식",
            "menu": "중화비빔밥\n8,000원\n야끼우동\n8,000원\n얼큰이짬뽕\n9,000원\n1. 짜장면+탕수육+캔콜라\n13,500원",
            "score": 97.06,
            "review": 23
        }
    ]
    ```

- 가게 ID로 조회

  https://knueat.herokuapp.com/{id}

  ### return type :

    ```sql
    예) : [https://knueat.herokuapp.com](https://knueat.herokuapp.com/)/1
    {
        "name": "배스킨라빈스대구경대북문점",
        "description": "영업시간/매일 10:00 - 23:00\n",
        "tel": "053-944-4406",
        "address": "대구광역시 북구 대학로 83 ",
        "lat": 35.892834,
        "lon": 128.60918,
        "location": "북문",
        "menu": [
            {
                "id": 1,
                "restaurantId": 1,
                "name": "파인트",Strn
                "price": "8,900원"
            },
            {
                "id": 2,
                "restaurantId": 1,
                "name": "쿼터",
                "price": "17,000원"
            },
            {
                "id": 3,
                "restaurantId": 1,
                "name": "패밀리",
                "price": "24,000원"
            },
            {
                "id": 4,
                "restaurantId": 1,
                "name": "하프갤론",
                "price": "29,000원"
            }
        ],
        "category": "카페/디저트",
        "score": 4144.9,
        "review": 905
    }
    ```

- 메뉴, 가게 이름 검색으로 조회(like)

  https://knueat.herokuapp.com/search?word=value

  **Request Parameters : word=value**

  ### return type :

    ```sql
    ex} https://knueat.herokuapp.com/search/?word=떡볶이
    [
            {
            "id": 19,
            "name": "북문골목떡볶이",
            "description": "평일 10:30 - 24:00\n",
            "tel": "053-941-7707",
            "address": "대구광역시 북구 대학로 91-2",
            "lat": 35.893433,
            "lon": 128.60977,
            "location": "북문",
            "category": "분식",
            "menu": "치즈떡볶이\n사진\n대표\n5,000원\n순대\n3,500원\n떢볶이\n3,000원\n쌀떡볶이\n3,000원",
            "score": 345.6,
            "review": 80
        },
        {
            "id": 27,
            "name": "착한떡볶이",
            "description": "\n",
            "tel": "",
            "address": "대구광역시 북구 경대로7길 13",
            "lat": 35.885082,
            "lon": 128.61224,
            "location": "쪽문&서문",
            "category": "분식",
            "menu": null,
            "score": 0.0,
            "review": 4
        },
        {
            "id": 30,
            "name": "선택떡볶이",
            "description": "\n",
            "tel": "053-214-2018",
            "address": "대구광역시 북구 경대로 97",
            "lat": 35.889366,
            "lon": 128.61732,
            "location": "동문",
            "category": "분식",
            "menu": "반반떡볶이(11가지 맛 중 2가지 맛 선택)(1~2인분)\n6,900원\n1인분떡볶이(1인분)\n4,000원\n치즈로제떡볶이(한통가득3~4인분(2L용기))\n16,000원\n반반떡볶이(11가지 맛 중 2가지 맛 선택)(1~2인분)\n6,900원",
            "score": 0.0,
            "review": 17
        }
    ]
    ```

- 학교 문 별 조회

  https://knueat.herokuapp.com/location/{location}

  ### {location} : STRING

    - 북문/동문/쪽문/서문

  ### return type :
```json
ex) https://knueat.herokuapp.com/eats/location/북문

[
    {
        "id": 1,
        "name": "배스킨라빈스대구경대북문점",
        "description": "영업시간/매일 10:00 - 23:00\n",
        "tel": "053-944-4406",
        "address": "대구광역시 북구 대학로 83 ",
        "lat": 35.892834,
        "lon": 128.60918,
        "location": "북문",
        "menu": "파인트\n8,900원\n주문수 2\n쿼터\n17,000원\n패밀리\n24,000원\n하프갤론\n29,000원",
        "category": "카페/디저트",
        "score": 4144.9,
        "review": 905
    },
    {
        "id": 3,
        "name": "마사",
        "description": "가게에 대한 상세정보가 없습니다.",
        "tel": "053-247-6678",
        "address": "대구 북구 산격로 6길 18",
        "lat": 35.892433,
        "lon": 128.60718,
        "location": "북문",
        "menu": "새우초밥\n12,000원\n마사모듬\n12,000원\n연어초밥\n14,000원\n연어+광어초밥\n14,000원",
        "category": "일식",
        "score": 3582.08,
        "review": 772
    },
...
]
]
```