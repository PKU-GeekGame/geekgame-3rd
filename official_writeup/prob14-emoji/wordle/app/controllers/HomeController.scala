package controllers

import javax.inject._
import play.api._
import play.api.mvc._
import java.security.MessageDigest
import java.util.Base64
import scala.util.Try
import java.util.Random

/**
 * This controller creates an `Action` to handle HTTP requests to the
 * application's home page.
 */
@Singleton
class HomeController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {
  val flag1 = "flag{s1Mp1e_brut3f0rc3}"
  val flag2 = "flag{d3c0d1n9_jwT_15_345y}"
  val flag3 = "flag{StateIess_game_IS_a_b4d_1d3a}"
  val remaining_guesses = Map("1" -> 64, "2" -> 8, "3" -> 3)
  val flags = Map("1" -> flag1, "2" -> flag2, "3" -> flag3)

  /**
   * Create an Action to render an HTML page.
   *
   * The configuration in the `routes` file means that this method
   * will be called when the application receives a `GET` request with
   * a path of `/`.
   */
  def index() = Action { implicit request: Request[AnyContent] =>
    Ok(views.html.index()).withSession(Session())
  }

  def md5(content: String): Array[Byte] = {
    MessageDigest.getInstance("MD5").digest(content.getBytes())
  }

  def md5b64(content: String): String = {
    new String(Base64.getEncoder().encode(md5(content + "PKU") concat md5(content + "GeekGame") concat md5(content + "2023")))
  }

  def md5b64_emoji(content: String): String = {
    md5b64(content).map(x => Character.toString(x.toInt + 0x1F410)).mkString
  }

  def seed(): String = {
    (System.currentTimeMillis() * Math.random()).toString()
  }

  def toArray(content: String): Array[Int] = {
    var result = Array[Int]()
    var i = 0
    while (i < content.length()) {
      var codePoint = Character.codePointAt(content, i);
      i += Character.charCount(codePoint);
      result :+= codePoint
    }
    result
  }

  def show(level: String) = Action { implicit request: Request[AnyContent] =>
    var session = request.session
    var guess = request.getQueryString("guess").getOrElse("")
    if (session.get("level").getOrElse("") != level) session = Session() + ("level" -> level)
    var timeout = false
    if (level == "3") {
      var start_time: Double = Try(session.get("start_time").getOrElse("").toDouble).toOption.getOrElse(-1)
      if (start_time == -1) {
        session = session + ("start_time" -> System.currentTimeMillis().toString)
      } else if (System.currentTimeMillis() - start_time > 60000) {
        timeout = true
      }
    }
    var results = session.get("results").getOrElse("")
    var _remaining_guesses = Try(session.get("remaining_guesses").getOrElse("").toInt).toOption.getOrElse(-1)
    if (_remaining_guesses == -1) {
      _remaining_guesses = remaining_guesses.get(level).getOrElse(0)
      session = session + ("remaining_guesses" -> _remaining_guesses.toString)
    }
    var target = level match {
      case "1" => md5b64_emoji(flag1)
      case "2" => {
        var _target = session.get("target").getOrElse("")
        if (_target == "") {
          _target = md5b64_emoji(flag2 + seed())
          session = session + ("target" -> _target)
        }
        _target
      }
      case "3" => {
        var _seed = session.get("seed").getOrElse("")
        if (_seed == "") {
          _seed = seed()
          session = session + ("seed" -> _seed)
        }
        md5b64_emoji(flag3 + _seed)
      }
    }
    var error = ""
    var flag = ""
    var result = ""
    if (timeout) {
      _remaining_guesses = 0
      session = Session()
      error = "<script>alert('Timeout. Please try to solve level 3 in one minute.');location='/';</script>"
    }
    if (guess != "" && _remaining_guesses > 0 && !timeout) {
      val guess_array = toArray(guess)
      val target_array = toArray(target)
      val target_set = target_array.toSet
      if (guess_array.length > 64) {
        error = "Error: Guess too long (maximum length is 64)"
      } else {
        _remaining_guesses = _remaining_guesses - 1
        session = session + ("remaining_guesses" -> _remaining_guesses.toString)
        result = (0 to guess_array.length - 1).map(x => if (guess_array(x) == target_array(x)) {
          "🟩"
        } else if (target_set contains guess_array(x)) {
          "🟨"
        } else {
          "🟥"
        }
        ).mkString
        if (result == "🟩" * 64) {
          flag = flags.get(level).getOrElse("")
        }
      }
    }
    Ok(views.html.main(remainingGuesses = _remaining_guesses, flag = flag, error = error, result = result, level = level, example=(0 to 63).map(x=>Character.toString((new Random()).nextInt(128) + 0x1F410)).mkString)).withSession(session)
  }
}
