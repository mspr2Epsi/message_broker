import pika, sys, os
from datetime import datetime
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

api_clients_count = 0
api_produits_count = 0
api_commandes_count = 0
log_messages = []  # Global list to store log messages

def log_message(text_area, message):
    log_messages.append(message)
    if "40" in message:
        text_area.insert(tk.END, message + "\n", "red")
    else:
        text_area.insert(tk.END, message + "\n")
    text_area.yview(tk.END)  # Auto-scroll to the end

def save_logs_to_file(filename='log_messages.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for message in log_messages:
            file.write(message + '\n')

def main(text_area):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='message_broker_client')
    channel.queue_declare(queue='message_broker_produit')
    channel.queue_declare(queue='message_broker_commande')

    def callback_client(ch, method, properties, body):
        global api_clients_count 
        api_clients_count += 1
        message = f"Nombre d’appel à l’API client {api_clients_count}\n[x] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Message reçu {body.decode()}"
        print(message)
        log_message(text_area, message)

    def callback_produit(ch, method, properties, body):
        global api_produits_count 
        api_produits_count += 1
        message = f"Nombre d’appel à l’API produit {api_produits_count}\n[x] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Message reçu {body.decode()}"
        print(message)
        log_message(text_area, message)

    def callback_commande(ch, method, properties, body):
        global api_commandes_count 
        api_commandes_count += 1
        message = f"Nombre d’appel à l’API commandes {api_commandes_count}\n[x] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Message reçu {body.decode()}"
        print(message)
        log_message(text_area, message)

    channel.basic_consume(queue='message_broker_client', on_message_callback=callback_client, auto_ack=True)
    channel.basic_consume(queue='message_broker_produit', on_message_callback=callback_produit, auto_ack=True)
    channel.basic_consume(queue='message_broker_commande', on_message_callback=callback_commande, auto_ack=True)

    print('Message broker en attente de message')
    channel.start_consuming()

def start_consumer_thread(text_area):
    consumer_thread = threading.Thread(target=main, args=(text_area,))
    consumer_thread.start()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Message Broker")

    text_area = ScrolledText(root, wrap=tk.WORD, width=100, height=30)
    text_area.pack(padx=10, pady=10)

    text_area.tag_configure("red", foreground="red")

    start_consumer_thread(text_area)

    def on_closing():
        save_logs_to_file()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print('Interrupted')
        save_logs_to_file()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)