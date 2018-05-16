#!/usr/bin/env python
# --*-- coding: utf-8 --

import pika


def on_message(channel, method_frame, header_frame, body):
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    print body


parameters = pika.URLParameters('amqp://maomao:qls1991@localhost:5672/web_develop')
connect = pika.BlockingConnection(parameters)
channel = connect.channel()

channel.exchange_declare('web_develop', exchange_type='direct', passive=False, durable=True, auto_delete=True)
channel.queue_declare('standrand1', durable=True, auto_delete=True)
channel.queue_bind(queue='standrand1', exchange='web_develop', routing_key='xxx_routing_key')

channel.basic_consume(on_message, 'standrand1')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connect.close()





