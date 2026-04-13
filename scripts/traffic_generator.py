#!/usr/bin/env python3

import argparse
import socket
import time
import threading

# Custom Python-based Traffic Generator
# Replaces D-ITG and iperf3 to avoid installation issues

def start_server():
    print("Starting Dummy Traffic Sink Servers...")
    ports_tcp = [80, 21]           # HTTP, FTP
    ports_udp = [5060, 554, 53, 5201] # VoIP, Video, DNS, Background
    
    def udp_sink(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', port))
        print(f" Listening UDP on port {port}")
        while True:
            try:
                sock.recvfrom(2048)
            except:
                pass
            
    def tcp_sink(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', port))
        sock.listen(5)
        print(f" Listening TCP on port {port}")
        while True:
            try:
                conn, _ = sock.accept()
                def handle(c):
                    while True:
                        try:
                            if not c.recv(2048): break
                        except:
                            break
                    c.close()
                threading.Thread(target=handle, args=(conn,), daemon=True).start()
            except:
                pass

    for p in ports_udp:
        threading.Thread(target=udp_sink, args=(p,), daemon=True).start()
    for p in ports_tcp:
        threading.Thread(target=tcp_sink, args=(p,), daemon=True).start()
    
    print("Servers running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers.")

def generate_udp(dst_ip, port, pkt_size, iat, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b'X' * pkt_size
    start = time.time()
    packets = 0
    print(f"Generating UDP to {dst_ip}:{port} (Size={pkt_size}B, IAT={iat}s) for {duration}s")
    while time.time() - start < duration:
        sock.sendto(payload, (dst_ip, port))
        packets += 1
        time.sleep(iat)
    print(f"Finished. Sent {packets} packets.")

def generate_tcp(dst_ip, port, chunk_size, iat, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting TCP to {dst_ip}:{port}...")
    try:
        sock.connect((dst_ip, port))
        payload = b'X' * chunk_size
        start = time.time()
        packets = 0
        print(f"Generating TCP to {dst_ip}:{port} (Chunk={chunk_size}B, IAT={iat}s) for {duration}s")
        while time.time() - start < duration:
            sock.send(payload)
            packets += 1
            time.sleep(iat)
        sock.close()
        print(f"Finished. Sent {packets} chunks.")
    except Exception as e:
        print(f"Connection failed: {e}. Make sure to run the server on {dst_ip} first using '--server'!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SDN Network Traffic Generator")
    parser.add_argument("--server", action="store_true", help="Run as a dummy sink server to receive traffic")
    parser.add_argument("-t", "--type", choices=["VoIP", "Video", "HTTP", "FTP", "DNS", "Background"], help="Traffic Type")
    parser.add_argument("-d", "--dst", help="Destination IP")
    parser.add_argument("--time", type=int, default=30, help="Duration in seconds (default: 30)")
    
    args = parser.parse_args()
    
    if args.server:
        start_server()
    elif args.type and args.dst:
        if args.type == "VoIP":
            # UDP, Port 5060, 160 bytes, 50 pkts/sec
            generate_udp(args.dst, 5060, 160, 0.02, args.time)
        elif args.type == "Video":
            # UDP, Port 554, 1000 bytes, 200 pkts/sec
            generate_udp(args.dst, 554, 1000, 0.005, args.time)
        elif args.type == "HTTP":
            # TCP, Port 80, 500 bytes, 20 pkts/sec
            generate_tcp(args.dst, 80, 500, 0.05, args.time)
        elif args.type == "FTP":
            # TCP, Port 21, 1460 bytes, max speed (very low iat)
            generate_tcp(args.dst, 21, 1460, 0.002, args.time)
        elif args.type == "DNS":
            # UDP, Port 53, 50 bytes, 2 pkts/sec
            generate_udp(args.dst, 53, 50, 0.5, args.time)
        elif args.type == "Background":
            # UDP, Port 5201, 1400 bytes, 100 pkts/sec
            generate_udp(args.dst, 5201, 1400, 0.01, args.time)
    else:
        print("Please provide both --type and --dst arguments, or run with --server")
