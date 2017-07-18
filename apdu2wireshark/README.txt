This is a python script for taking a SIM card APDU comms traffic dump (plaintext file), and sending it to Wireshark
for dissection.

Wireshark 1.12.0 will apply its GSM dissector as long as incoming traffic arrives at port 4729.

Example use:

$ ./apdu2wireshark.py -i test1.txt
