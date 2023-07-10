# Falcon FM을 이용한 Chat API 생성

## 인프라 설치하기

1) [Falcon Foundation Model 설치](./deploy-falcon-fm.md)에 따라 Amazon SageMaker의 JumpStart의 Falcon FM 모델을 설치합니다.

2) Cloud9 Console에 접속하여 [Create environment] 이름으로 “chatbot”를 입력하고, EC2 instance는 편의상 “m5.large”를 선택합니다. 나머지는 기본값을 유지하고, 하단으로 스크롤하여 [Create]를 선택합니다.

![noname](https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/7c20d80c-52fc-4d18-b673-bd85e2660850)

3) [Environment](https://ap-northeast-2.console.aws.amazon.com/cloud9control/home?region=ap-northeast-2#/)에서 “chatbot”를 [Open]한 후에 아래와 같이 터미널을 실행합니다.

![noname](https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/b7d0c3c0-3e94-4126-b28d-d269d2635239)

4) 소스를 다운로드합니다.

```java
git clone https://github.com/kyopark2014/chatbot-based-on-Falcon-FM
```

5) cdk 폴더로 이동하여 필요한 라이브러리를 설치합니다.

```java
cd chatbot-based-on-Falcon-FM/cdk-chatbot-falcon/ && npm install
```

6) 인프라를 설치합니다.

```java
cdk deploy
```

7) 설치가 완료되면 브라우저에서 아래와 같이 WebUrl을 확인합니다. 

![noname](https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/dfc27dcd-3d46-4471-bcaf-04f0f709b4d3)





결과는 아래와 같습니다.

Response의 예는 아래와 같습니다.

```json
{
   "ResponseMetadata":{
      "RequestId":"80e8d6c5-0362-44a0-ab6d-bf11b2f2963e",
      "HTTPStatusCode":200,
      "HTTPHeaders":{
         "x-amzn-requestid":"80e8d6c5-0362-44a0-ab6d-bf11b2f2963e",
         "x-amzn-invoked-production-variant":"AllTraffic",
         "date":"Mon, 10 Jul 2023 07:27:42 GMT",
         "content-type":"application/json",
         "content-length":"185",
         "connection":"keep-alive"
      },
      "RetryAttempts":0
   },
   "ContentType":"application/json",
   "InvokedProductionVariant":"AllTraffic",
   "Body":<botocore.response.StreamingBody object at 0x7f0379091400>
}
```

이때 Body는 json 포맷으로 decoding하면 아래와 같습니다.

```json
[
   {
      "generated_text":" Hello, Daniel! I've been practicing my super-power, which is to be a super-duper-super-hero of super-duper-super-duperness, that can do super-duper-heroey things"
   }
]
```
