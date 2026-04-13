#!/bin/bash

# run_experiment.sh
# Automates the setup of Ryu controller and Mininet for Graduation Project 1
# Designed for Ubuntu 22.04 LTS

echo "=================================================="
echo " Starting Graduation Project 1 Experiment Setup   "
echo "=================================================="

# Check if running as root (Required for Mininet)
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use: sudo ./scripts/run_experiment.sh)"
  exit
fi

# Detect if a virtual environment is being used
RYU_CMD="ryu-manager"
PY_CMD="python3"
if [ -f "/home/mohammed/ryu-env/bin/ryu-manager" ]; then
    echo "[*] Found Python 3.9 virtual environment (ryu-env). Using it..."
    RYU_CMD="/home/mohammed/ryu-env/bin/ryu-manager"
    PY_CMD="/home/mohammed/ryu-env/bin/python"
fi

# Clean previous Mininet instances to avoid conflicts
echo "[*] Cleaning up old Mininet artifacts..."
mn -c > /dev/null 2>&1

# Ensure data directory exists for logs
mkdir -p data

# Start Ryu Controller in a NEW terminal window
echo "[*] Opening a new terminal for Ryu Controller..."
# We use sudo -E to preserve the display environment variables so the terminal can open
sudo -E -u $SUDO_USER gnome-terminal -- bash -c "cd /home/mohammed/NewFinalProject && source /home/mohammed/ryu-env/bin/activate && ryu-manager src/controller.py --observe-links; exec bash"

# Wait for controller to fully boot
echo "[*] Waiting 5 seconds for Ryu to initialize in the new window..."
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
echo "    -> Please close the Ryu Controller terminal window manually, or wait while I force kill it..."
pkill -f "ryu-manager"

echo "[*] Experiment script finished. The test is complete!"
