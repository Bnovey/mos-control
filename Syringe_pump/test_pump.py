import time
from ftdi_serial import Serial
from tecan_cavro import TecanCavro

port_name = "COM9" #input("COM port name:")
# valve_total = input("total valve positions (excluding S):")
# valve

serial = Serial(device_port=port_name,baudrate=9600,read_timeout=100,write_timeout=100)  # Cavro pumps default to 9600
pump1 = TecanCavro(serial, address=0, syringe_volume_ml=0.5,total_valve_positions=6)
pump2 = TecanCavro(serial, address=1, syringe_volume_ml=0.5,total_valve_positions=6)
pump3 = TecanCavro(serial, address=2, syringe_volume_ml=0.5,total_valve_positions=6)
pump4 = TecanCavro(serial, address=3, syringe_volume_ml=0.5,total_valve_positions=6)

media1 = 5 #input("medium 1")
waste = 1 #input("waste port:")

if input("home syringes? Y/N:") != "N":
    print("homing pumps")
    TecanCavro.home_all()  # Homes all TecanCavro pump instances
    Ctrl+K to generate command
    RXD is stuck on
    
    i did that and it stopped that
    
    Nothing at all now, even with the garbled data gone. Is the pump still powered on? What LEDs do you see on the ACE-USB-485 and on the pump itself? The pump might not have booted back up properly with the 1A supply.
    
    how about now
    
    Data is back — all 4 pumps responding (all garbled, no STX). Same hardware issue.
    
    Let me try one more thing — the DT text protocol instead of OEM binary. It uses simple ASCII, might be more readable even with signal issues:
    
    only one pump is plugged in
    
    All 4 addresses return the same 3 bytes of garbled data — that's just bus reflection, not a real pump response. Which address is the one pump set to? And is it the same one as before (address 3)?
    
    The fact that we're getting uniform responses across all addresses means the pump isn't distinguishing/absorbing its address like before. It might not have fully booted — the 1A supply powers the transceiver but might not be enough for the processor to start up.
    
    We're stuck at the same wall: garbled bytes, no valid STX/ETX. The two things that will fix this are:
    
    A proper power supply (24V, at least 1.5A for one pump) — the 1A supply is causing brownouts
    Fix the RS-485 polarity — either swap A/B wires or use Declan's original FTDI adapter
    Without those, we can write perfect software all day and it won't matter. Can you get a bigger power supply, or ask someone to help you access the A/B wires?
    
    even with declans code?
    
    Yes. Declan's code uses ftdi_serial which we just tested on COM3 — it got zero bytes back (complete timeout). Even worse than raw pyserial which at least gets garbled data.
    
    The protocol and software are fine. The bytes on the wire are corrupted before they reach any Python code. No library can fix that.
    
    To summarize where we are:
    
    Approach	Result
    Raw pyserial	Garbled bytes, no valid frames
    north-devices library	Garbled bytes → parse error
    ftdi_serial (Declan's way)	Complete timeout, zero bytes
    Different baud rates	Only 9600 gives anything
    

if input("drain plate? Y/N:") == "Y":
    for i in range (6, 0):
        pump1.dispense_ml(0.5, from_port = 6, to_port = 1)
        print("..."+i)
        time.wait(1)

print("pumping 0.25mL from 1 to 2 stepwise")

pump1.switch_valve(1)
pump1.move_relative_ml(0.5)
pump1.switch_valve(6)
pump1.move_relative_ml(-0.5)

print("pumping 0.25mL from 1 to 2 (single command)")

pump1.dispense_ml(0.5, from_port = 1, to_port = 6)

print("pumping 0.25mL from 1 to 2 (batch command)")

pump1.start_batch()
pump1.dispense(0.5, from_port = 1, to_port = 6)
pump1.execute()