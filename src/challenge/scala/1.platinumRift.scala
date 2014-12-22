import math._
import scala.util._
import scala.collection.mutable.ArrayBuffer
import scala.util.control.Breaks._
import java.util.Random

class Node(val id: Int, val platinumSource: Int, var ownerId: Int, var pods: Array[Int]) {
    override def toString = f"Id : $id%d, platinumSource : $platinumSource%d, ownerId : $ownerId \n" + pods.mkString(", ")

    def update(ownerId: Int, pods: Array[Int]){
        this.ownerId = ownerId
        pods.copyToArray(this.pods)
    }

    def podsOnePlayerArePresent(idPlayer: Int): Boolean = if(pods(idPlayer) != 0) true else false
    def isZoneFree(myId: Int): Boolean = if(myId != this.ownerId) true else false
    def isZoneWithEnemy(myId: Int): Boolean = if(isZoneFree(myId) && ownerId != -1) true else false
    def isZoneWithPlatinum: Boolean = if(platinumSource > 0) true else false
    def ownedBy(ownerId: Int): Boolean = if(ownerId == this.ownerId) true else false
}

class Graph(val nbPlayers: Int, val myId: Int, val nbTotalZones: Int, val nbTotalLinks: Int) {
    var nodes: Map[Int, Node] = Map()
    var platinumZones: ArrayBuffer[Int] = ArrayBuffer()
    var adjacence: ArrayBuffer[ArrayBuffer[Int]] = ArrayBuffer()
    var myPlatinum = 0

    def isAllPlatinumZonesOwned: Boolean = {
        for(i <- platinumZones){
            if(!nodes(i).ownedBy(myId)) return false
        }
        return true
    }

    def isHalfPlatinumZonesOwned: Boolean = {
        var nbPlatinumZonesOwned = 0
        for(i <- platinumZones){
            if(nodes(i).ownerId == myId) nbPlatinumZonesOwned +=1
        }
        // Console.err.println("nbPlatinumZonesOwned : " + nbPlatinumZonesOwned)
        return (nbPlatinumZonesOwned >= (platinumZones.length / 2))
    }

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

    private def widthGraphMove(idZoneFrom: Int): String = {
        var orders = ""
        var queue = new scala.collection.mutable.Queue[Int]
        var actualIdNode = 0
        var markedNode: ArrayBuffer[Int] = ArrayBuffer()
        var idTarget = 0
        var fathers: Map[Int, Int] = Map()
        var idZoneFather = 0
        var zoneConditionsToBeATarget = false

        if(nodes(idZoneFrom).ownedBy(myId) && nodes(idZoneFrom).podsOnePlayerArePresent(myId)){
            queue += idZoneFrom
            breakable { while(!queue.isEmpty){
                actualIdNode = queue.dequeue
                markedNode += actualIdNode
                if(!isHalfPlatinumZonesOwned){
                    zoneConditionsToBeATarget = nodes(actualIdNode).isZoneFree(myId) && nodes(actualIdNode).isZoneWithPlatinum
                }
                else{
                     zoneConditionsToBeATarget = nodes(actualIdNode).isZoneFree(myId)
                }
                if(zoneConditionsToBeATarget) {
                        // Console.err.println("Plus de platinum !!!")
                        idTarget = actualIdNode
                        idZoneFather = idTarget
                        while(fathers(idZoneFather) != idZoneFrom){
                            idZoneFather = fathers(idZoneFather)
                        }
                        // Console.err.println("idZoneFrom : " + idZoneFrom + " -> father : " + idZoneFather + " dest : " + idTarget)
                        break
                    }

                for(i <- adjacence(actualIdNode)){
                    if(!markedNode.contains(i) && !queue.contains(i)){
                        queue += i
                        fathers += (i -> actualIdNode)
                    }
                }
            }}
            orders += "1 " + idZoneFrom + " " + idZoneFather + " "
        }
        orders
    }

    def move: String = {
        var orders = ""
        nodes.keys.foreach{ i =>
            while(nodes(i).pods(myId) > 0){
                orders += widthGraphMove(i)
                if(!orders.isEmpty) nodes(i).pods(myId) -= 1
            }
        }
        if(orders.length != 0) orders else "WAIT"
    }

    private def randomMove(idZoneFrom: Int): String = {
        var orders = ""
        if(nodes(idZoneFrom).ownedBy(myId) && nodes(idZoneFrom).podsOnePlayerArePresent(myId)){
            // var neighboursFree = for{i <- adjacence(idZoneFrom) if(nodes(i).isZoneFree(myId)} yield i
            var neighbours = adjacence(idZoneFrom)
            // Console.err.println("idZone : " + idZoneFrom + " -> " + neighbours.mkString(", "))
            val rand = new Random(System.currentTimeMillis());
            val random_index = rand.nextInt(neighbours.length);
            // Console.err.println("from : " + idZoneFrom + " to " + neighbours(random_index))
            orders += "1 " + idZoneFrom + " " + neighbours(random_index) + " "
        }
        orders
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
        if(nodes(idZone).ownedBy(myId)){
            var neighbours = adjacence(idZone)
            var neighboursWithEnemy = for{i <- neighbours if(nodes(i).isZoneWithEnemy(myId))}yield i
            if(neighboursWithEnemy.length != 0){
                breakable {for(j <- 0 until neighboursWithEnemy.length) if(nodes(neighboursWithEnemy(j)).isZoneFree(myId)) {
                    // Console.err.println("Zone %d is free", nodes(neighbours(j)).id)
                    orders += "1 " + idZone + " "
                    myPlatinum -= 20
                    // Console.err.println(orders)
                    break
                }}
            }
            // else
            // {
            //     // Console.err.println("idZone : " + idZone + " -> " + neighbours.mkString(", "))
            //     breakable {for(j <- 0 until neighbours.length) if(nodes(neighbours(j)).isZoneFree(myId)) {
            //         // Console.err.println("Zone %d is free", nodes(neighbours(j)).id)
            //         orders += "1 " + nodes(idZone).id + " "
            //         myPlatinum -= 20
            //         // Console.err.println(orders)
            //         break
            //     }}
            // }
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
            if(platinumSource > 0) graph.platinumZones += zoneId
        }
        // Console.err.println(graph.platinumZones.mkString(", "))

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
