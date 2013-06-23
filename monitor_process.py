import argparse
import sys
import time
import datetime

import psutil


def main():
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument('-p', '--pid', metavar='PID', type=int,
                            help='Specify PID of the target process.')
    arg_parser.add_argument('-o', '--output-file', metavar='FILENAME', default='monitor_process_{0}.log', 
                            help='Specify the name of output file.')
    arg_parser.add_argument('-f', '--output-format', metavar='FORMAT', choices=('json', 'csv'),
                            help='Specify the output data format.')

    args = arg_parser.parse_args()
    if not args.pid:
        arg_parser.print_help()
        sys.exit(1)

    output_fo = open(args.output_file.format(args.pid), "w")
    target_process = psutil.Process(args.pid)
    while True:
        output_fo.write("TIME: {0}|".format(datetime.datetime.now()))
        output_fo.write("PID: {0}|".format(args.pid))
        output_fo.write("NAME: {0}|".format(target_process.name))
        output_fo.write("CPU%: {0}|".format(target_process.get_cpu_percent()))
        cpu_times = target_process.get_cpu_times()
        output_fo.write("CPU_USER: {0}|".format(cpu_times.user))
        output_fo.write("CPU_SYSTEM: {0}|".format(cpu_times.system))
        mem_info = target_process.get_memory_info()
        output_fo.write("MEM_RSS: {0}|".format(mem_info.rss))
        output_fo.write("MEM_VMS: {0}|".format(mem_info.vms))
        io_info = target_process.get_io_counters()
        output_fo.write("IO_READ_COUNT: {0}|".format(io_info.read_count))
        output_fo.write("IO_WRITE_COUNT: {0}|".format(io_info.write_count))
        output_fo.write("IO_READ_BYTES: {0}|".format(io_info.read_bytes))
        output_fo.write("IO_WRITE_BYTES: {0}|".format(io_info.write_bytes))
        output_fo.write("FDS: {0}|".format(target_process.get_num_fds()))
        output_fo.write("LOAD: {0}|".format(open("/proc/loadavg").read().strip()))
        output_fo.write("\n")
        output_fo.flush()
        time.sleep(1)
    

if __name__ == "__main__":
    main()
