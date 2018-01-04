from Verilog_VCD.Verilog_VCD import parse_vcd


class VCDEngine(object):

    trace_element_mapping = {
        "instruction": (0, 32, {}),
        "address": (32, 63, {}),
        "pass_through": (63, 64, {}),
        "if_data": (64, 256, {
            "time_start": (65, 97, {}),
            "time_end": (97, 129, {}),
            "mem_access_req": (129, 193, {
                "time_start": (129, 161, {}),
                "time_end": (161, 193, {})
            }),
            "mem_access_res": (193, 257, {
                "time_start": (193, 225, {}),
                "time_end": (225, 257, {})
            })
        }),
        "id_data": (257, 321, {
            "time_start": (257, 289, {}),
            "time_end": (289, 321, {})
        }),
        "ex_data": (322, 450, {
            "time_start": (322, 354, {}),
            "time_end": (354, 386, {}),
            "mem_access_req": (386, 450, {
                "time_start": (386, 418, {}),
                "time_end": (418, 450, {})
            })
        }),
        "wb_data": (450, 578, {
            "time_start": (450, 482, {}),
            "time_end": (482, 514, {}),
            "mem_access_req": (514, 578, {
                "time_start": (514, 546, {}),
                "time_end": (546, 578, {})
            })
        })
    }

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
        processed_data = [(time, self.reformat_bitstring(bitstring))
                          for (time, bitstring) in parsed[1:]]

    def reformat_bitstring(self, bitstring):
        return 0


class TraceElement(object):

    instruction = ""
    address = ""
    if_data = {}
    id_data = {}
    ex_data = {}
    wb_data = {}


if __name__ == "__main__":
    vcd_engine = VCDEngine()
    vcd_engine.extract_tracing_information(
        "/home/jonathanrainer/Documents/Experiments/4_pulpino/Joushi/working/"
        "142133_04012018.vcd")