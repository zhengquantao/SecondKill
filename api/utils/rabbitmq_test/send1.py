"""
hello world
"""
import pika
# 建立连接对象
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
# 建立一个新通道
channel = connection.channel()
# 要连接的队列
channel.queue_declare(queue="hello")
# 发送数据
channel.basic_publish(exchange='', routing_key='hello', body="helloWorld")
print("[x] Sent 'hello World'")
connection.close()