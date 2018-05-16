#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import sys
import pika


parameters = pika.URLParameters('amqp://maomao:qls1991@localhost:5672/web_develop')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.confirm_delivery()      # 接受确认消息

channel.exchange_declare('web_develop', exchange_type='direct',
                         passive=False, durable=True, auto_delete=True)      # 声明消息交换机
if sys.argv[1]:
    msg = sys.argv[1]
else:
    msg = 'This is rabbitmq'


props = pika.BasicProperties(content_type='text/plain', delivery_mode=2)
if channel.basic_publish('web_develop', 'xxx_routing_key', msg, properties=props):
    print 'Message publish was confirmed'
else:
    print 'Message publish is not confirmed'

connection.close()










