# schoolfeed


## Site

Link: [https://schoolfeed.societyang.xyz](https://schoolfeed.societyang.xyz)

## Swagger

Link: [https://schoolfeed.societyang.xyz/swagger/](https://schoolfeed.societyang.xyz/swagger/)



###### Tools  
Docker(nginx & gunicorn), EC2, CloudFront, Route53  


## 작업 현황
Link: [https://trello.com/b/njERlYDN/schoolfeed](https://trello.com/b/njERlYDN/schoolfeed)

2019.5.1
Test Case 작성 : [https://github.com/LuceteYang/schoolfeed/commit/4f943b02f3d48a0247f5312d315947be630d3105](https://github.com/LuceteYang/schoolfeed/commit/4f943b02f3d48a0247f5312d315947be630d3105)



## Reference
#### Swagger Example 참고
https://django-rest-swagger.readthedocs.io/en/latest/

## 이슈 및 해결
1. test파일  TypeError: the JSON object must be str, not 'bytes'
https://stackoverflow.com/questions/42683478/typeerror-the-json-object-must-be-str-not-bytes/42683509
``` diff
-parseResponse = json.loads(response.content)
+parseResponse = json.loads(response.content.decode('utf-8'))
```
2. 로그인이나 에러메시지 커스텀 / naturaltime  
LANGUAGE_CODE 바꿔서 해결
https://stackoverflow.com/questions/9074957/django-localization-how-to-use-a-non-english-language-as-translate-from-langu
``` diff
-LANGUAGE_CODE = "en-us"
+LANGUAGE_CODE = "ko-kr"
```
3. 쿼리 로깅 확인

4. 쿼리셋 최적화 - 중복 DB쿼리 최소화 (select_related, prefetch_related, Django debug toolbar 활용)
https://wayhome25.github.io/django/2017/06/20/selected_related_prefetch_related/
https://wayhome25.github.io/django/2017/06/25/django-ajax-like-button/

5. 비밀번호 변경시 csrf에러
csrf 쿠키를 가져와서 Header로 전송하여 해결
https://docs.djangoproject.com/en/1.10/ref/csrf/#ajax