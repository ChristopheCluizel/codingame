import scala.collection.immutable.IndexedSeq
import scala.io.StdIn._

object Solution extends App {
  val weight: Map[Int, Set[Char]] = Map(
    1 -> Set('e', 'a', 'i', 'o', 'n', 'r', 't', 'l', 's', 'u'),
    2 -> Set('d', 'g'),
    3 -> Set('b', 'c', 'm', 'p'),
    4 -> Set('f', 'h', 'v', 'w', 'y'),
    5 -> Set('k'),
    8 -> Set('j', 'x'),
    10 -> Set('q', 'z')
  )

  def calculatePoints(word: String): Int = {
    val points: IndexedSeq[Int] = word.flatMap { letter =>
      weight.keys.filter(key => weight.get(key).get.contains(letter)) // get the keys whose its value contains the letter
    }
    points.sum
  }

  def getOccurrences(word: String): Map[Char, Int] = {
    word.groupBy(_.toChar).mapValues(_.length)
  }

  def canCreateTheWordWithLetters(letters: String, word: String): Boolean = {
    val lettersOccurrences: Map[Char, Int] = getOccurrences(letters)
    val wordOccurrences: Map[Char, Int] = getOccurrences(word)
    val sharedKeys: Set[Char] = lettersOccurrences.keys
      .toSet
      .intersect(wordOccurrences.keys.toSet)
    if(sharedKeys.size == wordOccurrences.keys.size) {
      sharedKeys.map(key => lettersOccurrences.get(key).get >= wordOccurrences.get(key).get).forall(bool => bool)
    }
    else false
  }

  /* get the size of the dictionary */
  val dictionarySize: Int = readInt()
  /* fill the dictionary with the words */
  var dictionary: Set[String] = Set[String]()
  for (i <- 0 until dictionarySize) {
    dictionary = dictionary + readLine()
  }
  /* get the letters and their occurrences */
  val letters: String = readLine()

  /* from the letters given, find the existing words we can create */
  val words: Set[String] = dictionary.filter(word => canCreateTheWordWithLetters(letters, word))

  /* calculate the points for each word */
  val wordsPoints: Set[(String, Int)] = words.map(word => (word, calculatePoints(word)))

  /* get the max points and the best word */
  val maxPoints: Int = wordsPoints.map(_._2).max
  val bestWord: String = wordsPoints.filter{case(word, points) => points == maxPoints}
    .head
    ._1

  println(bestWord)
}

