import subprocess

from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime

from src.vcd_engine import VCDEngine
from src.display_engine import DisplayEngine

class Joushi(object):

    sh_scripts_dir = Path("/home/jonathanrainer/Documents/Experiments/"
                          "4_pulpino/Joushi/sh_scripts")
    vcd_engine = VCDEngine()
    display_engine = DisplayEngine()

    def run(self, vivado_project_path, output_path,
            tcl_simulation_script, simulation_mode, simulation_set):
        # Generate an output location
        output_file_path = (output_path / "{0}.vcd".format(
            datetime.now().strftime("%H%M%S_%d%m%Y"))).expanduser()
        # Run the simulation to generate data
        subprocess.run(
            "{0} {1} {2} {3} {4} {5}".format(
                self.sh_scripts_dir / "run_vivado.sh",
                tcl_simulation_script.expanduser(),
                vivado_project_path.expanduser(),
                simulation_mode, simulation_set, output_file_path), shell=True)
        vcd_data = self.vcd_engine.extract_tracing_information(output_file_path)
        self.display_engine.process_and_display_data(vcd_data)


if __name__ == "__main__":
    argparser = ArgumentParser(prog="Joushi - A simulation management system",
                               description= "Run a specified simulation and "
                                            "visualise the output.")
    argparser.add_argument("vivado_project")
    argparser.add_argument("output_location")
    argparser.add_argument("tcl_simulation_script")
    argparser.add_argument("simulation_mode")
    argparser.add_argument("simulation_set")
    args = argparser.parse_args()
    system = Joushi()
    system.run(Path(args.vivado_project), Path(args.output_location),
               Path(args.tcl_simulation_script),
               args.simulation_mode, args.simulation_set)
