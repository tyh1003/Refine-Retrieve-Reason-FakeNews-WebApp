import json
from student_bot import StudentBot

bot = StudentBot(
    config_path="./config/student_bot_config.yaml"
)

with open(
    "./output/retrieve.jsonl",
    "r",
    encoding="utf-8"
) as f:

    data = json.loads(f.readline())

label, reason, knowledge = bot.predict(
    Rc=data["Rc"],
    Rv=data["Rv"],
    K_int=data["K_int"],
    K_ext=data["K_ext"]
)

print("\n===== RESULT =====")
print("label =", label)
print("reason =", reason)
print("knowledge =", knowledge)