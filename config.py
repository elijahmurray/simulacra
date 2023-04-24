from dotenv import load_dotenv
import os
load_dotenv()

# CONFIG

DEV_MODE=True

# OPENAI CONFIG
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
OPENAI_MODEL="gpt-3.5-turbo"
MAX_TOKENS=300

# MEMORY CONFIG

RETRIEVAL_WEIGHTS = {
  'importance': 0.5,
  'relevance': 0.5,
  'recency': 0.5,
}

# SIMULATION CONFIG

SIM_CLOCK_INCREMENT_MINUTES = 10

# PROMPTS

IMPORTANCE_PROMPT = '''
On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory. Do not ask for more information, only respond with an integer score and nothing else, including no other punctuation.
Memory: {description}
Rating: <fill in>
'''

REFLECTION_SALIENT_POINTS_PROMPT = '''
{recent_memories}
Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements?
'''

REFLECTION_GENERATION_PROMPT = '''
Statements about {agent_name}
{numbered_statement_list}
What 5 high-level insights can you infer from the above statements? (example format: insight (because of 1, 5, 3))
'''

INITIAL_PLAN_PROMPT = '''
Name: {agent_name} (age: {age})
{agent_summary_description}
Outline {agent_name}'s plan for the full day, with each plan having a duration of exactly 60 minutes, no more and no less. The start times should be at the top of the hour (for example 8:00 or 9:00, not 8:30 or 9:30). Do not include any information other than the plan in your response. Produce a plan faithfully, do not ask for more detail, do not ask for more information. Use the following JSON format to produce the schedule. Only return JSON in your response, no other text or markdown formatting:
{{
  "schedule":
  [
    {{
      "start_time": "8:00AM",
      "duration_minutes": 60,
      "description": "wake up"
    }},
    {{
      "start_time": "9:00AM",
      "duration_minutes": 60,
      "description": "eat breakfast"
    }}
  ]
}}
'''

PLAN_PROMPT_DAY = '''
Name: {agent_name} (age: {age})
{agent_summary_description}
The following was {agent_name}'s schedule yesterday:
{yesterday_schedule}
Outline {agent_name}'s plan for the full day, with each plan having a duration of exactly 60 minutes, no more and no less. The start times should be at the top of the hour (for example 8:00 or 9:00, not 8:30 or 9:30). Do not include any information other than the plan in your response. Produce a plan faithfully, do not ask for more detail, do not ask for more information. Use the following JSON format to produce the schedule. Only return JSON in your response, no other text or markdown formatting:
{{
  "schedule":
  [
    {{
      "start_time": "8:00AM",
      "duration_minutes": 60,
      "description": "wake up"
    }},
    {{
      "start_time": "9:00AM",
      "duration_minutes": 60,
      "description": "eat breakfast"
    }}
  ]
}}
'''

PLAN_PROMPT_BLOCK= '''
Name: {agent_name} (age: {age})
{agent_summary_description}
The following was {agent_name}'s schedule for the next one hour.
{block_schedule}
Detail {agent_name}'s plan for the whole hour, in exactly 6 tasks, each with a duration of 10 minutes. Only provide a schedule for the hour specified, do not plan past the end of the hour. Only plan six tasks and make all of them 10 minutes duration. Do not include any information other than the plan in your response. Produce a plan faithfully, do not ask for more detail, do not ask for more information. Use the following JSON format to produce the schedule. Only return JSON in your response, no other text or markdown formatting:
{{
  "schedule":
  [
    {{
      "start_time": "8:00AM",
      "duration_minutes": 10,
      "description": "wake up"
    }},
    {{
      "start_time": "8:10AM",
      "duration_minutes": 10,
      "description": "brush teeth"
    }}
  ]
}}
'''

PLAN_REACTION_PROMPT = '''
{agent_summary_description}
It is {datetime}.
{agent_name}'s status: {agent_name} is currently {current_action}.
Observation: {observation}
Summary of relevant context from {agent_name}'s memory:
{relevant_context}
Should {agent_name} react to the observation, and if so, what would be an appropriate reaction?
'''

DIALOGUE_INITIAL_PROMPT = '''
{agent_summary_description}
It is {datetime}.
{agent_name}'s status: {agent_name} is currently {current_action}.
Observation: {observation}
Summary of relevant context from {agent_name}'s memory:
{relevant_context}
{plan_reaction_response}
What should {agent_name} say to {other_agent_name}?
'''

DIALOGUE_CONTINUATION_PROMPT = '''
{agent_summary_description}
It is {datetime}.
{agent_name}'s status: {agent_name} is currently {current_action}.
Observation: {observation}
Summary of relevant context from {agent_name}'s memory:
{relevant_context}
Here is the dialogue history:
{dialogue_history}
What should {agent_name}'s response be?
'''

ACTION_LOCATION_PROMPT = '''
{agent_summary_description}
{agent_name} is currently in {current_location} that has {current_location_description}.
{agent_name} knows about the following locations: {known_locations}
Prefer to stay in the current area if the activity can be done there.
{agent_name} is planning to {next_action}.
Which area should {agent_name} go to?
'''

STATE_CHANGE_PROMPT = '''
{agent_name} is currently performing the following action: {current_action} on the following object: {current_object}.
What should we update the state of the object to? (e.g., if the object is a door, the state could be open or closed. If the object is a stove and the action is cooking, the state could be on or off.)
'''
