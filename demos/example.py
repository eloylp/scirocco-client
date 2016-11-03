from sciroccoclient.httpclient import HTTPClient


class ClientClass:
    def __init__(self):
        pass

    def run(self):
        c = HTTPClient('http://localhost', 'af123', 'DEFAULT_TOKEN')
        res = c.message_queue_push("af123", {"as":"sd"})
        print(res.message_data)
        res = c.message_queue_pull()
        print(res.message_data)


if __name__ == '__main__':
    p = ClientClass()
    p.run()
