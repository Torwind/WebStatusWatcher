from web_status_watcher.fingerprint import FingerprintHasher

html = "<html>Hello</html>"

hash1 = FingerprintHasher.sha256(html)

hash2 = FingerprintHasher.sha256(html)

print(hash1)

print(hash1 == hash2)