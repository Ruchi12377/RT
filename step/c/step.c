#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

void loop(void);

int frameCount;

int xBlinkWait = 1;
int yBlinkWait = 2;
int zBlinkWait = 3;

int _xCount;
int _yCount;
int _zCount;

bool _xState;
bool _yState;
bool _zState;

int main()
{
    while (1)
    {
        loop();
        //system("reset");
        usleep(1000000);
    }
}

void loop(void)
{
    frameCount++;

    if (frameCount - _xCount >= xBlinkWait)
    {
        _xState = _xState == false;
        _xCount = frameCount;
    }
    
    if (frameCount - _yCount >= yBlinkWait)
    {
        _yState = _yState == false;
        _yCount = frameCount;
    }
    
    if (frameCount - _zCount >= zBlinkWait)
    {
        _zState = _zState == false;
        _zCount = frameCount;
    }

    printf("%s : %s : %s\n",
    (_xState ? "true" : "false"),
    (_yState ? "true" : "false"),
    (_zState ? "true" : "false"));
}