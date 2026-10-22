import json

def handler(event, context):
    print("=== FUNÇÃO LAMBDA ATIVADA VIA LOCALSTACK ===")
    
    for record in event.get('Records', []):
        mensagem_bruta = record.get('Sns', {}).get('Message', '{}')
        print(f"Evento recebido do CineScope: {mensagem_bruta}")
        
    print("============================================")
    return {
        'statusCode': 200,
        'body': json.dumps('Evento processado com sucesso pelo CineScope Lambda!')
    }