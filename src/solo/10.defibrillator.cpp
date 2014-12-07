#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <iomanip>

using namespace std;

void afficherVector(std::vector<string> &vec)
{
    for(int i = 0; i < vec.size(); i++)
    {
        cerr<<vec[i]<<endl;
    }
}

double degreToRadian(double degree)
{
    return (degree * 2 * M_PI) / 360;
}

double radianToDegree(double radian)
{
    return (radian * 360) / (2*M_PI);
}

class Defibrillateur
{
public:
    Defibrillateur(){};
    Defibrillateur(int id, string nom, string adresse, string numTelephone, double longitude, double latitude)
    {
        m_id = id;
        m_nom = nom;
        m_adresse = adresse;
        m_numTelephone = numTelephone;
        m_longitude = degreToRadian(longitude);
        m_latitude = degreToRadian(latitude);
    }

    int getId()
    {
        return m_id;
    }

    string getNom()
    {
        return m_nom;
    }

    string getAdresse()
    {
        return m_adresse;
    }

    string getNumTelephone()
    {
        return m_numTelephone;
    }

    double getLongitude()
    {
        return m_longitude;
    }

    double getLatitude()
    {
        return m_latitude;
    }

    static Defibrillateur construireDefibrillateur(string caracteristiqueDefibri)
    {
        istringstream iss(caracteristiqueDefibri); 
        string champ;
        std::vector<string> vecChamps; 
        while(getline(iss, champ, ';' )) 
        { 
            vecChamps.push_back(champ); 
        } 
        string point = ".";
        vecChamps[4].replace(vecChamps[4].find(","), point.length(), point);
        vecChamps[5].replace(vecChamps[5].find(","), point.length(), point);
 
        int id;
        double longitude;
        double latitude; 
        id = atoi(vecChamps[0].c_str());
        longitude = atof(vecChamps[4].c_str());
        latitude = atof(vecChamps[5].c_str());

        return Defibrillateur(id, vecChamps[1], vecChamps[2], vecChamps[3], longitude, latitude);
    }

private:
    int m_id;
    string m_nom;
    string m_adresse;
    string m_numTelephone;
    double m_longitude;
    double m_latitude;

};

double calculerDistance(double longitudeUsager, double lattitudeUsager, Defibrillateur defibri)
{
    double x;
    double y;

    x = (defibri.getLongitude() - longitudeUsager) * cos((defibri.getLatitude() + lattitudeUsager) / 2);
    y = defibri.getLatitude() - lattitudeUsager;

    return sqrt(pow(x,2) + pow(y,2)) * 6371;
}

struct Carte
{
    Carte(){};
    Carte(Defibrillateur defibri, double distanceFromUser)
    {
        m_defibri = defibri;
        m_distanceFromUser = distanceFromUser;
    }

    Defibrillateur m_defibri;
    double m_distanceFromUser;
};

int main()
{
    string longitudeUsager;
    cin >> longitudeUsager; cin.ignore();
    string lattitudeUsager;
    cin >> lattitudeUsager; cin.ignore();

    string point = ".";
    longitudeUsager.replace(longitudeUsager.find(","), point.length(), point);
    lattitudeUsager.replace(lattitudeUsager.find(","), point.length(), point);

    int nbDefibrillateur;
    cin >> nbDefibrillateur; cin.ignore();

    std::vector<Defibrillateur> vecDefibri;
    std::vector<double> vecDistance;
    std::vector<Carte> vecCarte;
    Carte carte;
    double indexDistanceMini = 0;

    for (int i = 0; i < nbDefibrillateur; i++)
    {
        string caracteristiqueDefibri;
        getline(cin, caracteristiqueDefibri);
        carte.m_defibri = Defibrillateur::construireDefibrillateur(caracteristiqueDefibri);
        carte.m_distanceFromUser = calculerDistance(degreToRadian(atof(longitudeUsager.c_str())), degreToRadian(atof(lattitudeUsager.c_str())), carte.m_defibri);
        vecCarte.push_back(carte);
    }

    for(int i = 0; i < vecCarte.size(); i++)
    {
        if(vecCarte[indexDistanceMini].m_distanceFromUser > vecCarte[i].m_distanceFromUser)
            indexDistanceMini = i;
    }

    cout <<vecCarte[indexDistanceMini].m_defibri.getNom()<< endl;
}