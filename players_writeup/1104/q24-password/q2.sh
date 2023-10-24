xxd -r <(echo "00000000: 4d3c 2b1a 0100 0000") > plain.dat
# xxd -r <(echo "00000000: 4d3c 2b1a 0100 0000 ffff ffff ffff ffff") > plain.dat
bkcrack -C challenge_2.zip -c flag2.pcapng -p plain.dat -o 8 -x 0 0a0d0d0a -d flag2.pcapng
