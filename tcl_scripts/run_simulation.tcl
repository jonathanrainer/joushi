###
#
# Inputs
#   1 - Name of Project
#   2 - VCD Output Location
#   3 - Simulation Mode (Behavioural etc.)
#   4 - Simset (In Vivado)
#
###

# Open the project so that all simulation sets are available
open_project [lindex $argv 0]
# Run the specified simulation
launch_simulation -mode [lindex $argv 2] -simset [lindex $argv 3]
# Open a new VCD file to capture to required output
open_vcd [file join [lindex $argv 1] "[clock format [clock seconds] -format %T_%d%m%Y].vcd"]
log_vcd
run 2s
# Close the finished VCD file
close_vcd