"""
Tecan Cavro: pump at RS-485 address 2 aspirates from valve port 4 and dispenses to port 3.

Requires `ftdi_serial` and `tecan_cavro` on PYTHONPATH (same layout as MOS-03 Tecan_Cavro).

Run from this folder or set PYTHONPATH to the folder containing those modules:
  python cavro_addr2_port4_to_3.py
"""

from ftdi_serial import Serial
from tecan_cavro import TecanCavro

# --- edit for your setup ---
COM_PORT = "COM3"
VOLUME_ML = 0.5
SYRINGE_VOLUME_ML = 0.5
TOTAL_VALVE_POSITIONS = 6
PUMP_ADDRESS = 2
FROM_PORT = 4
TO_PORT = 3
# ---------------------------


def main() -> None:
    serial = Serial(
        device_port=COM_PORT,
        baudrate=9600,
        read_timeout=100,
        write_timeout=100,
    )
    # Only this instance is registered on TecanCavro.instances — safe for home_all().
    pump = TecanCavro(
        serial,
        address=PUMP_ADDRESS,
        syringe_volume_ml=SYRINGE_VOLUME_ML,
        total_valve_positions=TOTAL_VALVE_POSITIONS,
    )

    if input("Home pump before move? Y/N: ").strip().upper() == "Y":
        print("homing...")
        TecanCavro.home_all()

    print(
        f"Dispensing {VOLUME_ML} mL: pull from port {FROM_PORT}, push to port {TO_PORT} "
        f"(address {PUMP_ADDRESS})"
    )
    pump.dispense_ml(
        VOLUME_ML,
        from_port=FROM_PORT,
        to_port=TO_PORT,
    )
    print("done.")


if __name__ == "__main__":
    main()
