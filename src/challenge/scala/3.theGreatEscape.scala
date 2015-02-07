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

    def breadthFirstSearch(key: Int, height: Int, width: Int): (Array[Int], Array[Int]) = {
        var queue = new scala.collection.mutable.Queue[Int]
        var markedNode: ArrayBuffer[Int] = ArrayBuffer()
        var actualNodeKey = 0
        var fathers = new Array[Int](height*width)
        // var listNodesVisited = ""
        var distancesArray = new Array[Int](height*width)
        var keyFather = 0

        queue += key
        distancesArray(key) = 0
        while(!queue.isEmpty) {
            actualNodeKey = queue.dequeue
            markedNode += actualNodeKey
            // listNodesVisited += actualNodeKey.toString + ", "   // for debug
            /* treat actual node here */
            for(i <- getSuccessors(actualNodeKey)) {
                if(!markedNode.contains(i) && !queue.contains(i)) {
                    distancesArray(i) = distancesArray(actualNodeKey) + 1
                    queue += i
                    fathers(i) = actualNodeKey
                }
            }
        }
        // listNodesVisited = listNodesVisited.dropRight(2)
        (distancesArray, fathers)
    }

    // def calculateEccentricityOf(key: Int): (Int, Int) = {
    //     var queue = new scala.collection.mutable.Queue[Int]
    //     var markedNode: ArrayBuffer[Int] = ArrayBuffer()
    //     var actualNodeKey = 0
    //     var listNodesVisited = ""
    //     var eccentricity = 0
    //     var distances: scala.collection.mutable.Map[Int, Int] = scala.collection.mutable.Map()

    //     adjacence.keys.foreach(i => distances += (i -> -1))

    //     distances.update(key, 0)
    //     queue += key
    //     while(!queue.isEmpty) {
    //         actualNodeKey = queue.dequeue
    //         for(i <- getSuccessors(actualNodeKey)) if(distances(i) == -1) {
    //             queue += i
    //             distances.update(i, distances(actualNodeKey) + 1)
    //             eccentricity = distances(i)
    //         }
    //     }
    //     (key, eccentricity)
    // }

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
    var destinations = Array.ofDim[Int](nbPlayers, width)
    var walls: ArrayBuffer[Wall] = ArrayBuffer()
    var graph = new Graph[Int](width * height)
    var arrayGraph = Array.ofDim[Int](height, width)
    initiateGraph

    def initiateGraph = {
        var counter = 0
        for(i <- 0 until height) {
            for(j <- 0 until width) {
                graph.addNode(counter, counter)
                arrayGraph(i)(j) = counter
                counter += 1
            }
        }
        for(i <- 0 until height) {
            for(j <- 0 until width) {
                if(i - 1 >= 0) graph.addEdge(arrayGraph(i)(j), arrayGraph(i-1)(j), 1)
                if(i + 1 < height) graph.addEdge(arrayGraph(i)(j), arrayGraph(i+1)(j), 1)
                if(j - 1 >= 0) graph.addEdge(arrayGraph(i)(j), arrayGraph(i)(j-1), 1)
                if(j + 1 < height) graph.addEdge(arrayGraph(i)(j), arrayGraph(i)(j+1), 1)
            }
        }
    }
    def update(wall: Wall) = {
        if(wall.orientation == "H") {
            if(wall.position.y -1 >= 0) {
                graph.removeEdge(arrayGraph(wall.position.y)(wall.position.x), arrayGraph(wall.position.y -1)(wall.position.x))
                if(wall.position.x + 1 < width)
                    graph.removeEdge(arrayGraph(wall.position.y)(wall.position.x + 1), arrayGraph(wall.position.y -1)(wall.position.x + 1))
            }
        }
        else if(wall.orientation == "V") {
            if(wall.position.x - 1 >= 0) {
                graph.removeEdge(arrayGraph(wall.position.y)(wall.position.x), arrayGraph(wall.position.y)(wall.position.x - 1))
                if(wall.position.y + 1 < height)
                    graph.removeEdge(arrayGraph(wall.position.y + 1)(wall.position.x), arrayGraph(wall.position.y +1)(wall.position.x - 1))
            }
        }
    }
    def setDestinations(dragons: Array[Dragon]) = {
        for(k <- 0 until nbPlayers) {
            dragons(k).id match {
                case 0 => {
                    for(i <- 0 until height) destinations(k)(i) = arrayGraph(i)(width-1)
                }
                case 1 => {
                    for(i <- 0 until height) destinations(k)(i) = arrayGraph(i)(0)
                }
                case 2 => {
                    for(j <- 0 until width) destinations(k)(j) = arrayGraph(height-1)(j)
                }
                case 3 => {
                    for(j <- 0 until width) destinations(k)(j) = arrayGraph(0)(j)
                }
            }
        }
    }
    def displayDestinations = {
        for(i <- 0 until nbPlayers) {
            Console.err.println(destinations(i).mkString(", "))
        }
    }
    def getTarget(distancesArray: Array[Int]): Int = {
        var distanceMin = 100
        var indexMin = 0
        for(i <- destinations(myId)) {
            if(distancesArray(i) < distanceMin) {
                distanceMin = distancesArray(i)
                indexMin = i
            }
        }
        // Console.err.println("Target : " + indexMin)
        indexMin
    }

    def move(dragon: Dragon, target: Int, fathers: Array[Int]): String = {
        var keyDragon = coordinatesToKey(dragon.position.y, dragon.position.x, width)
        var keyFather = target

        while(fathers(keyFather) != keyDragon){
            keyFather = fathers(keyFather)
        }
        var positionFather = keyToCoordinates(keyFather, width)
        Console.err.println("Father : " + positionFather)

        if(dragon.position.x < positionFather.x) return "RIGHT"
        if(dragon.position.x > positionFather.x) return "LEFT"
        if(dragon.position.y > positionFather.y) return "UP"
        if(dragon.position.y < positionFather.y) return "DOWN"

        return "RIGHT"
    }

    override def toString: String = {
        var string = "Labyrinth width : " + width + ", height : " + height + ", nbPlayer : " + nbPlayers + ", myId : " + myId +
            ",  nbWallDeployed : " + nbWallDeployed + "\n"
        for(i <- 0 until walls.length) string += walls(i) + "\n"
        string
    }
    def keyToCoordinates(key: Int, width: Int): Position = new Position(key / width, key % width)
    def coordinatesToKey(y: Int, x: Int, width: Int): Int = width * y + x
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
        for(i <- 0 until nbPlayer) {
            dragons(i) = new Dragon(i, 0, new Position(0, 0))
        }

        var firstTurn = true
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
            if(firstTurn) {
                firstTurn = false
                labyrinth.setDestinations(dragons)
                // labyrinth.displayDestinations
            }

            val wallcount = readInt // number of walls on the board
            labyrinth.nbWallDeployed = wallcount
            while(labyrinth.walls.length < wallcount) labyrinth.walls += new Wall(new Position(0, 0), "")

            for(i <- 0 until wallcount) {
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

            var (distancesArray, fathers) = labyrinth.graph.breadthFirstSearch(labyrinth.arrayGraph(dragons(myId).position.y)(dragons(myId).position.x), height, width)
            // Console.err.println(distancesArray.mkString(", "))
            var target = labyrinth.getTarget(distancesArray)

            Console.err.println("target : " + labyrinth.keyToCoordinates(target, width))
            Console.err.println(labyrinth)
            // labyrinth.graph.display

            println(labyrinth.move(dragons(myId), target, fathers))
            // println("RIGHT") // action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
        }
    }
}
