from helpers import datetime_formatter, hour_formatter
from config import TIME_INCREMENT


# MEMORY_IMPORTANCE_PROMPT = "On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory.\n Memory: buying groceries at The Willows Market and Pharmacy\n Rating: <fill in>"
# WHAT_SHOULD_I_REFLECT_ON_PROMPT = "Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements?"
# CREATE_REFLECTION_PROMPT = "What 5 high-level insights can you infer from the above statements? (example format: insight (because of 1, 5, 3))"


def current_action_prompt(agent_summary, agent, current_datetime):
    prompt = f"""{agent_summary}.\n
        {agent.name}'s current plan is: \n{agent.cached_increment_plan} \n
        \nGiven it is now {hour_formatter(agent.current_datetime) },
        provide a definitive statement with no explanation for what {agent.name} 
        is doing, in the format: "At [time] {agent.name} is [action]."""

    return prompt


def create_plan_prompt(current_datetime, agent, detail_level="daily"):
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
            {agent.cached_daily_plan}
            Please break down {agent.name}'s plan, in hourly increments. Make sure to fill every hour slot, even if it's the same activity. Use the following format:
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
            \nBased on {agent.name}'s plan for this hour and given it is {hour_formatter(agent.current_datetime)}, please take your best guess to break down the next 60 minutes only. The plan should be listed in {TIME_INCREMENT} minute increments, starting from {hour_formatter(agent.current_datetime) }. Use the following format:
            8:00am - wake up
            8:05am - brush teeth/shower
            8:10am - brush teeth/shower
            8:15am - have breakfast
            8:20am - have breakfast
            8:25am - have breakfast
            8:30am - clean up breakfast
            8:35am - walk to work
            """


def should_replan(agent, agent_summary, relevant_memory_context):
    return f"""{agent_summary}.
        {agent.name}'s plan for the next hour is: \n{agent.cached_increment_plan} \n
        \nSummary of relevant context from {agent.name}'s memory:\n
        {relevant_memory_context}\n
        Should {agent.name} react to the observation, and if so, what would be an appropriate reaction?"""
