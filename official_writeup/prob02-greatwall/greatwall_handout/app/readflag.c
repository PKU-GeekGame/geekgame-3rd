#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
  setuid(0);
  FILE *fp = fopen("/flag", "r");
  char flag[64];
  fgets(flag, 64, fp);
  printf("%s", flag);
  return 0;
}