# Performance

Runs `wrk` against local instance.

## Usage

1. Edit `script.lua`

1. Edit parameters of following command

1. Run test:

  ```
  $ wrk \
    --threads 1 \
    --connections 1 \
    --duration 2s \
    --script script.lua \
    --latency \
      http://127.0.0.1:8081/repo/wg/wrk/refresh
  ```

## Sample results

```
...
Running 2s test @ http://127.0.0.1:8081/repo/wg/wrk/refresh
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    42.72ms    5.61ms  46.67ms   97.83%
    Req/Sec    23.00      4.70    30.00     70.00%
  Latency Distribution
     50%   43.33ms
     75%   43.37ms
     90%   43.40ms
     99%   46.67ms
  46 requests in 2.00s, 13.16KB read
Requests/sec:     22.96
Transfer/sec:      6.57KB
```
