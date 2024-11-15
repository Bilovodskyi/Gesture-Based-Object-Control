# data_sender.py

import asyncio
import websockets
import json
from multiprocessing import Process, Queue
from hand_tracking import hand_tracking


async def main(queue):
    async def send_hand_data(websocket):
        try:
            while True:
                if not queue.empty():
                    data = queue.get()

                    await websocket.send(json.dumps(data))
                await asyncio.sleep(0.01)
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print("Error:", e)

    async with websockets.serve(
        send_hand_data,
        "localhost",
        6789,
    ):
        print("WebSocket server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    # Create a queue for sharing data
    data_queue = Queue()

    # Start the hand tracking process
    hand_tracking_process = Process(target=hand_tracking, args=(data_queue,))
    hand_tracking_process.start()

    try:
        # Start the WebSocket server
        asyncio.run(main(data_queue))
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        # Terminate the hand tracking process
        hand_tracking_process.terminate()
        hand_tracking_process.join()
