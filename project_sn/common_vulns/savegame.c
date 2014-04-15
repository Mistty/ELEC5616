// savegame.c
// Compile using `gcc -fno-stack-protector savegame.c`

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Hero {
    unsigned int hp;
    char name[10];
    unsigned int gold;
};

int main(int argc, const char *argv[])
{
    struct Hero h;
    h.hp = 30;
    h.gold = 8;

    scanf("%s", h.name);

    printf("Name: %s\n", h.name);
    printf("HP: %d | Gold: %d\n", h.hp, h.gold);

    return 0;
}
