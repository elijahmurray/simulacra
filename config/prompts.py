from __future__ import annotations
from agent.agent import Agent
from utils.formatting_utils import hour_formatter
from config import TIME_INCREMENT
import datetime
from typing import List, Dict



# Elijah prompts, merge later
def current_action_prompt(agent_summary: str, agent: Agent, current_datetime: datetime.datetime) -> str:
    prompt = f"""{agent_summary}.\n
        {agent.name}'s current plan is: \n{agent.cached_increment_plan} \n
        \nGiven it is now {hour_formatter(agent.current_datetime) },
        provide a definitive statement with no explanation for what {agent.name}
        is doing, in the format: "At [time] {agent.name} is [action]."""

    return prompt


def create_plan_prompt(current_datetime: datetime.datetime, agent: Agent, detail_level: str = "daily"):
    if detail_level == "daily":
        return f"""Name: {agent.name} (age: {agent.age})
            {agent.cached_agent_summary}
            The following was {agent.name}'s schedule yesterday:
            {agent.biography_data['daily_routine']}
            Please outline a plan for {agent.name}'s day, in broad strokes.
            """
    if detail_level == "hourly":
        return f"""Name: {agent.name} (age: {agent.age})
            {agent.cached_agent_summary}
            \n{agent.name}'s plan for the day is to: \n
            {agent.cached_daily_plan}\n
            Please break down {agent.name}'s plan into hourly increments. Make sure to fill every hour slot, even if it's the same activity. Use the following format:
            8:00am - wake up
            9:00am - eat breakfast
            10:00am - go to work
            11:00am - work
            12:00pm - work
            1:00pm - have lunch
            """
    if "increment" in detail_level:
        return f"""Name: {agent.name} (age: {agent.age})
            {agent.cached_agent_summary}
            \nThis is {agent.name}'s plan for the day:\n
            {agent.cached_hourly_plan}
            \nBased on {agent.name}'s plan for this hour and given it is {hour_formatter(agent.current_datetime)}, please take your best guess to break down the next 60 minutes, and only the next 60 minutes. The plan should be listed in {TIME_INCREMENT} minute increments, starting from {hour_formatter(agent.current_datetime) }. Use the following format:
            8:00am - wake up
            8:05am - brush teeth/shower
            8:10am - brush teeth/shower
            8:15am - have breakfast
            8:20am - have breakfast
            8:25am - have breakfast
            8:30am - clean up breakfast
            8:35am - walk to work
            """


def update_plan_prompt(
    current_datetime: datetime.datetime, agent: Agent, detail_level:str = "hourly", relevant_memory_context:str = None
):
    if detail_level == "hourly":
        return f"""Name: {agent.name} (age: {agent.age})
            {agent.cached_agent_summary}
            \n{agent.name}'s original plan for the day was to: \n
            {agent.cached_hourly_plan}\n
            \nHowever, they recently had this observation:\n
            {relevant_memory_context}\n
            Please update {agent.name}'s plan in hourly increments, based on this observation. Make sure to fill every hour slot, even if you repeat activities. Use the following format:
            8:00am - wake up
            9:00am - eat breakfast
            10:00am - go to work
            11:00am - work
            12:00pm - work
            1:00pm - have lunch
            """
    if "increment" in detail_level:
        return f"""Name: {agent.name} (age: {agent.age})
            {agent.cached_agent_summary}
            \nThis was {agent.name}'s updated hourly plan for the day:\n
            {agent.cached_hourly_plan}
            \nBased on {agent.name}'s plan for this hour and given it is {hour_formatter(agent.current_datetime)}, please take your best guess to break down the next 60 minutes, and only the next 60 minutes. The plan should be listed in {TIME_INCREMENT} minute increments, starting from {hour_formatter(agent.current_datetime) }. Use the following format:
            8:00am - wake up
            8:05am - brush teeth/shower
            8:10am - brush teeth/shower
            8:15am - have breakfast
            8:20am - have breakfast
            8:25am - have breakfast
            8:30am - clean up breakfast
            8:35am - walk to work
            """


def should_replan_prompt(agent: Agent, agent_summary:str, relevant_memory_context:str):
    return f"""{agent_summary}.
        {agent.name} had this plan for the next hour: \n{agent.cached_increment_plan} \n
        \nThis is a recent observation for {agent.name}:\n
        {relevant_memory_context}\n
        Given this recent observation, is it likely {agent.name} would react to the observation? Limit yourself to a yes or no, nothing else. And if so, what would be an appropriate reaction?"""


# AM prompts, merge later.

def importance_prompt(description: str) -> str:
    template = '''
    On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory. Do not ask for more information, only respond with an integer score and nothing else, including no other punctuation.
    Memory: {description}
    Rating: <fill in>
    '''
    prompt = template.format(
        description=description
    )
    return prompt

def reflection_salient_points_prompt(recent_memories: List) -> str:
    template = '''
    {recent_memories}
    Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements?
    '''
    prompt = template.format(
        recent_memories=recent_memories
    )
    return prompt

def reflection_generation_prompt(agent_name: str, statements: List) -> str:
    template = '''
    Statements about {agent_name}
    {statements}
    What 5 high-level insights can you infer from the above statements? (example format: insight (because of 1, 5, 3))
    '''
    prompt = template.format(
        agent_name=agent_name,
        statements=statements
    )
    return prompt

def initial_plan_prompt(agent_name: str, age: int, agent_summary_description: str) -> str:
    template = '''
    Name: {agent_name} (age: {age})
    {agent_summary_description}
    Outline {agent_name}'s plan for the full day, starting at 12:00AM, with each plan having a duration of exactly 60 minutes, no more and no less. The start times should be at the top of the hour (for example 8:00 or 9:00, not 8:30 or 9:30). All 24 hours of the day should be covered, do not skip any hours. If the agent is sleeping for multiple hours, repeat the sleep task for all the hours the agent is sleeping. Do not include any information other than the plan in your response. Produce a plan faithfully, do not ask for more detail, do not ask for more information. Use the following JSON format to produce the schedule, but replace the content of the JSON as you see fit, do not be restricted by the example schedule. Only return JSON in your response, no other text or markdown formatting:
    {{
    "schedule":
    [
        {{
        "start_time": "6:00AM",
        "duration_minutes": 60,
        "description": "sleep"
        }},
        {{
        "start_time": "7:00AM",
        "duration_minutes": 60,
        "description": "sleep"
        }},
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
    prompt = template.format(
        agent_name=agent_name,
        age=age,
        agent_summary_description=agent_summary_description
    )
    return prompt

def plan_day_prompt(agent_name: str, age: int, agent_summary_description: str, yesterday_schedule: Dict) -> str:
    template = '''
    Name: {agent_name} (age: {age})
    {agent_summary_description}
    The following was {agent_name}'s schedule yesterday:
    {yesterday_schedule}
    Outline {agent_name}'s plan for the full day, starting at 12:00AM, with each plan having a duration of exactly 60 minutes, no more and no less. The start times should be at the top of the hour (for example 8:00 or 9:00, not 8:30 or 9:30). All 24 hours of the day should be covered, do not skip any hours. If the agent is sleeping for multiple hours, repeat the sleep task for all the hours the agent is sleeping. Do not include any information other than the plan in your response. Produce a plan faithfully, do not ask for more detail, do not ask for more information. Use the following JSON format to produce the schedule, but replace the content of the JSON as you see fit, do not be restricted by the example schedule. Only return JSON in your response, no other text or markdown formatting:
    {{
    "schedule":
    [
        {{
        "start_time": "6:00AM",
        "duration_minutes": 60,
        "description": "sleep"
        }},
        {{
        "start_time": "7:00AM",
        "duration_minutes": 60,
        "description": "sleep"
        }},
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
    prompt = template.format(
        agent_name=agent_name,
        age=age,
        agent_summary_description=agent_summary_description,
        yesterday_schedule=yesterday_schedule
    )
    return prompt

def plan_hour_prompt(agent_name: str, age: int, agent_summary_description: str, block_schedule: Dict):
    template = '''
    Name: {agent_name} (age: {age})
    {agent_summary_description}
    The following was {agent_name}'s schedule for the next one hour.
    {block_schedule}
    Detail {agent_name}'s plan for the whole hour, in exactly 6 tasks, each with a duration of 10 minutes. Only provide a schedule for the hour specified, do not plan past the end of the hour. Only plan six tasks and make all of them 10 minutes duration. Do not include any information other than the plan in your response. Produce a plan faithfully, do not ask for more detail, do not ask for more information. Use the following JSON format to produce the schedule, but replace the content of the JSON as you see fit, do not be restricted by the example schedule. Only return JSON in your response, no other text or markdown formatting:
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
    prompt = template.format(
        agent_name=agent_name,
        age=age,
        agent_summary_description=agent_summary_description,
        block_schedule=block_schedule
    )
    return prompt

def plan_reaction_prompt(agent_name: str, agent_summary_description: str, datetime: datetime.datetime, current_activity: str, observation: str, relevant_context: str):
    template = '''
    {agent_summary_description}
    It is {datetime}.
    {agent_name}'s current activity: {current_activity}.
    Observation: {observation}
    Summary of relevant context from {agent_name}'s memory:
    {relevant_context}
    Should {agent_name} react to the observation? If No, just respond "No" with no other words. If Yes, describe what the appropriate reaction would be very briefly. Example responses if Yes include:
    "Start a conversation with <person>"
    "Take a shower"
    "Sit down at the table"
    '''
    prompt = template.format(
        agent_name=agent_name,
        agent_summary_description=agent_summary_description,
        datetime=datetime,
        current_activity=current_activity,
        observation=observation,
        relevant_context=relevant_context
    )
    return prompt

def dialogue_initial_prompt(agent_name: str, agent_summary_description: str, datetime: datetime.datetime, current_action: str, observation: str, relevant_context: str, plan_reaction_response: str, other_agent_name: str):
    template = '''
    {agent_summary_description}
    It is {datetime}.
    {agent_name}'s status: {agent_name} is currently {current_action}.
    Observation: {observation}
    Summary of relevant context from {agent_name}'s memory:
    {relevant_context}
    {plan_reaction_response}
    What should {agent_name} say to {other_agent_name}?
    '''
    prompt = template.format(
        agent_name=agent_name,
        agent_summary_description=agent_summary_description,
        datetime=datetime,
        current_action=current_action,
        observation=observation,
        relevant_context=relevant_context,
        plan_reaction_response=plan_reaction_response,
        other_agent_name=other_agent_name
    )
    return prompt

def dialogue_continuation_prompt(agent_name: str, agent_summary_description: str, datetime: datetime.datetime, current_action: str, observation: str, relevant_context: str, dialogue_history: str, other_agent_name: str):
    template = '''
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
    prompt = template.format(
        agent_name=agent_name,
        agent_summary_description=agent_summary_description,
        datetime=datetime,
        current_action=current_action,
        observation=observation,
        relevant_context=relevant_context,
        dialogue_history=dialogue_history,
        other_agent_name=other_agent_name
    )
    return prompt

def action_location_prompt():
    template = '''
    {agent_summary_description}
    {agent_name} is currently in {current_location} that has {current_location_description}.
    {agent_name} knows about the following Known Locations: {known_locations}
    {agent_name} is planning to {next_action}.
    From the list of Known Locations provided, choose the location that makes the most sense for {agent_name}'s next activity. Prefer to stay in the current area if the activity can be done there.
    Do not include any information other than the selected location from the list in your response. Only include the JSON, do not include any other text or formatting other than the JSON before or after the JSON. Here is the JSON template you should follow when providing your response
    {{
    "location": "Bathroom in Truman's House"
    }}
    '''
    return prompt

def state_change_prompt():
    template = '''
    {agent_name} is currently performing the following action: {current_action} on the following object: {current_object}.
    What should we update the state of the object to? (e.g., if the object is a door, the state could be open or closed. If the object is a stove and the action is cooking, the state could be on or off.)
    '''
    return prompt

def reflection_questions_prompt():
    template = '''
    {recent_memories}
    Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements? Structure your reponse according to the JSON below. Do not include any information other than the 3 questions in your response. Only include the JSON, do not include any other text or formatting other than the JSON before or after the JSON. Here is the JSON template you should follow when providing your response:
    {{
    "questions": [
        "What is the name of the person who is the subject of the statement?",
        "What is the name of the person who is the object of the statement?",
        "What is the name of the person who is the indirect object of the statement?"
    }}
    '''
    return prompt

def reflection_prompt():
    template = '''
    Statements about {agent_name}:
    {statements}
    What 5 high-level insights can you infer from the above statements? Structure your reponse according to the JSON below. Do not include any information other than the 3 questions in your response. Only include the JSON, do not include any other text or formatting other than the JSON before or after the JSON. Here is the JSON template you should follow when providing your response:
    {{
    "insights": [
        {{
        "insight": "The insight you inferred",
        "evidence": ["Statement 1", "Statement 2", "Statement 3"]
        }}
    ]
    }}
    '''
    return prompt

