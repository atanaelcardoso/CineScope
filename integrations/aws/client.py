import os
import json
import boto3

class AWSClient:
    def __init__(self):
        self.sns_client = boto3.client(
            'sns',
            region_name='us-east-1',
            aws_access_key_id='fake',
            aws_secret_access_key='fake',
            endpoint_url='http://localstack:4566' 
        )

    def publish_movie_event(self, event_type, movie_id, movie_title):
        topic_arn = 'arn:aws:sns:us-east-1:000000000000:cinescope-movie-events'
        
        mensagem = {
            'event': event_type,
            'movie_id': movie_id,
            'movie_title': movie_title,
            'location': 'Extremoz, RN'
        }
        
        try:
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=json.dumps(mensagem)
            )
            print(f"🔥 [SNS] Evento {event_type} publicado com sucesso! MessageId: {response['MessageId']}")
            return response
        except Exception as e:
            print(f"❌ [SNS] Erro ao publicar no LocalStack: {e}")
            return None
