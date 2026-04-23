from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os, re

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
ADMIN_UID = os.environ.get("ADMIN_UID")

banned_words = []

if not SLACK_APP_TOKEN or not SLACK_BOT_TOKEN:
    print("token missing!")
    exit()


app = App(token=SLACK_BOT_TOKEN)


@app.message()
def all_handler(say, message):
     text = message.get("text", "").lower()
     user_id = message.get("user")
     event_ts = message.get("ts")
     matched_words = [word for word in banned_words if word in text]

     if matched_words:
          print("banned word found")
          alert = (
               f":confused-dino: CRITICAL ADMINISTRATION ALERT\n"
               f"User <@{user_id}> has said a banned word\n"
               f"Administrator <@{ADMIN_UID}> has been alerted immidiaetly\n"
               f"_hi there, im a joke bot that was created to replace the prometheus april fools messages by brny_"
          )
          say(text=alert, thread_ts=event_ts)
          return

@app.message(re.compile("clanker", re.IGNORECASE))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
def mention_handler(body, say):
        print("clanker easteregg")
        say('oi, orphmeteus is not a clanker')


@app.command("/orphmeteus")
def slash_handler(ack, body, say):
       ack()
       user_id = body['user_id']
       text = body['text']

       if user_id != ADMIN_UID:
            say(f":big-orpheus-plushie: woah, not cool <@{user_id}>. you can't do that.")
            print("invalid_perms")
            return
       
       if "set" in text.lower():
             parts = text.split()
             if len(parts) != 2 and parts[0].lower() != "set":
                say(":big-orpheus-plushie: too many arguments")
                print("too_much_args")
                return
             else:
                   to_ban = parts[1]
                   banned_words.append(to_ban)
                   say(f":big-orpheus-plushie: banned word '{to_ban}'")
                   print("word banned")
                   return
       elif "remove" in text.lower():
             parts = text.split()
             if len(parts) != 2 and parts[0].lower() != "remove":
                say(":big-orpheus-plushie: too many arguments")
                print("too_much_args")
                return
             else:
                   to_unban = parts[1]
                   if to_unban in banned_words:
                    banned_words.remove(to_unban)
                    say(f":big-orpheus-plushie: unbanned word {to_unban}")
                    print("unbanned word")
                    return
                   else:
                    say(f":big-orpheus-plushie: word is not banned")
                    print("word not banned")
                    return
                   

if __name__ == "__main__":
        print("starting")
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()