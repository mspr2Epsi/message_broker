import pika, sys, os
from datetime import datetime

api_clients_count=0
api_produits_count=0
api_commandes_count=0

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='message_broker_client')
    channel.queue_declare(queue='message_broker_produit')
    channel.queue_declare(queue='message_broker_commande')

    def callback_client(ch, method, properties, body):
        global api_clients_count 
        api_clients_count+=1
        print(f" Nombre d’appel à l’API client  {api_clients_count}")
        print(f" [x] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Message reçu {body}")

    def callback_produit(ch, method, properties, body):
        global api_produits_count 
        api_produits_count+=1
        print(f" Nombre d’appel à l’API produit  {api_produits_count}")
        print(f" [x] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Message reçu {body}")     

    def callback_commande(ch, method, properties, body):
        global api_commandes_count 
        api_commandes_count+=1
        print(f" Nombre d’appel à l’API commandes  {api_commandes_count}")
        print(f" [x] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Message reçu {body}")                   

    channel.basic_consume(queue='message_broker_client', on_message_callback=callback_client, auto_ack=True)
    channel.basic_consume(queue='message_broker_produit',on_message_callback=callback_produit, auto_ack=True)
    channel.basic_consume(queue='message_broker_commande',on_message_callback=callback_commande, auto_ack=True)

    print('Message broker en attente de message')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)