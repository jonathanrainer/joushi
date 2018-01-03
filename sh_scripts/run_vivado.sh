#!/usr/bin/env bash

source /opt/Xilinx/Vivado/2017.1/settings64.sh
vivado -mode batch -nojournal -nolog -source $1 -tclargs $2 $3 $4 $5