import math._
import scala.util._
import scala.Array._
import scala.collection.mutable.ArrayBuffer
import java.io.{BufferedReader, BufferedWriter, FileReader, FileWriter}
import scala.collection.mutable.ArrayBuffer
import scala.math.{max, min}

/**
  * Graph is a class which represents a graph structure. Its implementation is based on an adjacency list which is
  * less heavy than an adjacency matrix. One can use whatever kind of node with Graph.
  *
  * @author christophe
  * @param name The name of the graph.
  * @tparam T Enable any kind of node.
  */

class Graph[T](val name: String = "graph") {

  var numberOfEdges = 0

  /**
    * Implementation of the adjacency list. The key corresponds to the key of a father node and the value to an array
    * containing the key of the successor nodes of this father node.
    */
  var adjacency: Map[Int, ArrayBuffer[Int]] = Map()

  /**
    * Nodes is a list of all the nodes of the graph. It associates a key to any kind of node T.
    */
  var nodes: Map[Int, T] = Map()

  /**
    * Add a node to the graph.
    *
    * @param key  The key of the node inserted.
    * @param node The node inserted in the graph.
    */
  def addNode(key: Int, node: T) = {
    if (!nodes.contains(key)) {
      nodes += (key -> node)
      adjacency += (key -> new ArrayBuffer())
    }
  }

  /**
    * Add an edge to the graph between two nodes.
    *
    * @param key1  The key of the first node.
    * @param key2  The key of the second node.
    * @param value Not used yet.
    */
  def addEdge(key1: Int, key2: Int, value: Int) = {
    if (!adjacency(key1).contains(key2)) {
      adjacency(key1) += key2
      numberOfEdges += 1
    }
  }

  /**
    * Remove an edge of the graph between two nodes.
    *
    * @param key1 The key of the first node.
    * @param key2 The key of the second node.
    */
  def removeEdge(key1: Int, key2: Int) = {
    if (adjacency(key1).contains(key2)) adjacency(key1) -= key2
    numberOfEdges -= 1
  }

  /**
    * Indicate if the graph is empty.
    *
    * @return Return whether the graph is empty or not.
    */
  def isEmpty: Boolean = adjacency.isEmpty

  /**
    * Indicate if a node is present in the graph.
    *
    * @param key The key of the node considered.
    * @return Return whether the node is present or not.
    */
  def nodePresent(key: Int): Boolean = adjacency.contains(key)

  /**
    * Indicate if an edge is present between two nodes in the graph.
    *
    * @param key1 The key of the first node.
    * @param key2 The key of the second node.
    * @return Return whether the edge is present or not.
    */
  def edgePresent(key1: Int, key2: Int): Boolean = adjacency(key1).contains(key2)

  /**
    * Indicate the number of nodes in the graph.
    *
    * @return The number of nodes.
    */
  def numberOfNodes: Int = {
    nodes.size
  }

  /**
    * Save the graph in a text file.
    *
    * @param filePath The file path where will be stored the graph.
    *
    *                 The name of the file will be the name of the graph with the extension ".dot".
    */
  def save(filePath: String = "") = {
    val writer = new BufferedWriter(new FileWriter(filePath + name + ".dot"))
    writer.write(toString)
    writer.close()
  }

  /**
    * Redefine the toString method to describe a graph.
    */
  override def toString: String = {
    var string = numberOfEdges.toString + "\n" +
        "graph " + name + " {\n"
    adjacency.keys.foreach { i =>
      for (j <- adjacency(i).indices) {
        string += i.toString + " -> " + adjacency(i)(j).toString + "\n"
      }
    }
    string += "}"
    string
  }

  /**
    * Scan the graph by breadth first search.
    *
    * @param key The key of the start node.
    * @return A string of the nodes crossed, sorted by cross order.
    */
  def breadthFirstSearch(key: Int): String = {
    var queue = new scala.collection.mutable.Queue[Int]
    var markedNode: ArrayBuffer[Int] = ArrayBuffer()
    var actualNodeKey = 0
    var listNodesVisited = ""

    queue += key
    while (queue.nonEmpty) {
      actualNodeKey = queue.dequeue()
      markedNode += actualNodeKey
      listNodesVisited += actualNodeKey.toString + ", "
      // treat actual node here
      for (i <- getSuccessors(actualNodeKey)) if (!markedNode.contains(i) && !queue.contains(i)) queue += i
    }
    listNodesVisited = listNodesVisited.dropRight(2)
    listNodesVisited
  }

  /**
    * Calculate the eccentricity of a node. The eccentricity is the longest distance between a node and all the other
    * ones.
    *
    * @param key The key of the node whose one wants to calculate the eccentricity.
    * @return The value of the eccentricity of the node.
    */
  def calculateEccentricityOf(key: Int): Int = {
    var queue = new scala.collection.mutable.Queue[Int]
    var actualNodeKey = 0
    var eccentricity = 0
    var distances: scala.collection.mutable.Map[Int, Int] = scala.collection.mutable.Map()

    adjacency.keys.foreach(i => distances += (i -> -1))

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
    eccentricity
  }

  /**
    * Get the keys of the nodes which are the successors of another one.
    *
    * @param key The key of the node whose one wants the successors.
    * @return The keys of the successor nodes.
    */
  def getSuccessors(key: Int): ArrayBuffer[Int] = adjacency(key)

  /**
    * Delete all the leaves of the graph. A leaf is a node which doesn't have any successors. This method has sense
    * only for an oriented-graph.
    */
  def shedTheLeaves() = for (i <- adjacency.keys) if (getSuccessors(i).isEmpty) removeNode(i)

  /**
    * Remove a node of the graph.
    *
    * @param key The key of the node to remove.
    */
  def removeNode(key: Int) {
    nodes -= key
    adjacency -= key
    for (i <- adjacency.keys) if (adjacency(i).contains(key)) adjacency(i) -= key
  }

  /**
    * Display all the graph. Each node is displayed with its key, predecessors and successors.
    */
  def display(mazeWidth: Int) {
    adjacency.keys.foreach { i =>
      Console.err.println(s"key : $i, ${Conversion.keyToPosition(i, mazeWidth)} Node : ${
        adjacency(i).map(x => Conversion.keyToPosition(x, mazeWidth))
      }")
    }
  }

  /**
    * Get the keys of the nodes which are the predecessors of another one.
    *
    * @param key The key of the node whose one wants the predecessors.
    * @return The keys of the predecessor nodes.
    */
  def getPredecessors(key: Int): ArrayBuffer[Int] = {
    var predecessors: ArrayBuffer[Int] = ArrayBuffer()
    for (i <- adjacency.keys) {
      if (adjacency(i).contains(key)) {
        predecessors += i
      }
    }
    predecessors
  }
}

case class Position(x: Int, y: Int) {
  override def toString: String = s"($x, $y)"

  def distanceWith(that: Position): Double = {
    Math.sqrt((that.x - x) * (that.x - x) + (that.y - y) * (that.y - y))
  }

  def minus(that: Position): Position = {
    Position(this.x - that.x, this.y - that.y)
  }

  def plus(that: Position): Position = {
    Position(this.x + that.x, this.y + that.y)
  }

  def ==(that: Position): Boolean = {
    this.x == that.x && this.y == that.y
  }
}

class Unit(
  id: Int,
  position: Position,
  owner: Int
) {
  override def toString: String = s"id: $id, owner: $owner, $position"
}

case class Explorer(
  val id: Int,
  val position: Position,
  val owner: Int,
  val sanity: Int,
  val ignore1: Int,
  val ignore2: Int
) extends Unit(id, position, owner) {
  override def toString: String = s"Explorer id: $id, owner: $owner, $position, HP: $sanity"
}

case class Wanderer(
  val id: Int,
  val position: Position,
  val owner: Int,
  val timeRecall: Int,
  val state: Int,
  val target: Int
) extends Unit(id, position, owner) {
  override def toString: String = s"Wanderer id: $id, owner: $owner, $position, timeRecal/spawn: $timeRecall, " +
      s"state: $state, target: $target"
}

case class Spawn(
  val id: Int,
  val position: Position,
  val owner: Int,
  val timeSpawn: Int
) extends Unit(id, position, owner) {
  override def toString: String = s"Spawn id: $id, owner: $owner, $position, timeSpawn: $timeSpawn"
}

case class Board(
  width: Int,
  height: Int,
  squares: Array[Array[String]],
  var units: List[Unit]
) {
  override def toString: String = s"==== Board ====\nheight: $height, width: $width\n${units.mkString("\n")}"

  def squaresToString: String = squares.map(x => x.mkString("")).mkString("\n")

  def getExplorers: List[Explorer] = units.collect { case unit: Explorer => unit }

  def getWanderers: List[Wanderer] = units.collect { case unit: Wanderer => unit }
}

case class Game(
  board: Board,
  graph: Graph[Int]
) {
  override def toString: String = s"$board"
}

case class IA(game: Game) {
  def glueOneExplorer(): String = {
    val board = game.board
    val ennemy = board.getExplorers.filter(explorer => explorer.owner != 1).head
    s"MOVE ${ennemy.position.x} ${ennemy.position.y}"
  }

  def glueButEscape(): String = {
    val board = game.board
    val ennemyExplorers = board.getExplorers.filter(explorer => explorer.owner != 1)
    val myExplorer = board.getExplorers.filter(explorer => explorer.owner == 1).head

    val wanderers = board.getWanderers
    val wanderersKeys: List[Int] = wanderers.map(wanderer => Conversion.positionToKey(wanderer.position, board.width))
    val squares: List[Int] = game.graph.getSuccessors(Conversion.positionToKey(myExplorer.position, board.width)).toList

    if (squares.toSet.intersect(wanderersKeys.toSet).toList.size > 0) {
      escape()
    } else {
      if(ennemyExplorers.size > 0) {
        val ennemyExplorer = ennemyExplorers.head
        s"MOVE ${ennemyExplorer.position.x} ${ennemyExplorer.position.y}"
      } else {
        s"WAIT"
      }
    }
  }

  def escape(): String = {
    val board = game.board
    val myExplorer = board.getExplorers.filter(explorer => explorer.owner == 1).head
    val wanderers = board.getWanderers
    val wanderersKeys: List[Int] = wanderers.map(wanderer => Conversion.positionToKey(wanderer.position, board.width))
    val squares: List[Int] = game.graph.getSuccessors(Conversion.positionToKey(myExplorer.position, board.width)).toList
    val freeSquares = squares.toSet.diff(wanderersKeys.toSet).toList
    val targetNode: Int = if(freeSquares.size > 0) freeSquares.head else Conversion.positionToKey(myExplorer.position, board.width)
    val nextPosition = Conversion.keyToPosition(targetNode, board.width)

    s"MOVE ${nextPosition.x} ${nextPosition.y}"
  }
}

/**
  * This object allows to make conversions between different types.
  */
object Conversion {

  /**
    * Convert a key node of a graph to a coordinate square of the maze associated.
    *
    * @param key       The key node of a graph.
    * @param mazeWidth The width of the maze.
    * @return The coordinate of the maze square corresponding to the key node of the graph.
    * @see Position
    */
  def keyToPosition(key: Int, mazeWidth: Int): Position = new Position(key % mazeWidth, key / mazeWidth)

  /**
    * Convert a matrix to a graph.
    *
    * @param matrix The matrix to convert.
    * @return The graph corresponding to the matrix.
    */
  def matrixToGraph(matrix: Array[Array[Int]]): Graph[Int] = {
    val nbRows = matrix.length
    val nbColumns = matrix(0).length
    val graph = new Graph[Int]

    for (i <- 0 until nbRows; j <- 0 until nbColumns) {
      val actualCoord = new Position(j, i)
      val actualKey = positionToKey(actualCoord, nbColumns)
      graph.addNode(actualKey, 1)
      if (matrix(i)(j) == 0) {
        val neighbourKeys = findNeighbours(matrix, nbRows, nbColumns, actualCoord)
        neighbourKeys.foreach { key =>
          graph.addNode(key, 1)
          graph.addEdge(actualKey, key, 1)
        }
      }
    }
    graph
  }

  /**
    * Find the neighbours of a square which are not a wall (so equal 0).
    *
    * @param matrix    The matrix of squares.
    * @param nbRows    The number of rows of the matrix.
    * @param nbColumns The number of columns of the matrix.
    * @param square    The coordinate of the square we search its neighbours.
    * @return The list of the keys for null neighbours next to the square.
    */
  def findNeighbours(matrix: Array[Array[Int]], nbRows: Int, nbColumns: Int, square: Position): ArrayBuffer[Int] = {
    val fourNeighbourPositions = ArrayBuffer[Position]()
    val neighbourKeys = ArrayBuffer[Int]()

    fourNeighbourPositions += new Position(square.x, max(0, square.y - 1))
    fourNeighbourPositions += new Position(square.x, min(nbRows - 1, square.y + 1))
    fourNeighbourPositions += new Position(max(0, square.x - 1), square.y)
    fourNeighbourPositions += new Position(min(square.x + 1, nbColumns - 1), square.y)

    for (coord <- fourNeighbourPositions) {
      if (matrix(coord.y)(coord.x) == 0 && !(coord == square)) neighbourKeys += positionToKey(coord, nbColumns)
    }
    neighbourKeys
  }

  /**
    * Convert a square coordinate of a maze to a key node of the graph associated.
    *
    * @param coordinate The square coordinate of the maze.
    * @param mazeWidth  The width of the maze.
    * @return The key node of the graph corresponding to the maze square.
    * @see Position
    */
  def positionToKey(coordinate: Position, mazeWidth: Int): Int = mazeWidth * coordinate.y + coordinate.x
}

object Player extends App {
  val width = readInt
  val height = readInt
  val boardString = for {i <- 0 until height
                         val line = readLine
  } yield line

  val boardSquares = boardString.toArray.map(x => x.split(""))
  val board = Board(width, height, boardSquares, List())
  val adaptedSquares = board.squares.map(row => row.map { square =>
    if (square == ".")
      0
    else if (square == "#")
      1
    else
      0
  })
  val graph = Conversion.matrixToGraph(adaptedSquares)

  val game = Game(board, graph)
  val ia = IA(game)

//  Console.err.println(board.squaresToString)
//  game.graph.display(board.width)

  // sanitylosslonely: how much sanity you lose every turn when alone, always 3 until wood 1
  // sanitylossgroup: how much sanity you lose every turn when near another player, always 1 until wood 1
  // wandererspawntime: how many turns the wanderer take to spawn, always 3 until wood 1
  // wandererlifetime: how many turns the wanderer is on map after spawning, always 40 until wood 1
  val Array(sanitylosslonely,
  sanitylossgroup,
  wandererspawntime,
  wandererlifetime) = for (i <- readLine split " ") yield i.toInt

  // game loop
  while (true) {
    val entitycount = readInt // the first given entity corresponds to your explorer
    var firstUnit = true
    val units = for {
      i <- 0 until entitycount
      val Array(entitytype, _id, _x, _y, _param0, _param1, _param2) = readLine split " "
      val id = _id.toInt
      val x = _x.toInt
      val y = _y.toInt
      val param0 = _param0.toInt
      val param1 = _param1.toInt
      val param2 = _param2.toInt

      val unit: Unit = if (firstUnit) {
        firstUnit = false
        Explorer(id, Position(x, y), 1, param0, -1, -1)
      } else {
        if (entitytype == "EXPLORER") {
          Explorer(id, Position(x, y), -1, param0, -1, -1)
        } else if (entitytype == "WANDERER") {
          Wanderer(id, Position(x, y), 0, param0, param1, param2)
        } else {
          Spawn(id, Position(x, y), 0, param0)
        }
      }
    } yield unit

    board.units = units.toList

//    Console.err.println(game)

    println(ia.glueButEscape)
  }
}
