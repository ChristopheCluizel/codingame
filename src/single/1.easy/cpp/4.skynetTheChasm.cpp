#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
int main()
{
    bool hasJumped = false;
    int R; // the length of the road before the gap.
    cin >> R; cin.ignore();
    int G; // the length of the gap.
    cin >> G; cin.ignore();
    cerr<<"gap length : "<<G<<endl;
    int L; // the length of the landing platform.
    cin >> L; cin.ignore();
    int speedOfJump = G;

    // game loop
    while (1) {
        int S; // the motorbike's speed.
        cin >> S; cin.ignore();
        int X; // the position on the road of the motorbike.
        cin >> X; cin.ignore();

        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;
        if(!hasJumped)
        {
            if(S <= speedOfJump)
                cout<<"SPEED"<<endl;
            else if(S > speedOfJump + 1)
                cout<<"SLOW"<<endl;
            else if((R - (X + S) <= 0))
            {
                cout<<"JUMP"<<endl;
                hasJumped = true;
            }
            else
                cout<<"WAIT"<<endl;
        }
             // A single line containing one of 4 keywords: SPEED, SLOW, JUMP, WAIT.
        else
            cout<<"SLOW"<<endl;
    }
}