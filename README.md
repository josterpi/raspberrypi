
Temperature logging setup
=========================

In `templogger.py` edit the value of `LOCATION_TAG` to some value to identify
where you're logging temperatures.

`> crontab -e`

```
# Log the temperature every minute to a database
* * * * * /home/josterpi/raspberrypi/templogger.py
```

You can see what the temperature is real time at http://raspberrypi/temp
