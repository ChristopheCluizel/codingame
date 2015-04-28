#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <sstream>

using namespace std;

string recupererExtension(string &nomFichier)
{
    istringstream iss(nomFichier); 
    string mot; 

    std::size_t found;
    found=nomFichier.find('.');
    if(found!=string::npos)
    {
        while(getline(iss, mot, '.' )) 
        {  
        }
    }
    else
        return "";

    if(!mot.empty())
        return mot;
    else
        return "";
}

int main()
{
    int N; // Number of elements which make up the association table.
    cin >> N; cin.ignore();
    int Q; // Number Q of file names to be analyzed.
    cin >> Q; cin.ignore();

    map<string, string> mapExtensionMime;
    map<string, string>::iterator it;

    for (int i = 0; i < N; i++) 
    {
        string EXT; // file extension
        string MT; // MIME type.
        cin >> EXT >> MT; cin.ignore();
        transform(EXT.begin(), EXT.end(), EXT.begin(), ::tolower);
        // transform(MT.begin(), MT.end(), MT.begin(), ::tolower);
        mapExtensionMime.insert(pair<string, string>(EXT, MT));
    }

    for (int i = 0; i < Q; i++) 
    {
        string FNAME; // One file name per line.
        string extension;

        getline(cin, FNAME);
        transform(FNAME.begin(), FNAME.end(), FNAME.begin(), ::tolower);
        extension = recupererExtension(FNAME);

        it = mapExtensionMime.find(extension);
        if(it == mapExtensionMime.end())
        {
            cout << "UNKNOWN" << endl;
        }
        else
        {
            cout<<it->second<<endl;
        }
    }
}