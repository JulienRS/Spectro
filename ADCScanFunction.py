from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

from ctypes import cast, POINTER, c_ushort

import time

from mcculw import ul
from mcculw.enums import (ScanOptions, Status, FunctionType, ChannelType,
                          ULRange, DigitalPortType, TriggerSensitivity,
                          TriggerEvent, TriggerSource, InterfaceType)
from mcculw.ul import ULError
from mcculw.device_info import DaqDeviceInfo

try:
    from ui_examples_util import UIExample, show_ul_error
except ImportError:
    from .ui_examples_util import UIExample, show_ul_error


def ADCScanFunction(mc):

        use_device_detection = True
        board_num = 0

        chan_list = []
        chan_type_list = []
        gain_list = []
        num_chans = 8

        try:
            if use_device_detection:
                ul.ignore_instacal()
                devices = ul.get_daq_device_inventory(InterfaceType.ANY)
                ul.create_daq_device(board_num, devices[0])

            device_info = DaqDeviceInfo(board_num)
            
            if device_info.supports_daq_input:

                for i in range(0,1):
                    chan_list.append(i)
                    chan_type_list.append(ChannelType.ANALOG_SE)
                    gain_list.append(ULRange.UNI5VOLTS)
                    
                # chan_list.append(0)
                # chan_type_list.append(ChannelType.CTR16)
                # gain_list.append(ULRange.NOTUSED)
                    
                    
        except:
            print('ok')
            
            
            
        rate = 200000
        points_per_channel = 200
        total_count = points_per_channel * (num_chans)
        scan_options = (ScanOptions.FOREGROUND | ScanOptions.EXTTRIGGER)

        # Allocate a buffer for the scan
        memhandle = ul.win_buf_alloc_32(total_count)

        #Set the start trigger settings
        ul.daq_set_trigger(board_num, TriggerSource.EXTTTL,
                          TriggerSensitivity.HIGH_LEVEL,
                          chan_list[-1], chan_type_list[-1],
                          gain_list[-1], 3.3, 0, TriggerEvent.START)
        

        c = chan_list[0]
        # Run the scan
        ul.daq_in_scan(board_num, chan_list[0], chan_type_list[0],
                        gain_list[0], num_chans, rate, 0, total_count,
                        memhandle, scan_options)

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
                # ChannelType.ANALOG: lambda:
                #     'AI' + str(chan_list[ch_index]),
                # ChannelType.ANALOG_DIFF: lambda:
                #     'AI' + str(chan_list[ch_index]),
                ChannelType.ANALOG_SE: lambda:
                    'AI' + str(chan_list[ch_index]),
                # ChannelType.DIGITAL: lambda:
                #     chan_list[ch_index].name,
                # ChannelType.CTR: lambda:
                #     'CI' + str(chan_list[ch_index]),
            }[chan_type_list[ch_index]]()
            labels.append(channel_label)
        print(row_format.format(*labels))

        # Print the data
        data_index = 0
        for index in range(points_per_channel):
            display_data = [index]
            for ch_index in range(num_chans):
                data_label = {
                    # ChannelType.ANALOG: lambda:
                    #     '{:.3f}'.format(ctypes_array[data_index]),
                    # ChannelType.ANALOG_DIFF: lambda:
                    #     '{:.3f}'.format(ctypes_array[data_index]),
                    ChannelType.ANALOG_SE: lambda:
                        '{:.3f}'.format(ctypes_array[data_index]),
                    # ChannelType.DIGITAL: lambda:
                    #     '{:d}'.format(int(ctypes_array[data_index])),
                    # ChannelType.CTR: lambda:
                    #     '{:d}'.format(int(ctypes_array[data_index])),
                }[chan_type_list[ch_index]]()

                display_data.append(data_label)
                data_index += 1
            # Print this row
            print(row_format.format(*display_data))