import matplotlib.pyplot as plt
import numpy as np


class DisplayEngine(object):

    # Data format will be:
    # Column 0 - IF Phase
    # Column 1 - Memory REQ (IF)
    # Column 2 - Memory RES (IF)
    # Column 3 - ID Phase
    # Column 4 - EX Phase
    # Column 5 - Memory REQ (EX)
    # Column 6 - WB Phase
    # Column 7 - Memory RES (WB)

    test_data = [(1, 3), (1, 2), (1, 1), (1, 1), (1, 1), (0, 7), (1, 1), (1, 4)]

    @staticmethod
    def avg(a, b):
        return (a + b) / 2.0

    def display_results(self, data):
        fig = plt.figure(figsize=(35.08, 24.08))
        ax = fig.add_subplot(111)
        for (row_data, row_num, label, colour, alpha) in data:
            for pair in row_data:
                if pair[0] != pair[1]:
                    x1 = [pair[0], pair[1]]
                    y1 = np.array([row_num, row_num])
                    y2 = y1+1
                    plt.fill_between(x1, y1, y2=y2, facecolor=colour,
                                     linewidth=2, linestyle="dotted",
                                     edgecolor='black', alpha=alpha)
                    plt.text(self.avg(x1[0], x1[1]), self.avg(y1[0], y2[0]),
                             label, horizontalalignment='center',
                             verticalalignment='center', rotation=90)
        plt.ylim(len(data), 0)
        plt.show()

    def process_results(self, vcd_data):
        processed_results = [
            ([
                (int(x[1].if_data["time_start"], base=16),
                 int(x[1].if_data["time_end"], base=16)) for x in
                vcd_data
            ], 0, "IF", "purple", 1),
            ([
                (int(x[1].if_data["mem_access_req"]["time_start"], base=16),
                 int(x[1].if_data["mem_access_req"]["time_end"], base=16))
                for x in vcd_data
            ], 0, "MREQ", "orange", 0.3),
            ([
                (int(x[1].if_data["mem_access_res"]["time_start"], base=16),
                 int(x[1].if_data["mem_access_res"]["time_end"], base=16))
                for x in vcd_data
            ], 0, "MRES", "orange", 0.3),
            ([
                (int(x[1].id_data["time_start"], base=16),
                 int(x[1].id_data["time_end"], base=16)) for x in
                vcd_data
            ], 1, "ID", "red", 1),
            ([
                (int(x[1].ex_data["time_start"], base=16),
                 int(x[1].ex_data["time_end"], base=16)) for x in
                vcd_data
            ], 2, "EX", "blue", 1),
            ([
                (int(x[1].ex_data["mem_access_req"]["time_start"], base=16),
                 int(x[1].ex_data["mem_access_req"]["time_end"], base=16))
                for x in vcd_data
            ], 2, "MREQ", "violet", 0.3),
            ([
                (int(x[1].wb_data["time_start"], base=16),
                 int(x[1].wb_data["time_end"], base=16))
                for x in vcd_data
            ], 3, "WB", "purple", 1),
            ([
                (int(x[1].wb_data["mem_access_res"]["time_start"], base=16),
                 int(x[1].wb_data["mem_access_res"]["time_end"], base=16))
                for x in vcd_data
            ], 3, "MRES", "green", 0.3)
        ]
        return processed_results

    def process_and_display_data(self, vcd_data):
        processed_data = self.process_results(vcd_data)
        self.display_results(processed_data)

if __name__ == "__main__":
    de = DisplayEngine()
    de.display_results(de.data)
