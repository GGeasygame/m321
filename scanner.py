import pika
import json


def scan(function):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.100.19', port=2014))
        channel = connection.channel()

        # Declare exchange
        channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')

        # Declare and bind queue
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)

        # Consume messages
        for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
            try:
                json_body = json.loads(body)
                print(json_body)
                function(json_body)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
            except Exception as e:
                print(f"Error processing message: {e}")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"AMQP Connection Error: {e}")
    except pika.exceptions.AMQPChannelError as e:
        print(f"AMQP Channel Error: {e}")
    except pika.exceptions.AMQPChannelError as e:
        print(f"AMQP Channel Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()
