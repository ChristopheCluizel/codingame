import math._
import scala.util._

class Node(val id: Int, val platinumSource: Int, var ownerId: Int, var pods: Array[Int]) {
    override def toString = f"Id : $id%d, platinumSource : $platinumSource%d, ownerId : $ownerId \n" + pods.mkString(", ")
}

class Graph(val nbPlayers: Int, val myId: Int, val nbTotalZones: Int, val nbTotalLinks: Int) {
    var nodes:Map[Int, Map[Int, Node]] = Map()

    override def toString = {
        var listNode = ""
        for((id, adjacentNodes) <- nodes)
            listNode += adjacentNodes.head.toString + "\n"
        listNode
    }
}

object Player {

    def main(args: Array[String]) {
        // nbPlayers: the amount of players (2 to 4)
        // myId: my player ID (0, 1, 2 or 3)
        // nbZonesTotal: the amount of zones on the map
        // nbLinksTotal: the amount of links between all zones
        val Array(nbPlayers, myId, nbZonesTotal, nbLinksTotal) = for(i <- readLine split " ") yield i.toInt
        var graph = new Graph(nbPlayers, myId, nbZonesTotal, nbLinksTotal)

        for(i <- 0 until nbZonesTotal) {
            // zoneId: this zone's ID (between 0 and nbZonesTotal-1)
            // platinumSource: the amount of Platinum this zone can provide per game turn
            val Array(zoneId, platinumSource) = for(i <- readLine split " ") yield i.toInt
            graph.nodes += (zoneId -> Map(zoneId -> new Node(zoneId, platinumSource, -1, Array(0, 0, 0, 0))))
        }
        Console.err.println(graph.toString)

        for(i <- 0 until nbLinksTotal) {
            val Array(zone1, zone2) = for(i <- readLine split " ") yield i.toInt
        }

        // game loop
        while(true) {
            val myPlatinum = readInt // my available Platinum
            for(i <- 0 until nbZonesTotal) {
                // zoneId: this zone's ID
                // ownerId: the player who owns this zone (-1 otherwise)
                // podsp0: player 0's PODs on this zone
                // podsp1: player 1's PODs on this zone
                // podsp2: player 2's PODs on this zone (always 0 for a two player game)
                // podsp3: player 3's PODs on this zone (always 0 for a two or three player game)
                val Array(zoneId, ownerId, podsp0, podsp1, podsp2, podsp3) = for(i <- readLine split " ") yield i.toInt
            }

            println("WAIT") // first line for movement commands, second line for POD purchase (see the protocol in the statement for details)
            println("1 73")
        }
    }
}
