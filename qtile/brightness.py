import sys
import subprocess

def cmd_output_as_int(cmd):
    result = subprocess.check_output(cmd).decode('utf-8').replace('\n', '')
    result = int(result)
    return result

def exec_cmd(cmd):
    subprocess.call(cmd, shell=True)

def run():
    brightness_file = '/sys/class/backlight/intel_backlight/brightness'
    max_brightness_file = '/sys/class/backlight/intel_backlight/max_brightness'
    current_brightness = cmd_output_as_int(['cat', brightness_file])
    max_brightness = cmd_output_as_int(['cat', max_brightness_file])
    min_brightness = 50

    args = sys.argv[1:]

    if len(args) == 0:
        return

    value = int(args[-1])
    next_brightness = current_brightness

    if 'inc' in args:
        next_brightness += value

    if 'dec' in args:
        next_brightness -= value

    if next_brightness > max_brightness:
        return

    if next_brightness < min_brightness:
        return

    exec_cmd(f'echo {next_brightness} > {brightness_file}')

run()
