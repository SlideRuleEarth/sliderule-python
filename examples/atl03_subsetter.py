# Imports
import os
import sys
import math
import time
import argparse
import configparser
import logging
import traceback
import multiprocessing
import sliderule
from datetime import datetime, timedelta
from sliderule import icesat2, earthdata

# Command Line Arguments
parser = argparse.ArgumentParser(description="""Subset ATL03 granules""")
parser.add_argument('--domain',         '-d', type=str, default="slideruleearth.io")
parser.add_argument('--organization',   '-o', type=str, default="developers")
parser.add_argument('--desired_nodes',  '-n', type=int, default=1)
parser.add_argument('--time_to_live',   '-l', type=int, default=120) # minutes
parser.add_argument('--aoi',            '-a', type=str, default="examples/grandmesa.geojson")
parser.add_argument('--rgt',                  type=int, default=None)
parser.add_argument('--cycle',                type=int, default=None)
parser.add_argument('--region' ,              type=int, default=None)
parser.add_argument('--track',                type=int, default=None)
parser.add_argument('--beam',                 type=str, nargs='+', default=['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r'])
parser.add_argument('--pass_invalid',         action='store_true', default=False)
parser.add_argument('--cnf',                  type=int, default=icesat2.CNF_NOT_CONSIDERED)
parser.add_argument('--ats',                  type=int, default=None)
parser.add_argument('--cnt',                  type=int, default=None)
parser.add_argument('--len',                  type=int, default=None)
parser.add_argument('--res',                  type=int, default=None)
parser.add_argument('--subset_pixel_size',    type=float, default=None)
parser.add_argument('--proj',                 type=str, default=None)
parser.add_argument('--ignore_poly_for_cmr',  type=bool, default=None)
parser.add_argument('--name',                 type=str, default='output')
parser.add_argument('--no_geo',               action='store_true', default=False)
parser.add_argument('--output_path',    '-p', type=str, default="hosted") # "hosted" tells sliderule to host results in a bucket it owns
parser.add_argument('--timeout',        '-t', type=int, default=600) # seconds
parser.add_argument('--generate',             action='store_true', default=False)
parser.add_argument('--simulate_delay',       type=float, default=1)
parser.add_argument('--startup_wait',         type=int, default=120) # seconds
parser.add_argument('--granules_per_request', type=int, default=None) # None == all granules
parser.add_argument('--concurrent_requests',  type=int, default=1)
parser.add_argument('--slice',                type=int, nargs=2, default=None)
parser.add_argument('--log_file',       '-f', type=str, default="sliderule.log")
parser.add_argument('--verbose',        '-v', action='store_true', default=False)
args,_ = parser.parse_known_args()

# Setup Log File
LOG_FORMAT              = '%(created)f %(levelname)-5s [%(filename)s:%(lineno)5d] %(message)s'
log                     = logging.getLogger(__name__)
format                  = logging.Formatter(LOG_FORMAT)
logfile                 = logging.FileHandler(args.log_file)
logfile.setFormatter(format)
log.addHandler(logfile)
log.setLevel(logging.INFO)
logfile.setLevel(logging.INFO)

# Setup Config Parser for Credentials
home_directory          = os.path.expanduser('~')
aws_credential_file     = os.path.join(home_directory, '.aws', 'credentials')
config                  = configparser.RawConfigParser()

# Check for Hosted Option
if args.output_path == "hosted":
    credentials = None
else:
    credentials = {}

# Check Organization
organization            = args.organization
desired_nodes           = args.desired_nodes
if args.organization == "None":
    organization        = None
    desired_nodes       = None

# Get Area of Interest
if args.subset_pixel_size:
    region = sliderule.toregion(args.aoi, cellsize=args.subset_pixel_size)
    raster = region["raster"]
else:
    region = sliderule.toregion(args.aoi)
    raster = None

# Populate Request Parameters
parms = {
    "asset": "icesat2",
    "poly": region["poly"],
    "raster": raster,
    "proj": args.proj,
    "ignore_poly_for_cmr": args.ignore_poly_for_cmr,
    "rgt": args.rgt,
    "cycle": args.cycle,
    "region": args.region,
    "pass_invalid": args.pass_invalid,
    "cnf": args.cnf,
    "ats": args.ats,
    "cnt": args.cnt,
    "len": args.len,
    "res": args.res,
    "timeout": args.timeout,
    "output": {
        "path": "",
        "format": "parquet",
        "as_geo": not args.no_geo,
        "open_on_complete": False,
        "region": "us-west-2",
        "credentials": credentials
    }
}

# Clear Out None Keys
keys_to_delete = []
for key in parms:
    if parms[key] == None:
        keys_to_delete.append(key)
for key in keys_to_delete:
    del parms[key]

# Get Resources
resources = earthdata.search(parms)
if args.slice != None:
    resources = resources[args.slice[0]:args.slice[1]]

# Calculate Requests
requests = []
granules_per_request = len(resources)
if granules_per_request == 0:
    log.critical(f'no resources to process, exiting')
    sys.exit(0)    
if args.granules_per_request != None:
    granules_per_request = args.granules_per_request
for i in range(0, len(resources), granules_per_request):
    requests.append(resources[i:i+granules_per_request])

# Display Parameters
log.info(f'organization = {organization}')
log.info(f'desired_nodes = {desired_nodes}')
log.critical(f'logfile = {args.log_file}')
log.info(f'concurrent_requests = {args.concurrent_requests}')
log.info(f'granules_per_request = {granules_per_request}')
log.info(f'num_granules = {len(resources)}')
log.info(f'parms = \n{parms}')

# Create Request Queue
rqst_q = multiprocessing.Queue()

#
# Update Credentials
#
def update_credentials(worker_id):

    # Log Maintanence Action
    now = datetime.now()
    expiration = now + timedelta(minutes=args.time_to_live)
    log.info(f'<{worker_id}> updating capacity and credentials until {expiration.strftime("%I:%M:%S")}')

    # Update Pending Capacity of Cluster
    if args.generate:
        sliderule.update_available_servers(desired_nodes=desired_nodes, time_to_live=args.time_to_live)
    elif args.simulate_delay > 0:
        time.sleep(args.simulate_delay)

    # Read AWS Credentials
    if credentials != None:
        config.read(aws_credential_file)
        parms["output"]["credentials"] = {
            "aws_access_key_id": config.get('default', 'aws_access_key_id'),
            "aws_secret_access_key": config.get('default', 'aws_secret_access_key'),
            "aws_session_token": config.get('default', 'aws_session_token')
        }

    # Finish Request
    log.info(f'<{worker_id}> finished update')

#
# Process Request
#
def process_request(worker_id, count, resources):

    # Start Processing
    log.info(f'<{worker_id}> processing {len(resources)} resources: {resources[0]} ...')

    # Set Output Path
    if credentials != None:
        parms["output"]["path"] = f'{args.output_path}/{args.name}_{count}.{"parquet" if args.no_geo else "geoparquet"}'
    else:
        parms["output"]["asset"] = "sliderule-stage"

    # Make Request
    if args.generate:
        outfile = icesat2.atl03sp(parms, resources=resources)
    else:
        outfile = parms["output"]["path"]
        if args.simulate_delay > 0:
            time.sleep(args.simulate_delay)

    # Finish Request
    log.info(f'<{worker_id}> finished {len(resources)} resources: {resources[0]} ...')
    log.info(f'<{worker_id}> writing {outfile}')

#
# Worker
#
def worker(worker_id):

    # Initialize Python Client
    if args.generate:
        icesat2.init(args.domain, verbose=args.verbose, loglevel=logging.INFO, organization=organization, desired_nodes=desired_nodes, time_to_live=args.time_to_live, rethrow=True)
        log.info(f'<{worker_id}> waiting {args.startup_wait} seconds for the newly created cluster to obtain credentials')
        time.sleep(args.startup_wait)
    elif args.simulate_delay > 0:
        time.sleep(args.simulate_delay)

    # While Queue Not Empty
    complete = False
    while not complete:

        # Get Request
        try:
            count, resources = rqst_q.get(block=False)
        except Exception as e:
            # Handle No More Requests
            if rqst_q.empty():
                log.info(f'<{worker_id}> no more requests {e}')
                complete = True                
            else:
                log.info(f'<{worker_id}> exception: {e}')
            time.sleep(5) # prevents a spin
            continue

        # Process Request
        attempts = 3
        success = False
        while attempts > 0 and not success:
            attempts -= 1
            try:
                update_credentials(worker_id)
                process_request(worker_id, count, resources)
                success = True
            except Exception as e:
                log.critical(f'attempt {3 - attempts} of 3 failed to process: {e}')
                print(traceback.format_exc())

# Queue Processing Requests
count = 0
for rqst in requests:
    log.debug(f'queueing processing request of {len(rqst)} resources: {rqst[0]} ...')
    rqst_q.put((count, rqst))
    count += 1

# Create Workers
processes = [multiprocessing.Process(target=worker, args=(worker_id,), daemon=True) for worker_id in range(args.concurrent_requests)]

# Start Workers
for process in processes:
    process.start()

# Wait for Workers to Complete
for process in processes:
    process.join()
log.info('all processing requests completed')   
