#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

using namespace std;

/* definition of the class Zone */
class Zone
{   
public:
    Zone(int zoneId, int platiniumSource);
    int getZoneId();
    int getPlatiniumSource();
    int getOwnerId();
    int* getTabNbPodEachPlayerPresent();
    vector<int> getVecAdjacentZones();
    int getNbOwnPodPresent(int myId);

    void setIdOwner(int idOwner);
    void addAdjacentZone(int zoneId);
    void addPodInTabPodEachPlayerPresent(int indexPlayer, int nbPod);
    void setTabPodEachPlayerPresent(int tabPod[]);

    bool isOwnPodPresent(int myId);

    /* for debug */
    void display();

private:
    int m_id;
    int m_ownerId;
    int m_platiniumSource;
    vector<int> m_vecAdjacentZones;
    int m_tabNbPodEachPlayerPresent[4];
};

/* implementation of the class Zone */
Zone::Zone(int zoneId, int platiniumSource)
{
    m_id = zoneId;
    m_platiniumSource = platiniumSource;
    m_ownerId = -1;
    for(int i = 0; i < 4; i++)
    {
        m_tabNbPodEachPlayerPresent[i] = 0;
    }
}

int Zone::getZoneId()
{
    return m_id;
}

int Zone::getPlatiniumSource()
{
    return m_platiniumSource;
}

int Zone::getOwnerId()
{
    return m_ownerId;
}

int* Zone::getTabNbPodEachPlayerPresent()
{
    return m_tabNbPodEachPlayerPresent;
}

vector<int> Zone::getVecAdjacentZones()
{
    return m_vecAdjacentZones;
}

void Zone::setIdOwner(int idOwner)
{
    m_ownerId = idOwner;
}

void Zone::addAdjacentZone(int zoneId)
{
    m_vecAdjacentZones.push_back(zoneId);
}

void Zone::addPodInTabPodEachPlayerPresent(int indexPlayer, int nbPod)
{
    m_tabNbPodEachPlayerPresent[indexPlayer] += nbPod;
}

void Zone::setTabPodEachPlayerPresent(int tabPod[])
{
    for(int i = 0; i < 4; i++)
    {
        m_tabNbPodEachPlayerPresent[i] = tabPod[i];
    }
}

bool Zone::isOwnPodPresent(int myId)
{
    return m_tabNbPodEachPlayerPresent[myId] != 0;
}

int Zone::getNbOwnPodPresent(int myId)
{
    return m_tabNbPodEachPlayerPresent[myId];
}

void Zone::display()
{
    cerr<<"============================================="<<endl;
    cerr<<"Zone "<<m_id<<" owned by "<<m_ownerId<<" produces "<<m_platiniumSource<<" platinum"<<endl;
    cerr<<"Troops present : P0 -> "<<m_tabNbPodEachPlayerPresent[0]<<" | P1 -> "<<m_tabNbPodEachPlayerPresent[1]<<" | P2 -> "<<
        m_tabNbPodEachPlayerPresent[2]<<" | P3 -> "<<m_tabNbPodEachPlayerPresent[3]<<endl;
    cerr<<"-------- adjacent zones -------"<<endl;
    for(int i = 0; i < m_vecAdjacentZones.size(); i++)
    {
        cerr<<m_vecAdjacentZones[i]<<" | ";
    }
    cerr<<endl;
}

class ComparePlatinumQuantity
{
    public:
        bool operator()(Zone zone1, Zone zone2)
        {
            return zone1.getPlatiniumSource() > zone2.getPlatiniumSource();
        }
};

/* function */
void displayAllZones(vector<Zone> vecZones)
{
    for(int i = 0; i < vecZones.size(); i++)
    {
        vecZones[i].display();
    }
}

string createMovingOrders(int myId, vector<Zone> vecZones)
{
    int idZoneDest = 0;
    int idZoneOrigine = 0;
    int nbOfDest = 0;
    int indexAlea = 0;
    string orders;

    for(int i = 0; i < vecZones.size(); i++)
    {
        ostringstream oss1;
        ostringstream oss2;
        if(vecZones[i].isOwnPodPresent(myId))
        {
            idZoneOrigine = vecZones[i].getZoneId();
            nbOfDest = vecZones[i].getVecAdjacentZones().size();
            cerr<<"idZone : "<<idZoneOrigine<<" nbOfDest : "<<nbOfDest<<endl;
            indexAlea = rand() % nbOfDest;
            idZoneDest = vecZones[i].getVecAdjacentZones()[indexAlea];
            cerr<<"indexAlea : "<<indexAlea<<" idZoneDest : "<<idZoneDest<<endl;

            oss1 << idZoneOrigine;
            orders += "1 " + oss1.str() + " ";
            oss2 << idZoneDest;
            orders += oss2.str() + " ";
        }
    }
    if(!orders.empty())
    {
        orders.pop_back();
        return orders;
    }
    else
        return "WAIT";
}

int findZoneOfDeployment(int myId, vector<Zone> &vecZones)
{
    vector<int> vecIdZonesWithPlatinum;
    // displayAllZones(vecZones);
    for(int i = 0; i < vecZones.size(); i++)
    {
        if(vecZones[i].getPlatiniumSource() > 0)
        {
            vecIdZonesWithPlatinum.push_back(vecZones[i].getZoneId());
            // cerr<<"id zone with platinum "<<vecIdZonesWithPlatinum[i]<<endl;
        }
    }
    // for(int i = 0; i < vecIdZonesWithPlatinum.size(); i++)
    // {
    //     cerr<<"zone plat : "<<vecIdZonesWithPlatinum[i]<<endl;
    // }
    
    for(int i = 0; i < vecIdZonesWithPlatinum.size(); i++)
    {
        int zoneOwnerId = vecZones[i].getOwnerId();
        // cerr<<"zoneOwnerId : "<<zoneOwnerId<<endl;
        if((zoneOwnerId == myId || zoneOwnerId == -1) && (vecZones[i].getTabNbPodEachPlayerPresent()[myId] == 0))
        {
            vecZones[i].addPodInTabPodEachPlayerPresent(myId, 1);
            // displayAllZones(vecZones);
            return vecZones[i].getZoneId();
        }
    }
    return vecIdZonesWithPlatinum[0]; 
}

string createBuyingOrders(int myId, vector<Zone> vecZones, int platinumReserve)
{
    string orders;
    int deployingZoneId = 0;

    if(platinumReserve >= 20)
    {
        while(platinumReserve >= 20)
        {
            ostringstream oss;
            // cerr<<"platinumReserve : "<<platinumReserve<<endl;
            deployingZoneId = findZoneOfDeployment(myId, vecZones);
            // displayAllZones(vecZones);
            // cerr<<"deployingZoneId : "<<deployingZoneId<<endl;
            oss << deployingZoneId;
            orders += "1 " + oss.str() + " ";
     
            platinumReserve -= 20;
        }
        orders.pop_back();
        return orders;
    }
    else
        return "WAIT";
}

int main()
{
    int playerCount; // the amount of players (2 to 4)
    int myId; // my player ID (0, 1, 2 or 3)
    int zoneCount; // the amount of zones on the map
    int linkCount; // the amount of links between all zones
    vector<Zone> vecZones;

    srand (time(NULL));
    cin >> playerCount >> myId >> zoneCount >> linkCount; cin.ignore();
    // cerr<<"zoneCount : "<<zoneCount<<endl;

    for (int i = 0; i < zoneCount; i++)
    {
        int zoneId; // this zone's ID (between 0 and zoneCount-1)
        int platinumSource; // the amount of Platinum this zone can provide per game turn
        cin >> zoneId >> platinumSource; cin.ignore();
        vecZones.push_back(Zone(zoneId, platinumSource));
    }

    for (int i = 0; i < linkCount; i++) {
        int zone1;
        int zone2;
        cin >> zone1 >> zone2; cin.ignore();
        vecZones[zone1].addAdjacentZone(zone2);
        vecZones[zone2].addAdjacentZone(zone1);
    }
    sort(vecZones.begin(), vecZones.end(), ComparePlatinumQuantity());

    // displayAllZones(vecZones);

    int counter = 0; //for debug
    // while(counter < 1) 
    while(1)
    {
        int platinumReserve;
        cin >> platinumReserve; cin.ignore();

        for (int i = 0; i < zoneCount; i++)
        {
            int zId; // this zone's ID
            int ownerId; // the player who owns this zone (-1 otherwise)
            int podsP0; // player 0's PODs on this zone
            int podsP1; // player 1's PODs on this zone
            int podsP2; // player 2's PODs on this zone (always 0 for a two player game)
            int podsP3; // player 3's PODs on this zone (always 0 for a two or three player game)
            cin >> zId >> ownerId >> podsP0 >> podsP1 >> podsP2 >> podsP3; cin.ignore();
            // cerr<<zId<<" | "<<ownerId<<" | "<<podsP0<<" | "<<podsP1<<" | "<<podsP2<<" | "<<podsP3<<endl;

            int tabPod[4] = {podsP0, podsP1, podsP2, podsP3};
            for(int j = 0; j < zoneCount; j++)
            {
                if(vecZones[j].getZoneId() == zId)
                {
                    // cerr<<"j : "<<j<<" vecZOne i : "<<vecZones[j].getZoneId()<<endl;
                    // cerr<<"ownerId : "<<ownerId<<endl;
                    vecZones[j].setIdOwner(ownerId);
                    vecZones[j].setTabPodEachPlayerPresent(tabPod);
                    break;
                }
            }       
        }

        // displayAllZones(vecZones);
        cout << createMovingOrders(myId, vecZones) << endl; // movements
        cout << createBuyingOrders(myId, vecZones, platinumReserve)<<endl; // buying
        counter++;
    }
}