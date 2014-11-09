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

    void setIdOwner(int idOwner);
    void addAdjacentZone(int zoneId);
    void setTabNbPodEachPlayerPresent(int tabNbPodEachPlayerPresent[]);

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
    m_id = idOwner;
}

void Zone::addAdjacentZone(int zoneId)
{
    m_vecAdjacentZones.push_back(zoneId);
}

void Zone::setTabNbPodEachPlayerPresent(int tabNbPodEachPlayerPresent[])
{
    for(int i = 0; i < 4; i++)
    {
        m_tabNbPodEachPlayerPresent[i] = tabNbPodEachPlayerPresent[i];
    }
}

void Zone::display()
{
    cout<<"============================================="<<endl;
    cout<<"Zone "<<m_id<<" owned by "<<m_ownerId<<" produces "<<m_platiniumSource<<" platinum"<<endl;
    cout<<"Troops present : P0 -> "<<m_tabNbPodEachPlayerPresent[0]<<" | P1 -> "<<m_tabNbPodEachPlayerPresent[1]<<" | P2 -> "<<
        m_tabNbPodEachPlayerPresent[2]<<" | P3 -> "<<m_tabNbPodEachPlayerPresent[3]<<endl;
    cout<<"-------- adjacent zones -------"<<endl;
    for(int i = 0; i < m_vecAdjacentZones.size(); i++)
    {
        cout<<m_vecAdjacentZones[i]<<" | ";
    }
    cout<<endl;
}

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
    return "WAIT";
}

// struct myclass {
//   bool operator() (Zone zone1, Zone zone2) { return (zone1.getPlatiniumSource() > zone2.getPlatiniumSource());}
// } myobject;

int findZoneOfDeployment(int myId, vector<Zone> vecZones)
{
    vector<Zone> vecZonesWithPlatinum;

    for(int i = 0; i < vecZones.size(); i++)
    {
        if(vecZones[i].getPlatiniumSource() > 0)
            vecZonesWithPlatinum.push_back(vecZones[i]);
    }
    // reverse(vecZonesWithPlatinum.begin(), vecZonesWithPlatinum.end(), myobject);
    // displayAllZones(vecZonesWithPlatinum);
    for(int i = 0; i < vecZonesWithPlatinum.size(); i++)
    {
        int zoneOwnerId = vecZonesWithPlatinum[i].getOwnerId();
        // cout<<"zoneOwnerId : "<<zoneOwnerId<<endl;
        if((zoneOwnerId == myId || zoneOwnerId == -1) && (vecZonesWithPlatinum[i].getTabNbPodEachPlayerPresent()[myId] == 0))
            return vecZonesWithPlatinum[i].getZoneId();
    }
    return -1; 
}

string createBuyingOrders(int myId, vector<Zone> vecZones, int platinumReserve)
{
    string orders;
    int deployingZoneId = 0;
    ostringstream oss;

    while(platinumReserve >= 20)
    {
        // cout<<"platinumReserve : "<<platinumReserve<<endl;
        deployingZoneId = findZoneOfDeployment(myId, vecZones);
        // cout<<"deployingZoneId : "<<deployingZoneId<<endl;
        oss << deployingZoneId;
        if(deployingZoneId != -1)
            orders += "1 " + oss.str() + " ";
 
        platinumReserve -= 20;
    }
    orders[orders.size() - 1] = '\0';

    if(!orders.empty())
        return orders;
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
    cin >> playerCount >> myId >> zoneCount >> linkCount; cin.ignore();

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

    // displayAllZones(vecZones);

    int counter = 0; //for debug
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
        }


        cout << createMovingOrders(myId, vecZones) << endl; // movements
        cout << createBuyingOrders(myId, vecZones, platinumReserve) << endl; // buying
        counter++;
    }
}