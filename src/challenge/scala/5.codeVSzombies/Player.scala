import scala.collection.mutable.ArrayBuffer
import scala.io.StdIn
import scala.math._

/**
 * Save humans, destroy zombies!
 **/
object Player extends App {

  val ash = new Ash(Point(0, 0))

  abstract class Personage(val id: Int, var position: Point) {
    def distanceWith(that: Personage): Double = {
      that match {
        case zombie: Zombie => this.position.distanceWith(zombie.nextPosition)
        case _ => this.position.distanceWith(that.position)
      }
    }
    def nextPosition(distance: Int, target: Personage): Point = {
      this.position.addDistanceTowardPoint(distance, target.position)
    }
    override def toString: String = s"""($id, $position)"""
  }

  case class Point(x: Int, y: Int) {
    def distanceWith(that: Point): Double = {
      val xA = this.x
      val yA = this.y
      val xB = that.x
      val yB = that.y
      sqrt((xB - xA) * (xB - xA) + (yB - yA) * (yB - yA))
    }
    def addDistanceTowardPoint(distance: Int, that: Point): Point = {
      val xA = this.x
      val yA = this.y
      val xB = that.x
      val yB = that.y
      val AE = abs(xB - xA)
      val AB = this.distanceWith(that)
      val theta = acos(AE / AB)
      if(xB - xA > 0 && yB - yA > 0)
        new Point((distance * cos(theta) + this.x).toInt, (distance * sin(theta) + this.y).toInt)
      if(xB - xA < 0 && yB - yA > 0)
        new Point((distance * -cos(theta) + this.x).toInt, (distance * sin(theta) + this.y).toInt)
      if(xB - xA < 0 && yB - yA < 0)
       new Point((distance * -cos(theta) + this.x).toInt, (distance * -sin(theta) + this.y).toInt)
      else
        new Point((distance * cos(theta) + this.x).toInt, (distance * -sin(theta) + this.y).toInt)
    }

    override def toString: String = s"""($x,$y)"""
  }

  class Ash(position: Point) extends Personage(12000, position: Point)

  class Human(id: Int, position: Point) extends Personage(id: Int, position: Point)

  class Zombie(id: Int, position: Point, var nextPosition: Point) extends Personage(id: Int, position: Point)

  // game loop
  while (true) {
    var humans: ArrayBuffer[Human] = ArrayBuffer[Human]()
    var zombies: ArrayBuffer[Zombie] = ArrayBuffer[Zombie]()

    val Array(x, y) = for (i <- StdIn.readLine() split " ") yield i.toInt
    ash.position = new Point(x, y)
    val humanCount = StdIn.readInt()
    for (i <- 0 until humanCount) {
      val Array(humanId, humanX, humanY) = for (i <- StdIn.readLine split " ") yield i.toInt
      humans += new Human(humanId, Point(humanX, humanY))
    }
    val zombieCount = StdIn.readInt()
    for (i <- 0 until zombieCount) {
      val Array(zombieId, zombieX, zombieY, zombieXNext, zombieYNext) = for (i <- StdIn.readLine split " ") yield i.toInt
      zombies += new Zombie(zombieId, Point(zombieX, zombieY), Point(zombieXNext, zombieYNext))
    }

    val humansNotConvicted = humans.filter{human =>
      val oneZombieOnHuman = zombies.map(zombie => (human, zombie.distanceWith(human)))
        .map { case (_, distanceWithZombie) => distanceWithZombie }
        .forall(_ > 400)
      val nextAshPos = ash.nextPosition(1000, human)
      val dist = nextAshPos.distanceWith(human.position)

//      System.err.println(s"""====== ${human.id} ===""")
//      System.err.println(s"""current pos Ash: ${ash.position}""")
//      System.err.println(s"""next pos Ash: $nextAshPos""")
//      System.err.println(s"""dist: $dist""")
      oneZombieOnHuman || dist <= 2000
    }

    val nearestHuman: Human = humansNotConvicted.map(human => (human, ash.distanceWith(human))).sortBy(_._2)
      .head
      ._1

    println( s"""${nearestHuman.position.x} ${nearestHuman.position.y}""")
  }
}