from flask import Flask, request, render_template # type: ignore
from services.mysql_service import MySQLService
from services.redis_service import RedisService

app = Flask(__name__)
redis_service = RedisService()
mysql_service = MySQLService()

@app.route("/", methods=["GET", "POST"])
def form():
    message = ""
    if request.method == "POST":
        name = request.form["name"]

        # Save to Redis
        redis_service.save_user(name)

        # Save to MySQL
        mysql_service.save_user(name)

        message = f"Hello, {name}! Welcome to the page."
    return render_template("form.html", message=message)

if __name__ == "__main__":
    try:
        app.run(debug=True, host="0.0.0.0", port=5000)
    finally:
        mysql_service.close()