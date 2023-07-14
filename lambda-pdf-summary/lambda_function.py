import json
import boto3
import os
import time
from multiprocessing import Process
from io import BytesIO
import PyPDF2
from langchain import PromptTemplate, SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler

s3 = boto3.client('s3')
s3_bucket = os.environ.get('s3_bucket') # bucket name
s3_prefix = os.environ.get('s3_prefix')
endpoint_name = os.environ.get('endpoint')

class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
        input_str = json.dumps({'inputs': prompt, **model_kwargs})
        #input_str = json.dumps({'inputs': prompt, 'parameters': model_kwargs})
        return input_str.encode('utf-8')
      
    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]

content_handler = ContentHandler()

def get_summary_from_pdf(file_type, s3_file_name):
    summary = ''
    
    if file_type == 'pdf':
        s3r = boto3.resource("s3")
        doc = s3r.Object(s3_bucket, s3_prefix+'/'+s3_file_name)
        #doc = s3r.Object('cdkchatbotfalconstack-chatbotstoragef9db61b9-vbcslny70mso', '/docs/sample.pdf')
        
        contents = doc.get()['Body'].read()
        reader = PyPDF2.PdfReader(BytesIO(contents))
        
        raw_text = []
        for page in reader.pages:
            raw_text.append(page.extract_text())
        contents = '\n'.join(raw_text)    

        aws_region = boto3.Session().region_name
        parameters = {
            "max_length": 200
        }        
        content_handler = ContentHandler()

        llm = SagemakerEndpoint(
            endpoint_name = endpoint_name, 
            region_name = aws_region, 
            model_kwargs = parameters,
            content_handler = content_handler
        )
        output = llm('Building a website can be done in 10 simple steps')
        print(output)

        new_contents = str(contents[:4000]).replace("\n"," ") 
        print('new_contents: ', new_contents)

        text = 'Create a 200 words summary of this document: '+ new_contents
        payload = {
                "inputs": text,
                "parameters":{
                    "max_new_tokens": 300,
                }
            }
            
        response = query_endpoint(payload, endpoint_name)
        print('response:', response)

        statusCode = response['statusCode']       
        if(statusCode==200):
            response_payload = response['body']
            print('response_payload:', response_payload)

        if response_payload != '':
            summary = response_payload
        else:
            summary = 'Falcon did not find an answer to your question, please try again'               
        print('summary:', summary)
    
    return summary    
    
def query_endpoint(payload, endpoint_name):
    client = boto3.client('runtime.sagemaker')
    response = client.invoke_endpoint(
        EndpointName=endpoint_name, 
        ContentType='application/json', 
        Body=json.dumps(payload).encode('utf-8'))                
    print('response:', response)
        
    statusCode = response['ResponseMetadata']['HTTPStatusCode']        
    if(statusCode==200):
        response_payload = json.loads(response['Body'].read())
        print('response_payload:', response_payload)

        outputText = ""
        print('len:', len(response_payload))
        if len(response_payload) == 1:
            outputText = response_payload[0]['generated_text']
        else:
            for resp in response_payload:
                outputText = outputText + resp['generated_text'] + '\n'
                
        return {
            'statusCode': statusCode,
            'body': outputText
        }
            
    else:
        return {
            'statusCode': statusCode,
            'body': json.dumps(response)
        }
    
def lambda_handler(event, context):
    print(event)

    object = event['object']
    print('object: ', object)
    
    start = int(time.time())
    
    summary = get_summary_from_pdf('pdf', object)

    if(summary != ''):
        return {
            'statusCode': 200,
            'msg': summary,
        }                                       
    else: 
        return {
            'statusCode': 500,
            'msg': "No contents",
        }
    
    
