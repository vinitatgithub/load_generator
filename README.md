# Load Generator Script
This script can be run to generate load and calculate throughput for a given service.

Run the service under test and update the `url` variable in the script to point to the endpoint under test. Also update the `request_type` and `payload` variables and then run the python script.

## Output
* Total Requests: Total number of requests made during the test.
* Successful Requests: Total number of successful requests.
* Total Time Taken: The total execution time measured using time.time() at the start and end of the load test.
* Throughput: The throughput (requests per second) of the load test.