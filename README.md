# Buffer-Overflow-Attack
The goal of this project is to implement a “fuzzer”, or fuzz tester. Fuzz testing is one way of discovering security vulnerabilities in any code that processes potentially malicious input.

This project is based on a simple jpeg to bmp format conversion open source code called ‘jpgbmp.cpp’. There are 8 bugs added that cause the program to crash. When a bug is triggered, jpg2bmp program will crash with “segmentation fault” and print out “You triggered Bug #n !” in stderr where n is a number between 1 to 8 indicating which bug has been triggered.

1.Design of Buffer Overflow

• The beginning of ”buff” array was filled with the 27 bytes of shellcode provided in shellcode.h file 
starting from buff[0] to buff[26].

• ”buff” array was filled with a arbitrary addresses and values at a random starting position with null 
terminator at the end. 

buff[24] = 0x50; buff[25] = 0xeb; buff[26] = 0xff; buff[27] = 0xff; buff[28] = 0xff; buff[29] = 0x7f; buff[30] 
= 0x00; 
• Then the exploit.c was compiled using make command. and the gdb debugger was run
