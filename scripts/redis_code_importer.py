import csv
import json
import os
from typing import Optional

import redis
from sshtunnel import SSHTunnelForwarder

from ukrdc.services.codes import Codes

UKRDC_INSTANCE = "live_app_ssh"

code_conv_list_path = "conf/pv2_codes/code_conv_lists/"
code_list_path = "conf/pv2_codes/code_lists/"
code_exclusion_path = "conf/pv2_codes/code_exclusions/"
satellite_map_path = "conf/pv2_codes/satellite_map/satellite_map.csv"


def import_codes(host: str, port: int):
    r = redis.Redis(host=host, port=port, db=0)

    # Clear Existing Data
    r.flushall()

    # Code Map
    for filename in os.listdir(code_conv_list_path):
        csvreader = csv.reader(
            open(code_conv_list_path + filename, "r", newline="", encoding="utf-8")
        )

        print(f"Importing {filename}")
        for row in csvreader:
            source_coding_standard = row[0]
            source_code = row[1]
            destination_coding_standard = row[2]
            destination_code = row[3]

            Codes().set_code_mapping_item(
                r,
                source_coding_standard,
                source_code,
                destination_coding_standard,
                destination_code,
            )

    # Code List
    for filename in os.listdir(code_list_path):
        csvreader = csv.reader(
            open(code_list_path + filename, "r", newline="", encoding="utf-8")
        )

        print(f"Importing {filename}")
        for row in csvreader:
            coding_standard = row[0]
            try:
                code = row[1]
            except Exception:
                print(filename)
                print(row)
                raise

            if len(row) >= 3:
                description: Optional[str] = row[2]
            else:
                description = None

            if len(row) >= 4:
                code_type: Optional[str] = row[3]
            else:
                code_type = None

            if len(row) >= 5:
                units: Optional[str] = row[4]
            else:
                units = None

            key = "CODE_LIST:"
            key += coding_standard + ":"
            key += code

            if description:
                r.hset(key, "description", description)
            else:
                r.hset(key, "description", code)

            if code_type:
                r.hset(key, "code_type", code_type)

            if units:
                r.hset(key, "units", units)

    # Code Exclusions
    for filename in os.listdir(code_exclusion_path):
        csvreader = csv.reader(
            open(code_exclusion_path + filename, "r", newline="", encoding="utf-8")
        )

        for row in csvreader:

            coding_standard = row[0]
            code = row[1]
            system = row[2]

            Codes().set_code_exclusion(r, coding_standard, code, system)

    # Satellite Map

    csvreader = csv.reader(open(satellite_map_path, "r", newline="", encoding="utf-8"))

    for row in csvreader:
        satellite_code = row[0]
        main_unit_code = row[1]

        key = "SATELLITE_LIST:"
        key += satellite_code

        r.set(key, main_unit_code)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true")

    local: bool = parser.parse_args().local

    if local:
        import_codes("localhost", 6379)

    else:

        fname = os.path.expanduser("~/.config/ukrdc/services/db_conf.json")
        print("Configuration File: ", fname)
        with open(fname) as fhandle:
            params = json.load(fhandle)

        with SSHTunnelForwarder(
            (params[UKRDC_INSTANCE]["HOST"], 22),
            ssh_password=params[UKRDC_INSTANCE]["PASSWORD"],
            ssh_username=params[UKRDC_INSTANCE]["USER"],
            remote_bind_address=("localhost", 6379),
            # Make an SSH Tunnel to Redis on the chosen App Server
        ) as ukrdc_redis_tunnel:
            host = "localhost"
            port = ukrdc_redis_tunnel.local_bind_port
            import_codes(host, port)
