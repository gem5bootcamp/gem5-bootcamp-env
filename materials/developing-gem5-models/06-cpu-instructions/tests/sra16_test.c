#include <stdint.h>
#include <stdio.h>
int main(void)
{
  uint16_t shift_amount = 1;
  uint64_t input = 0xFFFEFFFEFFFEFFFE, output = 0;
  printf("RISC-V Packed SRA16 test (shift by 1) for 0xFFFEFFFEFFFEFFFE \n");
  asm volatile("sra16 %0, %1,%2\n":"=r"(output):"r"(input),"r"(shift_amount):);
  printf("Output is %LX \n", output);
  if (output == 0xFFFFFFFFFFFFFFFF) {
     printf("Test Passed! \n");
  }
  return 0;
}
