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

  def listNodes = nodes.map { case (key, node) => node }.toList

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
  var nbOfCyborgs: Int,
  val production: Int,
  val unknown1: Int,
  val unknown2: Int,
  var importance: Int
) {
  override def toString: String = s"id: $id, owner: $owner, cyborgs: $nbOfCyborgs, prod: $production, " +
      s"unknown1: $unknown1, unknown2: $unknown2, importance: $importance"
}

case class Troop(
  val id: Int,
  val owner: Int,
  val fromFactoryId: Int,
  val toFactoryId: Int,
  val nbOfCyborgs: Int,
  val remainingTurns: Int
) {
  override def toString: String = s"id: $id, owner: $owner, cyborgs: $nbOfCyborgs, fromFactoryId: $fromFactoryId, " +
      s"toFactoryId: $toFactoryId, remainingTurns: $remainingTurns"
}

case class Bomb(
  val id: Int,
  val owner: Int,
  val fromFactoryId: Int,
  val toFactoryId: Int,
  val remainingTurns: Int,
  val unknown: Int
) {
  override def toString: String = s"id: $id, owner: $owner, fromFactoryId: $fromFactoryId, " +
      s"toFactoryId: $toFactoryId, remainingTurns: $remainingTurns"
}

case class Game(
  val nbOfFactories: Int,
  var nbOfEdges: Int,
  val factories: Graph[Factory],
  var troops: ArrayBuffer[Troop],
  var bombs: ArrayBuffer[Bomb]
) {
  var nbOfBomb = 2
  var myStartFactoryId = 0
  var enemyStartFactoryId = 0

  override def toString: String = s"nbOfFactories: $nbOfFactories, nbOfEdges: $nbOfEdges\n==== factories " +
      s"====\n$factories\n==== troops ==== \n${troops.mkString("\n")}\n==== bombs ====\n${bombs.mkString("\n")}"

  def getMostProdFactories: List[Factory] = {
    factories.listNodes.sortBy(factory => factory.production).reverse
  }

  /**
    * if there are remaining neutral factories
    */
  def initialPhase: Boolean = {
    factories.listNodes.filter(factory => List(10, 9, 8).contains(factory.importance) && factory.owner == 0).length > 0
  }

  def getRemainingCyborgs: Int = {
    factories.listNodes.map(factory => factory.nbOfCyborgs).sum
  }

  def findStartFactories = {
    myStartFactoryId = getFactories(1).head.id
    enemyStartFactoryId = getFactories(-1).head.id
  }

  def getFactories(owner: Int): List[Factory] = {
    factories.listNodes.filter(factory => factory.owner == owner)
  }

  def weightFactories = {
    factories.listNodes.foreach { factory =>
      val distanceWithEnemy = distanceBetween(enemyStartFactory, factory)
      val distanceWithMe = distanceBetween(myStartFactory, factory)
      if (factory.production == 3) {
        if (distanceWithMe <= distanceWithEnemy) {
          factory.importance = 10
        } else {
          factory.importance = 5
        }
      } else if (factory.production == 2) {
        if (distanceWithMe < distanceWithEnemy) {
          factory.importance = 9
        } else {
          factory.importance = 4
        }
      } else if (factory.production == 1) {
        if (distanceWithMe < distanceWithEnemy) {
          factory.importance = 8
        } else {
          factory.importance = 3
        }
      } else {
        factory.importance = 0
      }
    }
  }

  def myStartFactory = factories.nodes(myStartFactoryId)

  def enemyStartFactory = factories.nodes(enemyStartFactoryId)

  def distanceBetween(factory1: Factory, factory2: Factory): Int = {
    factories.adjacencyMatrix(factory1.id)(factory2.id)
  }

  def factoryUnderControl(factory: Factory): Boolean = {
    val troopsTowardsFactory = getTroopsTowardsFactory(factory)
    val myTroops = troopsTowardsFactory.filter(troop => troop.owner == 1)
    val ennemyTroops = troopsTowardsFactory.filter(troop => troop.owner == -1)

    val myTroopsSum = myTroops.map(troop => troop.nbOfCyborgs).sum
    val enemyTroopsSum = ennemyTroops.map(troop => troop.nbOfCyborgs).sum

    (factory.owner == 0 && (myTroopsSum > enemyTroopsSum + factory.nbOfCyborgs)) || (factory.owner == 1 && (factory
        .nbOfCyborgs + myTroopsSum) > enemyTroopsSum)
  }

  def getTroopsTowardsFactory(factory: Factory): List[Troop] = {
    troops.filter(troop => troop.toFactoryId == factory.id).toList
  }

  def availableCyborgs(factory: Factory): Int = {
    val troopsTowardsFactory = getTroopsTowardsFactory(factory)

    val myTroopsSum = troopsTowardsFactory.filter(troop => troop.owner == 1).map(troop => troop.nbOfCyborgs).sum
    val enemyTroopsSum = troopsTowardsFactory.filter(troop => troop.owner == -1).map(troop => troop.nbOfCyborgs).sum

    factory.nbOfCyborgs + myTroopsSum - enemyTroopsSum
  }
}

case class IA() {
  def default_strategy(game: Game): String = {
    val bombOrders: List[String] = getBombOrder(game)
    val upgradeFactoriesOrders: List[String] = upgradeFactories(game)

    val myStrongFactories = game.getFactories(1).sortBy(factory => factory.nbOfCyborgs).reverse

    val moveOrders = if (myStrongFactories.length != 0) {
      val myStrongFactory = myStrongFactories.head
      val targetFactories = game.factories
          .listNodes
          .filter(factory => factory.owner == 0 || factory.owner == -1)
          .filter(factory => factory.nbOfCyborgs < myStrongFactory.nbOfCyborgs)
          .sortBy(factory => (-factory.production, game.distanceBetween(myStrongFactory, factory)))
      //      Console.err.println(targetFactories.mkString("\n"))
      if (targetFactories.length != 0) {
        val targetFactory = targetFactories.head
        List(s"MOVE ${myStrongFactory.id} ${targetFactory.id} ${nbOfCyborgsToMove(myStrongFactory.nbOfCyborgs)}")
      } else {
        val ennemyFactories = game.getFactories(-1)
        if (ennemyFactories.length == 0) {
          List()

        } else {
          val targetFactory = ennemyFactories.sortBy(factory => game.distanceBetween(myStrongFactory, factory)).head
          List(s"MOVE ${myStrongFactory.id} ${targetFactory.id} ${nbOfCyborgsToMove(myStrongFactory.nbOfCyborgs)}")
        }
      }
    } else {
      List()
    }

    (bombOrders ::: upgradeFactoriesOrders ::: moveOrders).mkString(";")
    //    println(if (finalOrder != "") finalOrder else "WAIT")
  }

  def getBombOrder(game: Game): List[String] = {
    if (game.nbOfBomb > 0) {
      val factories = game.getFactories(-1)
          .filter(
            factory => !game.bombs.filter(bomb => bomb.owner == 1).map(bomb => bomb.toFactoryId).contains(factory.id))
          .filter(factory => !game.troops.filter(troop => troop.owner == 1).map(troop => troop.toFactoryId)
              .contains(factory.id))
          .sortBy(factory => factory.production)
          .reverse
      if (factories.length > 0) {
        val targetFactory = factories.head
        val sourceFactory = game.getFactories(1)
            .sortBy(factory => game.distanceBetween(factory, targetFactory))
            .head
        game.nbOfBomb -= 1
        List(s"BOMB ${sourceFactory.id} ${targetFactory.id}")
      } else {
        List()
      }
    } else {
      List()
    }
  }

  def upgradeFactories(game: Game): List[String] = {
    val factories = game.getFactories(1).filter(factory => factory.nbOfCyborgs > 10)
    factories.map(factory => s"INC ${factory.id}")
  }

  def nbOfCyborgsToMove(total: Int): Int = {
    val minimumOfCyborgs = 10
    val couldGo = total - minimumOfCyborgs
    if (couldGo > 0) couldGo else 0
  }

  //  TODO fix timeout because of error if all my troops are travelling and I don't have factory any more
  def colonize(game: Game): String = {
    val simulatedGame = game

    val targetFactories = simulatedGame.factories
        .listNodes
        .filter(factory => List(10, 9, 8).contains(factory.importance) && !game.factoryUnderControl(factory))
    Console.err.println(targetFactories.mkString("\n"))
    val sortedTargetFactories = getNearestMyFactories(simulatedGame, targetFactories)

    sortedTargetFactories.flatMap { case (neutralFactory, t) =>
      val myFactories = t.map(x => x._1)
      myFactories.map { myFacto =>
        if (neutralFactory.nbOfCyborgs >= 0 && myFacto.nbOfCyborgs > 0 && neutralFactory.id != myFacto.id) {
          if (myFacto.nbOfCyborgs > neutralFactory.nbOfCyborgs) {
            val troopsToSend = neutralFactory.nbOfCyborgs + 1
            myFacto.nbOfCyborgs = myFacto.nbOfCyborgs - troopsToSend
            neutralFactory.nbOfCyborgs = neutralFactory.nbOfCyborgs - troopsToSend
            s"MOVE ${myFacto.id} ${neutralFactory.id} $troopsToSend"
          } else {
            val troopsToSend = myFacto.nbOfCyborgs
            myFacto.nbOfCyborgs = myFacto.nbOfCyborgs - troopsToSend
            neutralFactory.nbOfCyborgs = neutralFactory.nbOfCyborgs - troopsToSend
            s"MOVE ${myFacto.id} ${neutralFactory.id} $troopsToSend"
          }
        } else ""

      }
    }.filter(x => x != "").mkString(";")
  }

  def getNearestMyFactories(game: Game, targetFactories: List[Factory]): List[(Factory, List[(Factory, Int)])] = {
    val myFactories = game.getFactories(1)
    targetFactories.map { neutralFactory =>
      val distanceBetweenThisFactoryAndMyFactories = myFactories
          .map(myFactory => (myFactory, game.distanceBetween(myFactory, neutralFactory))).sortBy(t => t._2)
      (neutralFactory, distanceBetweenThisFactoryAndMyFactories)
    }.sortBy(t => t._2.head._2)
  }

  def holdFactories(game: Game): String = {
    val simulatedGame = game

    val safeFactories: List[(Factory, Int)] = simulatedGame.getFactories(1)
        .filter(factory => simulatedGame.factoryUnderControl(factory))
        .map(factory => (factory, game.availableCyborgs(factory)))

    val factoriesInDanger: List[(Factory, Int)] = simulatedGame.factories.listNodes
        .filter(factory => List(10, 9, 8).contains(factory.importance) || factory.owner == 1)
        .filter(factory => !simulatedGame.factoryUnderControl(factory))
        .map(factory => (factory, abs(game.availableCyborgs(factory))))
        .reverse
        .sortBy { case (factory, helpNeeded) => helpNeeded }

    Console.err.println("---- Safe ----")
    Console.err.println(safeFactories.sortBy(x => x._1.id).mkString("\n"))
    Console.err.println("---- Danger ----")
    Console.err.println(factoriesInDanger.sortBy(x => x._1.id).mkString("\n"))

    factoriesInDanger.flatMap { case (factory, helpNeeded) =>
      safeFactories.map { case (myFacto, availableCyborgs) =>
        if (availableCyborgs >= helpNeeded) {
          myFacto.nbOfCyborgs = myFacto.nbOfCyborgs - helpNeeded
          s"MOVE ${myFacto.id} ${factory.id} $helpNeeded"
        } else {
          myFacto.nbOfCyborgs = myFacto.nbOfCyborgs - availableCyborgs
          s"MOVE ${myFacto.id} ${factory.id} $availableCyborgs"
        }
      }
    }.filter(x => x != "").mkString(";")
  }
}

object Player extends App {
  val factorycount = readInt // the number of factories
  val linkcount = readInt // the number of links between factories

  val graph = new Graph[Factory](factorycount)
  val game = Game(factorycount, linkcount, graph, ArrayBuffer(), ArrayBuffer())
  val ia = IA()

  for (i <- 0 until linkcount) {
    val Array(factoryId1, factoryId2, distance) = for (i <- readLine split " ") yield i.toInt
    graph.addEdge(factoryId1, factoryId2, distance)
    graph.addEdge(factoryId2, factoryId1, distance)
  }

  var firstTurn = true

  while (true) {
    val entitycount = readInt // the number of entities (e.g. factories and troops)
    game.troops = ArrayBuffer()
    game.bombs = ArrayBuffer()
    for (i <- 0 until entitycount) {
      val Array(_entityid, entitytype, _arg1, _arg2, _arg3, _arg4, _arg5) = readLine split " "
      val entityid = _entityid.toInt
      val arg1 = _arg1.toInt
      val arg2 = _arg2.toInt
      val arg3 = _arg3.toInt
      val arg4 = _arg4.toInt
      val arg5 = _arg5.toInt
      if (entitytype == "FACTORY") {
        game.factories.addNode(entityid, Factory(entityid, arg1, arg2, arg3, arg4, arg5, 0))
      } else if (entitytype == "TROOP") {
        game.troops += Troop(entityid, arg1, arg2, arg3, arg4, arg5)
      } else {
        game.bombs += Bomb(entityid, arg1, arg2, arg3, arg4, arg5)
      }
    }

    if (firstTurn) {
      firstTurn = false
      game.findStartFactories
    }

    game.weightFactories

//    Console.err.println(game)

    //    TODO implement middle phase
    val moveOrder: String = if (game.initialPhase) {
      Console.err.println("INITIAL PHASE")
      ia.colonize(game)
    } else {
      Console.err.println("MIDDLE PHASE")
      ia.holdFactories(game)
      //      ia.default_strategy(game)
    }

    val bombOrders: List[String] = ia.getBombOrder(game)
    val upgradeFactoriesOrders: List[String] = ia.upgradeFactories(game)

    val finalOrder = (bombOrders ::: (List(moveOrder).filter(x => x != "")) ::: upgradeFactoriesOrders).mkString(";")
    if (finalOrder != "") println(finalOrder) else println("WAIT")
  }
}