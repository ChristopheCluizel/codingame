import math._
import scala.util._
import scala.collection.mutable.ArrayBuffer
import scala.util.control.Breaks._

class Node(val id: Int, val platinumSource: Int, var ownerId: Int, var pods: Array[Int]) {
    override def toString = f"Id : $id%d, platinumSource : $platinumSource%d, ownerId : $ownerId \n" + pods.mkString(", ")

    def update(ownerId: Int, pods: Array[Int]){
        this.ownerId = ownerId
        pods.copyToArray(this.pods)
    }

    def podsOnePlayerArePresent(idPlayer: Int): Boolean = if(pods(idPlayer) != 0) true else false
    def isZoneFree: Boolean = if(pods.sum == 0) true else false
}

class Graph(val nbPlayers: Int, val myId: Int, val nbTotalZones: Int, val nbTotalLinks: Int) {
    var nodes: Map[Int, Node] = Map()
    var adjacence: ArrayBuffer[ArrayBuffer[Int]] = ArrayBuffer()
    var myPlatinum = 0

    override def toString = {
        var listNode = ""
        for(i <- nodes){
            listNode += i.toString + "\n"
        }
        listNode
    }

    def displayNeighbours(idZone: Int) {
        Console.err.println(adjacence(idZone).mkString(", "))
    }

    def move: String = {
        "WAIT"
    }

    def invade: String = {
        var orders = ""

        nodes.keys.foreach{ i =>
            if(myPlatinum >= 20){
                orders += spawnNextToFreeZone(i)
            }
        }
        if(orders.length != 0) orders else "WAIT"
    }

    private def spawnNextToFreeZone(idZone: Int): String = {
        var orders = ""
        // Console.err.println(nodes(idZone).toString)
        if(nodes(idZone).podsOnePlayerArePresent(myId)){
            var neighbours = adjacence(idZone)
            // Console.err.println("idZone : " + idZone + " -> " + neighbours.mkString(", "))
            breakable {for(j <- 0 until neighbours.length) if(nodes(neighbours(j)).isZoneFree) {
                // Console.err.println("Zone %d is free", nodes(neighbours(j)).id)
                nodes(idZone).pods(myId) += 1
                orders += "1 " + nodes(idZone).id + " "
                myPlatinum -= 20
                // Console.err.println(orders)
                break
            }}
        }

        orders
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
            graph.adjacence += ArrayBuffer()
            graph.nodes += (zoneId -> new Node(zoneId, platinumSource, -1, Array(0, 0, 0, 0)))
        }

        for(i <- 0 until nbLinksTotal) {
            val Array(zone1, zone2) = for(i <- readLine split " ") yield i.toInt
            graph.adjacence(zone1) += zone2
            graph.adjacence(zone2) += zone1
        }
        // graph.displayNeighbours(0)

        while(true) {
            val myPlatinum = readInt // my available Platinum
            graph.myPlatinum = myPlatinum
            for(i <- 0 until nbZonesTotal) {
                // zoneId: this zone's ID
                // ownerId: the player who owns this zone (-1 otherwise)
                // podsp0: player 0's PODs on this zone
                // podsp1: player 1's PODs on this zone
                // podsp2: player 2's PODs on this zone (always 0 for a two player game)
                // podsp3: player 3's PODs on this zone (always 0 for a two or three player game)
                val Array(zoneId, ownerId, podsp0, podsp1, podsp2, podsp3) = for(i <- readLine split " ") yield i.toInt
                graph.nodes(zoneId).update(ownerId, Array(podsp0, podsp1, podsp2, podsp3))
            }
            //Console.err.println(graph.toString)

            println(graph.move) // first line for movement commands, second line for POD purchase (see the protocol in the statement for details)
            println(graph.invade)
        }
    }
}
