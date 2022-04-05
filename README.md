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

• A breakpoint was set for the foo() function in order to overflow the ”buff” array in the foo function of 
the target.c file 

• Gdb commands like Infoframe, x &variable, x address were used to get the address information of the 
stack memory of the foo() function

2 Stack memory allocation 

• From Figure 4 and Figure 5, the address for the instruction pointer (rip) is 0x7fffffffec58 and ’buff’ 
variable in the foo() functions is 0x7fffffffeba0. The offset value required to overwrite the return address 
to execute the shellcode is given as below: 

offset = rip address - buff address = 0x7fffffffec58 - 0x7fffffffeba0 = 184 in decimal 

• To change the flow to the beginning of shellcode, revise the exploit.c code using the offset value to fill 
the return address in the ’buff’ variable. 

The return address is the starting address of the ’buff’ array. The stack memory allocation graph of the 
foo() function is shown in the Figure 6. buff[184] = 0xa0; buff[185] = 0xeb; buff[186] = 0xff; buff[187] = 
0xff; buff[188] = 0xff; buff[189] = 0x7f; buff[190] = 0x00

3 Output of exploit.c Code 

• The exploit.c code was run after correctly filling the ’buff’ array that exploits the stack overflow 
vulnerability of a given target code

