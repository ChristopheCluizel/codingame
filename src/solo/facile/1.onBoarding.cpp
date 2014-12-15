#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

/**
 * The code below will read all the game information for you.
 * On each game turn, information will be available on the standard input, you will be sent:
 * -> the total number of visible enemies
 * -> for each enemy, its name and distance from you
 * The system will wait for you to write an enemy name on the standard output.
 * Once you have designated a target:
 * -> the cannon will shoot
 * -> the enemies will move
 * -> new info will be available for you to read on the standard input.
 **/
int trouverIndexMin(vector<int> &tabDist);
int main()
{

    // game loop
    while (1) {
        int count; // The number of current enemy ships within range
        cin >> count; cin.ignore();
        vector<string> tabEnemies;
        vector<int> tabDist;
        
        for (int i = 0; i < count; i++) {
            string enemy; // The name of this enemy
            int dist; // The distance to your cannon of this enemy
            
            cin >> enemy >> dist; cin.ignore();
            tabEnemies.push_back(enemy);
            tabDist.push_back(dist);
        }
        int indexMini =  trouverIndexMin(tabDist);
        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;
        
        cout << tabEnemies[indexMini] << endl; // The name of the most threatening enemy (HotDroid is just one example)
    }
}
int trouverIndexMin(vector<int> &tabDist)
{
    int indexMin = 0;
    
    for(int i = 0; i < tabDist.size(); i++)
    {
        if(tabDist[i] < tabDist[indexMin])
            indexMin = i;
    }
    return indexMin;
}