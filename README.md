# Falcon FM을 이용한 Chat API 생성

여기서는 [Falcon Foundation Model](https://aws.amazon.com/ko/blogs/machine-learning/technology-innovation-institute-trains-the-state-of-the-art-falcon-llm-40b-foundation-model-on-amazon-sagemaker/)을 [Amazon SageMaker JumpStart](https://aws.amazon.com/ko/sagemaker/jumpstart/?sagemaker-data-wrangler-whats-new.sort-by=item.additionalFields.postDateTime&sagemaker-data-wrangler-whats-new.sort-order=desc)을 이용하여 설치하고 웹브라우저 기반의 Chatbot을 생성하는 방법에 대해 설명합니다. 이때의 Architecture는 아래와 같습니다.

사용자는 CloudFront를 통해 채팅 웹페이지에 접속합니다. 이때 사용자가 텍스트를 입력하면 Lambda를 통해 SageMaker Endpoint로 요청이 전달됩니다. 이때 Falcon Foundation Model이 응답하면 이를 다시 브라우저에 표시합니다. 이때 Falcon Foundation Model은 SageMaker JumpStart를 통해 설치하고, AWS CDK를 통해 관련된 인프라를 설치합니다. 

<img src="https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/13c45617-9b47-4d8d-a68d-a344e0cb8bc3" width="700">


## Chatbot 구현하기

사용자가 입력한 text는 CloudFront - API Gateway를 통해 Lambda로 전달됩니다. 이때 전달된 텍스트 입력을 event에서 분리한 후에 payload를 생성합니다.

```python
text = event['text']

payload = {
    "inputs": text,
    "parameters":{
        "max_new_tokens": 200,
    }
}
```

아래와 같이 boto3를 이용해 endpoint로 payload를 전달합니다. 이때 출력의 statusCode가 200일때 body의 generated_text를 추출합니다.

```python
client = boto3.client('runtime.sagemaker')

endpoint_name = os.environ.get('endpoint')
response = client.invoke_endpoint(
    EndpointName=endpoint_name, 
    ContentType='application/json', 
    Body=json.dumps(payload).encode('utf-8'))                
        
statusCode = response['ResponseMetadata']['HTTPStatusCode']        

outputText = ""        
if(statusCode==200):
    response_payload = json.loads(response['Body'].read())

    if len(response_payload) == 1:
        outputText = response_payload[0]['generated_text']
    else:
        for resp in response_payload:
            outputText = outputText + resp['generated_text'] + '\n'
```

참고로 Falcon의 Response 예는 아래와 같습니다.

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



## 직접 실습하여 보기

### Falcon FM 설치하기

[Falcon Foundation Model 설치](./deploy-falcon-fm.md)에 따라 Amazon SageMaker의 JumpStart의 Falcon FM을 설치합니다.

### 인프라 설치하기

[AWS CDK를 이용한 인프라 설치하기](./cdk-chatbot-falcon/README.md)에 따라 인프라를 설치하고 WEB URL로 접속합니다.

### 실행 결과

1) "Building a website can be done in 10 simple steps"에 대한 답변

![image](https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/deca3b03-9652-420d-ab67-34a5d8046ed9)


2) "Guide me how to travel from New York to LA."에 대한 답변

![image](https://github.com/kyopark2014/chatbot-based-on-Falcon-FM/assets/52392004/433d895f-5153-4745-9f68-90e02cb32f15)


### 인프라 정리하기

Cloud9에 접속하여 아래와 같이 삭제를 합니다.

```java
cdk destroy
```

Falcon FM 모델의 inference를 위해 GPU를 포함한 "ml.g5.2xlarge"를 사용하고 있으므로, 더이상 사용하지 않을 경우에 반드시 삭제하여야 합니다. 이를 위해 [Inference Console](https://ap-northeast-2.console.aws.amazon.com/sagemaker/home?region=ap-northeast-2#/endpoints)에 접속해서 Endpoint를 삭제합니다. 마찬가지로 [Model console](https://ap-northeast-2.console.aws.amazon.com/sagemaker/home?region=ap-northeast-2#/models)과 [Endpoint configuration](https://ap-northeast-2.console.aws.amazon.com/sagemaker/home?region=ap-northeast-2#/endpointConfig)에서 설치한 Falcon을 삭제합니다. 
