import math._
import scala.util._
import scala.collection.mutable.ArrayBuffer

class Graph[T](nbNodes: Int) {
    var adjacence: Map[Int, ArrayBuffer[Int]] = Map()

    def addNode(key: Int, node: T) = {
        adjacence += (key -> new ArrayBuffer())
    }
    def addEdge(key1 :Int, key2:Int, value: Int) = {
        adjacence(key1) += (key2)
    }
    def removeEdge(key1 :Int, key2 :Int) = {
        adjacence(key1) -= key2
        adjacence(key2) -= key1
    }
    def isEmpty: Boolean = adjacence.isEmpty
    def nodePresent(key: Int): Boolean = adjacence.contains(key)
    def edgePresent(key1: Int, key2: Int): Boolean = adjacence(key1).contains(key2)
    def getPredecessors(key: Int): ArrayBuffer[Int] = {
        var predecessors: ArrayBuffer[Int] = ArrayBuffer()
        for(i <- 0 until adjacence.size) {
            if(adjacence(i).contains(key)) {
                predecessors += i
            }
        }
        predecessors
    }
    def getSuccessors(key: Int): ArrayBuffer[Int] = adjacence(key)

    def breadthFirstSearch(key: Int): String = {
        var queue = new scala.collection.mutable.Queue[Int]
        var markedNode: ArrayBuffer[Int] = ArrayBuffer()
        var actualNodeKey = 0
        var listNodesVisited = ""

        queue += key
        while(!queue.isEmpty) {
            actualNodeKey = queue.dequeue
            markedNode += actualNodeKey
            listNodesVisited += actualNodeKey.toString + ", "   // for debug
            // treat actual node here
            for(i <- getSuccessors(actualNodeKey)) if(!markedNode.contains(i) && !queue.contains(i)) queue += i
        }
        listNodesVisited = listNodesVisited.dropRight(2)
        listNodesVisited
    }

    def calculateEccentricityOf(key: Int): (Int, Int) = {
        var queue = new scala.collection.mutable.Queue[Int]
        var markedNode: ArrayBuffer[Int] = ArrayBuffer()
        var actualNodeKey = 0
        var listNodesVisited = ""
        var eccentricity = 0
        var distances: scala.collection.mutable.Map[Int, Int] = scala.collection.mutable.Map()

        adjacence.keys.foreach(i => distances += (i -> -1))

        distances.update(key, 0)
        queue += key
        while(!queue.isEmpty) {
            actualNodeKey = queue.dequeue
            for(i <- getSuccessors(actualNodeKey)) if(distances(i) == -1) {
                queue += i
                distances.update(i, distances(actualNodeKey) + 1)
                eccentricity = distances(i)
            }
        }
        (key, eccentricity)
    }

    def keyToCoordinates(key: Int): Position = new Position(key / 4, key % 4 - 1)
    def coordinatesToKey(y: Int, x: Int, width: Int): Int = width * y + x

    def display = adjacence.keys.foreach {i =>
        Console.err.println("key : " + i + ", Node : " + adjacence(i).toString +
                ", Successors : " + getSuccessors(i).mkString(", ") +
                ", Predecessors : " + getPredecessors(i).mkString(", "))
    }
}

object Orientation extends Enumeration {
    type Orientation = Value
    val H, V = Value
}

import Orientation._

class Dragon(var id: Int, var nbWallLeft: Int, var position: Position) {
    override def toString: String = "Dragon id : " + id + " position : "  + position + " nbWallLeft : " + nbWallLeft
}

class Position(var y: Int, var x: Int) {
    override def toString: String = "(" + x + ", " + y + ")"
}

class Wall(var position: Position, var orientation: String) {
    override def toString: String = "Wall position " + position + ", orientation : " + orientation
}

class Labyrinth(val width: Int, val height: Int, val nbPlayers: Int, val myId: Int) {
    var nbWallDeployed = 0
    var walls: ArrayBuffer[Wall] = ArrayBuffer()
    var graph = new Graph[Int](width * height)
    initiateGraph

    def initiateGraph = {
        var counter = 0
        for(i <- 0 until height) {
            for(j <- 0 until width) {
                graph.addNode(counter, counter)
                counter += 1
            }
        }
        for(i <- 0 until height) {
            for(j <- 0 until width) {
                if(i - 1 >= 0) graph.addEdge(graph.coordinatesToKey(i, j, width), graph.coordinatesToKey(i-1, j, width), 1)
                if(i + 1 < height) graph.addEdge(graph.coordinatesToKey(i, j, width), graph.coordinatesToKey(i+1, j, width), 1)
                if(j - 1 >= 0) graph.addEdge(graph.coordinatesToKey(i, j, width), graph.coordinatesToKey(i, j-1, width), 1)
                if(j + 1 < height) graph.addEdge(graph.coordinatesToKey(i, j, width), graph.coordinatesToKey(i, j+1, width), 1)
            }
        }
    }
    def update(wall: Wall) = {
        if(wall.orientation == "H") {
            if(wall.position.y -1 >= 0) {
                graph.removeEdge(graph.coordinatesToKey(wall.position.y, wall.position.x, width), graph.coordinatesToKey(wall.position.y -1, wall.position.x, width))
                if(wall.position.x + 1 < width)
                    graph.removeEdge(graph.coordinatesToKey(wall.position.y, wall.position.x + 1, width), graph.coordinatesToKey(wall.position.y -1, wall.position.x + 1, width))
            }
        }
        if(wall.orientation == "V") {
            if(wall.position.x - 1 >= 0) {
                graph.removeEdge(graph.coordinatesToKey(wall.position.y, wall.position.x, width), graph.coordinatesToKey(wall.position.y, wall.position.x - 1, width))
                if(wall.position.y + 1 < height)
                    graph.removeEdge(graph.coordinatesToKey(wall.position.y + 1, wall.position.x, width), graph.coordinatesToKey(wall.position.y +1, wall.position.x - 1, width))
            }
        }
    }

    override def toString: String = {
        var string = "Labyrinth width : " + width + ", height : " + height + ", nbPlayer : " + nbPlayers + ", myId : " + myId +
            ",  nbWallDeployed : " + nbWallDeployed + "\n"
        for(i <- 0 until walls.length) string += walls(i) + "\n"
        string
    }
}

object Player {

    def main(args: Array[String]) {
        // w: width of the board
        // h: height of the board
        // playercount: number of players (2,3, or 4)
        // myid: id of my player (0 = 1st player, 1 = 2nd player, ...)
        val Array(width, height, nbPlayer, myId) = for(i <- readLine split " ") yield i.toInt
        var labyrinth = new Labyrinth(width, height, nbPlayer, myId)
        var dragons = new Array[Dragon](nbPlayer)
        var previousWallCount = 0
        for(i <- 0 until nbPlayer) {
            dragons(i) = new Dragon(i, 0, new Position(0, 0))
        }

        // game loop
        while(true) {
            for(i <- 0 until nbPlayer) {
                // x: x-coordinate of the player
                // y: y-coordinate of the player
                // wallsleft: number of walls available for the player
                val Array(x, y, wallsleft) = for(i <- readLine split " ") yield i.toInt
                dragons(i).id = i
                dragons(i). nbWallLeft = wallsleft
                dragons(i).position = new Position(y, x)
                Console.err.println(dragons(i).toString)
            }

            val wallcount = readInt // number of walls on the board
            labyrinth.nbWallDeployed = wallcount
            while(labyrinth.walls.length < wallcount) labyrinth.walls += new Wall(new Position(0, 0), "")

            for(i <- previousWallCount until wallcount) {
                // wallx: x-coordinate of the wall
                // wally: y-coordinate of the wall
                // wallorientation: wall orientation ('H' or 'V')
                val Array(_wallx, _wally, wallorientation) = readLine split " "
                val wallx = _wallx.toInt
                val wally = _wally.toInt
                labyrinth.walls(i).position = new Position(wally, wallx)
                labyrinth.walls(i).orientation = wallorientation
                labyrinth.update(labyrinth.walls(i))
            }
            previousWallCount = wallcount

            Console.err.println(labyrinth)
            // labyrinth.graph.display

            println("RIGHT") // action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
        }
    }
}
