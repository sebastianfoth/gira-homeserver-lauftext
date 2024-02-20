# coding: UTF-8
# MIT License
#
# Copyright (c) 2024 Sebastian Foth - Software Solutions
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class Lauftext20017(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "sebastianfoth_text_lauftext")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_INPUT_TEXT=1
        self.PIN_I_INPUT_UPDATE_IN_SEC=2
        self.PIN_I_INPUT_STEP=3
        self.PIN_I_INPUT_TEXT_WIDTH=4
        self.PIN_I_INPUT_START_POSITION=5
        self.PIN_I_INPUT_ON_OFF=6
        self.PIN_O_OUTPUT_TEXT=1

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

    def on_init(self):
        """Gets called on initialization. Contains all variable and service initializations"""

        # Initialize Debugger Section
        self.debugger_section = self.FRAMEWORK.create_debug_section()
        self.debugger_section.set_value("Status", "[OK] Initializing..")

        # Create a field for interval
        self.interval = None

        # Set all fields used for input
        self.value_input_text = None
        self.value_input_update_in_sec = None
        self.value_input_step = None
        self.value_input_text_width = None
        self.value_input_start_position = None
        self.value_input_on_off = None

        # Map the input to local fields for easier access
        self.map_input_to_local_values()

        # Set all fields used for text handling
        self.current_start_position = self.value_input_start_position
        self.output_text = ""

        # Debugger
        self.debugger_section.set_value("Status", "[OK] Initialized, waiting for start")

    def on_input_value(self, index, value):
        """Gets called if an input value on the logic element changes"""

        # Map all inputs
        self.map_input_to_local_values()

        # Abort if not all variables are set
        if not self.check_all_vars_set():
            self.debugger_section.set_value("Status", "[ERR] Not all variables set")
            self.stop_interval()
            return

        # Reset values for output creation
        self.current_start_position = 0

        # Stop if it is set to off
        if self.value_input_on_off == 0:
            self.debugger_section.set_value("Status", "[OK] Stopped due to external request")
            self.stop_interval()
            return

        # Start the interval
        self.initialize_interval()

        # Proper debug output
        self.debugger_section.set_value("Status", "[OK] Interval active, system OK")

    def on_interval(self):
        """Gets called by the interval. Contains all logic to update the scrolling text. Sends it to the output."""

        self.output_text = (self.value_input_text * 2)[
                           self.current_start_position:self.current_start_position + self.value_input_text_width]
        self.current_start_position = (self.current_start_position + self.value_input_step) % len(self.value_input_text)
        self._set_output_value(self.PIN_O_OUTPUT_TEXT, self.output_text)

    def map_input_to_local_values(self):
        """Maps the inputs to local variables within the class"""

        self.value_input_text = self._get_input_value(self.PIN_I_INPUT_TEXT)
        self.value_input_update_in_sec = self._get_input_value(self.PIN_I_INPUT_UPDATE_IN_SEC)
        self.value_input_step = self._get_input_value(self.PIN_I_INPUT_STEP)
        self.value_input_text_width = self._get_input_value(self.PIN_I_INPUT_TEXT_WIDTH)
        self.value_input_start_position = self._get_input_value(self.PIN_I_INPUT_START_POSITION)
        self.value_input_on_off = self._get_input_value(self.PIN_I_INPUT_ON_OFF)

    def check_all_vars_set(self):
        """Checks if all required variables are set"""

        return self.value_input_text is not None and self.value_input_update_in_sec is not None and self.value_input_step is not None and self.value_input_text_width is not None and self.value_input_start_position is not None and self.value_input_on_off is not None

    def initialize_interval(self):
        """Initializes the internally used interval"""
        self.stop_interval()

        self.interval = self.FRAMEWORK.create_interval()
        self.interval.set_interval(self.value_input_update_in_sec * 1000, self.on_interval)
        self.interval.start()

    def stop_interval(self):
        """Stops the internally used interval.

        Attention: This method not only stops the interval but also removes the reference to it. Gira seems to have issues when we are just stopping the interval created during initialization, as this leads to multiple active intervals from time to time."""

        if not self.interval is None:
            self.interval.stop()
            self.interval = None
