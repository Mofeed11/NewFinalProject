#!/bin/bash

# run_experiment.sh
# Automates the setup of Ryu controller and Mininet for Graduation Project 1
# Designed for Ubuntu 22.04 LTS

echo "=================================================="
echo " Starting Graduation Project 1 Experiment Setup   "
echo "=================================================="

# Check if running as root (Required for Mininet)
if [ "$EUID" -ne 0 ]
  then echo "Please run as root (use: sudo ./scripts/run_experiment.sh)"
  exit
fi

# Clean previous Mininet instances to avoid conflicts
echo "[*] Cleaning up old Mininet artifacts..."
mn -c > /dev/null 2>&1

# Ensure data directory exists for logs
mkdir -p data

# Start Ryu Controller in the background
echo "[*] Starting Ryu Controller with QoS and ML integration..."
ryu-manager src/controller.py --observe-links > data/ryu_controller.log 2>&1 &
RYU_PID=$!
echo "    -> Ryu running in background (PID: $RYU_PID)"
echo "    -> Controller logs are being saved to data/ryu_controller.log"

# Wait for controller to fully boot
echo "[*] Waiting 5 seconds for Ryu to initialize..."
sleep 5

# Start Mininet Custom Topology
echo "[*] Starting Mininet Topology..."
echo "    -> You will enter the Mininet CLI."
echo "    -> Try running inside Mininet: h1 ping -c 5 h8"
echo "    -> Or generate traffic: h1 python3 scripts/traffic_generator.py -t VoIP -d 10.0.0.8"
echo "=================================================="
echo "Type 'exit' in Mininet CLI when you are done."
echo ""

# Launch Mininet (will block here until user exits)
python3 scripts/topology.py

# Cleanup after user exits Mininet
echo ""
echo "[*] Mininet session ended. Cleaning up..."
echo "    -> Killing Ryu Controller (PID: $RYU_PID)..."
kill -9 $RYU_PID

echo "[*] Experiment script finished. Check 'data/ryu_controller.log' for ML and RL outputs."
