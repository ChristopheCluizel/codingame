import scala.collection.mutable.ArrayBuffer
import scala.io.StdIn._

object Direction extends Enumeration {
  type Direction = Value
  val SOUTH, EAST, NORTH, WEST = Value
}
object State extends Enumeration {
  type State = Value
  val BREAKER, NON_BREAKER = Value
}

import Direction._
import State._

object Solution extends App {
  case class Position(var x: Int, var y: Int)
  case class Robot(var position: Position, var direction: Direction, var state: State)
  case class Player(cityMap: Array[Array[Char]], robot: Robot, var directions: Array[Direction], var teleportPositions: Option[(Position, Position)]) {

    def findStartEndPositions: (Position, Position) = {
      var startPosition: Position = Position(0, 0)
      var endPosition: Position = Position(0, 0)

      for (i <- cityMap.indices) {
        for (j <- cityMap(i).indices) {
          if (cityMap(i)(j) == '@') {
            startPosition = Position(j, i)
          }
          if (cityMap(i)(j) == '$') {
            endPosition = Position(j, i)
          }
        }
      }
      (startPosition, endPosition)
    }
    def findTeleports: Option[(Position, Position)] = {
      val teleportPositions: ArrayBuffer[Position] = ArrayBuffer[Position]()
      for (i <- cityMap.indices) {
        for (j <- cityMap(i).indices) {
          if (cityMap(i)(j) == 'T') {
            teleportPositions += Position(j, i)
          }
        }
      }
      if(teleportPositions.isEmpty)
        None
      else
        Some(teleportPositions.head, teleportPositions(1))
    }
    def updateDirection(newDirection: Direction): Unit = {
      robot.direction = newDirection
    }
    def invertDirections(): Unit = {
      directions = directions.reverse
    }
    def playOneTurn: Direction = {
      checkActualAction()
      var nextPosition = getNextPosition
      val directionsIt = directions.toIterator
      while(!isNextMovePossible(nextPosition)) {
        updateDirection(directionsIt.next())
        nextPosition = getNextPosition
      }
      move(nextPosition)
      robot.direction
    }
    def checkActualAction(): Unit = {
      val (x, y) = (robot.position.x, robot.position.y)
      cityMap(y)(x) match {
        case 'B' => changeState
        case 'I' => invertDirections()
        case 'T' => teleport()
        case 'N' => robot.direction = NORTH
        case 'S' => robot.direction = SOUTH
        case 'E' => robot.direction = EAST
        case 'W' => robot.direction = WEST
        case _ =>
      }
    }
    def isNextMovePossible(nextPosition: Position): Boolean = {
      val (x, y) = (nextPosition.x, nextPosition.y)
      cityMap(y)(x) match {
        case '#' => false
        case 'X' =>
          if(robot.state == BREAKER) {
            cityMap(y)(x) = ' ' // remove the wall
            true
          } else false
        case _ => true
      }
    }
    def teleport(): Unit = {
      if(robot.position.equals(teleportPositions.get._1)) robot.position = teleportPositions.get._2
      else robot.position = teleportPositions.get._1
    }
    def move(nextPosition: Position): Unit = {
      robot.position = nextPosition
    }
    def changeState: Unit = {
      if(robot.state == BREAKER) robot.state = NON_BREAKER
      else robot.state = BREAKER
    }
    def getNextPosition: Position = {
      robot.direction match {
        case SOUTH => Position(robot.position.x, robot.position.y + 1)
        case NORTH => Position(robot.position.x, robot.position.y - 1)
        case WEST => Position(robot.position.x - 1, robot.position.y)
        case EAST => Position(robot.position.x + 1, robot.position.y)
      }
    }
  }

  val Array(nbRows, nbColumns) = for (i <- readLine() split " ") yield i.toInt
  val cityMap = Array.ofDim[Char](nbRows, nbColumns)
  for (i <- 0 until nbRows) {
    cityMap(i) = readLine().toArray
  }

  val robot = Robot(Position(0, 0), SOUTH, NON_BREAKER)
  val player: Player = Player(cityMap, robot, Array(SOUTH, EAST, NORTH, WEST), None)
  val (startPosition, endPosition) = player.findStartEndPositions
  player.teleportPositions = player.findTeleports
  player.robot.position = startPosition

  val movements: ArrayBuffer[Direction] = ArrayBuffer[Direction]()
  var nbTurns: Int = 0
  val nbTurnsMax: Int = nbRows * nbColumns
  while(nbTurns < nbTurnsMax && !player.robot.position.equals(endPosition)) {
    nbTurns += 1
    val movement = player.playOneTurn
    movements += movement
  }
  if(nbTurns == nbTurnsMax) {
    println("LOOP")
  }
  else {
    println(movements.mkString("\n"))
  }
}
