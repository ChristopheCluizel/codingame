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
    int L;
    cin >> L; cin.ignore();
    int H;
    cin >> H; cin.ignore();
    string T;
    getline(cin, T);
    char temp;
    // cout<<T<<endl;
    vector< vector<char> > tabAlphabet;
    for (int i = 0; i < H; i++)
    {
        vector<char> row;
        for(int j = 0; j < L*26; j++)
        {
            cin >> temp;
            row.push_back(temp);
        }
        tabAlphabet.push_back(row);
    }
    for (int i = 0; i < H; i++)
    {
        for(int j = 0; j < L; j++)
        {
            cout<<tabAlphabet[i][j];
        }
        cout<<endl;
    }

    // Write an action using cout. DON'T FORGET THE "<< endl"
    // To debug: cerr << "Debug messages..." << endl;

    

}