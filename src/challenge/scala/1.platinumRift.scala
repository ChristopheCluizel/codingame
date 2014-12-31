import math._
import scala.util._
import scala.collection.mutable.ArrayBuffer
import scala.util.control.Breaks._
import java.util.Random

/**
 * TicToc allows for easy benchmarking of different parts in source code.
 * Just inherit the TicToc trait, then start a time measurement with tic,
 * and stop it using toc.
 * As of now tic-tocs can be nested but can not overlap, as the underlying
 * data structure is a stack: a toc always terminates the last tic.
 * The reason for this decision was that the TicToc trait and its methods
 * should be as lightweight as possible in order not to falsify the measured
 * run times.
 * @author fgysin
 */
trait TicToc {
  import scala.collection.mutable.LinkedList
  import scala.collection.mutable.Stack
  import java.io._

  var timeCounter: Int = 0
  var tics: Stack[Long] = Stack()
  var times: LinkedList[(String, Long)] = LinkedList()

  /**
   * Starts a time measurement.
   */
  def tic() {
    tics = tics.push(System.currentTimeMillis())
  }

  /**
   * Stops the last started time measurement.
   * @param descr a description of the last measurement period
   */
  def toc(descr: String) {
    var t = System.currentTimeMillis() - tics.pop()
    if (null != descr && !"".equals(descr))
      times = times :+ (descr, t)
    else {
      times = times :+ ("time" + timeCounter, t)
      timeCounter += 1
    }
  }

  /**
   * Write the logged times to a file. There is some formatting sugar contained
   * that checks if a file with this name already exists. If yes, the run times
   * are added at the bottom of the existing file (this is useful if you repeat
   * the same measurement multiple times), else the file is created.
   * @param path The path of the file to write the times log.
   */
  def writeTimesLog(path: String) {
    var linesToPrint = outLines
    try {
      // Check if the file was alreay created, if yes only
      // append the timings not the timing information.
      val lr = new LineNumberReader(new FileReader(path))
      val read = lr.readLine()
      if (null != read && read.startsWith("Timings")) {
        linesToPrint = linesToPrint.drop(2)
      }
      lr.close()
    } catch {
      case _ =>
    }
    // Write the timings and or timing information.
    val fw = new FileWriter(path, true);
    linesToPrint.foreach { l => fw.write(l + "\n"); }
    fw.close()
  }

  /**
   * Print the logged times.
   */
  def printTimesLog() {
    outLines.foreach { l => println(l); }
  }

  /**
   * String output of the current times and their respective descriptions.
   * @return
   */
  def outLines(): List[String] = {
    var list = List[String]()
    list ::= ("Timings of " + this.getClass().toString())
    list ::= "description:" + times.map(x => "\t" + x._1).reduce(_ + _)
    list ::= "times(ms):" + times.map(x => "\t" + x._2).reduce(_ + _)
    list.reverse
  }

}

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
    var idZoneMySpawn = 0
    var idZoneEnemySpawn = 0

    def isAllPlatinumZonesOwned: Boolean = {
        for(i <- platinumZones){
            if(!nodes(i).ownedBy(myId)) return false
        }
        return true
    }

    def idAdjacentZoneFree(idZone: Int): Int = {
        for(i <- adjacence(idZone)){
            if(nodes(i).ownerId != myId) return i
        }
        return -42
    }

    def isHalfPlatinumZonesOwned: Boolean = {
        var nbPlatinumZonesOwned = 0
        for(i <- platinumZones){
            if(nodes(i).ownerId == myId) nbPlatinumZonesOwned +=1
        }
        // Console.err.println("nbPlatinumZonesOwned : " + nbPlatinumZonesOwned)
        return (nbPlatinumZonesOwned >= (platinumZones.length / 3))
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
            var idZoneFreeNextToActualZone = idAdjacentZoneFree(idZoneFrom)
            if(idZoneFreeNextToActualZone != -42) {
                idZoneFather = idZoneFreeNextToActualZone
            }
            else {
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
            }
            nodes(idZoneFather).ownerId = myId
            orders += "1 " + idZoneFrom + " " + idZoneFather + " "
        }
        orders
    }

    def move: String = {
        var orders = ""
        nodes.keys.foreach{ i =>
            breakable {while(nodes(i).pods(myId) > 0){
                // if(i == idZoneMySpawn && nodes(i).pods(myId) <= 5) break
                orders += widthGraphMove(i)
                if(!orders.isEmpty) nodes(i).pods(myId) -= 1
            }}
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

        // nodes.keys.foreach{ i =>
        //     if(myPlatinum >= 20){
        //         orders += spawnNextToFreeZone(i)
        //     }
        // }
        // if(orders.length != 0) orders else "WAIT"
        return "WAIT"
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

object Player extends TicToc{

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

        var firstTurn = true
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
            if(firstTurn) {
                for(i <- 0 until nbZonesTotal) {
                    if(graph.nodes(i).ownedBy(myId)) graph.idZoneMySpawn = i
                    if(graph.nodes(i).isZoneWithEnemy(myId)) graph.idZoneEnemySpawn = i
                }
                // Console.err.println("my spawn : " + graph.idZoneMySpawn)
                // Console.err.println("his spawn : " + graph.idZoneEnemySpawn)
                firstTurn = false
            }
            //Console.err.println(graph.toString)

            //tic
            println(graph.move) // first line for movement commands, second line for POD purchase (see the protocol in the statement for details)
            //toc("Move")
            //Console.err.println(outLines)
            println(graph.invade)
        }
    }
}
