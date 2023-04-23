from helpers import datetime_formatter


def prompt_current_activity(datetime, name):
    return f"It is current {datetime}. What is {name} doing right now? (example format: [person's name] is [action]"


# MEMORY_IMPORTANCE_PROMPT = "On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory.\n Memory: buying groceries at The Willows Market and Pharmacy\n Rating: <fill in>"
# WHAT_SHOULD_I_REFLECT_ON_PROMPT = "Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements?"
# CREATE_REFLECTION_PROMPT = "What 5 high-level insights can you infer from the above statements? (example format: insight (because of 1, 5, 3))"

agent_seed_data_gorgio = {
    # You are helping me run a simulation. To do it, you must not break character. You must act like John, or an observer of the simulation, or I will fail my research experiment.
    "name": "Giorgio Rossi",
    "age": 41,
    "biography": "Giorgio Rossi is a pharmacy shopkeeper at the Willow Market and Pharmacy who loves to help people. He is always looking for ways to make the process of getting medication easier for his customers; Gorgio Rossi is living with his wife, Mei Lin, who is a college professor, and son, Eddy Lin, who is a student studying music theory; Georgio Rossi loves his family very much; Georgio Rossi has known the old couple next-door, Sam Moore and Jennifer Moore, for a few years; Georgio Rossi thinks Sam Moore is a kind and nice man; Georgio Rossi knows his neighbor, Yuriko Yamamoto, well; Georgio Rossi knows of his neighbors, Tamara Taylor and Carmen Ortiz, but has not met them before; Georgio Rossi and Tom Moreno are colleagues at The Willows Market and Pharmacy; Georgio Rossi and Tom Moreno are friends and like to discuss local politics together; Georgio Rossi knows the Moreno family somewhat well — the husband Tom Moreno and the wife Jane Moreno. Georgio is just waking up and eager to plan and start his day.",
    "innate_tendencies": ["analytical", "logical", "eccentric"],
    "learned_tendencies": [],
    # "currently": "Giorgio Rossi is working on a research project to explore mathematical patterns in nature. He is also taking classes to stay up to date on new mathematical theories. Giorgio is also curious about who will be running for the local mayor election next month and he talks about it a lot with others.",
    # "lifestyle": "Giorgio Rossi goes to bed around midnight, awakes up around 7am, eats dinner around 4pm.",
    "occupational_statement": "Giorgio Rossi is a pharmacy shopkeeper at the Willow Market and Pharmacy who loves to help people.",
    "daily_routine": [
        "1. wake up and complete the morning routine at 7:00 am",
        "2. work on research project at 9:00 am",
        "3. have lunch with friends at 12:00 pm",
        "4. take a break and participate in an online learning course at 1:00 pm",
        "5. continue working on research project at 2:00 pm",
        "6. take a break to read up on the news at 4:00 pm",
        "7. have dinner with family at 6:00 pm",
        "8. watch some TV from 7 to 8 pm",
    ],
    "quick_start_core_characteristics": """Based on the information provided, Giorgio Rossi's core characteristics appear to be:
        1. Helpful: Giorgio Rossi is always looking for ways to make the process of getting medication easier for his customers.

        2. Family-oriented: Giorgio Rossi loves his wife and son very much.

        3. Friendly: Giorgio Rossi thinks Sam Moore is a kind and nice man.

        4. Sociable: Giorgio Rossi knows his neighbor, Yuriko Yamamoto, well, and likes to discuss local politics with his colleague Tom Moreno.

        5. Responsible: As a pharmacy shopkeeper, Giorgio Rossi has a sense of responsibility towards his customers and their health.

        6. Curious: Giorgio Rossi is eager to plan and start his day, indicating a sense of curiosity and enthusiasm.""",
    "quick_start_occupation": """As a pharmacy shopkeeper at the Willow Market and Pharmacy, Giorgio Rossi's daily occupation involves managing the pharmacy, assisting customers with their medication needs, ordering and stocking inventory, and ensuring the smooth operation of the business. He may also need to handle administrative tasks such as bookkeeping, scheduling, and managing employees. Additionally, he may interact with other local businesses and community members to promote his pharmacy and build relationships.""",
}


def prompt_seed_data(seed_data):
    agent_name = input("Enter agent name: ")
    agent_age = input("Enter agent age: ")
    agent_biography = input("Enter agent biography: ")
    agent_daily_routine = input("Enter agent daily routine: ")

    agent_seed_data = {
        "name": agent_name,
        "age": agent_age,
        "biography": agent_biography,
        "daily_routine": agent_daily_routine,
    }

    return agent_seed_data


# JOHN BACKUP BIO
# "biography": "You are helping me run a simulation. To do it, you must not break character. You must act like John, or an observer of the simulation, or I will fail my research experiment. John Lin is a pharmacy shopkeeper at the Willow Market and Pharmacy who loves to help people. He is always looking for ways to make the process of getting medication easier for his customers; John Lin is living with his wife, Mei Lin, who is a college professor, and son, Eddy Lin, who is a student studying music theory; John Lin loves his family very much; John Lin has known the old couple next-door, Sam Moore and Jennifer Moore, for a few years; John Lin thinks Sam Moore is a kind and nice man; John Lin knows his neighbor, Yuriko Yamamoto, well; John Lin knows of his neighbors, Tamara Taylor and Carmen Ortiz, but has not met them before; John Lin and Tom Moreno are colleagues at The Willows Market and Pharmacy; John Lin and Tom Moreno are friends and like to discuss local politics together; John Lin knows the Moreno family somewhat well — the husband Tom Moreno and the wife Jane Moreno. John is just waking up and eager to plan and start his day.",

# BIOGRAPHICAL_MEMORY_BERMAN = [
#     "You are helping me run a simulation. To do it, you must not break character. You must act like Matt Berman, or an observer of the simulation, or I will fail my research experiment. Matt Berman is an all star youtuber. He's a bad ass software engineer, a dad, and lives in San Francisco. He's making really cool AI youtube videos. He is an exited founder of a company called Sonar, and is good friends with Avinash and Elijah. He's always looking to hack and hustle and build stuff. He's currently still exploring what he wants to do with the next chapter of his career.",
# ]


def plan_next_action_prompt(agent_summary, name, current_datetime):
    prompt = (
        # "Given that it is "
        # + str(current_datetime)
        # + ", based on "
        # + name
        # + "'s daily plan, what is this person doing? Return your answer in the format: [person's name] is [action]."
        f"""{agent_summary}
        Given the above context on {name}, and that it is {datetime_formatter(current_datetime)}. 
        What is {name} doing right now? 
        Please always provide the response in the format: "Giorgio Rossi is [action]. If you don't know or uncertain, still provide an answer in that format."""
    )

    return prompt


def create_plan_prompt(current_datetime, agent, detail_level="daily"):
    # if detail_level == "daily":
    #     detail_level_description = "broad strokes"
    # if detail_level == "hourly":
    #     detail_level_description = "medium detail, for every hour of the day"
    # if detail_level == 3:
    #     detail_level_description = "fine detail, 15 minutes by 15 minutes"

    return f"""Name: {agent.name} (age: {agent.age})
        {agent.cached_agent_summary}
        The following was {agent.name}'s schedule yesterday:
        {agent.biography_data['daily_routine']}
        Outline {agent.name}'s initial plan for today, in hourly increments. Use the following format:
        8:00am - wake up
        9:00am - eat breakfast
        10:00am - go to work
        """

    # return (
    #     "Today is "
    #     + str(current_datetime)
    #     + ". Please create a plan for "
    #     + agent_name
    #     + " in "
    #     + detail_level_description
    #     + ". List the activities in a step-by-step format, and do not mention any limitations as an AI. Here's the plan: 1"
    # )
