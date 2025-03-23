## Task description

Analyze logs (a folder consisting of `.log` files stored in HDFS) of a multithreaded Minecraft server. Calculate a day average of logs by a thread-type, output them as `{thread_type}\t{day_average}` and sort by an average in descending order. A sample of logs from a particular `.log` file looks like this:
```
[2017-12-31.00:08:50] [Server thread/INFO]: Mine was successfully updated.
[2017-12-31.00:08:50] [Server thread/INFO]: [Janitor] The trash will be cleaned up in 60 seconds!
[2017-12-31.00:08:53] [Craft Scheduler Thread - 89944/INFO]: [Metrics] Connection timed out
[2017-12-31.00:08:53] [Craft Scheduler Thread - 89940/INFO]: [Metrics] Connection timed out
[2017-12-31.00:09:50] [Server thread/INFO]: Mine was successfully updated.
[2017-12-31.00:09:09:50] [Server thread/INFO]: [Janitor] Trash will be removed in 0 seconds!
```

## Output example
```
Server	9876
AutoSaveWorld	9875
Main	9874
```