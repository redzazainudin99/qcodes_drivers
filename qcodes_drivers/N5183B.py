import numpy as np

from typing import Any
from qcodes.instrument_drivers.Keysight.N51x1 import N51x1
from qcodes.utils.validators import Arrays
 
"""""This driver has been updated to allow for frequency sweeps using the N5138B signal generator.
"""""


class LinSpaceSetpoints(Parameter):
    """A parameter which generates an array of evenly spaced setpoints from start, stop,
    and points parameters.
    """

    def __init__(
        self, name: str, start: Parameter, stop: Parameter, points: Parameter, **kwargs
    ):
        super().__init__(name, snapshot_get=False, snapshot_value=False, **kwargs)
        self._start = start
        self._stop = stop
        self._points = points

    def get_raw(self):
        return np.linspace(self._start(), self._stop(), self._points())



class N5183B(N51x1):
    def __init__(self, name: str, address: str, **kwargs: Any):
        super().__init__(name, address, min_power=-20, max_power=19, **kwargs)

        
        self.trigger_input_slope = Parameter(
            name="trigger_input_slope",
            instrument=self,
            get_cmd="TRIG:SLOP?",
            set_cmd="TRIG:SLOP {}",
            val_mapping={"positive": "POS", "negative": "NEG"},
        )

        #for step sweep

        self.frequency_mode = Parameter(
            name="frequency_mode",
            instrument=self,
            set_cmd="FREQ:MODE {}",
            get_cmd="FREQ:MODE?",
            val_mapping={"cw": "CW", "list": "LIST"},
            docstring="for step sweep, set to 'list'",
        )

        self.list_type = Parameter(
            name="list_type",
            instrument=self,
            set_cmd="LIST:TYPE {}",
            get_cmd="LIST:TYPE?",
            val_mapping={"step": "STEP", "list": "LIST"},
            docstring="for step sweep, set to 'STEP'",
        )

        self.frequency_start = Parameter(
            name="frequency_start",
            instrument=self,
            set_cmd='FREQ:STAR {:.5f}',
            get_cmd='FREQ:STAR?',
            get_parser=float,
            unit='Hz',
            vals=Numbers(min_value=9e3,max_value=13e9),
        )

        self.frequency_stop = Parameter(
            name="frequency_stop",
            instrument=self,
            set_cmd='FREQ:STOP {:.5f}',
            get_cmd='FREQ:STOP?',
            get_parser=float,
            unit='Hz',
            vals=Numbers(min_value=9e3,max_value=13e9),
        )

        self.sweep_points = Parameter(
            name="sweep_points",
            instrument=self,
            set_cmd='SWE:POIN {}',
            get_cmd='SWE:POIN?',
            get_parser=int,
        )

        self.dwell_time = Parameter(
            name="dwell_time",
            instrument=self,
            set_cmd='SWE:DWEL {:.2f}',
            get_cmd='SWE:DWEL?',
            get_parser=int,
            unit='S',
        )

        self.power_amp = Parameter(
            name="power_amplitude",
            instrument=self,
            set_cmd='POW:AMPL {:.2f}',
            get_cmd='POW:AMPL?',
            get_parser=float,
            unit='dBm',
            vals=Numbers(min_value=-20,max_value=19),
        )

        
        #trigger-related functions

        self.point_trigger_source = Parameter(
            name="point_trigger_source",
            instrument=self,
            get_cmd="LIST:TRIG:SOUR?",
            set_cmd="LIST:TRIG:SOUR {}",
            val_mapping={
                "bus": "BUS",
                "immediate": "IMM",
                "external": "EXT",
                "key": "KEY",
            },
        )

        self.output_trigger = Parameter(
            name="output_trigger",
            instrument=self,
            set_cmd='{}:OUTP SWE',
            get_cmd='?:OUTP SWE',
            get_parser=int,
            val_mapping={1: "TRIG1", 2: "TRIG2"},
            docstring="choose the output trigger port",
        )

        self.sweep_done = Parameter(
            name="sweep_done",
            instrument=self,
            get_cmd="STAT:OPER:COND?",
            get_parser=lambda x: int(x) & 8 == 0,
        )

        #added functions

        self.add_function(
            name="preset",
            call_cmd="*RST",
        )
        self.preset()

        self.add_function(
            name="clear_screen",
            call_cmd="*CLS",
        )

        self.add_function(
            name="start_sweep",
            call_cmd="INIT",
        )

        self.add_function(
            name="end_sweep",
            call_cmd="OUTP:STAT OFF",
        )

        #for twotone measurement

        self.frequencies = LinSpaceSetpoints(
            name="frequencies",
            instrument=self,
            start=self.frequency_start,
            stop=self.frequency_stop,
            points=self.sweep_points,
            unit="Hz",
            vals=Arrays(shape=(self.sweep_points.cache,)),
        )

     
