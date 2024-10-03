import asyncio
import websockets
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext

async def listen_for_messages(websocket, text_area):
  async for message in websocket:
    print(f"Received message: {message}")  
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"{message}\n")
    text_area.config(state=tk.DISABLED)


async def send_message(websocket, message):
  if message:
      print(f"Sending message: {message}") 
      await websocket.send(message)

def on_send_button_click(websocket, input_field, loop):
  message = input_field.get()
  if message:
      # Schedule the send_message coroutine on the asyncio event loop
      asyncio.run_coroutine_threadsafe(send_message(websocket, message), loop)
      input_field.delete(0, tk.END)

async def run_client(text_area, input_field, send_button, loop):
  async with websockets.connect("ws://localhost:12345") as websocket:
      # Start listening for messages
      asyncio.create_task(listen_for_messages(websocket, text_area))

      # Bind the send button to the send function
      send_button.config(command=lambda: on_send_button_click(websocket, input_field, loop))

      # Keep the event loop running
      while True:
          await asyncio.sleep(0.1)  # Small sleep to yield control

def start_client():
  # Set up the GUI
  root = tk.Tk()
  root.title("Chat Client")

  text_area = scrolledtext.ScrolledText(root, height=20, width=50, state=tk.DISABLED)
  text_area.pack()

  input_field = tk.Entry(root, width=50)
  input_field.pack()

  send_button = tk.Button(root, text="Send")
  send_button.pack()

  # Start the asyncio event loop in a separate thread
  loop = asyncio.new_event_loop()
  t = Thread(target=lambda: loop.run_forever())
  t.start()

  # Schedule the run_client coroutine
  asyncio.run_coroutine_threadsafe(run_client(text_area, input_field, send_button, loop), loop)

  # Run the Tkinter main loop
  root.mainloop()

if __name__ == "__main__":
  start_client()