import os
def getCPUTemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return float((res.replace("temp=", "").replace("'C\n", "")))

print(getCPUTemperature())
