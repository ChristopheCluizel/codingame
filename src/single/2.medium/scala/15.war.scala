import math._
import scala.util._
import scala.collection.mutable.Queue


case class Card(card: String) {
  val values = Array("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
  val suitsChar = Array('H', 'D', 'C', 'S')
  val suitsString = Array("H", "D", "C", "S")

  val value = card.split(suitsChar).toList.head
  val suit = card.split("").intersect(suitsString).head

  override def toString: String = {
    s"$card"
  }

  def <(that: Card): Boolean = {
    val index1 = this.values.indexOf(this.value)
    val index2 = that.values.indexOf(that.value)

    index1 < index2
  }

  def ==(that: Card): Boolean = {
    val index1 = this.values.indexOf(this.value)
    val index2 = that.values.indexOf(that.value)

    index1 == index2
  }
}

object Solution extends App {
  def war(p1Cards: Queue[Card], p2Cards: Queue[Card], p1: Queue[Card], p2: Queue[Card]): Unit = {
//    Console.err.println("---- War ----")
    val p11 = p1Cards.dequeue
    val p12 = p1Cards.dequeue
    val p13 = p1Cards.dequeue
    val p21 = p2Cards.dequeue
    val p22 = p2Cards.dequeue
    val p23 = p2Cards.dequeue

    p1 += p11
    p1 += p12
    p1 += p13

    p2 += p21
    p2 += p22
    p2 += p23
    fight(p1Cards, p2Cards, p1, p2)
  }

  def fight(p1Cards: Queue[Card], p2Cards: Queue[Card], p1: Queue[Card], p2: Queue[Card]) = {
//    Console.err.println("**** Fight ****")
    val card1 = p1Cards.dequeue
    val card2 = p2Cards.dequeue

    p1 += card1
    p2 += card2

      if (card1 == card2) {
        war(p1Cards, p2Cards, p1, p2)
      }
      else {
        if(card1 < card2) {
          p2Cards ++= p1
          p2Cards ++= p2
        } else {
          p1Cards ++= p1
          p1Cards ++= p2
        }
      }
  }

  def testCase4: (List[Card], List[Card]) = {
    val l1 = List(Card("8C"),Card("KD"),Card("AH"),Card("QH"),Card("2S"))
    val l2 = List(Card("8D"),Card("2D"),Card("3H"),Card("4D"),Card("3S"))
    (l1, l2)
  }


  def testCase5: (List[Card], List[Card]) = {
    val l1 = List(Card("10H"),Card("KD"),Card("6C"),Card("10S"),Card("8S"),Card("AD"),Card("QS"),Card("3D"),Card("7H"),Card("KH"),Card("9D"),Card("2D"),Card("JC"),Card("KS"),Card("3S"),Card("2S"),Card("QC"),Card("AC"),Card("JH"),Card("7D"),Card("KC"),Card("10D"),Card("4C"),Card("AS"),Card("5D"),Card("5S"))
    val l2 = List(Card("2H"),Card("9C"),Card("8C"),Card("4S"),Card("5C"),Card("AH"),Card("JD"),Card("QH"),Card("7C"),Card("5H"),Card("4H"),Card("6H"),Card("6S"),Card("QD"),Card("9H"),Card("10C"),Card("4D"),Card("JS"),Card("6D"),Card("3H"),Card("8H"),Card("3C"),Card("7S"),Card("9S"),Card("8D"),Card("2C"))
    (l1, l2)
  }

  def testCase7: (List[Card], List[Card]) = {
    val l1 = List(Card("AH"),Card("4H"),Card("5D"),Card("6D"),Card("QC"),Card("JS"),Card("8S"),Card("2D"),Card("7D"),Card("JD"),Card("JC"),Card("6C"),Card("KS"),Card("QS"),Card("9D"),Card("2C"),Card("5S"),Card("9S"),Card("6S"),Card("8H"),Card("AD"),Card("4D"),Card("2H"),Card("2S"),Card("7S"),Card("8C"))
    val l2 = List(Card("10H"),Card("4C"),Card("6H"),Card("3C"),Card("KC"),Card("JH"),Card("10C"),Card("AS"),Card("5H"),Card("KH"),Card("10S"),Card("9H"),Card("9C"),Card("8D"),Card("5C"),Card("AC"),Card("3H"),Card("4S"),Card("KD"),Card("7C"),Card("3S"),Card("QH"),Card("10D"),Card("3D"),Card("7H"),Card("QD"))
    (l1, l2)
  }

  def testCase8: (List[Card], List[Card]) = {
    val l1 = List(Card("5S"),Card("8D"),Card("10H"),Card("9S"),Card("4S"),Card("6H"),Card("QC"),Card("6C"),Card("6D"),Card("9H"),Card("2C"),Card("7S"),Card("AC"),Card("5C"),Card("7D"),Card("9D"),Card("QS"),Card("4D"),Card("3C"),Card("JS"),Card("2D"),Card("KD"),Card("10S"),Card("QD"),Card("3H"),Card("8H"))
    val l2 = List(Card("4C"),Card("JC"),Card("8S"),Card("10C"),Card("5H"),Card("7H"),Card("3D"),Card("AH"),Card("KS"),Card("10D"),Card("JH"),Card("6S"),Card("2S"),Card("KC"),Card("8C"),Card("9C"),Card("KH"),Card("3S"),Card("AD"),Card("JD"),Card("4H"),Card("7C"),Card("2H"),Card("QH"),Card("5D"),Card("AS"))
    (l1, l2)
  }

  val simulate = false
  val p1Cards = new Queue[Card]
  val p2Cards = new Queue[Card]
  var turns = 0


  if (simulate) {
    val (l1, l2) = testCase8
    p1Cards ++= l1
    p2Cards ++= l2
  } else {
    val n = readInt // the number of cards for player 1
    for (i <- 0 until n) {
      val cardp1 = readLine // the n cards of player 1
      p1Cards += Card(cardp1)
    }
    val m = readInt // the number of cards for player 2
    for (i <- 0 until m) {
      val cardp2 = readLine // the m cards of player 2
      p2Cards += Card(cardp2)
    }
  }


//  Console.err.println(p1Cards)
//  Console.err.println(p2Cards)

  try {
    while (p1Cards.nonEmpty && p2Cards.nonEmpty) {
      turns += 1
//      Console.err.println(s"==== Fight $turns ====")
      fight(p1Cards, p2Cards, new Queue[Card], new Queue[Card])
//      Console.err.println(p1Cards)
//      Console.err.println(p2Cards)
    }

    if (p1Cards.nonEmpty && p2Cards.isEmpty) println(s"1 $turns")
    else if (p1Cards.isEmpty && p2Cards.nonEmpty) print(s"2 $turns")
    else println("PAT")
  }catch {
    case e: Exception => println("PAT")
  }
}
