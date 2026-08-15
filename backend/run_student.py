import json

from student_bot import StudentBot


print("StudentBot Start")

bot = StudentBot(
    config_path="./config/student_bot_config.yaml"
)

with open(
    "./output/retrieve.jsonl",
    "r",
    encoding="utf-8"
) as f:
    lines = f.readlines()

data = json.loads(lines[-1])

label, conf, reason = bot.predict(
    Rc=data["Rc"],
    Rv=data["Rv"],
    K_int=data["K_int"],
    K_ext=data["K_ext"]
)

result = {
    "vid": data.get("vid"),
    "pred_label": label,
    "conf": conf,
    "reason": reason,
    "knowledge": [],
}

with open(
    "./output/final_result.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=2
    )

print("StudentBot Done")
