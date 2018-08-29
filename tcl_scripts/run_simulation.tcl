###
#
# Inputs
#   1 - Name of Project
#   2 - Simulation Mode (Behavioural etc.)
#   3 - Simset (In Vivado)
#   4 - VCD Output Location
#
###

# Open the project so that all simulation sets are available
open_project [lindex $argv 0]
# Run the specified simulation
launch_simulation -mode [lindex $argv 1] -simset [lindex $argv 2]
# Open a new VCD file to capture to required output
open_vcd [lindex $argv 3]
log_vcd /ryuki_testbench/tracer/*
restart
run 100000ns
# Close the finished VCD file
close_vcd