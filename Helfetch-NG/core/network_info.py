# core/network_info.py

import subprocess
import requests
import json
import re
import socket # استيراد socket للحالة الاحتياطية لـ Local IP

def get_network_info():
    """
    Collects network-related information including local IP, public IP, ISP, and location.
    """
    info = {}

    # 1. Local IP Address
    local_ip = 'N/A'
    try:
        # Get default gateway IP for Linux
        result = subprocess.run(['ip', 'route', 'get', '1.1.1.1'], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if 'src' in line:
                match = re.search(r'src (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                if match:
                    local_ip = match.group(1)
                    break
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback for systems where 'ip route' might not work or for Windows
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) # Connect to a public server to get local IP
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            local_ip = 'N/A'
            
    info['Local IP'] = local_ip

    # 2. Public IP Address, ISP, and Location (City, Country)
    public_ip = 'N/A'
    isp = 'N/A'
    city = 'N/A'
    country = 'N/A'
    
    try:
        # Using ip-api.com for public IP, ISP, city, and country
        # This service has a rate limit for free tier (45 requests per minute from an IP)
        # **التغيير هنا: إضافة مهلة زمنية (timeout) للطلب**
        response = requests.get("http://ip-api.com/json/", timeout=2) # مهلة 2 ثانية
        data = json.loads(response.text)
        
        if data and data.get("status") == "success":
            public_ip = data.get("query", "N/A")
            isp = data.get("isp", "N/A")
            city = data.get("city", "N/A")
            country = data.get("country", "N/A")
            
    except requests.exceptions.RequestException as e:
        # Handle network errors, e.g., no internet connection or timeout
        # print(f"Network info error: {e}", file=sys.stderr) # لإظهار الخطأ إذا أردت تتبع المشكلة
        pass
    except json.JSONDecodeError:
        # Handle errors in parsing JSON response
        pass

    info['Public IP'] = public_ip
    info['ISP'] = isp
    info['City'] = city
    info['Country'] = country
    
    # 3. Bandwidth Usage (Sent/Received)
    sent_mb = 'N/A'
    recv_mb = 'N/A'
    try:
        # Linux specific: Parse /proc/net/dev
        with open('/proc/net/dev', 'r') as f:
            net_dev_content = f.readlines()
        
        # Skip header lines
        for line in net_dev_content[2:]:
            parts = line.split(':')
            if len(parts) == 2:
                interface_name = parts[0].strip()
                # Exclude loopback interface
                if interface_name != 'lo':
                    data = parts[1].split()
                    # Data columns: 0:bytes_received, 1:packets_received, ..., 8:bytes_transmitted
                    bytes_received = int(data[0])
                    bytes_transmitted = int(data[8])

                    # Convert to MB and round to one decimal place
                    recv_mb = f"{(bytes_received / (1024 * 1024)):.1f}MB"
                    sent_mb = f"{(bytes_transmitted / (1024 * 1024)):.1f}MB"
                    # We usually just pick the first non-loopback interface for simplicity
                    break
    except (FileNotFoundError, IndexError, ValueError):
        pass # Keep N/A if file not found or parsing fails
    
    info['Bandwidth Usage'] = f"Sent: {sent_mb}, Recv: {recv_mb}"

    return info

# For testing this module independently
if __name__ == "__main__":
    network_data = get_network_info()
    for key, value in network_data.items():
        print(f"{key}: {value}")
