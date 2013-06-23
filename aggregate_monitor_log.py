import sys
import re
import argparse


def get_param_value(line, param_name):
    raw_params = line.split("|")
    for raw_param in raw_params:
        if raw_param.find(param_name) != -1:
            param_name, param_value = raw_param.split(":")
            return param_value

def main():
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument('-s', '--start-date', metavar='DATETIME', 
                            help='''Specify the date and time from which script should collect data. 
                                    Date format: YYYY-mm-dd HH:MM:SS''')
    arg_parser.add_argument('-f', '--finish-date', metavar='DATETIME', 
                            help='Specify the date and time until which script should collect data.')

    args = arg_parser.parse_args()
    if (not args.start_date and 
        not args.finish_date):
        arg_parser.print_help()
        sys.exit(1)

    log_lines = sys.stdin.readlines()
    filtered_log_lines = []
    need_to_add = False
    for line in log_lines:
        if (args.start_date and
            re.search(args.start_date, line)):
            need_to_add = True
        if (args.finish_date and
            re.search(args.finish_date, line)):
            need_to_add = False

        if need_to_add:
            filtered_log_lines.append(line)

    interesting_params = ('CPU_USER', 'CPU_SYSTEM', 'IO_READ_COUNT', 'IO_WRITE_COUNT', 'LOAD')
    first_line = filtered_log_lines[0]
    last_line = filtered_log_lines[-1]
    total_cpu_user = float(get_param_value(last_line, "CPU_USER")) -  float(get_param_value(first_line, "CPU_USER"))
    total_cpu_system = float(get_param_value(last_line, "CPU_SYSTEM")) -  float(get_param_value(first_line, "CPU_SYSTEM"))
    io_read_count = float(get_param_value(last_line, "IO_READ_COUNT")) -  float(get_param_value(first_line, "IO_READ_COUNT"))
    io_write_count = float(get_param_value(last_line, "IO_WRITE_COUNT")) -  float(get_param_value(first_line, "IO_WRITE_COUNT"))

    sum_cpu_percent = 0
    line_count = len(filtered_log_lines)
    for line in filtered_log_lines:
        sum_cpu_percent += float(get_param_value(line, "CPU%"))
        sys.stdout.write(line)

    print("DEBUG: avg_cpu_percent is {:.2f}".format(sum_cpu_percent/line_count))
    print("DEBUG: total_cpu_user is {0}".format(total_cpu_user))
    print("DEBUG: total_cpu_system is {0}".format(total_cpu_system))
    print("DEBUG: total_cpu is {0}".format(total_cpu_system + total_cpu_user))
    print("DEBUG: io_read_count is {0}".format(io_read_count))
    print("DEBUG: io_write_count is {0}".format(io_write_count))


if __name__ == "__main__":
    main()
