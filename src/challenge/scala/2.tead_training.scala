import math._
import scala.util._
import Array._
import scala.collection.mutable.ArrayBuffer
import java.io.File
import java.io.FileReader
import java.io.BufferedReader
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

class Graph[X](nbNodes: Int) extends TicToc{
    var adjacence: Map[Int, ArrayBuffer[Int]] = Map()

    def addNode(key: Int, node: X) = {
        adjacence += (key -> new ArrayBuffer())
    }
    def addEdge(key1 :Int, key2:Int, value: Int) = {
        adjacence(key1) += (key2)
    }
    def isEmpty: Boolean = adjacence.isEmpty
    def successorIsEmpty(key: Int): Boolean = adjacence(key).size == 1
    def nodePresent(key: Int): Boolean = adjacence.contains(key)
    def edgePresent(key1: Int, key2: Int): Boolean = adjacence(key1).contains(key2)
    def getPredecessors(key: Int): ArrayBuffer[Int] = {         // this function fails
        var predecessors: ArrayBuffer[Int] = ArrayBuffer()
        for(i <- 0 until adjacence.size) {
            if(adjacence(i).contains(key)) predecessors += adjacence(i)(0)
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

    def shedTheLeaves() = {
        var leaves: ArrayBuffer[Int] = ArrayBuffer()
        adjacence.keys.foreach {i =>
            if(successorIsEmpty(i)) {
                // println(i + " isEmpty")
                adjacence -= i
                leaves += i
            }
        }
        for(j <- 0 until leaves.size) {
            adjacence.keys.foreach {i =>
                if(adjacence(i).contains(leaves(j)))
                adjacence(i) -= leaves(j)
            }
        }
    }

    def display = adjacence.keys.foreach {i =>
        println("key : " + i + ", Node : " + adjacence(i).toString + ", Successors : " + getSuccessors(i).mkString(", ")) //+ ", Predecessors : " + getPredecessors(i).mkString(", "))
    }
}

object Solution extends TicToc {
    def main(args: Array[String]) {
        var file = new File("../../../ressource/inputTeads/Test_" + args(0) + "_input.txt")
        var fr = new FileReader(file)
        var br = new BufferedReader(fr)
        var s: String = ""

        var nbNodes = br.readLine.toInt
        nbNodes += 1
        var graph = new Graph[Int](nbNodes)
        var eccentricity = 0
        var radius = 0
        var eccentricityMin = 1000000

        tic
        for(i <- 0 until nbNodes - 1){
            val Array(key1, key2) = for(i <- br.readLine split " ") yield i.toInt
            if(!graph.nodePresent(key1)) graph.addNode(key1, key1)
            if(!graph.nodePresent(key2)) graph.addNode(key2, key2)
            graph.addEdge(key1, key2, 1)
            graph.addEdge(key2, key1, 1)
        }
        println("Lenght of adjacence : " + graph.adjacence.size)
        // graph.display

        var counter = 0
        while(graph.adjacence.size > 2) {
            graph.shedTheLeaves()
            // println("===============")
            // graph.display
            counter += 1
        }
        // println("adjacent size : " + graph.adjacence.size)
        if(graph.adjacence.size == 2) counter += 1
        toc("Calculation of the centre")
        println("Eccentricity : " + counter)
        Console.err.println(outLines)

        // var counter = 0
        // graph.adjacence.keys.foreach {i =>
        //     tic
        //     eccentricity = graph.calculateEccentricityOf(i)
        //     toc("Calculation of 1 eccentricity")
        //     if(eccentricity < eccentricityMin) eccentricityMin = eccentricity
        //     counter +=1
        //     // Console.err.println("counter : " + counter)
        //     Console.err.println(outLines)
        // }
        // Console.err.println("key : " + i + " -> eccentricity : " + eccentricity(i))
        // Console.err.println("eccentricityMin " + eccentricityMin)

        // println(eccentricityMin)
    }
}
