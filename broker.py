import pika
import json

# Параметры подключения к RabbitMQ
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_NOTIFICATION_QUEUE = "notifications"

# Создание соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
channel = connection.channel()

# Создание очереди
channel.queue_declare(queue='new_orders')
channel.queue_declare(queue='process_order')
channel.queue_declare(queue='client_sending_notfications')

# Функция для валидации заказа
def validate_order(order):
    if not all(key in order for key in ["customer_id", "items"]):
        return False
    else:
        return True

# Функция создания заказов
def create_order(customer_id, items):
    order = {"customer_id": customer_id, "items": items}

    if validate_order(order):
        return order
    else:
        print("Ошибка: Невалидный заказ.")
        return None

# Функция для отправки заказа в очередь
def send_order_to_queue(order):
    message = json.dumps(order)
    channel.basic_publish(exchange='', routing_key='process_order', body=message)
    print(f"Заказ отправлен в очередь: {order}")

# Обработка заказов
def process_order(ch, method, properties, body):

    order = json.loads(body.decode())

    print(f"Обработка заказа: {order}")

    confirm_order(order)

    update_order_status(order, "обрабатывается")

    prepare_for_delivery(order)

    print(f"Заказ {order['customer_id']} обработан успешно.")

    ch.basic_ack(delivery_tag=method.delivery_tag)

# Функция подтверждения заказа
def confirm_order(order):
    print(f"Заказ {order['customer_id']} подтвержден.")

# Функция обновления статуса заказа
def update_order_status(order, status):
    print(f"Статус заказа {order['customer_id']} обновлен на {status}.")

# Функция подготовки заказа к доставке
def prepare_for_delivery(order):
    print(f"Заказ {order['customer_id']} подготовлен к доставке.")

# Функция для отправки уведомления клиенту
def send_notification(order, message):
    notification = {
        "customer_id": order["customer_id"],
        "message": message
    }
    channel.basic_publish(exchange='', routing_key=RABBITMQ_NOTIFICATION_QUEUE, body=json.dumps(notification))
    print(f"Уведомление отправлено: {notification}")

channel.basic_consume(queue='client_sending_notfications', on_message_callback=process_order, auto_ack=False)

print("Ожидание сообщений...")

order = create_order("customer_1", [{"item_name": "Товар 1", "quantity": 2}])
send_order_to_queue(order)
send_notification(order, 'Заказ отправлен!')

channel.start_consuming()

connection.close()