#!/usr/bin/env python3

# import modules
import subprocess
import time


# declare some variables
ip_list = ["8.8.8.8", "1.1.1.1"]
sleeptime = 1          # seconds
timeout = 1            # seconds
outage_sleeptime = 1    # seconds


# quick function definition
def ping_all(ip_list):

    # initialize list
    success_list = [False for i in ip_list]

    # loop over all ips and check if they can be pinged
    for idx in range(0, len(ip_list)):

        return_code = subprocess.run(
            f"ping -c 1 -t {timeout} {ip_list[idx]}",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True
        ).returncode

        if return_code == 0:
            success_list[idx] = True
        else:
            success_list[idx] = False

    return success_list


internet_out = False
while True:

    # check if internet is out by pinging
    success_list = ping_all(ip_list)

    if not all(success_list):
        internet_out = True
    else:
        internet_out = False

    # if internet is out, report an outage and calculate how long it
    # takes for it to come back online
    if internet_out:

        subprocess.run(
            "echo Internet outage detected. Determining outage length...",
            shell=True
        )
        outage_start_time = time.time()

        while internet_out:

            success_list = ping_all(ip_list)

            if any(success_list):
                internet_out = False

            time.sleep(outage_sleeptime)

        outage_end_time = time.time()
        outage_duration = outage_end_time - outage_start_time
        subprocess.run(
            "echo Internet was out for (min:sec): "
            f"{outage_duration / 60:.0f}:{outage_duration % 60:.0f}",
            shell=True
        )

    time.sleep(sleeptime)
