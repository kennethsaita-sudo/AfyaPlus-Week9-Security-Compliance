from urllib.parse import urlparse

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}

def transit_ok(url: str) -> bool:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.hostname:
        return False
    if parsed.hostname in LOCAL_HOSTS:
        return parsed.scheme in {"http", "https"}
    return parsed.scheme == "https"

def require_safe_transit(url: str) -> None:
    if not transit_ok(url):
        raise ValueError("Cleartext non-localhost URL denied")

if __name__ == "__main__":
    assert transit_ok("http://localhost:8000")
    assert transit_ok("https://partner.example.org/api")
    assert not transit_ok("http://partner.example.org/api")
    print("PASS: TLS policy denies cleartext production hosts")
