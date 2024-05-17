import pika, sys, os
from datetime import datetime

api_clients_count=0
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='message_broker')

    def callback(ch, method, properties, body):
        global api_clients_count 
        api_clients_count+=1
        print(f" Nombre d’appel à l’API client  {api_clients_count}")
        print(f" [x] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Message reçu {body}")

    channel.basic_consume(queue='message_broker', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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