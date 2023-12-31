"""
File:                       DaqSetTrigger01.py

Library Call Demonstrated:  mcculw.ul.daq_set_trigger()

Purpose:                    Sets start and stop triggers. These triggers are
                            used to initiate and terminate A/D conversion using
                            mcculw.ul.daq_in_scan(), with
                            mcculw.enums.ScanOptions.EXTTRIGGER selected.

Demonstration:              Sets start and stop triggers
                            and displays the input channels data.

Other Library Calls:        mcculw.ul.win_buf_alloc()
                            mcculw.ul.win_buf_free()
                            mcculw.ul.daq_in_scan()
                            mcculw.ul.get_status()
                            mcculw.ul.to_eng_units()
                            mcculw.ul.stop_background()

Special Requirements:       Device must support mcculw.ul.daq_in_scan().
                            Channel 0 should have a signal that transitions
                            from below 2V to above applied.
                            Counter 0 should have a TTL signal applied.
"""
from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

import tkinter as tk
from tkinter import messagebox
from ctypes import cast, POINTER, c_ushort

from mcculw import ul
from mcculw.enums import (ScanOptions, Status, FunctionType, ChannelType,
                          ULRange, DigitalPortType, TriggerSensitivity,
                          TriggerEvent, TriggerSource)
from mcculw.ul import ULError
from mcculw.device_info import DaqDeviceInfo

try:
    from ui_examples_util import UIExample, show_ul_error
except ImportError:
    from .ui_examples_util import UIExample, show_ul_error


class DaqSetTrigger01(UIExample):
    def __init__(self, master=None):
        super(DaqSetTrigger01, self).__init__(master)
        # By default, the example detects all available devices and selects the
        # first device listed.
        # If use_device_detection is set to False, the board_num property needs
        # to match the desired board number configured with Instacal.
        use_device_detection = True
        self.board_num = 0

        self.chan_list = []
        self.chan_type_list = []
        self.gain_list = []
        self.num_chans = 10

        try:
            if use_device_detection:
                self.configure_first_detected_device()

            self.device_info = DaqDeviceInfo(self.board_num)
            if self.device_info.supports_daq_input:
                self.init_scan_channel_info()
                self.create_widgets()
            else:
                self.create_unsupported_widgets()
        except ULError:
            self.create_unsupported_widgets(True)

    def init_scan_channel_info(self):
        # Add analog input channels
        for i in range(0,7):
            self.chan_list.append(i)
            self.chan_type_list.append(ChannelType.ANALOG_SE)
            self.gain_list.append(ULRange.UNI10VOLTS)
        

        # Add a digital input channel
        self.chan_list.append(DigitalPortType.FIRSTPORTA)
        self.chan_type_list.append(ChannelType.DIGITAL8)
        self.gain_list.append(ULRange.NOTUSED)

        # Add a counter input channel
        self.chan_list.append(0)
        self.chan_type_list.append(ChannelType.CTR16)
        self.gain_list.append(ULRange.NOTUSED)
        

    def start_scan(self):
        rate = 100
        points_per_channel = 100
        total_count = points_per_channel * self.num_chans
        scan_options = (ScanOptions.BACKGROUND |
                        ScanOptions.CONTINUOUS | ScanOptions.EXTTRIGGER)

        # Allocate a buffer for the scan
        self.memhandle = ul.win_buf_alloc(total_count)

        # Check if the buffer was successfully allocated   
        if not self.memhandle:
            messagebox.showerror("Error", "Failed to allocate memory")
            self.start_button["state"] = tk.NORMAL
            return

        try:
            # Set the start trigger settings
            ul.daq_set_trigger(self.board_num, TriggerSource.EXTTTL,
                               TriggerSensitivity.RISING_EDGE,
                               self.chan_list[0], self.chan_type_list[0],
                               self.gain_list[0], 5, 0, TriggerEvent.START)
            
            # Set the stop trigger settings
#            ul.daq_set_trigger(self.board_num, TriggerSource.EXTTTL,
#                               TriggerSensitivity.ABOVE_LEVEL,
#                               self.chan_list[2], self.chan_type_list[2],
#                               self.gain_list[2], 2, 0, TriggerEvent.STOP)

            # Run the scan
            ul.daq_in_scan(self.board_num, self.chan_list, self.chan_type_list,
                           self.gain_list, self.num_chans, rate, 0, total_count,
                           self.memhandle, scan_options)

            # Cast the memhandle to a ctypes pointer
            # Note: the ctypes array will only be valid until win_buf_free
            # is called.
            # A copy of the buffer can be created using win_buf_to_array
            # before the memory is freed. The copy can be used at any time.
            self.array = cast(self.memhandle, POINTER(c_ushort))
        except ULError as e:
            # Free the allocated memory
            ul.win_buf_free(self.memhandle)
            show_ul_error(e)
            return

        # Start updating the displayed values
        self.update_displayed_values()

    def update_displayed_values(self):
        # Get the status from the device
        status, curr_count, curr_index = ul.get_status(
            self.board_num, FunctionType.DAQIFUNCTION)

        # Display the status info
        self.update_status_labels(status, curr_count, curr_index)

        # Display the values
        self.display_values(curr_index, curr_count)

        # Call this method again until the stop button is pressed
        if status == Status.RUNNING:
            self.after(100, self.update_displayed_values)
        else:
            # Free the allocated memory
            ul.win_buf_free(self.memhandle)
            self.set_ui_idle_state()

    def update_status_labels(self, status, curr_count, curr_index):
        if status == Status.IDLE:
            self.setpoint_status_label["text"] = "Idle"
        else:
            self.setpoint_status_label["text"] = "Running"

        self.index_label["text"] = str(curr_index)
        self.count_label["text"] = str(curr_count)

    def display_values(self, curr_index, curr_count):
        array = self.array

        # If no data has been gathered, don't add data to the labels
        if curr_count > 1:
            # Convert the analog value to volts and display it
            chan_0_eng_value = ul.to_eng_units(
                self.board_num, self.gain_list[0], array[curr_index])
            self.chan_0_label["text"] = '{:.3f}'.format(
                chan_0_eng_value) + " Volts"

            # Display the digital port value as hex
            self.digital_label["text"] = '0x' + \
                '{:0<2X}'.format(array[curr_index + 1])

            # Display the counter value
            self.counter_0_label["text"] = str(array[curr_index + 2])

    def stop(self):
        ul.stop_background(self.board_num, FunctionType.DAQIFUNCTION)

    def set_ui_idle_state(self):
        self.start_button["command"] = self.start
        self.start_button["text"] = "Start"

    def start(self):
        self.start_button["command"] = self.stop
        self.start_button["text"] = "Stop"
        self.start_scan()

    def create_widgets(self):
        '''Create the tkinter UI'''
        self.device_label = tk.Label(self)
        self.device_label.pack(fill=tk.NONE, anchor=tk.NW)
        self.device_label["text"] = ('Board Number ' + str(self.board_num)
                                     + ": " + self.device_info.product_name
                                     + " (" + self.device_info.unique_id + ")")

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.X, anchor=tk.NW)

        curr_row = 0
        chan_0_left_label = tk.Label(main_frame, justify=tk.LEFT, padx=3)
        chan_0_left_label["text"] = "Channel 0:"
        chan_0_left_label.grid(row=curr_row, column=0, sticky=tk.W)

        self.chan_0_label = tk.Label(main_frame, justify=tk.LEFT, padx=3)
        self.chan_0_label.grid(row=curr_row, column=1, sticky=tk.W)

        curr_row += 1
        digital_left_label = tk.Label(main_frame, justify=tk.LEFT, padx=3)
        digital_left_label["text"] = "FIRSTPORTA:"
        digital_left_label.grid(row=curr_row, column=0, sticky=tk.W)

        self.digital_label = tk.Label(main_frame, justify=tk.LEFT, padx=3)
        self.digital_label.grid(row=curr_row, column=1, sticky=tk.W)

        curr_row += 1
        counter_0_left_label = tk.Label(
            main_frame, justify=tk.LEFT, padx=3)
        counter_0_left_label["text"] = "Counter 0:"
        counter_0_left_label.grid(row=curr_row, column=0, sticky=tk.W)

        self.counter_0_label = tk.Label(
            main_frame, justify=tk.LEFT, padx=3)
        self.counter_0_label.grid(row=curr_row, column=1, sticky=tk.W)

        curr_row += 1
        setpoint_status_left_label = tk.Label(
            main_frame, justify=tk.LEFT, padx=3)
        setpoint_status_left_label["text"] = "Status:"
        setpoint_status_left_label.grid(
            row=curr_row, column=0, sticky=tk.W)

        self.setpoint_status_label = tk.Label(
            main_frame, justify=tk.LEFT, padx=3)
        self.setpoint_status_label["text"] = "Idle"
        self.setpoint_status_label.grid(
            row=curr_row, column=1, sticky=tk.W)

        curr_row += 1
        index_left_label = tk.Label(main_frame, justify=tk.LEFT, padx=3)
        index_left_label["text"] = "Index:"
        index_left_label.grid(row=curr_row, column=0, sticky=tk.W)

        self.index_label = tk.Label(main_frame, justify=tk.LEFT, padx=3)
        self.index_label["text"] = "-1"
        self.index_label.grid(row=curr_row, column=1, sticky=tk.W)

        curr_row += 1
        count_left_label = tk.Label(main_frame, justify=tk.LEFT, padx=3)
        count_left_label["text"] = "Count:"
        count_left_label.grid(row=curr_row, column=0, sticky=tk.W)

        self.count_label = tk.Label(main_frame, justify=tk.LEFT, padx=3)
        self.count_label["text"] = "0"
        self.count_label.grid(row=curr_row, column=1, sticky=tk.W)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.RIGHT, anchor=tk.SE)

        self.start_button = tk.Button(button_frame)
        self.start_button["text"] = "Start"
        self.start_button["command"] = self.start
        self.start_button.grid(row=0, column=0, padx=3, pady=3)

        quit_button = tk.Button(button_frame)
        quit_button["text"] = "Quit"
        quit_button["command"] = self.master.destroy
        quit_button.grid(row=0, column=1, padx=3, pady=3)


if __name__ == "__main__":
    # Start the example
    DaqSetTrigger01(master=tk.Tk()).mainloop()
