import boto3
import json

pagerduty_file = open("pd_key.txt")
pagerduty_key = pagerduty_file.read()
pagerduty_key = pagerduty_key.replace("\n","").strip()

goss_key_file = open("goss_key.txt")
goss_key = goss_key_file.read()
goss_key = goss_key.replace("\n","").strip()

goss_secret_file = open("goss_secret.txt")
goss_secret = goss_secret_file.read()
goss_secret = goss_secret.replace("\n","").strip()

def list_pagerduty_users(api_key):

	base_url = "https://api.pagerduty.com/users"
	headers = {
	    "Content-Type": "application/json",
	    "Authorization": f"Token token={api_key}"
	}
	
	
	offset = 0
	params = {
		"limit":100,
		"offset":offset
	}

	#combine all additional parameters into one json object
	json_args = {"headers":headers, "params":params}

	#construct final payload including url and request type
	payload = {"url":base_url, "type":"get", "json_args":json_args}
	#convert payload to bytes
	payload = json.dumps(payload)

	#call lambda forwarder
	lambda_client = boto3.client('lambda', aws_access_key_id=goss_key, aws_secret_access_key=goss_secret, region_name='us-east-1')
	response = lambda_client.invoke(FunctionName='InfraSRE-HttpForwarder',InvocationType='RequestResponse',Payload=payload)


	response_main = response['Payload']

	response_main = response_main.read()

	response_main = json.loads(response_main.decode("utf-8"))

	for item in response_main['body']:
		print(item)

list_pagerduty_users(pagerduty_key)