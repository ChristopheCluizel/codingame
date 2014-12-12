#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

string alphabetMinuscule = "abcdefghijklmnopqrstuvwxyz";
string alphabetMajuscule = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

int trouverIndiceLettreDansAlphabet(char lettre)
{
    for(int i =0; i < 27; i++)
    {
        if((alphabetMajuscule[i] == lettre) || (alphabetMinuscule[i] == lettre))
            return i;
    }

    return 26;
}

int main()
{
    int L;
    cin >> L; cin.ignore();
    int H;
    cin >> H; cin.ignore();
    string phrase;
    getline(cin, phrase);
    
    vector<string> tabAlphabet;
    int indice;

    for (int i = 0; i < H; i++)
    {
        string ligne;
        getline(cin, ligne);
        tabAlphabet.push_back(ligne);
    }

    for(int j = 0; j < H; j++)
    {
        for(int i = 0; i < phrase.size(); i++)   // pour chaque lettre de la phrase
        {
            indice = trouverIndiceLettreDansAlphabet(phrase[i]);
            //cerr<<"indice : "<<indice<<endl;
            for(int k = indice * L; k < (indice *L) + L; k++)
            {
                cout<<tabAlphabet[j][k];
            }
        }
        cout<<endl;
    }
}