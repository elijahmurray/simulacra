from __future__ import annotations
from agent.agent import Agent
from utils.formatting_utils import hour_formatter
from config import TIME_INCREMENT
import datetime


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
