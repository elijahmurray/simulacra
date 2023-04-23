from helpers import datetime_formatter


def prompt_current_activity(datetime, name):
    return f"It is current {datetime}. What is {name} doing right now? (example format: [person's name] is [action]"


# MEMORY_IMPORTANCE_PROMPT = "On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory.\n Memory: buying groceries at The Willows Market and Pharmacy\n Rating: <fill in>"
# WHAT_SHOULD_I_REFLECT_ON_PROMPT = "Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements?"
# CREATE_REFLECTION_PROMPT = "What 5 high-level insights can you infer from the above statements? (example format: insight (because of 1, 5, 3))"


def plan_next_action_prompt(agent_summary, agent, current_datetime):
    prompt = f"""{agent_summary}.
        {agent.name}'s plan for the day was: \n{agent.daily_plan} \n and the plan for the next hour was to \n{agent.next_hour_plan}.
        \nGiven the above context on {agent.name}, and that it is {datetime_formatter(current_datetime)}. 
        What is {agent.name} doing right now? 
        Please always provide the response in the format: "Giorgio Rossi is [action]. If you don't know or uncertain, still provide an answer in that format."""

    return prompt


def create_plan_prompt(current_datetime, agent, detail_level="daily"):
    if detail_level == "daily":
        return f"""Name: {agent.name} (age: {agent.age})
            {agent.cached_agent_summary}
            The following was {agent.name}'s schedule yesterday:
            {agent.biography_data['daily_routine']}
            Outline {agent.name}'s initial plan for today, in hourly increments. Use the following format:
            8:00am - wake up
            9:00am - eat breakfast
            10:00am - go to work
            """
    if "hourly" in detail_level:
        return f"""Name: {agent.name} (age: {agent.age})
            {agent.cached_agent_summary}
            The following was {agent.name}'s plan for the day:
            {agent.daily_plan}
            Based on the daily plan, break down {agent.name}'s daily plan but only for the next 60 minutes starting at {agent.current_datetime }, into four, 15 minute increments. Use the following format:
            8:15am - wake up
            8:30am - brush teeth/shower
            8:45am - brush teeth/shower
            9:15am - have breakfast
            9:30am - walk to work
            """
