package proj756

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object Utility {
  /*
    Utility to get an Int from an environment variable.
    Return defInt if the environment var does not exist
    or cannot be converted to a string.
  */
  def envVarToInt(ev: String, defInt: Int): Int = {
    try {
      sys.env(ev).toInt
    } catch {
      case e: Exception => defInt
    }
  }

  /*
    Utility to get an environment variable.
    Return defStr if the environment var does not exist.
  */
  def envVar(ev: String, defStr: String): String = {
    sys.env.getOrElse(ev, defStr)
  }
}

object RMusic {

  val feeder = csv("music.csv").eager.random

  val rmusic = forever("i") {
    feed(feeder)
    .exec(http("RMusic ${i}")
      .get("/api/v1/music/${music_id}"))
      .pause(1)
  }

}

object RUser {

  val feeder = csv("users.csv").eager.circular

  val ruser = forever("i") {
    feed(feeder)
    .exec(http("RUser ${i}")
      .get("/api/v1/user/${user_id}"))
    .pause(1)
  }

}
object RPlaylist {

  // val feeder = csv("playlist.csv").eager.circular
  // // val feeder = csv("playlist.csv").readRecords

  // val rplaylist = forever("i") {
  //   feed(feeder)
  //   .exec(http("RPlaylist ${i}")
  //     .get("/api/v1/playlist/${playlist_id}"))
  //   .pause(1)

  // val rplaylist = exec(http("RPlaylist")
  //                   .get("/api/v1/playlist/${playlist_id}"))
  //                   .foreach(feeder, "RPlaylist") {
  //                     exec(flattenMapIntoAttributes("${playlist_id}"))
  //                   }.pause(1)
  val rplaylist  = exec(http("RPlaylist").get("/api/v1/playlist/cda67851-5ad5-4e28-b9c4-e2c44882100a")).pause(1)

  }


object CreateUser {
  // val feeder = csv("user.csv").eager.circular

  var createUser = exec(http("User Body")
                    .post("/api/v1/user/")
                    .body(StringBody(
                    """{
                      "lname": "Mathur",
                      "email": "am@gmail.com",
                      "fname": "Anisha",
                      "playlist": []
                      }""")))
                  .pause(1)
}

object CreateSong {
  // val feeder = csv("music.csv").eager.circular

  var createSong = exec(http("Song Body")
                    .post("/api/v1/music/")
                    .body(StringBody(
                    """{
                      "Artist": "Stephanie Beatriz",
                      "SongTitle": "We don't talk about Bruno"
                        }""")))
                  .pause(1)
}

object CreatePlaylist {
  // val feeder = csv("playlist.csv").eager.circular

  /*var createPlaylist = forever("i") {
    feed(feeder)
    .exec(http("Playlist Body")
    .post("/api/v1/playlist/")
    .body(StringBody(
      """{
        "title": "${title}",
        "user_id": "423a10a6-ab66-48c5-a1c7-dffb3169d744"
        }""")))
    .pause(1)
  }*/
  var createPlaylist = exec(http("Playlist Body")
                        .post("/api/v1/playlist/")
                        .body(StringBody(
                        """{
                          "title": "The Best Ever!",
                          "user_id": "423a10a6-ab66-48c5-a1c7-dffb3169d744"
                        }""")))
                      .pause(1)                     
}

/*object AddSongToPlaylist {
  /* Add Existing Song to Playlist (GET) & (PUT) */
  val playlist_feeder = csv("playlist.csv").eager.circular
  val music_feeder = csv("music.csv").eager.circular

  val addSongPlaylist = forever("i") {
    feed(playlist_feeder).exec(http("RPlaylist ${i}"))
    .exec(http("RPlaylist ${i}")
    .get("/api/v1/playlist/${playlist_id}"))
    .pause(1)
    .exec(http("AddSong to Playlist ${i}")
    .put("/api/v1/playlist/${playlist_id}"))
    .pause(1)

  }
}
*/

/*object AddSongToNewPlaylist {
  /* Create New Playlist (POST)
  Add song to new playlist (PUT)
  */

}*/

// scenario to check add song to playlist functionality
object AddSongToPlaylist {
  val p_feeder = csv("playlist.csv").eager.circular

  val addsong = feed(p_feeder)
              .exec(http("AddSongToPlaylist")
                .put("/api/v1/playlist/${playlist_id}")
                .body(StringBody("""{
                  "title": "Playlist_5", "music_id": "6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea"}""")).asJson)
              .pause(1)
  }

// scenario for remove song from playlist
object RemoveSongFromPlaylist {
  val p_feeder = csv("playlist.csv").eager.circular
  val m_feeder = csv("music.csv").eager.random

  val removesong = feed(p_feeder)
                  .feed(m_feeder)
                  .exec(http("RemoveSongFromPlaylist")
                    .put("/api/v1/playlist/${playlist_id}/${music_id}")
                    .body(StringBody("""{
                      "title": "${title}"}""")).asJson)
                  .pause(1)
}

object DeletePlaylist {
  val p_feeder = csv("playlist.csv").eager.circular

  val deleteplaylist = feed(p_feeder)
                      .exec(http("DeletePlaylist")
                        .delete("/api/v1/playlist/${playlist_id}")
                        .body(StringBody("""{
                          "user_id": "47cc62ed-bcee-434a-b35b-551e1b1e0450"}""")).asJson)
                      .pause(1)
}

// scenario to check update user functionality
/*object UUser {
  val feeder = csv("user.csv").eager.circular

  val uuser = forever("i") {
    feed(feeder)
    .exec(http("UUser ${i}")
      .put("/api/v1/user/${user_id}")
      .body(StringBody("""{
        "playlist":[],
        "email":"am@gmail.com",
        "fname":"Anisha",
        "lname":"Mathur"
      }""")).asJson
      .headers("Authorization":"abc"))
    .pause(1)
  }
}
*/
/*
  After one S1 read, pause a random time between 1 and 60 s
*/
object RUserVarying {
  val feeder = csv("users.csv").eager.circular

  val ruser = forever("i") {
    feed(feeder)
    .exec(http("RUserVarying ${i}")
      .get("/api/v1/user/${user_id}"))
    .pause(1, 60)
  }
}

/*
  After one S2 read, pause a random time between 1 and 60 s
*/

object RMusicVarying {
  val feeder = csv("music.csv").eager.circular

  val rmusic = forever("i") {
    feed(feeder)
    .exec(http("RMusicVarying ${i}")
      .get("/api/v1/music/${music_id}"))
    .pause(1, 60)
  }
}

/*
  After one S3 read, pause a random time between 1 and 60 s
*/

object RPlaylistVarying {
  val feeder = csv("playlist.csv").eager.random

  val rmusic = forever("i") {
    feed(feeder)
    .exec(http("RPlaylistVarying ${i}")
      .get("/api/v1/playlist/${playlist_id}"))
    .pause(1, 60)
  }
}

// object PlaylistProcess {
//   val u_feeder = csv("user.csv").eager.circular
//   val m_feeder = csv("music.csv").eager.random

//   val playlistprocess = forever("i") {
//     feed(u_feeder)
//     .feed(m_feeder)
//     .exec(http("PlaylistProcess ${i}")
//       .post("/api/v1/playlist/")
//       .body(StringBody(
//       """{
//         "title": "The Best Ever!",
//         "user_id": "423a10a6-ab66-48c5-a1c7-dffb3169d744"
//       }""")))
//     .pause(1)
//     .exec()
//   }
// }

/*
  Failed attempt to interleave reads from User and Music tables.
  The Gatling EDSL only honours the second (Music) read,
  ignoring the first read of User. [Shrug-emoji] 
 */
/*object RBoth {

  val u_feeder = csv("users.csv").eager.circular
  val m_feeder = csv("music.csv").eager.random
  val p_feeder = csv("playlist.csv").eager.random

  val rboth = forever("i") {
    feed(u_feeder)
    .exec(http("RUser ${i}")
      .get("/api/v1/user/${user_id}"))
    .pause(1);

    feed(m_feeder)
    .exec(http("RMusic ${i}")
      .get("/api/v1/music/${music_id}"))
    .pause(1)

    feed(p_feeder)
    .exec(http("RPlaylist ${i}")
      .get("/api/vi/playlist/${playlist_id}"))
    .pause(1)
  }

}*/

// Get Cluster IP from CLUSTER_IP environment variable or default to 127.0.0.1 (Minikube)
class ReadTablesSim extends Simulation {
  val httpProtocol = http
    .baseUrl("http://" + Utility.envVar("CLUSTER_IP", "127.0.0.1") + "/")
    .acceptHeader("application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    .authorizationHeader("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZGJmYmMxYzAtMDc4My00ZWQ3LTlkNzgtMDhhYTRhMGNkYTAyIiwidGltZSI6MTYwNzM2NTU0NC42NzIwNTIxfQ.zL4i58j62q8mGUo5a0SQ7MHfukBUel8yl8jGT5XmBPo")
    .acceptLanguageHeader("en-US,en;q=0.5")
}

class ReadUserSim extends ReadTablesSim {
  val scnReadUser = scenario("ReadUser")
      .exec(RUser.ruser)

  setUp(
    scnReadUser.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class ReadMusicSim extends ReadTablesSim {
  val scnReadMusic = scenario("ReadMusic")
    .exec(RMusic.rmusic)

  setUp(
    scnReadMusic.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class ReadPlaylistSim extends ReadTablesSim {
  val scnReadPlaylist = scenario("ReadPlaylist")
    .exec(RPlaylist.rplaylist)

  setUp(
    scnReadPlaylist.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class AddSongToPlaylistSim extends ReadTablesSim {
  val scnAddSong = scenario("AddSongToPlaylist")
    .exec(AddSongToPlaylist.addsong)

  setUp(
    scnAddSong.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class RemoveSongFromPlaylistSim extends ReadTablesSim {
  val scnRemoveSong = scenario("RemoveSongFromPlaylist")
    .exec(RemoveSongFromPlaylist.removesong)

  setUp(
    scnRemoveSong.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class DeletePlaylistSim extends ReadTablesSim {
  val scnDeletePlaylist = scenario("DeletePlaylist")
    .exec(DeletePlaylist.deleteplaylist)

  setUp(
    scnDeletePlaylist.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

/*

class UpdateUserSim extends ReadTableSim {
  val scnUpdateUser = scenario("UUser")
    .exec(UUser.uuser)

  setUp(
    scnUpdateUser.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}
*/

class CreatePlaylistSim extends ReadTablesSim {
  val scnCreatePlaylist = scenario("CreatePlaylist")
  .exec(CreatePlaylist.createPlaylist)

  setUp(
    scnCreatePlaylist.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class CreateSongSim extends ReadTablesSim {
  val scnCreateSong = scenario("CreateSong")
  .exec(CreateSong.createSong)

  setUp(
    scnCreateSong.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class CreateUserSim extends ReadTablesSim {
  val scnCreateUser = scenario("CreateUser").forever(){
    exec(CreateUser.createUser)
  }

  setUp(
    scnCreateUser.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}


class PlaylistProcessSim extends ReadTablesSim {
  val scnPlaylistProcess = scenario("PlaylistProcess").forever(){
     exec(CreatePlaylist.createPlaylist)
     .pause(1)
    .exec(AddSongToPlaylist.addsong)
    // .exec(RPlaylist.rplaylist)
  }
  setUp(
    scnPlaylistProcess.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class NewUserProcessSim extends ReadTablesSim {
  val scnNewUserProcess = scenario("NewUserProcess").forever(){
     exec(CreateUser.createUser)
     .exec(CreateSong.createSong)
     .exec(CreatePlaylist.createPlaylist)
    .exec(AddSongToPlaylist.addsong)
    // .exec(RPlaylist.rplaylist)
  }
  
  setUp(
    scnNewUserProcess.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)

}

/*
  Read both services concurrently at varying rates.
  Ramp up new users one / 10 s until requested USERS
  is reached for each service.
*/
/*class ReadBothVaryingSim extends ReadTablesSim {
  val scnReadMV = scenario("ReadMusicVarying")
    .exec(RMusicVarying.rmusic)

  val scnReadUV = scenario("ReadUserVarying")
    .exec(RUserVarying.ruser)

  val scnReadPV = scenario("ReadPlaylistVarying")
    .exec(RPlaylistVarying.rplaylist)

  val users = Utility.envVarToInt("USERS", 10)

  setUp(
    // Add one user per 10 s up to specified value
    scnReadMV.inject(rampConcurrentUsers(1).to(users).during(10*users)),
    scnReadUV.inject(rampConcurrentUsers(1).to(users).during(10*users)),
    scnReadPV.inject(rampConcurrentUsers(1).to(users).during(10*users))
  ).protocols(httpProtocol)
}*/

/*
  This doesn't work---it just reads the Music table.
  We left it in here as possible inspiration for other work
  (or a warning that this approach will fail).
 */
/*
class ReadBothSim extends ReadTablesSim {
  val scnReadBoth = scenario("ReadBoth")
    .exec(RBoth.rboth)

  setUp(
    scnReadBoth.inject(atOnceUsers(1))
  ).protocols(httpProtocol)
}
*/
