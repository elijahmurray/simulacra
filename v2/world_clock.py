import datetime
import Agent

TIME_INCREMENT=5# in_minutes

class WorldClock:
    def __init__(self):
        self.start_datetime = self.determine_start_time
        self.current_datetime = self.start_datetime

    def determine_start_time():
        return datetime.now
    
    def advance_time(self):
        agents = Agent.all
        agents.each(agent) {agent.step_checker}
        self.current_datetime += TIME_INCREMENT




# world_clock: #not persisted
#   step:
#     agents_output_current_action_statement (natural language)