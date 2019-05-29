"""
RabbitMQ_client
"""
import pika


class InterRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue="miaosha")
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        self.response = body


    def call(self, n):
        self.response = None
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,

            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


# init_message = InterRpcClient()
# m = {"we": "xxxx"}
# get_message = init_message.call(m).decode("utf-8")
# message = eval(get_message)
# message = json.loads(get_message.replace("\'", "\""))