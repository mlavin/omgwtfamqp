import asyncio
import aioamqp
import json
import random


async def callback(channel, body, envelope, properties):
    data = json.loads(body.decode('utf-8'))
    routing_key = 'build.{project}.{user}'.format(**data)
    print('Task for {project}/{user} started...'.format(**data))
    update = data.copy()
    update['status'] = 'started'
    await channel.publish(json.dumps(update),
                          exchange_name='omg',
                          routing_key=routing_key)
    await asyncio.sleep(random.random() * 10)
    if random.random() < 0.90:
        print('Task for {project}/{user} passed!'.format(**data))
        update['status'] = 'succeeded'
    else:
        print('Task for {project}/{user} failed.'.format(**data))
        update['status'] = 'failed'
    await channel.publish(json.dumps(update),
                          exchange_name='omg',
                          routing_key=routing_key)
    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)


async def receive():
    transport, connection = await aioamqp.connect()
    channel = await connection.channel()
    await channel.exchange(exchange_name='omg', type_name='topic')
    await channel.queue(queue_name='omg.tasks')
    await channel.queue_bind(exchange_name='omg',
                             queue_name='omg.tasks',
                             routing_key='incoming.#')
    print('Waiting for incoming tasks. To exit press CTRL+C')
    await channel.basic_consume(callback, queue_name='omg.tasks')


loop = asyncio.get_event_loop()
loop.run_until_complete(receive())
loop.run_forever()
