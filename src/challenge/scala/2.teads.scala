import math._
import scala.util._
import Array._
import scala.collection.mutable.ArrayBuffer

class Graph[X](nbNodes: Int) {
    var adjacence: Map[Int, ArrayBuffer[Int]] = Map()

    def addNode(key: Int, node: X) = {
        adjacence += (key -> new ArrayBuffer())
    }
    def addEdge(key1 :Int, key2:Int, value: Int) = {
        adjacence(key1) += (key2)
    }
    def isEmpty: Boolean = adjacence.isEmpty
    def nodePresent(key: Int): Boolean = adjacence.contains(key)
    def edgePresent(key1: Int, key2: Int): Boolean = adjacence(key1).contains(key2)
    def getPredecessors(key: Int): ArrayBuffer[Int] = {
        var predecessors: ArrayBuffer[Int] = ArrayBuffer()
        for(i <- 0 until adjacence.size) {
            if(adjacence(i).contains(key)) predecessors += adjacence(i)(0)
        }
        predecessors
    }
    def getSuccessors(key: Int): ArrayBuffer[Int] = {
        var successors: ArrayBuffer[Int] = ArrayBuffer()
        for(j <- adjacence(key)) {
            successors += j
        }
        successors
    }

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

    def calculateEccentricityOf(key: Int): Int = {
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
        eccentricity
    }

    def display = adjacence.keys.foreach {i =>
        println("key : " + i + ", Node : " + adjacence(i).toString + ", Successors : " + getSuccessors(i).mkString(", ") + ", Predecessors : " + getPredecessors(i).mkString(", "))
    }
}

object Solution {
    def main(args: Array[String]) {
        var nbNodes = readInt
        nbNodes += 1
        var graph = new Graph[Int](nbNodes)
        var eccentricity = 0
        var radius = 0
        var eccentricityMin = 1000000

        for(i <- 0 until nbNodes - 1){
            val Array(key1, key2) = for(i <- readLine split " ") yield i.toInt
            if(!graph.nodePresent(key1)) graph.addNode(key1, key1)
            if(!graph.nodePresent(key2)) graph.addNode(key2, key2)
            graph.addEdge(key1, key2, 1)
            graph.addEdge(key2, key1, 1)
        }
        // graph.display
        graph.adjacence.keys.foreach {i =>
            eccentricity = graph.calculateEccentricityOf(i)
            if(eccentricity < eccentricityMin) eccentricityMin = eccentricity
        }

        // Console.err.println("key : " + i + " -> eccentricity : " + eccentricity(i))
        // Console.err.println("eccentricityMin " + eccentricityMin)

        println(eccentricityMin)
    }
}
