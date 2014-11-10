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
    vector<Zone> getAdjacentZones();
    vector<int> getVecIdAdjacentZones();
    int getNbOwnPodPresent(int myId);

    void setIdOwner(int idOwner);
    void addAdjacentZone(int zoneId);
    void addPodInTabPodEachPlayerPresent(int indexPlayer, int nbPod);
    void setTabPodEachPlayerPresent(int tabPod[]);

    bool isOwnPodPresent(int myId);
    int findIdAjacentZoneWithMaxPlatinum(int myId);
    int createMovingOrders_randomMove();

    /* for debug */
    void display();

private:
    int m_id;
    int m_ownerId;
    int m_platiniumSource;
    vector<int> m_vecIdAdjacentZones;   // should be deleted ??
    vector<Zone> m_vecAdjacentZones;
    int m_tabNbPodEachPlayerPresent[4];
};

class ComparePlatinumQuantity
{
    public:
        bool operator()(Zone zone1, Zone zone2)
        {
            return zone1.getPlatiniumSource() > zone2.getPlatiniumSource();
        }
};

/* global variables */
vector<Zone> vecZones;

/* declaration of functions */
Zone getZoneWithId(int idZone);
void displayAllZones(vector<Zone> vecZones);

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

vector<int> Zone::getVecIdAdjacentZones()
{
    return m_vecIdAdjacentZones;
}

vector<Zone> Zone::getAdjacentZones()
{
    return m_vecAdjacentZones;
}   

void Zone::setIdOwner(int idOwner)
{
    m_ownerId = idOwner;
}

void Zone::addAdjacentZone(int zoneId)
{
    m_vecIdAdjacentZones.push_back(zoneId);
    m_vecAdjacentZones.push_back(getZoneWithId(zoneId));
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

int Zone::findIdAjacentZoneWithMaxPlatinum(int myId)
{
    vector<Zone> vecZonesPotentialDestination;

    // cerr<<"idZone : "<<m_id<<endl;
    for(int i = 0; i < m_vecAdjacentZones.size(); i++)
    {
        if(getZoneWithId(m_vecAdjacentZones[i].getZoneId()).getOwnerId() != myId)
            vecZonesPotentialDestination.push_back(m_vecAdjacentZones[i]);
    }
    // displayAllZones(vecZonesPotentialDestination);
    if(vecZonesPotentialDestination.empty())    // all the adjacent zones are mine -> random move
    {
        return createMovingOrders_randomMove();
    }
    else
    {
        for(int i = 0; i < vecZonesPotentialDestination.size(); i++)
        {
            if(vecZonesPotentialDestination[i].getPlatiniumSource() == 0)
                vecZonesPotentialDestination.erase(vecZonesPotentialDestination.begin() + i);
        }
        sort(vecZonesPotentialDestination.begin(), vecZonesPotentialDestination.end(), ComparePlatinumQuantity());

        if(!vecZonesPotentialDestination.empty())
            return vecZonesPotentialDestination[0].getZoneId();
        else
            return createMovingOrders_randomMove();
    }
}

void Zone::display()
{
    cerr<<"============================================="<<endl;
    cerr<<"Zone "<<m_id<<" owned by "<<m_ownerId<<" produces "<<m_platiniumSource<<" platinum"<<endl;
    cerr<<"Troops present : P0 -> "<<m_tabNbPodEachPlayerPresent[0]<<" | P1 -> "<<m_tabNbPodEachPlayerPresent[1]<<" | P2 -> "<<
        m_tabNbPodEachPlayerPresent[2]<<" | P3 -> "<<m_tabNbPodEachPlayerPresent[3]<<endl;
    cerr<<"-------- adjacent zones -------"<<endl;
    for(int i = 0; i < m_vecIdAdjacentZones.size(); i++)
    {
        cerr<<m_vecIdAdjacentZones[i]<<" | ";
    }
    cerr<<endl;
}

int Zone::createMovingOrders_randomMove()
{
    int index;
    int nbOfDest = m_vecAdjacentZones.size();

    index = rand() % nbOfDest;

    return m_vecAdjacentZones[index].getZoneId(); 
}

/* function */
void displayAllZones(vector<Zone> vecZones)
{
    for(int i = 0; i < vecZones.size(); i++)
    {
        vecZones[i].display();
    }
}

Zone getZoneWithId(int idZone)
{
    for(int i = 0; i < vecZones.size(); i++)
    {
        if(vecZones[i].getZoneId() == idZone)
        {
            return vecZones[i];
            break;
        }
    }
}

string buildOrdersForOneMovement(int idZoneOrigine, int idZoneDest)
{
    string orders;
    ostringstream oss1;
    ostringstream oss2;

    oss1 << idZoneOrigine;
    orders += "1 " + oss1.str() + " "; // '1' for the move of 1 Pod 
    oss2 << idZoneDest;
    orders += oss2.str() + " ";

    return orders;
}

int createMovingOrders_attractPlatinumMove(Zone zone, int myId)
{
    return zone.findIdAjacentZoneWithMaxPlatinum(myId);
}

string createMovingOrders(int myId)
{
    int idZoneDest = 0;
    int idZoneOrigine = 0;
    // int nbOfDest = 0;
    int indexDest = 0;
    string orders;

    for(int i = 0; i < vecZones.size(); i++)
    {
        if(vecZones[i].isOwnPodPresent(myId))
        {
            idZoneOrigine = vecZones[i].getZoneId();
            // cerr<<"idZone : "<<idZoneOrigine<<" nbOfDest : "<<nbOfDest<<endl;
            // cerr<<"indexAlea : "<<indexAlea<<" idZoneDest : "<<idZoneDest<<endl;
            
            // idZoneDest = vecZones[i].createMovingOrders_randomMove();
            idZoneDest = createMovingOrders_attractPlatinumMove(vecZones[i], myId);
            vecZones[i].addPodInTabPodEachPlayerPresent(myId, 1);

            orders += buildOrdersForOneMovement(idZoneOrigine, idZoneDest);
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

int findZoneOfDeployment(int myId)
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

string createBuyingOrders(int myId, int platinumReserve)
{
    string orders;
    int deployingZoneId = 0;

    if(platinumReserve >= 20)
    {
        while(platinumReserve >= 20)
        {
            ostringstream oss;
            // cerr<<"platinumReserve : "<<platinumReserve<<endl;
            deployingZoneId = findZoneOfDeployment(myId);
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

    bool firstRound = true;
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
        string moveOrderTemp = createMovingOrders(myId);
        string buyingAndDeploy = createBuyingOrders(myId, platinumReserve);

        cout << moveOrderTemp << endl; // movements
        if(firstRound)
        {
            cout<<"WAIT"<<endl;
            firstRound = false;
        }
        else
        {
            cout << buyingAndDeploy <<endl; // buying and deploy
        }

        //cerr<<"move : "<<moveOrderTemp<<endl;
        //cerr<<"buyAndDeploy : "<<buyingAndDeploy<<endl;
    }
}