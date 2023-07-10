# CDK를 이용한 인프라 설치하기

여기서는 [Cloud9](https://aws.amazon.com/ko/cloud9/)에서 [AWS CDK](https://aws.amazon.com/ko/cdk/)를 이용하여 인프라를 설치합니다.

1) [Cloud9 Console](https://ap-northeast-2.console.aws.amazon.com/cloud9control/home?region=ap-northeast-2#/create)에 접속하여 [Create environment]에서 이름으로 “chatbot”를 입력하고, EC2 instance는 편의상 “m5.large”를 선택합니다. 나머지는 기본값을 유지하고, 하단으로 스크롤하여 [Create]를 선택합니다.

![noname](https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/7c20d80c-52fc-4d18-b673-bd85e2660850)

2) [Environment](https://ap-northeast-2.console.aws.amazon.com/cloud9control/home?region=ap-northeast-2#/)에서 “chatbot”를 [Open]한 후에 아래와 같이 터미널을 실행합니다.

![noname](https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/b7d0c3c0-3e94-4126-b28d-d269d2635239)

3) 소스를 다운로드합니다.

```java
git clone https://github.com/kyopark2014/chatbot-based-on-Falcon-FM
```

4) cdk 폴더로 이동하여 필요한 라이브러리를 설치합니다.

```java
cd chatbot-based-on-Falcon-FM/cdk-chatbot-falcon/ && npm install
```

5) 인프라를 설치합니다.

```java
cdk deploy
```

6) 설치가 완료되면 브라우저에서 아래와 같이 WebUrl을 확인합니다. 

![noname](https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/dfc27dcd-3d46-4471-bcaf-04f0f709b4d3)

