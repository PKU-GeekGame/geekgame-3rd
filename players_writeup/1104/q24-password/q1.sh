# https://www.acceis.fr/cracking-encrypted-archives-pkzip-zip-zipcrypto-winzip-zip-aes-7-zip-rar/
xxd -r <(echo "00000000: cf 504b 0304 1400 0000 0800") > plain.dat
bkcrack -C challenge_1.zip -c chromedriver_linux64.zip -p plain.dat -o -1 -x 5845130 504b0506

bkcrack -C challenge_1.zip -c flag1.txt -k a07691d6 69ff16f6 85e8542f -d flag1.txt
