import asyncio
import websockets
import tkinter as tk
from threading import Thread

async def listen_for_messages(websocket, text_area):
  async for message in websocket:
      text_area.insert(tk.END, f"{message}\n")

def start_client():
  async def run_client():
      async with websockets.connect("ws://localhost:12345") as websocket:
          # Start a thread to listen for incoming messages
          Thread(target=asyncio.run, args=(listen_for_messages(websocket, text_area),)).start()

          # Send messages from the input field
          while True:
              message = input_field.get()
              if message:
                  await websocket.send(message)
                  input_field.delete(0, tk.END)

  asyncio.run(run_client())

# Set up the GUI
root = tk.Tk()
root.title("Chat Client")

text_area = tk.Text(root)
text_area.pack()

input_field = tk.Entry(root)
input_field.pack()

send_button = tk.Button(root, text="Send", command=lambda: Thread(target=start_client).start())
send_button.pack()

root.mainloop()