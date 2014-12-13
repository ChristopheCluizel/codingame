#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <list>

using namespace std;


class Node
{
public:
    Node(int id, bool isGatewayNode)
    {
        m_id = id;
        m_isGatewayNode = isGatewayNode;
    }
    void setIsGatewayNode(bool isGatewayNode)
    {
        m_isGatewayNode = isGatewayNode;
    }
    bool getIsGatewayNode()
    {
        return m_isGatewayNode;
    }
    int getId()
    {
        return m_id;
    }
    void addIdAdjacentNodes(int idAdjacentNode)
    {
        m_idAdjacentNodes.push_back(idAdjacentNode);
    }
    vector<int> getIdAdjacentNodes()
    {
        return m_idAdjacentNodes;
    }
    void deleteIdAdjacentNodes(int idAdjacentNode)
    {
        for(int i = 0; i < m_idAdjacentNodes.size(); i++)
        {
            if(m_idAdjacentNodes[i] == idAdjacentNode)
            {
                m_idAdjacentNodes.erase(m_idAdjacentNodes.begin() + i);
            }
        }
    }
    void displayIdAdjacentNodes()
    {
        cerr<<"IdAdjacentNodes (size : "<<m_idAdjacentNodes.size()<<") of Node "<<m_id<<endl;
        for(int i = 0; i < m_idAdjacentNodes.size(); i++)
        {
            cerr<<m_idAdjacentNodes[i]<<", ";
        }
        cerr<<endl;
    }
    void displayNode()
    {
        cerr<<"---------------------------"<<endl;
        cerr<<"Node "<<m_id<<" -> isGatewayNode : "<<m_isGatewayNode<<endl;
        displayIdAdjacentNodes();
    }

private:
    int m_id;
    bool m_isGatewayNode;
    vector<int> m_idAdjacentNodes;
};

class Network
{
public:
    Network(int nbTotalNodes, int nbLinks, int nbExitGateways)
    {
        m_nbTotalNodes = nbTotalNodes;
        m_nbLinks = nbLinks;
        m_nbExitGateways = nbExitGateways;
    }
    void setIdSkynetNode(int idSkynetNode)
    {
        m_idSkynetNode = idSkynetNode;
    }
    int getIdSkynetNode()
    {
        return m_idSkynetNode;
    }
    int getNbTotalNodes()
    {
        return m_nbTotalNodes;
    }
    int getNbLinks()
    {
        return m_nbLinks;
    }
    int getNbExitGateways()
    {
        return m_nbExitGateways;
    }
    void addNode(Node *node)
    {
        m_nodes.insert(pair<int, Node*>(node->getId(), node));
    }
    void addIdGatewayNode(int idNode)
    {
        m_idGatewayNodes.push_back(idNode);
    }
    vector<int> getIdGatewayNode()
    {
        return m_idGatewayNodes;
    }
    map<int, Node*> getNodes()
    {
        return m_nodes;
    }
    bool idGatewayPresentAmongAdjacentNodes(vector<int> const& idAdjacentNodes, int &idGatewayPresentAmongAdjacentNodes)
    {
        for(int i = 0; i < idAdjacentNodes.size(); i++)
        {
            if(m_nodes.at(idAdjacentNodes[i])->getIsGatewayNode())
            {
                idGatewayPresentAmongAdjacentNodes = idAdjacentNodes[i];
                return true;
            }
        }

        return false;
    }
    bool isIdNodePresent(int idNode)
    {
        if(m_nodes.find(idNode) == m_nodes.end())
            return false;
        else
            return true;
    }
    void displayNodes()
    {
        cerr<<"------------- Id Nodes of network -----------"<<endl;
        for(int i = 0; i < m_nbTotalNodes; i++)
        {
            m_nodes.at(i)->displayNode();
        }
    }
    void displayIdGatewayNodes()
    {
        cerr<<"------------- Id gatewayNodes -----------"<<endl;
        for(int i = 0; i < m_nbExitGateways; i++)
        {
            cerr<<m_idGatewayNodes[i]<<endl;
        }
    }

private:
    int m_nbTotalNodes;
    int m_nbLinks;
    int m_nbExitGateways;
    int m_idSkynetNode;
    map<int, Node*> m_nodes;
    vector<int> m_idGatewayNodes;
};

int main()
{
    srand (time(NULL));
    int nbTotalNodes; // the total number of nodes in the level, including the gateways
    int nbLinks; // the number of links
    int nbExitGateways; // the number of exit gateways
    cin >> nbTotalNodes >> nbLinks >> nbExitGateways; cin.ignore();

    Network network(nbTotalNodes, nbLinks, nbExitGateways);

    for (int i = 0; i < nbLinks; i++)
    {
        int N1; // N1 and N2 defines a link between these nodes
        int N2;
        cin >> N1 >> N2; cin.ignore();
        // cerr<<"N1 : "<<N1<<" -> N2 : "<<N2<<endl;
        if(!network.isIdNodePresent(N1))
        {
            network.addNode(new Node(N1, false));
        }
        if(!network.isIdNodePresent(N2))
        {
            network.addNode(new Node(N2, false));
        }
        network.getNodes().at(N1)->addIdAdjacentNodes(N2);
        network.getNodes().at(N2)->addIdAdjacentNodes(N1);
    }

    // cerr<<"nbTotalNodes : "<<network.getNbTotalNodes()<<endl;
    // cerr<<"nbLinks : "<<network.getNbLinks()<<endl;
    // cerr<<"nbExitGateways : "<<network.getNbExitGateways()<<endl;

    //cerr<<endl<<endl;

    /* add idGatewayNode */
    for (int i = 0; i < nbExitGateways; i++)
    {
        int idGatewayNode; // the index of a gateway node
        cin >> idGatewayNode; cin.ignore();
        network.addIdGatewayNode(idGatewayNode);
        network.getNodes().at(idGatewayNode)->setIsGatewayNode(true);
    }
    // network.displayNodes();
    // network.displayIdGatewayNodes();

    // game loop
    while (1)
    {
        int idSkynetNode; // The index of the node on which the Skynet agent is positioned this turn
        int idNodeDestToCut;
        cin >> idSkynetNode; cin.ignore();

        network.setIdSkynetNode(idSkynetNode);
        if(network.idGatewayPresentAmongAdjacentNodes(network.getNodes().at(idSkynetNode)->getIdAdjacentNodes(), idNodeDestToCut))
        {
            network.getNodes().at(idSkynetNode)->deleteIdAdjacentNodes(idNodeDestToCut);
            network.getNodes().at(idNodeDestToCut)->deleteIdAdjacentNodes(idSkynetNode);
            cout << idSkynetNode <<" "<<idNodeDestToCut << endl;
        }
        else
        {
            int idRandomGateway;
            Node *gatewayNode;
            int counterGateways = 0;
            int idAdjacentZone;

            do
            {
                idRandomGateway = network.getIdGatewayNode()[rand() % nbExitGateways];
                gatewayNode = network.getNodes().at(idRandomGateway);
                counterGateways ++;
            }while(gatewayNode->getIdAdjacentNodes().empty() && counterGateways < network.getNbExitGateways()*10);
            // cerr<<"idRandomGateway : "<<idRandomGateway<<endl;
            // cerr<<"idRandomGatewayByGetId : "<<gatewayNode->getId()<<endl;
            // cerr<<"idAdjacentGateway : "<<gatewayNode->getIdAdjacentNodes()[0]<<endl;
            // gatewayNode->displayIdAdjacentNodes();

            idAdjacentZone = gatewayNode->getIdAdjacentNodes()[0];
            network.getNodes().at(idRandomGateway)->deleteIdAdjacentNodes(idAdjacentZone);
            network.getNodes().at(idAdjacentZone)->deleteIdAdjacentNodes(idRandomGateway);

            cout<<idRandomGateway<<" "<< idAdjacentZone<<endl;
        }

    }
}
