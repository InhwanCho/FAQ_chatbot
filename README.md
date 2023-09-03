# FAQ_chatbot(Streamlit & Slack version)


## Streamlit version 실행 방법

1. 환경 설정
```python
pip install -r requirements.txt
```
2. API KEY 설정

  .env 파일을 설정하거나
  os.environ으로 설정해주세요

3. 실행
```
streamlit run main.py
```

### 사용 방법
```
👻 사용 방법  👻 :
1. 아래 "질문하기"에 질문을 입력하세요.
2. FAQ에 대해 질문 하려면 "FAQ 질문"을 눌러주세요.
3. 질문을 구글링하려면 "구글링 하기"를 눌러주세요.
```

## 실행

실행 화면





## Slack version 실행 방법

1. 환경 설정

2. API KEY 설정

3. 실행
```
python slack.py
```
4. 슬랙 실행 후 워크스페이스의 채널 확인


## 슬랙(Slack) 상세 설정

- 슬랙은 csv, json파일을 'vector'로 만들어서 코사인 유사도를 이용하여 출력하는 형태의 `vectordb`를 이용하였습니다.

1. 슬랙에 로그인하여 워크스패이스를 만들기

2. [슬랙 api 홈페이지](https://api.slack.com/ "슬랙") 들어가기
   
2. 로그인 후 우측 상단의 `Your APPs` -> `Mange Your APPs` -> `Create APP`

3. 앱을 생성 하고 `OAuth & Permissions` 에서 아래와 같이 설정
   
<img width="500" alt="슬랙(Slack) 설정" src="https://github.com/InhwanCho/FAQ_chatbot/assets/111936229/61bf6eee-c06e-4b2c-ad74-aa7758737d26">

4. `Basic Information`에서 `App-Level Tokens` -> `Generate Token and Scopes`에서 아래와 같이 설정(`SLACK_APP_TOKEN` - 지금 저장하기 않아도 됨)
<img width="500" alt="슬랙 설정" src="https://github.com/InhwanCho/FAQ_chatbot/assets/111936229/3b8049c7-d108-4667-b385-f1dee88ea355">

5. `Socket Mode`에 들어가서 `enable socket mode`
<img width="500" alt="소켓모드 활성화" src="https://github.com/InhwanCho/FAQ_chatbot/assets/111936229/e993a9b7-de0c-450e-9daf-f32a064b0381">

6. `Event Subscriptions`에 들어가서 `enable events`

7. `Subscribe to bot events`을 열어서 아래와 같이 설정 후 `save changes` 누르기
<img width="500" alt="이벤트 추가" src="https://github.com/InhwanCho/FAQ_chatbot/assets/111936229/24a5a034-f6c7-48cb-b340-4e5cd8405759">

8. `Basic Information` -> `Install to Workspace` -> `# 채널명` 설정

9. slack.py의 토큰을 다음과 같이 설정 후 `python slack.py`
```
[Basic Information -> Signing Secret]   == SLACK_SIGNING_SECRET 
[Basic Information -> App-Level Tokens] == SLACK_BOT_TOKEN
[OAuth & Permissions -> TOKEN]          == SLACK_APP_TOKEN
```

10. 슬랙을 실행 후 설정한 `# 채널명`에 들어가서 왼쪽 위의 `# 채널명`을 클릭 후 `통합` -> `앱` -> `설정 한 APP 이름` 추가합니다.

11. 다음과 같은 결과를 얻을 수 있습니다.

<img width="500" alt="Slack" src="https://github.com/InhwanCho/FAQ_chatbot/assets/111936229/0b75c16e-86e4-4a86-b752-d5eb2f4a731f">
