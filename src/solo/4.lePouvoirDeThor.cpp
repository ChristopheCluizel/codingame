#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

int main()
{
    int posLight_x; // the X position of the light of power
    int posLight_y; // the Y position of the light of power
    int posThor_x; // Thor's starting X position
    int posThor_y; // Thor's starting Y position
    cin >> posLight_x >> posLight_y >> posThor_x >> posThor_y; cin.ignore();

    // game loop
    while (1) 
    {
        int energie = 0; // The level of Thor's remaining energy, representing the number of moves he can still make.
        // float distance[8];
        // float angle;
        cin >> energie; cin.ignore();

        if(posThor_y == posLight_y && posThor_x < posLight_x)
        {
            cout<<"E"<<endl;
            posThor_x++;
        }
        if(posThor_y == posLight_y && posThor_x > posLight_x)
        {
            cout<<"W"<<endl;
            posThor_x--;
        }
        if(posThor_x == posLight_x && posThor_y > posLight_y)
        {
            cout<<"N"<<endl;
            posThor_y--;
        }
        if(posThor_x == posLight_x && posThor_y < posLight_y)
        {
            cout<<"S"<<endl;
            posThor_y++;
        }

        if(posThor_x < posLight_x && posThor_y < posLight_y)
        {
            cout<<"SE"<<endl;
            posThor_x++;
            posThor_y++;
        }
        else if(posThor_x < posLight_x && posThor_y > posLight_y)
        {
            cout<<"NE"<<endl;
            posThor_x++;
            posThor_y--;
        }
        else if(posThor_x > posLight_x && posThor_y < posLight_y)
        {
            cout<<"SW"<<endl;
            posThor_x--;
            posThor_y++;
        }
        else if(posThor_x > posLight_x && posThor_y > posLight_y)
        {
            cout<<"NW"<<endl;
            posThor_x--;
            posThor_y--;
        }

    }
}