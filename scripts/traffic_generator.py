#!/usr/bin/env python3

import os
import subprocess
import time
import random

# Example script for Mininet Hosts to generate traffic
# Usage inside Mininet:
# mininet> h1 python3 scripts/traffic_generator.py -t VoIP -d h5

import argparse

def generate_voip(dst_ip):
    # VoIP: D-ITG with G.711 codec (64 Kbps, 20 ms packet interval, 160 bytes/packet)
    print(f"Generating VoIP traffic to {dst_ip}")
    # ITGSend -a dst_ip -T UDP -c 160 -C 50 -t 30000
    os.system(f"ITGSend -a {dst_ip} -T UDP -c 160 -C 50 -t 30000 &")

def generate_video(dst_ip):
    # Video: D-ITG with H.264 model (2 Mbps, variable packet size)
    print(f"Generating Video traffic to {dst_ip}")
    os.system(f"ITGSend -a {dst_ip} -T UDP -c 1000 -C 250 -t 30000 &")

def generate_http(dst_ip):
    # HTTP: D-ITG with HTTP model
    print(f"Generating HTTP traffic to {dst_ip}")
    os.system(f"ITGSend -a {dst_ip} -T TCP -O 500 -t 30000 &")

def generate_ftp(dst_ip):
    # FTP: iperf3 TCP with 5 Mbps target, 30-second duration
    print(f"Generating FTP traffic to {dst_ip}")
    os.system(f"iperf3 -c {dst_ip} -b 5M -t 30 &")

def generate_dns(dst_ip):
    # DNS: D-ITG with DNS model
    print(f"Generating DNS traffic to {dst_ip}")
    os.system(f"ITGSend -a {dst_ip} -T UDP -c 50 -C 10 -t 30000 &")

def generate_background(dst_ip):
    # Background: iperf3 UDP with 1 Mbps, large packets
    print(f"Generating Background traffic to {dst_ip}")
    os.system(f"iperf3 -c {dst_ip} -u -b 1M -l 1400 -t 30 &")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Network Traffic")
    parser.add_argument("-t", "--type", choices=["VoIP", "Video", "HTTP", "FTP", "DNS", "Background"], required=True)
    parser.add_argument("-d", "--dst", required=True, help="Destination IP")
    
    args = parser.parse_args()
    
    if args.type == "VoIP":
        generate_voip(args.dst)
    elif args.type == "Video":
        generate_video(args.dst)
    elif args.type == "HTTP":
        generate_http(args.dst)
    elif args.type == "FTP":
        generate_ftp(args.dst)
    elif args.type == "DNS":
        generate_dns(args.dst)
    elif args.type == "Background":
        generate_background(args.dst)
