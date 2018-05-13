import math._
import scala.util._
import scala.Array._
import scala.collection.mutable.ArrayBuffer

class Graph[X](nbNodes: Int) {
  var nodes: Map[Int, X] = Map()
  var adjacencyMatrix = ofDim[Int](nbNodes, nbNodes)

  for (i <- 0 until nbNodes) {
    for (j <- 0 until nbNodes) {
      adjacencyMatrix(i)(j) = 0
    }
  }

  def addNode(key: Int, node: X) = nodes += (key -> node)

  def addEdge(key1: Int, key2: Int, value: Int) = adjacencyMatrix(key1)(key2) = value

  def isEmpty: Boolean = nodes.isEmpty

  def nodePresent(key: Int): Boolean = nodes.contains(key)

  def edgePresent(key1: Int, key2: Int): Boolean = adjacencyMatrix(key1)(key2) > 0

  def breadthFirstSearch(key: Int): String = {
    var queue = new scala.collection.mutable.Queue[Int]
    var markedNode: ArrayBuffer[Int] = ArrayBuffer()
    var actualNodeKey = 0
    var listNodesVisited = ""

    queue += key
    while (queue.nonEmpty) {
      actualNodeKey = queue.dequeue()
      markedNode += actualNodeKey
      listNodesVisited += actualNodeKey.toString + ", " // for debug
      // treat actual node here
      for (i <- getSuccessors(actualNodeKey)) if (!markedNode.contains(i) && !queue.contains(i)) queue += i
    }
    listNodesVisited = listNodesVisited.dropRight(2)
    listNodesVisited
  }

  def calculateEccentricityOf(key: Int): (Int, Int) = {
    var queue = new scala.collection.mutable.Queue[Int]
    var actualNodeKey = 0
    var eccentricity = 0
    var distances: scala.collection.mutable.Map[Int, Int] = scala.collection.mutable.Map()

    nodes.keys.foreach(i => distances += (i -> -1))

    distances.update(key, 0)
    queue += key
    while (queue.nonEmpty) {
      actualNodeKey = queue.dequeue()
      for (i <- getSuccessors(actualNodeKey)) if (distances(i) == -1) {
        queue += i
        distances.update(i, distances(actualNodeKey) + 1)
        eccentricity = distances(i)
      }
    }
    (key, eccentricity)
  }

  def getSuccessors(key: Int): ArrayBuffer[Int] = {
    var successors: ArrayBuffer[Int] = ArrayBuffer()
    for (j <- 0 until nbNodes) {
      if (adjacencyMatrix(key)(j) > 0) successors += j
    }
    successors
  }

  override def toString: String = {
    val nodesRes = nodes.keys.toList.sorted.map(i =>
      "key : " + i + ", Node : " + nodes(i).toString
    )
    nodesRes.mkString("\n")
  }

  def getPredecessors(key: Int): ArrayBuffer[Int] = {
    var predecessors: ArrayBuffer[Int] = ArrayBuffer()
    for (i <- 0 until nbNodes) {
      if (adjacencyMatrix(i)(key) > 0) predecessors += i
    }
    predecessors
  }

  def edgesToString: String = {
    val res = for (
      i <- 0 until nbNodes;
      j <- 0 until nbNodes
    ) yield s"($i, $j): ${adjacencyMatrix(i)(j)}"
    res.toList.mkString("|")
  }
}

case class Factory(
  val id: Int,
  val owner: Int,
  val nbOfCyborgs: Int,
  val production: Int,
  val unknown1: Int,
  val unknown2: Int
) {
  override def toString: String = s"owner: $owner, cyborgs: $nbOfCyborgs, prod: $production, unknown1: $unknown1, " +
      s"unknown2: $unknown2"
}

case class Troop(
  val id: Int,
  val owner: Int,
  val fromFactoryId: Int,
  val toFactoryId: Int,
  val nbOfCyborgs: Int,
  val remainingTurns: Int
) {
  override def toString: String = s"owner: $owner, cyborgs: $nbOfCyborgs, fromFactoryId: $fromFactoryId, " +
      s"toFactoryId: $toFactoryId, remainingTurns: $remainingTurns"
}

case class Game(
  val nbOfFactories: Int,
  var nbOfEdges: Int,
  val factories: Graph[Factory],
  var troops: ArrayBuffer[Troop]
) {
  override def toString: String = s"nbOfFactories: $nbOfFactories, nbOfEdges: $nbOfEdges\n==== factories ====\n$factories\n==== troops ==== \n${troops.mkString("\n")}"
}

object Player extends App {
  val factorycount = readInt // the number of factories
  val linkcount = readInt // the number of links between factories

  val graph = new Graph[Factory](factorycount)
  val game = Game(factorycount, linkcount, graph, ArrayBuffer())

  for (i <- 0 until linkcount) {
    val Array(factoryId1, factoryId2, distance) = for (i <- readLine split " ") yield i.toInt
    graph.addEdge(factoryId1, factoryId2, distance)
    graph.addEdge(factoryId2, factoryId1, distance)
  }

  Console.err.println("==== Edges ====")
  Console.err.println(graph.edgesToString)

  while (true) {
    val entitycount = readInt // the number of entities (e.g. factories and troops)
    game.troops = ArrayBuffer()
    for (i <- 0 until entitycount) {
      val Array(_entityid, entitytype, _arg1, _arg2, _arg3, _arg4, _arg5) = readLine split " "
      val entityid = _entityid.toInt
      val arg1 = _arg1.toInt
      val arg2 = _arg2.toInt
      val arg3 = _arg3.toInt
      val arg4 = _arg4.toInt
      val arg5 = _arg5.toInt
      if (entitytype == "FACTORY") {
        game.factories.addNode(entityid, Factory(entityid, arg1, arg2, arg3, arg4, arg5))
      } else {
        game.troops += Troop(entityid, arg1, arg2, arg3, arg4, arg5)
      }
    }

    Console.err.println(game)

    // Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
    println("WAIT")
  }
}