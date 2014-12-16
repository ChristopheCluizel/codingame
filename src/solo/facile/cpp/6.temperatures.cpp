#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

using namespace std;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
 int calculerMinimum(vector<int> tab)
 {
    int mini = abs(tab[0]);

    for(int i = 0; i < tab.size(); i++)
    {
        if(mini > abs(tab[i]))
            mini = abs(tab[i]);
    }

    return mini;
 }
int main()
{
    int N; // the number of temperatures to analyse
    string TEMPS; // the N temperatures expressed as integers ranging from -273 to 5526
    cin >> N; cin.ignore();
    getline(cin, TEMPS);
    // cout<<"temp  : "<<TEMPS<<endl;
    string strTemp;
    vector<int> tabTemperature;
    istringstream iss(TEMPS);
    int nombre = 0;
    int minimum  = 0;

    while (getline(iss, strTemp, ' ')) 
    { 
        istringstream issConversion(strTemp);
        issConversion >> nombre;
        tabTemperature.push_back(nombre); 
    }
    // for(int i = 0; i < tabTemperature.size(); i++)
    // {
    //     cout<<tabTemperature[i]<<endl;
    // }
    if(tabTemperature.empty())
        cout<<"0"<<endl;
    else
    {
        minimum = calculerMinimum(tabTemperature);
        vector<int> tabIndiceTempPositive;
        vector<int> tabIndiceTempNegative;

        for(int i = 0; i < tabTemperature.size(); i++)
        {
            if(tabTemperature[i] == minimum)
                tabIndiceTempPositive.push_back(i);
            if(tabTemperature[i] == -minimum)
                tabIndiceTempNegative.push_back(i);
        }

        if(tabIndiceTempPositive.empty())
            cout<<tabTemperature[tabIndiceTempNegative[0]]<<endl;
        else
            cout<<tabTemperature[tabIndiceTempPositive[0]]<<endl;
    }

    // cerr<<"minimum : "<<minimum<<endl;
}