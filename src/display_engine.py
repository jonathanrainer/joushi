import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import MultipleLocator, FormatStrFormatter


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
        ax.grid(which="major", color="black", linestyle="-", linewidth=1,
                axis="x")
        ax.grid(which="minor", color="black", linestyle="--", linewidth=1,
                axis="x", alpha=0.3)
        ax.set_axisbelow(True)
        for (row_data, row_num, label, colour, line_colour, alpha) in data[0]:
            for col_index, pair in enumerate(row_data):
                if not(pair[0] == pair[1] and pair[0] == 0):
                    x1 = [pair[0], pair[1]+1]
                    y1 = np.array([col_index, col_index])
                    y2 = y1+1
                    plt.fill_between(x1, y1, y2=y2, facecolor=colour,
                                     linewidth=2, linestyle="dotted",
                                     edgecolor=line_colour, alpha=alpha)
                    plt.text(self.avg(x1[0], x1[1]), self.avg(y1[0], y2[0]),
                             label, horizontalalignment='center',
                             verticalalignment='center', rotation=90,
                             color="white")
        for axis in [ax.yaxis]:
            axis.set(ticks=np.arange(0.5, len(data[1])),
                     ticklabels=[x[1] for x in data[1]])
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_major_formatter(FormatStrFormatter("%d"))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        plt.ylim(len(data[1]), 0)
        plt.xlim(0, max([max(max(y)) for y in [x[0] for x in data[0]]])+5)
        plt.yticks(fontname="monospace")
        plt.show()

    def process_results(self, vcd_data):
        processed_results = ([
            ([
                (int(x[1].if_data["time_start"], base=16),
                 int(x[1].if_data["time_end"], base=16)) for x in
                vcd_data
            ], 0, "IF", "white",  "black", 1),
            ([
                (int(x[1].if_data["mem_access_req"]["time_start"], base=16),
                 int(x[1].if_data["mem_access_req"]["time_end"], base=16))
                for x in vcd_data
            ], 0, "MREQ", "red", "white", 0.5),
            ([
                (int(x[1].if_data["mem_access_res"]["time_start"], base=16),
                 int(x[1].if_data["mem_access_res"]["time_end"], base=16))
                for x in vcd_data
            ], 0, "MRES", "yellow", "white", 0.5),
            ([
                (int(x[1].id_data["time_start"], base=16),
                 int(x[1].id_data["time_end"], base=16)) for x in
                vcd_data
            ], 1, "ID", "green", "black", 1),
            ([
                (int(x[1].ex_data["time_start"], base=16),
                 int(x[1].ex_data["time_end"], base=16)) for x in
                vcd_data
            ], 2, "EX", "blue", "black", 1),
            ([
                (int(x[1].ex_data["mem_access_req"]["time_start"], base=16),
                 int(x[1].ex_data["mem_access_req"]["time_end"], base=16))
                for x in vcd_data
            ], 2, "MREQ", "purple", "white", 0.3),
            ([
                (int(x[1].wb_data["time_start"], base=16),
                 int(x[1].wb_data["time_end"], base=16))
                for x in vcd_data
            ], 3, "WB", "orange", "black", 1),
            ([
                (int(x[1].wb_data["mem_access_res"]["time_start"], base=16),
                 int(x[1].wb_data["mem_access_res"]["time_end"], base=16))
                for x in vcd_data
            ], 3, "MRES", "brown", "white", 0.3)
        ],
        [
            (tick_num, "Instruction: {0}\nAddr: {1}".format(
                x[1].instruction, x[1].address)
             ) for tick_num, x in
            enumerate(vcd_data)
        ])
        return processed_results

    def process_and_display_data(self, vcd_data):
        processed_data = self.process_results(vcd_data)
        self.display_results(processed_data)

if __name__ == "__main__":
    de = DisplayEngine()
    de.display_results(de.data)
