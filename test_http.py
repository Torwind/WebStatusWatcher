from web_status_watcher.network import HttpClient

client = HttpClient()

response = client.get("https://example.com")

print(response.status_code)
print(response.elapsed)
print(response.content_length)

client.close()