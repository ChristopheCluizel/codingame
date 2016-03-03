import scala.collection.mutable.ArrayBuffer
import scala.io.StdIn
import scala.math.{sqrt, acos, Pi}

object Player extends App {
  val checkpointRadius = 600

  def radianToDegree(radian: Double): Double = (radian * 360) / (2 * Pi)

  class Vector(val x: Double, val y: Double) {
    def getAngleWith(that: Vector): Double = {
      radianToDegree(acos(this.getScalarProductWith(that) / (this.getNorm * that.getNorm)))
    }
    def getScalarProductWith(that: Vector): Double = this.x * that.x + this.y * that.y
    def getNorm: Double = sqrt(x * x + y * y)
    def normalize: Vector = this / this.getNorm
    def *(factor: Double): Vector = new Vector(x * factor, y * factor)
    def /(factor: Double): Vector = this * (1 / factor)
    def +(that: Vector): Vector = new Vector(this.x + that.x, this.y + that.y)
    def toPosition: Position = new Position(x.toInt, y.toInt)
    override def toString: String = s"($x, $y)"
  }

  case class Position(val x: Int, val y: Int) {
    override def toString: String = s"Pos($x, $y)"
    def distanceWith(that: Position): Double = sqrt((that.x - this.x) * (that.x - this.x) + (that.y - this.y) * (that.y - this.y))
    def middleWith(that: Position): Position = {
      Position((this.x + that.x) / 2, (this.y + that.y) / 2)
    }
    def +(that: Position): Position = new Position(this.x + that.x, this.y + that.y)
    def getVectorWith(that: Position): Vector = new Vector(that.x - this.x, that.y - this.y)
  }

  case class Speed(x1: Int, y1: Int) extends Vector(x1, y1) {
    override def toString: String = s"Speed($x1, $y1)"
    def toVector: Vector = new Vector(x1, y1)
  }

  case class Checkpoint(val id: Int, val position: Position) {
    override def toString: String = s"id: $id, $position"
  }

  case class Track(val nbLaps: Int, val nbCheckpoints: Int, val checkpoints: ArrayBuffer[Checkpoint] = ArrayBuffer()) {
    override def toString: String = {
      var res = ""
      res += s"nbLaps: $nbLaps, nbCheckpoints: $nbCheckpoints\n"
      checkpoints.foreach(checkpoint => res += s"$checkpoint\n")
      res
    }
  }

  case class Pod(val id: Int = 0, var position: Position = new Position(0, 0), var speed: Speed = new Speed(0, 0), var angle: Int = 0, var nextCheckpoint: Int = 0, var actualCheckpoint: Int = 1, var rank: Int = 1, var state: String = "neutral", var points: Double = 0) {
    def getRealSpeed: Double = {
      sqrt(speed.x * speed.x + speed.y * speed.y)
    }
    override def toString: String = s"id: $id, $position, $speed, angle: $angle\nnextCheckpoint: $nextCheckpoint, rank: $rank, state: $state"
  }

  case class Game(val track: Track, val myPods: Array[Pod] = Array(new Pod(id = 1), new Pod(id = 2)), val yourPods: Array[Pod] = Array(new Pod(id = 3), new Pod(id = 4))) {
    def updatePods(): Unit = {
      for (i <- 0 until 2) {
        val Array(x, y, vx, vy, angle, nextcheckpointid) = for (i <- StdIn.readLine() split " ") yield i.toInt
        myPods(i).position = new Position(x, y)
        myPods(i).speed = new Speed(vx, vy)
        myPods(i).angle = angle
        myPods(i).nextCheckpoint = nextcheckpointid
      }
      for (i <- 0 until 2) {
        val Array(x, y, vx, vy, angle, nextcheckpointid) = for (i <- StdIn.readLine() split " ") yield i.toInt
        yourPods(i).position = new Position(x, y)
        yourPods(i).speed = new Speed(vx, vy)
        yourPods(i).angle = angle
        yourPods(i).nextCheckpoint = nextcheckpointid
      }
    }
    override def toString: String = {
      var res = ""
//      res += s"=== Track ===\n$track\n"
      res += s"=== My pods ===\n"
      myPods.foreach(pod => res += s"---$pod\n")
      res += s"=== Your pods ===\n"
      yourPods.foreach(pod => res += s"---$pod\n")
      res
    }
    def getPositionOfACheckpoint(checkpointId: Int): Position = {
      track.checkpoints.filter(checkpoint => checkpoint.id == checkpointId)(0).position
    }
    def formatOutput(position: Position, thrust: Any): String = {
      s"${position.x} ${position.y} $thrust"
    }
    def calculateThrust(pod: Pod, targetPosition: Position): Int = {
      val realSpeed = pod.getRealSpeed
      val distanceBetweenPodAndCheckpoint = pod.position.distanceWith(targetPosition)
      val angleBetweenPodAndCheckpoint = getAngleBetweenPodAndCheckpoint(pod, targetPosition)
      System.err.println(s"realSpeed: $realSpeed")
      System.err.println(s"angleBetweenPodAndCheckpoint: $angleBetweenPodAndCheckpoint")
      if(-7 <= angleBetweenPodAndCheckpoint && angleBetweenPodAndCheckpoint <= 7 && distanceBetweenPodAndCheckpoint > 1200) 125
      else 75
    }
    def calculateAttackThrust(pod: Pod, targetPosition: Position): Int = {
      val angleBetweenPodAndTarget = getAngleBetweenPodAndCheckpoint(pod, targetPosition)
      if(-10 <= angleBetweenPodAndTarget && angleBetweenPodAndTarget <= 10) 200
      else 100
    }
    def getAngleBetweenPodAndCheckpoint(pod: Pod, checkpointPosition: Position): Double = {
      val xA = pod.position.x
      val yA = pod.position.y
      val xB = checkpointPosition.x
      val yB = checkpointPosition.y
      val podCheckpointVector: Vector = new Vector(xB - xA, yB - yA)
      pod.speed.getAngleWith(podCheckpointVector)
    }
    def getTargetPod: Pod = {
      val sortedPods: Array[Pod] = yourPods.sortBy(pod => pod.rank)
      sortedPods(0)
    }
    def getBlockingPosition: Position = {
      val targetPod = getTargetPod
      val targetPodCheckpoint: Position = getPositionOfACheckpoint(targetPod.nextCheckpoint)
      targetPod.position.middleWith(targetPodCheckpoint)
    }
    def isCollisionWithEnemis(pod: Pod): Boolean = yourPods.exists(foePod => pod.position.distanceWith(foePod.position) < 850)
    def getNextSpeed(thrust: Int, vectorTowardTarget: Vector, actualSpeed: Vector): Vector = {
      val w = vectorTowardTarget
//      System.err.println(s"w: $w")
//      System.err.println(s"norme de w: ${w.getNorm}")
//      System.err.println(s"w norme: ${w / 2}")
//      System.err.println(s"w norme: ${w / w.getNorm}")
//      System.err.println(s"w norme * thrust: ${(w / w.getNorm) * thrust}")
      ((w / w.getNorm) * thrust + actualSpeed) * 0.86
    }
    def getNextPosition(actualPosition: Position, speed: Vector): Position = speed.toPosition + actualPosition
    def getBestThrust(pod: Pod, targetPosition: Position): Int = {
      var thrust = 200
      var position = pod.position
      var speed = pod.speed.toVector
      var counter = 0
      while(position.distanceWith(targetPosition) >= 400) {
        speed = getNextSpeed(thrust, pod.position.getVectorWith(targetPosition), speed)
        position = getNextPosition(position, speed)
        counter += 1
        thrust = 70
        System.err.println(s"counter: $counter")
        System.err.println(s"speed: $speed")
        System.err.println(s"position: $position")
        System.err.println(s"distance: ${position.distanceWith(targetPosition)}")
      }
      return 12
    }
    def playForOnePod(pod: Pod): Unit = {
      getBestThrust(pod, getPositionOfACheckpoint(pod.nextCheckpoint))
      if(pod.state == "neutral") {
        var thrust: Any = None
        val nextCheckpointPosition: Position = getPositionOfACheckpoint(pod.nextCheckpoint)
        if(!isCollisionWithEnemis(pod)) {
          thrust = 100 //calculateThrust(pod, nextCheckpointPosition)
        }
        else {
          thrust = "SHIELD"
        }
        println(formatOutput(nextCheckpointPosition, thrust))
      }
      else if (pod.state == "attack") {
        var thrust: Any = None
        val targetPosition = getTargetPod.position + (getTargetPod.speed * 3).toPosition
        if(isCollisionWithEnemis(pod)) {
          thrust = "SHIELD"
        }
        else {
          thrust = calculateAttackThrust(pod, targetPosition)
        }
        println(formatOutput(targetPosition, thrust))
      }
    }
    def updatePodRanking(): Unit = {
      val pods: Array[Pod] = myPods ++ yourPods
      pods.foreach { pod =>
        val distanceBetweenPodAndCheckpoint = pod.position.distanceWith(getPositionOfACheckpoint(pod.nextCheckpoint))
        pod.points = pod.points.toInt + checkpointRadius / distanceBetweenPodAndCheckpoint
        if(pod.nextCheckpoint != pod.actualCheckpoint) {
          pod.points = pod.points + 1.0
          pod.actualCheckpoint = pod.nextCheckpoint
        }
//        System.err.println(s"id: ${pod.id}, $distanceBetweenPodAndCheckpoint, pts: ${pod.points}")
      }
      val podSortedByPoints = pods.sortBy(pod => pod.points)(Ordering[Double].reverse)
      podSortedByPoints.indices.foreach(i => podSortedByPoints(i).rank = i + 1)
    }
    def playTurn(): Unit = {
      myPods(1).state = "attack"
      playForOnePod(myPods(0))
      playForOnePod(myPods(1))
    }
  }

  val nbLaps = StdIn.readInt()
  val nbCheckpoints = StdIn.readInt()
  val track = new Track(nbLaps, nbCheckpoints)

  for (i <- 0 until nbCheckpoints) {
    val Array(checkpointx, checkpointy) = for (i <- StdIn.readLine() split " ") yield i.toInt
    track.checkpoints.append(new Checkpoint(i, new Position(checkpointx, checkpointy)))
  }

  val game = new Game(track)
  while (true) {
    game.updatePods()
    System.err.println(game)
    game.playTurn()
    game.updatePodRanking()
  }
}