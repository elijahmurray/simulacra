from flask import Flask, render_template, jsonify, request
from agent.agent import Agent
import datetime

from shared_agent import agent


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_agent_data")
def get_agent_data():
    data = {
        "name": agent.name,
        "innate_tendencies": agent.innate_tendencies,
        "learned_tendencies": agent.learned_tendencies,
        "current_datetime": agent.current_datetime,
        "next_action": agent.next_action,
        "age": agent.age,
        "occupational_statement": agent.occupational_statement,
        "biography_data": agent.biography_data,
        "daily_plan": agent.daily_plan,
        "next_hour_plan": agent.next_hour_plan,
        "cached_daily_occupation": agent.cached_daily_occupation,
        "cached_core_characteristics": agent.cached_core_characteristics,
        # "cached_self_assessment": agent.cached_self_assessment,
    }
    return jsonify(data)


@app.route("/update_agent", methods=["POST"])
def update_agent():
    if request.is_json:
        data = request.get_json()
        global agent
        # agent.biography_data = data["biography_data"]
        # agent.daily_plan = data["quick_start_data"]["quick_start_daily_plan"]
        # agent.cached_daily_occupation = data["quick_start_data"][
        #     "quick_start_occupation"
        # ]
        # agent.cached_core_characteristics = data["quick_start_data"][
        #     "quick_start_core_characteristics"
        # ]
        agent.current_datetime = datetime.datetime.fromisoformat(
            data["current_datetime"]
        )
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5001, debug=True)
