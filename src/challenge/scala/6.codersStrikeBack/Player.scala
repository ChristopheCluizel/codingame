import scala.collection.mutable.ArrayBuffer
import scala.io.StdIn

object Player extends App {

  case class Position(val x: Int, val y: Int) {
    override def toString: String = s"Pos($x, $y)"
  }

  case class Speed(val x: Int, val y: Int) {
    override def toString: String = s"Speed($x, $y)"
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

  case class Pod(var position: Position = new Position(0, 0), var speed: Speed = new Speed(0, 0), var angle: Int = 0, var nextCheckpoint: Int = 0) {
    override def toString: String = s"$position\n$speed\nangle: $angle"
  }

  case class Game(val track: Track, val myPods: Array[Pod] = Array(new Pod(), new Pod()), val yourPods: Array[Pod] = Array(new Pod(), new Pod())) {
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
      res += s"=== Track ===\n$track\n"
      res += s"--- My pods ---\n"
      myPods.foreach(pod => res += s"$pod\n")
      res += s"--- Your pods ---\n"
      yourPods.foreach(pod => res += s"$pod\n")
      res
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
    println("8000 4500 100")
    println("8000 4500 100")
  }
}