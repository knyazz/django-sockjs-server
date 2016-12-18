from django.conf import settings

__author__ = 'Sergey Kravchuk'


class SockJSServerSettings(object):

    def __init__(self, options=None):
        conf = getattr(settings, 'DJANGO_SOCKJS_SERVER', None)
        if not conf:
            raise Exception('django-sockjs-server error! No settings.')

        self.rabbitmq_server = conf.get('RABBIT_SERVER', dict())
        self.redis_server = conf.get('REDIS_SERVER', dict())

        self.rabbitmq_user = self.rabbitmq_server.get('user', 'guest')
        self.rabbitmq_password = self.rabbitmq_server.get('password', 'guest')
        self.rabbitmq_host = self.rabbitmq_server.get('server_host', 'localhost')
        self.rabbitmq_port = int(self.rabbitmq_server.get('server_port', 5672))
        self.rabbitmq_vhost = self.rabbitmq_server.get('server_vhost', '/')
        self.rabbitmq_exchange_name = self.rabbitmq_server.get('exchange_name', 'sockjs')
        self.rabbitmq_exchange_type = self.rabbitmq_server.get('exchange_type', 'direct')
        self.rabbitmq_queue_name = self.rabbitmq_server.get('queue_name', 'ws01')

        self.redis_host = self.redis_server.get('host', 'localhost')
        self.redis_port = self.redis_server.get('port', '6379')
        self.redis_db = self.redis_server.get('db', 0)
        self.redis_password = self.redis_server.get('redis_password', None)
        self.redis_prefix = self.redis_server.get('redis_prefix', 'sockjs:')

        self.listen_addr = conf.get('listen_addr', '0.0.0.0')
        self.listen_port = int(conf.get('listen_port', 8083))
        self.listen_location = conf.get('listen_location', '/ws')
        self.secret_key = conf.get('secret_key', 'not_set_secret_key')
        self.sockjs_url = conf.get('sockjs_url', ['http://localhost:8083/ws'])

        self.router_settings = conf.get('router_settings', dict())
