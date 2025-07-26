import hashlib

def generate_user_id(ssid: str) -> str:
    """
    Generate a consistent anonymized user ID based on SSID (Wi-Fi name).
    """
    return hashlib.sha256(ssid.encode()).hexdigest()[:16]
