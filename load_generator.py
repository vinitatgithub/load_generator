import requests
import concurrent.futures
import time
import json

class LoadTest:
    def __init__(self, url, number_of_threads, requests_per_thread, request_type='GET', payload=None):
        self.url = url
        self.number_of_threads = number_of_threads
        self.requests_per_thread = requests_per_thread
        self.request_type = request_type.upper()  # Ensure request type is uppercase
        self.payload = payload
        self.total_requests = number_of_threads * requests_per_thread
        self.successful_requests = 0

    def start(self):
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.number_of_threads) as executor:
            futures = [
                executor.submit(self.send_request)
                for _ in range(self.total_requests)
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    response_code, response_text = future.result()
                    if response_code == 200 or response_code == 201:  # Consider successful responses based on status code
                        self.successful_requests += 1
                    print(f"Response Code: {response_code}")
                    print(f"Response: {response_text[:100]}")  # Print only the first 100 chars of the response
                except Exception as e:
                    print(f"Error: {e}")

        end_time = time.time()
        total_time = end_time - start_time
        self.calculate_throughput(total_time)

    def send_request(self):
        try:
            if self.request_type == 'GET':
                response = requests.get(self.url)
            elif self.request_type == 'POST':
                headers = {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Authorization': 'Bearer your_token',
                    'Content-Type': 'application/json'
                }
                response = requests.post(self.url, data=json.dumps(self.payload), headers=headers)
            else:
                raise ValueError("Unsupported request type: " + self.request_type)

            return response.status_code, response.text
        except Exception as e:
            return None, str(e)

    def calculate_throughput(self, total_time):
        throughput = self.successful_requests / total_time if total_time > 0 else 0
        print(f"Total Requests: {self.total_requests}")
        print(f"Successful Requests: {self.successful_requests}")
        print(f"Total Time Taken: {total_time:.2f} seconds")
        print(f"Throughput: {throughput:.2f} requests per second")


if __name__ == "__main__":
    url = "http://127.0.0.1:5000/post"  # Replace with your local server URL
    number_of_threads = 10  # Number of concurrent threads
    requests_per_thread = 5  # Number of requests per thread
    request_type = 'POST'  # 'GET' or 'POST'
    payload = {"key": "value"}  # Sample payload for POST requests

    load_test = LoadTest(url, number_of_threads, requests_per_thread, request_type, payload)
    load_test.start()
