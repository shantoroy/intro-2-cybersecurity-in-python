import scapy.all as scapy
from collections import defaultdict
import time
import logging

# Configure logging
logging.basicConfig(filename='ids.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Known malicious IPs (for demonstration purposes)
MALICIOUS_IPS = {"192.168.1.10", "10.0.0.5"}
# Sample attack signatures (basic example)
SIGNATURES = {"malicious_payload": b"evil_command"}
# Thresholds for anomaly detection
PORT_SCAN_THRESHOLD = 10  # More than 10 ports accessed in a short time
TRAFFIC_SPIKE_THRESHOLD = 100  # More than 100 packets within 10 seconds

# Dictionary to track port scanning attempts
port_scan_attempts = defaultdict(list)
traffic_counter = defaultdict(int)

def log_alert(alert_type, packet):
    """Logs potential intrusion attempts."""
    message = f"[ALERT] {alert_type} detected! Source IP: {packet[scapy.IP].src}, Destination IP: {packet[scapy.IP].dst}"
    logging.warning(message)

def detect_malicious_ip(packet):
    """Detects traffic from known malicious IPs."""
    if packet.haslayer(scapy.IP):
        if packet[scapy.IP].src in MALICIOUS_IPS:
            log_alert("Malicious IP Traffic", packet)

def detect_signature(packet):
    """Compares packet payloads against known attack signatures."""
    if packet.haslayer(scapy.Raw):
        payload = packet[scapy.Raw].load
        for signature_name, signature in SIGNATURES.items():
            if signature in payload:
                log_alert(f"Signature Match: {signature_name}", packet)

def detect_port_scanning(packet):
    """Detects potential port scanning by tracking connection attempts."""
    if packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP):
        src_ip = packet[scapy.IP].src
        dst_port = packet[scapy.TCP].dport if packet.haslayer(scapy.TCP) else packet[scapy.UDP].dport
        port_scan_attempts[src_ip].append(time.time())
        # Keep only the last 10 seconds of attempts
        port_scan_attempts[src_ip] = [t for t in port_scan_attempts[src_ip] if time.time() - t < 10]
        if len(port_scan_attempts[src_ip]) > PORT_SCAN_THRESHOLD:
            log_alert("Port Scanning Detected", packet)
            port_scan_attempts[src_ip] = []  # Reset after alerting

def detect_traffic_anomalies(packet):
    """Detects unusual traffic spikes."""
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        traffic_counter[src_ip] += 1
        time.sleep(10)  # Reset counter every 10 seconds
        if traffic_counter[src_ip] > TRAFFIC_SPIKE_THRESHOLD:
            log_alert("Traffic Spike Detected", packet)
            traffic_counter[src_ip] = 0

def packet_handler(packet):
    """Main packet processing function."""
    detect_malicious_ip(packet)
    detect_signature(packet)
    detect_port_scanning(packet)
    detect_traffic_anomalies(packet)

if __name__ == "__main__":
    logging.info("[INFO] Starting Intrusion Detection System...")
    scapy.sniff(prn=packet_handler, store=False)
