from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

from ctypes import cast, POINTER, c_ushort

from mcculw import ul
from mcculw.enums import (InterfaceType, ScanOptions, Status, FunctionType, ChannelType,
                          ULRange, DigitalPortType, TriggerSensitivity,
                          TriggerEvent, TriggerSource)
from mcculw.ul import ULError
from mcculw.device_info import DaqDeviceInfo

import time

use_device_detection = True
board_num = 0

chan_list = []
chan_type_list = []
gain_list = []
num_chans = 1

try:
    if use_device_detection:
        ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.ANY)
        ul.create_daq_device(board_num, devices[0])

    device_info = DaqDeviceInfo(board_num)
    
    if device_info.supports_daq_input:

        for i in range(0,num_chans):
            chan_list.append(i)
            chan_type_list.append(ChannelType.ANALOG)
            gain_list.append(ULRange.UNI10VOLTS)
            
        chan_list.append(0)
        chan_type_list.append(ChannelType.CTR16)
        gain_list.append(ULRange.NOTUSED)
               
except:
    print('ok')
    
    
    
rate = 200000
points_per_channel = 10
total_count = points_per_channel * (num_chans)
scan_options = (ScanOptions.BACKGROUND |
                ScanOptions.CONTINUOUS | ScanOptions.EXTTRIGGER)

# Allocate a buffer for the scan
memhandle = ul.win_buf_alloc(total_count)

#Set the start trigger settings
ul.daq_set_trigger(board_num, TriggerSource.EXTTTL,
                  TriggerSensitivity.RISING_EDGE,
                  chan_list[-1], chan_type_list[-1],
                  gain_list[-1], 5, 0, TriggerEvent.START)

c = chan_list[0:8]
# Run the scan
ul.daq_in_scan(board_num, chan_list[0:8], chan_type_list[0:8],
                gain_list[0:8], num_chans, rate, 0, total_count,
                memhandle, scan_options)

time.sleep(1)

ul.stop_background(board_num, FunctionType.DAQIFUNCTION)

    # Cast the memhandle to a ctypes pointer
    # Note: the ctypes array will only be valid until win_buf_free
    # is called.
    # A copy of the buffer can be created using win_buf_to_array
    # before the memory is freed. The copy can be used at any time.
ctypes_array = cast(memhandle, POINTER(c_ushort))

row_format = '{:>5}' + '{:>10}' * num_chans

# Print the channel name headers
labels = ['Index']
for ch_index in range(num_chans):
    channel_label = {
        ChannelType.ANALOG: lambda:
            'AI' + str(chan_list[ch_index]),
        ChannelType.ANALOG_DIFF: lambda:
            'AI' + str(chan_list[ch_index]),
        ChannelType.ANALOG_SE: lambda:
            'AI' + str(chan_list[ch_index]),
        ChannelType.DIGITAL: lambda:
            chan_list[ch_index].name,
        ChannelType.CTR: lambda:
            'CI' + str(chan_list[ch_index]),
    }[chan_type_list[ch_index]]()
    labels.append(channel_label)
print(row_format.format(*labels))

# Print the data
data_index = 0
for index in range(points_per_channel):
    display_data = [index]
    for ch_index in range(num_chans):
        data_label = {
            ChannelType.ANALOG: lambda:
                '{:.3f}'.format(ctypes_array[data_index]),
            ChannelType.ANALOG_DIFF: lambda:
                '{:.3f}'.format(ctypes_array[data_index]),
            ChannelType.ANALOG_SE: lambda:
                '{:.3f}'.format(ctypes_array[data_index]),
            ChannelType.DIGITAL: lambda:
                '{:d}'.format(int(ctypes_array[data_index])),
            ChannelType.CTR: lambda:
                '{:d}'.format(int(ctypes_array[data_index])),
        }[chan_type_list[ch_index]]()

        display_data.append(data_label)
        data_index += 1
    # Print this row
    print(row_format.format(*display_data))

