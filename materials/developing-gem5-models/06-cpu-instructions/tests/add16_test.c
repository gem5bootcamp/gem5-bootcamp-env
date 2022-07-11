#include <stdint.h>
#include <stdio.h>
int main(void)
{
  uint64_t num1 = 0xFFFFFFFFFFFFFFFF, num2 = 0xFFFFFFFFFFFFFFFF, output = 0;
  printf("RISC-V Packed Addition using 0xFFFFFFFFFFFFFFFF and 0xFFFFFFFFFFFFFFFF \n");
  asm volatile("add16 %0, %1,%2\n":"=r"(output):"r"(num1),"r"(num2):);
  printf("Output is 0x%LX \n", output);
  if (output == 0xFFFEFFFEFFFEFFFE) {
     printf("Test Passed! \n");
  }
  return 0;
}
