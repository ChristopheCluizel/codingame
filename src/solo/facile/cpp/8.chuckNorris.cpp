#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

using namespace std;

void afficherVector(std::vector<int> &messageBinaire)
{
    for(int i = 0; i < messageBinaire.size(); i++)
    {
        cerr<<messageBinaire[i];
    }
    cerr<<endl;
}

std::vector<int> charToBinaire(char lettre)
{
    int quotient = 42;
    int reste = 0;
    std::vector<int> vecLettreBinaire;
    
    while(quotient != 0)
    {
        quotient = lettre / 2;
        // cerr<<"quotient : "<<quotient<<endl;
        reste = lettre % 2;
        // cerr<<"reste : "<< reste<<endl;
        lettre = quotient;
        vecLettreBinaire.push_back(reste);
    }
    while(vecLettreBinaire.size() < 7)
    {
        vecLettreBinaire.push_back(0);
    }
    reverse(vecLettreBinaire.begin(), vecLettreBinaire.end());

    return vecLettreBinaire;
}

void stringToBinaire(string messageOriginal, std::vector<int> &messageBinaire)
{
    std::vector<int> vecLettreBinaire;

    cerr<<"messageOriginal : "<<messageOriginal<<endl;
    for(int i = 0; i < messageOriginal.size(); i++)
    {
        vecLettreBinaire = charToBinaire(messageOriginal[i]);
        messageBinaire.insert(messageBinaire.end(), vecLettreBinaire.begin(), vecLettreBinaire.end());
    }
}

void conversionChuck(std::vector<int> &vecMessageBinaire, string &messageCode)
{
    int chiffreRef = 0;
    int curseur = 0;

    while(curseur < vecMessageBinaire.size())
    {
        chiffreRef = vecMessageBinaire[curseur];
        curseur++;
        if(chiffreRef == 0)
            messageCode += "00 0";
        else
            messageCode += "0 0";

        while(vecMessageBinaire[curseur] == chiffreRef && curseur < vecMessageBinaire.size())
        {
            messageCode += "0";
            curseur++;
        }
        messageCode += " ";
    }
    messageCode.pop_back();
}

int main()
{
    string MESSAGE;
    getline(cin, MESSAGE);
    vector<int> vecMessageBinaire;
    string messageCode;

    stringToBinaire(MESSAGE, vecMessageBinaire);
    afficherVector(vecMessageBinaire);
    conversionChuck(vecMessageBinaire, messageCode);

    cout << messageCode << endl;
}