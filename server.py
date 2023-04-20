from flask import Flask, request, jsonify
from agent import Agent
from world_operations import create_world
import threading

app = Flask(__name__)
world = create_world()
agents = []

@app.route('/initialize_agent', methods=['POST'])
def initialize_agent():
    agent_data = request.json
    agent_name = agent_data['name']
    agent_description = agent_data['description']
    agent = Agent(agent_name, agent_description, world)
    agents.append(agent)
    return jsonify({'status': 'success', 'agent_name': agent_name})

@app.route('/move_agent', methods=['POST'])
def move_agent():
    move_data = request.json
    agent_name = move_data['agent_name']
    destination = move_data['destination']
    agent = next((a for a in agents if a.name == agent_name), None)
    if agent is None:
        return jsonify({'status': 'error', 'message': 'Agent not found'})

    success = agent.move(destination)
    if success:
        return jsonify({'status': 'success', 'message': f'{agent_name} moved to {destination}'})
    else:
        return jsonify({'status': 'error', 'message': f'Could not move {agent_name} to {destination}'})

@app.route('/agent_action', methods=['POST'])
def agent_action():
    action_data = request.json
    agent_name = action_data['agent_name']
    action_type = action_data['action_type']

    agent = next((a for a in agents if a.name == agent_name), None)
    if agent is None:
        return jsonify({'status': 'error', 'message': 'Agent not found'})

    if action_type == 'create_reflection':
        reflection = agent.create_reflection()
        return jsonify({'status': 'success', 'reflection': reflection})
    elif action_type == 'create_plan':
        plan = agent.create_plan()
        return jsonify({'status': 'success', 'plan': plan})
    elif action_type == 'generate_dialogue':
        other_agent_name = action_data['other_agent_name']
        other_agent = next((a for a in agents if a.name == other_agent_name), None)
        if other_agent is None:
            return jsonify({'status': 'error', 'message': 'Other agent not found'})

        dialogue = agent.generate_dialogue(other_agent)
        return jsonify({'status': 'success', 'dialogue': dialogue})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid action type'})

if __name__ == '__main__':
    app.run()
