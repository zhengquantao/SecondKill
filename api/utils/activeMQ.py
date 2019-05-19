"""
消息队列设置
"""
import stomp

queue_name = "/queue/SampleQueue"
topic_name = "/topic/SampleTopic"
listener_name = "SampleListener"
address = "127.0.0.1"
port = 61613


class SampleListener(object):
    def on_message(self, headers, message):
        print("headers:%s" % headers)
        print("message:%s" % message)
        return message, headers


# 将消息推送到队列中
def send_to_queue(msg):
    conn = stomp.Connection10([(address, port)])
    conn.start()
    conn.connect()
    # 要给的队列名称， 内容
    conn.send(queue_name, msg)
    conn.disconnect()


# 从队列接收消息
def receive_from_queue():
    conn = stomp.Connection10([(address, port)])
    # 要接收的队列名 内容
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    conn.subscribe(queue_name)
    conn.disconnect()