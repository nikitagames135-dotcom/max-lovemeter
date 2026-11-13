from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

MESSAGES = [
    (90, "Вы буквально созданы для романтической комедии! 💍"),
    (75, "Кажется, между вами есть особенная искра! ✨"),
    (55, "У вас есть общие темы — это хорошее начало! 🌷"),
    (35, "Вы разные, зато есть что интересного узнать друг о друге! 💌"),
    (0, "Любовь не измеряется цифрами. Может, вас ждёт сюрприз! 💗"),
]

def compatibility(name1, name2, hobbies1, hobbies2):
    first = {x.strip().casefold() for x in hobbies1.split(",") if x.strip()}
    second = {x.strip().casefold() for x in hobbies2.split(",") if x.strip()}

    if first or second:
        union = first | second
        overlap = len(first & second) / len(union) if union else 0
        score = round(25 + overlap * 70)
    else:
        # Игровой результат, если интересы не указаны.
        seed = f"{name1.casefold()}|{name2.casefold()}"
        score = 40 + int(hashlib.sha256(seed.encode()).hexdigest()[:2], 16) % 51

    # Небольшая вариация для развлечения, не является настоящей оценкой отношений.
    seed = f"{name1.casefold()}|{name2.casefold()}"
    variation = int(hashlib.sha256(seed.encode()).hexdigest()[2:4], 16) % 9 - 4
    return max(1, min(99, score + variation))

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    message = ""
    name1 = ""
    name2 = ""
    error = ""

    if request.method == "POST":
        name1 = request.form.get("name1", "").strip()[:30]
        name2 = request.form.get("name2", "").strip()[:30]
        hobbies1 = request.form.get("hobbies1", "").strip()[:200]
        hobbies2 = request.form.get("hobbies2", "").strip()[:200]

        if not name1 or not name2:
            error = "Пожалуйста, укажите оба имени."
        else:
            result = compatibility(name1, name2, hobbies1, hobbies2)
            message = next(text for threshold, text in MESSAGES if result >= threshold)

    return render_template(
        "index.html",
        result=result,
        message=message,
        name1=name1,
        name2=name2,
        error=error,
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
