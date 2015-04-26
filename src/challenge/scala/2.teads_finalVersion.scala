import math._
import scala.util._
import Array._
import scala.collection.mutable.ArrayBuffer
import java.io.File
import java.io.FileReader
import java.io.BufferedReader

class Graph[X](nbNodes: Int){
    var adjacence: Map[Int, ArrayBuffer[Int]] = Map()

    def addNode(key: Int, node: X) = {
        adjacence += (key -> new ArrayBuffer())
    }
    def addEdge(key1 :Int, key2:Int, value: Int) = {
        adjacence(key1) += (key2)
    }
    def isEmpty: Boolean = adjacence.isEmpty
    def isALeaf(key: Int): Boolean = adjacence(key).size == 1
    def nodePresent(key: Int): Boolean = adjacence.contains(key)
    def edgePresent(key1: Int, key2: Int): Boolean = adjacence(key1).contains(key2)
    def getSuccessors(key: Int): ArrayBuffer[Int] = adjacence(key)

    def shedTheLeaves() = {
        var leaves: ArrayBuffer[Int] = ArrayBuffer()
        adjacence.keys.foreach {i =>
            if(isALeaf(i)) {
                leaves += i
            }
        }
        for(j <- 0 until leaves.size) {
            adjacence(getSuccessors(leaves(j))(0)) -= leaves(j)
            adjacence -= leaves(j)
        }

    }

    def display = adjacence.keys.foreach {i =>
    Console.err.println("key : " + i + ", Node : " + adjacence(i).toString + ", Successors : " + getSuccessors(i).mkString(", "))
    }
}

object Solution {
    def main(args: Array[String]) {

        var nbNodes = readLine.toInt
        nbNodes += 1
        var graph = new Graph[Int](nbNodes)

        for(i <- 0 until nbNodes - 1){
            val Array(key1, key2) = for(i <- readLine split " ") yield i.toInt
            if(!graph.nodePresent(key1)) graph.addNode(key1, key1)
            if(!graph.nodePresent(key2)) graph.addNode(key2, key2)
            graph.addEdge(key1, key2, 1)
            graph.addEdge(key2, key1, 1)
        }

        var counter = 0
        while(graph.adjacence.size > 2) {
            graph.shedTheLeaves()
            counter += 1
        }
        if(graph.adjacence.size == 2) counter += 1

        println(counter)
    }
}
