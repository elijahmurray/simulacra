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
        agent.memories = data["memories"]
        # agent.memory_stream = MemoryStream.from_dict(data["memory_stream"])
        agent.name = data["name"]
        agent.innate_tendencies = data["innate_tendencies"]
        agent.learned_tendencies = data["learned_tendencies"]
        agent.current_datetime = datetime.datetime.fromisoformat(
            data["current_datetime"]
        )
        agent.next_action = data["next_action"]
        agent.age = data["age"]
        agent.occupational_statement = data["occupational_statement"]
        agent.biography_data = data["biography_data"]
        agent.daily_plan = data["daily_plan"]
        agent.next_hour_plan = data["next_hour_plan"]
        agent.cached_daily_occupation = data["cached_daily_occupation"]
        agent.cached_core_characteristics = data["cached_core_characteristics"]

        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5001, debug=True)
