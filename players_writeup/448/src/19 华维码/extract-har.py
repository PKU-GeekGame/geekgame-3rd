import base64
import json
import os

os.chdir(os.path.dirname(__file__))
os.makedirs("output", exist_ok=True)

with open("prob19.geekgame.pku.edu.cn.har", "r", -1, "utf8") as reader:
  data = json.load(reader)

entries = data["log"]["entries"]

i = 0
for entry in entries:
  request_url = entry["request"]["url"]
  if not ".png" in request_url:
    continue

  response_content = entry["response"]["content"]["text"]

  i += 1
  with open(f"{i:03d}.jpg", "wb") as writer:
    writer.write(base64.decodebytes(response_content.encode("utf8")))