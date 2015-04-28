object Player {
  def main(a: Array[String]) {
    var Array(w, x, y, z) = for(i <- readLine split " ") yield i.toInt
    while(true) {
        var o = ""
        if(z < x) {o="S"; z+=1} else if(z > x) {o="N"; z-=1}
        if(y < w) {o+="E"; y+=1} else if(y > w) {o+="W"; y-=1}
        println(o)
    }
  }
}
