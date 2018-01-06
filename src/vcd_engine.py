import operator

from functools import reduce

from Verilog_VCD.Verilog_VCD import parse_vcd


class VCDEngine(object):
    trace_element_mapping = [
        (["instruction"], 0, 32),
        (["address"], 32, 64),
        (["pass_through"], 64, 65),
        (["if_data", "time_start"], 65, 97),
        (["if_data", "time_end"], 97, 129),
        (["if_data", "mem_access_req", "time_start"], 129, 161),
        (["if_data", "mem_access_req", "time_end"], 161, 193),
        (["if_data", "mem_access_res", "time_start"], 193, 225),
        (["if_data", "mem_access_res", "time_end"], 225, 257),
        (["id_data", "time_start"], 257, 289),
        (["id_data", "time_end"], 289, 321),
        (["ex_data", "time_start"], 322, 354),
        (["ex_data", "time_end"], 354, 386),
        (["ex_data", "mem_access_req", "time_start"], 386, 418),
        (["ex_data", "mem_access_req", "time_end"], 418, 450),
        (["wb_data", "time_start"], 450, 482),
        (["wb_data", "time_end"], 482, 514),
        (["wb_data", "mem_access_res", "time_start"], 514, 546),
        (["wb_data", "mem_access_res", "time_end"], 546, 578)
    ]

    def extract_tracing_information(self, vcd_file):
        # Grab the required signal trace from the VCD file
        parsed = [
            v['tv'] for _, v in
            parse_vcd(str(vcd_file),
                      siglist=["ryuki_testbench.tracer.trace_data_o[31:0]"],
                      opt_timescale="ns").items()
        ][0]
        # Reformat the data so that it's an object containing each data
        # item rather than one large bit string.
        processed_data = [(time, TraceElement(bitstring, [["pass_through"]],
                                              self.trace_element_mapping))
                          for (time, bitstring) in parsed[1:]]
        return processed_data


class TraceElement(object):

    instruction = ""
    address = ""
    if_data = {}
    id_data = {}
    ex_data = {}
    wb_data = {}

    def __init__(self, bitstring, fields_to_ignore, trace_element_mapping):
        self.if_data = {
            "time_start": 0,
            "time_end": 0,
            "mem_access_req": {
                "time_start": 0,
                "time_end": 0
            },
            "mem_access_res": {
                "time_start": 0,
                "time_end": 0
            }
        }
        self.id_data = {
            "time_start": 0,
            "time_end": 0
        }
        self.ex_data = {
            "time_start": 0,
            "time_end": 0,
            "mem_access_req": {
                "time_start": 0,
                "time_end": 0
            }
        }
        self.wb_data = {
            "time_start": 0,
            "time_end": 0,
            "mem_access_res": {
                "time_start": 0,
                "time_end": 0
            }
        }
        extended_bitstring = bitstring
        # Since SystemVerilog seems to strip out leading zeroes we have to add
        # them back in
        if len(bitstring) < trace_element_mapping[-1][2] - 1:
            extended_bitstring = \
                "0" * (trace_element_mapping[-1][2] - len(bitstring) - 1) + \
                bitstring
        # Iterate over the individual elements of a Trace Element
        for (field, start, end) in trace_element_mapping:
            # If the field we're looking at is in the fields to ignore
            if field not in fields_to_ignore:
                # If the field list is of length then we have a top level field
                if len(field) == 1:
                    setattr(self, field[0],
                            self.fixed_length_hex(extended_bitstring[start:end],
                                                  32))
                else:
                    self.set_in_dict(
                        getattr(self, field[0]), field[1:],
                        self.fixed_length_hex(extended_bitstring[start:end], 32)
                    )

    @staticmethod
    def get_from_dict(data_dict, map_list):
        return reduce(operator.getitem, map_list, data_dict)

    def set_in_dict(self, data_dict, map_list, value):
        self.get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value

    @staticmethod
    def fixed_length_hex(bit_string, required_bit_length):
        interim_hex = hex(int(bit_string, base=2))
        if required_bit_length // 4 != (len(interim_hex) - 2):
            return \
                "0x" + \
                "0" * ((required_bit_length // 4) - len(interim_hex) + 2) + \
                interim_hex[2:]
        else:
            return interim_hex


if __name__ == "__main__":
    vcd_engine = VCDEngine()
    results = vcd_engine.extract_tracing_information(
        "../working/102553_05012018.vcd")
    from src.display_engine import DisplayEngine
    display_engine = DisplayEngine()
    display_engine.process_and_display_data(results)
