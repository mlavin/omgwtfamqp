import asyncio
import aioamqp
import json
import os
import uuid

from aiohttp import web, WSMsgType


async def hook(request):
    data = await request.post()
    project = data.get('project', None)
    user = data.get('user', None)
    if not (project and user):
        raise web.HTTPBadRequest()

    channel = await request.app['connection'].channel()
    routing_key = 'incoming.{project}.{user}'.format(project=project, user=user)
    message = json.dumps({
        'project': project,
        'user': user,
        'status': 'incoming',
        'uid': uuid.uuid4().hex,
    })
    await channel.publish(message, exchange_name='omg', routing_key=routing_key)
    return web.Response(text='OK')


async def socket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    channel = await request.app['connection'].channel()
    result = await channel.queue_declare('', exclusive=True)
    await channel.queue_bind(exchange_name='omg', queue_name=result['queue'], routing_key='#')

    async def message(channel, body, envelope, properties):
        if not ws.closed:
            ws.send_str(body.decode('utf-8'))
        await channel.basic_client_ack(envelope.delivery_tag)

    await channel.basic_consume(message, queue_name=result['queue'])

    async for msg in ws:
        if msg.type != WSMsgType.TEXT:
            break
    await channel.close()
    return ws


app = web.Application()
app.router.add_post('/', hook)
app.router.add_get('/socket', socket)
app.router.add_static('/', os.path.join(os.path.dirname(__file__), 'public'))


async def connect():
    app['transport'], app['connection'] = await aioamqp.connect()
    channel = await app['connection'].channel()
    await channel.exchange(exchange_name='omg', type_name='topic')


async def cleanup(app):
    await app['connection'].close(timeout=1.0)
    app['transport'].close()


def main():
    app.on_shutdown.append(cleanup)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect())
    web.run_app(app)


if __name__ == '__main__':
    main()
