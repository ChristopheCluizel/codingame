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

    def findShortestPathsFrom(StartNode: Int, height: Int, width: Int): (Array[Int], Array[Int]) = { // find the shortest path between startNode and all the other nodes of the graph
        var queue = new scala.collection.mutable.Queue[Int]
        var markedNode: ArrayBuffer[Int] = ArrayBuffer()    // indicates if the node has already been treated
        var actualNodeKey = 0   // node which is currently treated
        var fathers = new Array[Int](height*width)  // keeps the fathers of all the nodes
        var distancesArray = new Array[Int](height*width)   // keeps the distances between the startNode and all the other ones

        queue += StartNode
        distancesArray(StartNode) = 0 // distance between a node and itself is null
        while(!queue.isEmpty) {
            actualNodeKey = queue.dequeue
            markedNode += actualNodeKey
            /* treat actual node here */
            for(i <- getSuccessors(actualNodeKey)) {    // get all the successors of the current node
                if(!markedNode.contains(i) && !queue.contains(i)) {
                    distancesArray(i) = distancesArray(actualNodeKey) + 1
                    queue += i
                    fathers(i) = actualNodeKey
                }
            }
        }
        (distancesArray, fathers)
    }

    def calculateEccentricityOf(key: Int): (Int, Int) = {   // not used here
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

    def display = adjacence.keys.foreach {i =>
        Console.err.println("key : " + i + ", Node : " + adjacence(i).toString +
                ", Successors : " + getSuccessors(i).mkString(", ") +
                ", Predecessors : " + getPredecessors(i).mkString(", "))
    }
}

class Dragon(var id: Int, var nbWallLeft: Int, var position: Position) {
    var distancesFromOtherNodes: ArrayBuffer[Int] = ArrayBuffer()
    var fathers: ArrayBuffer[Int] = ArrayBuffer()
    var nodeFather = 0
    var nodeTarget = 0
    override def toString: String = "Dragon id : " + id + " position : "  + position + " nbWallLeft : " + nbWallLeft
}

class Position(var y: Int, var x: Int) {
    override def toString: String = "(" + x + ", " + y + ")"
}

class Wall(var position: Position, var orientation: String) {
    override def toString: String = "Wall position " + position + ", orientation : " + orientation
}

class Labyrinth(val width: Int, val height: Int, var nbPlayers: Int, val myId: Int) {
    var nbWallDeployed = 0
    var destinations = Array.ofDim[Int](nbPlayers, width)   // destinations nodes for each players. players = rows, destinations = columns
    var dragons = new Array[Dragon](nbPlayers)
    var walls: ArrayBuffer[Wall] = ArrayBuffer()    // array of the nodes deployed
    var graph = new Graph[Int](width * height)  // representation of the labyrinth for finding the shortest path: 1 node = 1 square of the labyrinth
    var arrayGraph = Array.ofDim[Int](height, width)    // representation of the labyrinth: 1 square = 1 node of the graph
    initiateGraph

    def initiateGraph = {   // fill the graph and the array labyrinth
        var counter = 0
        for(i <- 0 until height) {  // fill the array labyrinth and add nodes to the graph labyrinth
            for(j <- 0 until width) {
                graph.addNode(counter, counter)
                arrayGraph(i)(j) = counter
                counter += 1
            }
        }
        for(i <- 0 until height) {  // add edges to the graph labyrinth for adjacents squares
            for(j <- 0 until width) {
                if(i - 1 >= 0) graph.addEdge(arrayGraph(i)(j), arrayGraph(i-1)(j), 1)
                if(i + 1 < height) graph.addEdge(arrayGraph(i)(j), arrayGraph(i+1)(j), 1)
                if(j - 1 >= 0) graph.addEdge(arrayGraph(i)(j), arrayGraph(i)(j-1), 1)
                if(j + 1 < height) graph.addEdge(arrayGraph(i)(j), arrayGraph(i)(j+1), 1)
            }
        }
    }
    def update(wall: Wall) = {  // update the graph labyrinth with the walls deployed. 1 wall deployed => 2 edges removed
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
    def setDestinations = { // at the beginning of the game set the node destinations of each players
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
    def findPathForDragons = {
        for(i <- dragons) {
            if(i.position.x != -1) {    // test if i (dragon) is always playing
                var (distances, fathers) = graph.findShortestPathsFrom(coordinatesToKey(i.position.y, i.position.x, width), height, width)
                i.distancesFromOtherNodes ++= distances.toBuffer
                i.fathers ++= fathers
                i.nodeTarget = getTarget(i.id, i.distancesFromOtherNodes.toArray)

                var keyDragon = coordinatesToKey(i.position.y, i.position.x, width)
                var keyFather = i.nodeTarget

                while(fathers(keyFather) != keyDragon){
                    keyFather = fathers(keyFather)
                }
                i.nodeFather = keyFather
                var positionFather = keyToCoordinates(i.nodeFather, width)
                Console.err.println("dragon " + i.id + " -> target : " + keyToCoordinates(i.nodeTarget, width) + ", father : " + positionFather)
            }
        }
    }

    def getTarget(idDragon: Int, distancesArray: Array[Int]): Int = {  // find the best destination among the 9 possible for a dragon
        var distanceMin = 100
        var indexMin = 0
        for(i <- destinations(idDragon)) {
            if(distancesArray(i) < distanceMin) {
                distanceMin = distancesArray(i)
                indexMin = i
            }
        }
        // Console.err.println("Target : " + indexMin)
        indexMin
    }

    def move(dragon: Dragon, positionFather: Position): String = { // move my dragon
        if(dragon.position.x < positionFather.x) return "RIGHT"
        if(dragon.position.x > positionFather.x) return "LEFT"
        if(dragon.position.y > positionFather.y) return "UP"
        if(dragon.position.y < positionFather.y) return "DOWN"

        return "RIGHT" // default value
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
        var firstTurn = true
        val Array(width, height, nbPlayer, myId) = for(i <- readLine split " ") yield i.toInt
        var labyrinth = new Labyrinth(width, height, nbPlayer, myId)

        while(true) {

            /* ------------- Update of dragons -------------------- */
            for(i <- 0 until nbPlayer) {
                val Array(x, y, wallsleft) = for(i <- readLine split " ") yield i.toInt // (x,y) coordinates of the player, wallsleft : nb of walls
                labyrinth.dragons(i) = new Dragon(i, wallsleft, new Position(y, x))
                Console.err.println(labyrinth.dragons(i))
            }
            if(firstTurn) { // fix the destinations for each player at the beginning of the game
                firstTurn = false
                labyrinth.setDestinations
                // labyrinth.displayDestinations
            }

            /* ------------- Update of walls -------------------- */
            labyrinth.nbWallDeployed = readInt // number of walls on the board
            while(labyrinth.walls.length < labyrinth.nbWallDeployed) labyrinth.walls += new Wall(new Position(0, 0), "")
            for(i <- 0 until labyrinth.nbWallDeployed) {
                val Array(_wallx, _wally, wallorientation) = readLine split " " //(wallx, wally): coordinates of the wall, wallorientation: wall orientation
                labyrinth.walls(i).position = new Position(_wally.toInt, _wallx.toInt)    // fix the position of the wall
                labyrinth.walls(i).orientation = wallorientation    // fix the orientation of the wall
                labyrinth.update(labyrinth.walls(i))    // update the labyrinth according to the walls deployed
            }

            /* ------------- Strategy -------------------- */
            labyrinth.findPathForDragons

            Console.err.println(labyrinth)
            // labyrinth.graph.display
            println(labyrinth.move(labyrinth.dragons(myId), labyrinth.keyToCoordinates(labyrinth.dragons(myId).nodeFather, width))) // action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
        }
    }
}
