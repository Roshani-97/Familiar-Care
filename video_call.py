##########-------------------------------Server side-------------------------------###################
import cv2
import socket
import pickle
import struct
import threading

# Server Configuration
SERVER_IP = "0.0.0.0"
PORT = 9999

# Flags for controlling camera
camera_on = True

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(5)

print("📞 Waiting for a connection...")
client_socket, addr = server_socket.accept()
print(f"✅ Connected to {addr}")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Error: Couldn't open webcam!")
    client_socket.close()
    server_socket.close()
    exit()

def toggle_camera():
    """Function to turn the camera ON/OFF"""
    global camera_on
    camera_on = not camera_on

def send_video():
    """Thread function to send video frames"""
    global camera_on
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Couldn't capture frame!")
                break

            if camera_on:
                frame = cv2.resize(frame, (640, 480))  # Reduce frame size
                frame = cv2.flip(frame, 1)  # Flip for correct orientation

                # Serialize frame
                data = pickle.dumps(frame)
                message = struct.pack("Q", len(data)) + data

                try:
                    client_socket.sendall(message)
                except BrokenPipeError:
                    print("❌ Client Disconnected!")
                    break

            # Display video
            cv2.imshow("Doctor Video", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("c"):  # Toggle Camera on pressing 'C'
                toggle_camera()

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()
        server_socket.close()
        print("✅ Server Closed!")

# Start video thread


#########################----------------------client side----------------------##########################3

import cv2
import socket
import pickle
import struct
import threading

# Server IP and Port
SERVER_IP = "127.0.0.1"
PORT = 9999

# Flags for controlling camera
camera_on = True

# Create Client Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_IP, PORT))
    print(f"✅ Connected to Server: {SERVER_IP}:{PORT}")
except ConnectionRefusedError:
    print("❌ Error: Server is not running!")
    exit()

# Open Webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Error: Could not open webcam!")
    client_socket.close()
    exit()

def toggle_camera():
    """Function to turn the camera ON/OFF"""
    global camera_on
    camera_on = not camera_on

def receive_video():
    """Thread function to receive video frames from server"""
    try:
        data = b""
        payload_size = struct.calcsize("Q")

        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)  # 4K buffer
                if not packet:
                    print("❌ Server Disconnected!")
                    return
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)

            if camera_on:
                cv2.imshow("Patient's Video", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("c"):  # Toggle Camera
                toggle_camera()

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()
        print("✅ Client Closed!")

# Start receiving video in a separate thread
video_thread = threading.Thread(target=receive_video)
video_thread.daemon = True
video_thread.start()
video_thread.join()
video_thread = threading.Thread(target=send_video)
video_thread.daemon = True
video_thread.start()
video_thread.join()
