# Django SockJS-server 

Simple sockjs server for django.

## Requirements:

* sockjs-tornado >= 1.0.0
* pika >= 0.9.12
* django >= 1.4
* redis >= 2.9.1

## Installation:
```
pip install git+https://github.com/knyazz/django-sockjs-server
```

Add django-sockjs-server to your INSTALLED_APPS in settings.py

```
  INSTALLED_APPS = (
       ...
       'django_sockjs_server',
       ...
  )
  ```

Define ```DJANGO_SOCKJS_SERVER``` in ```settings.py```.

```
DJANGO_SOCKJS_SERVER = {
    'RABBIT_SERVER': {
        'host': 'localhost',
        'user': 'guest',
        'password': 'guest',
        'port': 5672,
        'vhost': '/',
        'exchange_name': 'sockjs',
        'queue_name': 'ws01',
        'exchange_type': 'direct',
    },
    'REDIS_SERVER': {
        'host': 'localhost',
        'port': '6379',
        'db': 0,
    },
    'listen_addr': '0.0.0.0',
    'listen_port': 8083,
    'listen_location': '/ws'
    'secret_key': 'xe4pa7gysp4phe2rhyd',
    'sockjs_url': ['http://localhost:8083/ws']
}
```
* RABBIT_SERVER['host'] - rabbitmq server
* RABBIT_SERVER['user'] - rabbitmq user
* RABBIT_SERVER['password'] - rabbitmq password
* RABBIT_SERVER['port'] - rabbitmq port
* RABBIT_SERVER['vhost'] - rabbitmq vhost
* RABBIT_SERVER['exchange_name'] - exchange name
* RABBIT_SERVER['exchange_type'] - type exchange
* listen_addr - listen sockjs server address
* listen_port - listen sockjs server port
* listen_location - listen sockjs server location
* secret_key - salt for subscribe
* sockjs_url - path for client sockjs
* REDIS_SERVER.['host'] - redis server host
* REDIS_SERVER.['port'] - redis server port
* REDIS_SERVER.['db'] - redis db



## Usage:
<center>
<img src="https://raw.github.com/alfss/django-sockjs-server/master/README_1.png" alt="1.png">
</center>

Run sockjs-server

```
./manage.py sockjs_server
```

Append sockjs client library to your page
```
   <head>
       <script src="http://cdn.sockjs.org/sockjs-0.3.min.js">
       ...
```

Open page in browser and connect to sockjs-tornado server

```
        {% load sockjs_server_tags %}
        window.sockjs_action_pull = new Array();
        var new_conn = function() {
            window.connection_sockjs = new SockJS('{% sockjs_server_url %}');
            window.connection_sockjs.onmessage = function(e) {
                document.write(e.data);
                document.write("<br/ >");
            };

            connection_sockjs.onclose = function(e) {
                setTimeout(function() { new_conn(); }, 5000);
            };

            connection_sockjs.onopen = function(e) {
            };
        };
        new_conn();

```


To get this messages you need to subscribe by token

```
        SockJS.prototype.emit = function (token, data) {
            var meta_dict = {
                token:token,
                data:data
            };
            this.send(JSON.stringify(meta_dict))
        };

        connection_sockjs.addEventListener("open", function() {
                connection_sockjs.emit('{% sockjs_auth_token 'user' %}', {'channel': 'user'});
            }
        );

        or

        connection_sockjs.addEventListener("open", function() {
                connection_sockjs.emit('{% sockjs_auth_token 'user' '1' %}', {'channel': 'user'+ '1'});
              }
        );
```


Send a message from django

```
    client = SockJsServerClient()
    test_message = dict()
    room = 'user'
    data = dict()
    data['user_name'] = "Sergey Kravchuk"
    data['user_id'] = 1
    connections = client.get_connections(room)
    for conn in connections:
        conn_id = conn.get('id')
        host = conn.get('host')
        if conn_id and host:
            message = {
                'uid': conn_id,
                'host': host,
                'data': data,
                'room': room
            }
            client.publish_message(message)  
```



Get websocket stats

```
curl http://localhost:8083/stats/
uptime_seconds: 5
memory_use_byte: 0
memory_resident_use_byte: 0
memory_stack_size_byte: 0
last_rabbitmq_reconnect: 2013-09-26 13:04:16.302877+00:00
connect_rabbitmq_time_seconds: 5
connects: 0
channel_count: 0

http://localhost:8083/stats/debug
uptime_seconds: 5
memory_use_byte: 0
memory_resident_use_byte: 0
memory_stack_size_byte: 0
last_rabbitmq_reconnect: 2013-09-26 13:04:16.302877+00:00
connect_rabbitmq_time_seconds: 5
connects: 0
channel_count: 0
channels: [u'user']

```
