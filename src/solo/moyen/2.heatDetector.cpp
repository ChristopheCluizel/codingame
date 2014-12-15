#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int dichotomieEntre(int min, int max)
{
    //cerr<<"min : "<<min<<" -> max : "<<max<<")"<<endl;
    return (max + min) / 2;
}

int main()
{
    int buildingWidth; // width of the building.
    int buildingHeight; // height of the building.
    cin >> buildingWidth >> buildingHeight; cin.ignore();
    // cerr<<"taille building : ("<<buildingWidth<<", "<<buildingHeight<<endl;
    int nbTurnsMax; // maximum number of turns before game over.
    cin >> nbTurnsMax; cin.ignore();
    int x;
    int y;
    int minHeight = 0, maxHeight = buildingHeight;
    int minWidth = 0 , maxWidth = buildingWidth;
    cin >> x >> y; cin.ignore();

    // game loop
    while (1)
    {
        string bomb_dir; // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
        cin >> bomb_dir; cin.ignore();
        //cerr<<"message : "<<bomb_dir<<endl;

        if(bomb_dir.find("U") != string::npos)
        {
            maxHeight = y;
        }

        if(bomb_dir.find("D") != string::npos)
        {
            minHeight = y;
        }

        if(bomb_dir.find("R") != string::npos)
        {
            minWidth = x;
        }

        if(bomb_dir.find("L") != string::npos)
        {
            maxWidth = x;
        }

        // cerr<<"minHeight : "<<minHeight<<" -> maxHeight : "<<maxHeight<<endl;
        // cerr<<"minWidth : "<<minWidth<<" -> maxWidth : "<<maxWidth<<endl;
        x = dichotomieEntre(minWidth, maxWidth);
        y = dichotomieEntre(minHeight, maxHeight);

        cout << x << " " << y << endl; // the location of the next window Batman should jump to.
    }
}
