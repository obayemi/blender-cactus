import json


async def send_file(client, file_name):
    print("Sending file : ", file_name)
    file = open(file_name, "rb")
    await client.send(json.dumps({"type": "file", "name": "test_b.png"}))
    await client.send(file.read())
    print("File sended")


async def recv_file(websocket, file_name):
    print("< Receiving file : ", file_name)
    file = open(file_name, "xb")
    data = await websocket.recv()
    file.write(data)
    file.close()
    print("< File received")


async def send_error(websocket, error):
    await websocket.send(json.dumps({"type": "error", "message": error}))
