# PROMPTS

SIM_CLOCK_INCREMENT = 10

IMPORTANCE_PROMPT = '''
On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory.
Memory: {memory}
Rating: <fill in>
'''

RETRIEVAL_WEIGHTS = {
  'importance': 0.5,
  'relevance': 0.5,
  'recency': 0.5,
}

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
Outline {agent_name}'s initial plan for the day, in hourly increments. Use the following format:
8:00am - wake up
9:00am - eat breakfast
10:00am - go to work
'''

PLAN_PROMPT_DAY = '''
Name: {agent_name} (age: {age})
{agent_summary_description}
The following was {agent_name}'s schedule yesterday:
{yesterday_schedule}
Outline {agent_name}'s initial plan for today, in hourly increments. Use the following format:
8:00am - wake up
9:00am - eat breakfast
10:00am - go to work
'''

PLAN_PROMPT_HOUR = '''
Name: {agent_name} (age: {age})
{agent_summary_description}
The following was {agent_name}'s schedule for one hour.
{hour_schedule}
Provide a detailed breakdown of tasks in the hour in increments as small as 5 minutes and as large as 15 minutes. Us the following format:
8:00am - wake up
8:05am - brush teeth
8:10am - make bed
8:15am - eat breakfast
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

