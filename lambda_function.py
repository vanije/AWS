import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
				# TODO implement
				s3 = boto3.client("s3")
				bucket = "comprehend-ses-bucket"
				key = "sample.txt"
				file = s3.get_object(Bucket = bucket, Key = key)
				
				paragraph = str(file['Body'].read())
				
				comprehend = boto3.client("comprehend")

				
				#learning code


				lan = comprehend.detect_dominant_language(Text = paragraph)
				x = str(lan['Languages'][0]['LanguageCode'])

				print("Extracted Language : " + str(lan))
				print("Extracted LanguageCode : " + x)
								
				response = comprehend.detect_sentiment(Text = paragraph, LanguageCode = "en")
				
				print("Extracted Sentiment:" + str(response))
				
				ent = comprehend.detect_entities(Text = paragraph, LanguageCode = "en")
				print("Extracted Entities:" + str(ent))
				
				
				SENDER = "Vani SE <vanise@amazon.com>"
				RECIPIENT = "vanise+"+ x +"@amazon.com"
				AWS_REGION = "us-east-1"
				
				SUBJECT = "Amazon SES Test"
				
				# The email body for recipients with non-HTML email clients.
				BODY_TEXT = ("Amazon SES Test (Python)\r\n"
													"This email was sent with Amazon SES using the "
													"AWS SDK for Python (Boto)."
												)
												
				# The HTML body of the email.
				BODY_HTML = """<html>
				<head></head>
				<body>
								<h1>Amazon SES Test (SDK for Python)</h1>
								<p>"""+paragraph+"""</p>
				</body>
				</html>
												"""
				
				# The character encoding for the email.
				CHARSET = "UTF-8"
																
				# Create a new SES resource and specify a region.
				client = boto3.client('ses',region_name=AWS_REGION)


								
				# Try to send the email.
				try:
				#Provide the contents of the email.
						response = client.send_email(
										Destination={
														'ToAddresses': [
																		RECIPIENT,
														],
										},
										Message={
														'Body': {
																		'Html': {
																						'Charset': CHARSET,
																						'Data': BODY_HTML,
																		},
																		'Text': {
																						'Charset': CHARSET,
																						'Data': BODY_TEXT,
																		},
														},
														'Subject': {
																		'Charset': CHARSET,
																		'Data': SUBJECT,
														},
										},
										Source=SENDER,
										
										)
					# Display an error if something goes wrong. 
				except ClientError as e:
								print(e.response['Error']['Message'])
				else:
								print("Email sent! Message ID:"),
								print(response['MessageId'])
								
				
				#ending learning code
					
				return {
								'statusCode': 200,
								'body': json.dumps('Hello from Lambda!')
				}
