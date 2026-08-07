from web_status_watcher.network import HttpClient


client = HttpClient(
    timeout=5.0,
    retry_attempts=3,
    retry_delay=0,
)

response = client.get(
    "https://example.com",
)

print(response.status_code)
print(response.elapsed)
print(response.content_length)

client.close()