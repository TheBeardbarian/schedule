from agents import *

tuesday_totes_schedule = {0:2, 1:2, 2:1, 3:2, 4:2, 5:3, 6:5, 7:12, 8:23, 9:26, 10:26, 11:29, 12:26, 13:27, 14:26, 15:24, 16:18, 17:17, 18:14, 19:11, 20:9, 21:6, 22:4, 23:3}

tuesday_test_case = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0}

# Empty variables to keep count of how many agents are schedule for each shift
three_agent_count = 0
six_agent_count = 0
seven_agent_count = 0
eight_agent_count = 0
eight_thirty_agent_count = 0
nine_agent_count = 0
ten_agent_count = 0
eleven_agent_count = 0
twelve_agent_count = 0
fourteen_agent_count = 0
fifteen_agent_count = 0
eighteen_agent_count = 0
eighteen_thirty_agent_count = 0
count_list = [three_agent_count, six_agent_count, seven_agent_count, eight_agent_count, nine_agent_count, ten_agent_count,
            eleven_agent_count, twelve_agent_count, fourteen_agent_count, fifteen_agent_count, eighteen_agent_count]

agent_list = [three_agent, six_agent, seven_agent, eight_agent, nine_agent, ten_agent, eleven_agent, twelve_agent, fourteen_agent,
                    fifteen_agent, eighteen_agent]

peak_hours = list(range(7, 24))

class Schedule:

    def __init__(self, day_totes_schedule, day_test_case, count_list, agent_list):
        self.day_totes_schedule = day_totes_schedule
        self.day_test_case = day_test_case
        self.count_list = count_list
        self.agent_list = agent_list
        self.needs = []
        self.potential_fills = []

    def add_agent(self, agent_type):
        for hour, count in agent_type.labor_hours.items():
            self.day_test_case[hour] += count
        self.count_list[self.agent_list.index(agent_type)] += 1

    def calculate_needs(self):
        for agent in self.agent_list:
            agent.match = 0

        self.needs = []
        for h, c in self.day_test_case.items():
            if self.day_test_case[h] < self.day_totes_schedule[h]:
                self.needs.append(h)

        self.potential_fills = []
        for h in self.needs:
            for agent in self.agent_list:
                if h in agent.labor_hours and agent not in self.potential_fills:
                    self.potential_fills.append(agent)
                    agent.match += agent.labor_hours[h]
                elif h in agent.labor_hours and agent in self.potential_fills:
                    agent.match += agent.labor_hours[h]
                else:
                    continue
        self.potential_fills.sort(key=lambda x: x.match, reverse=True)

    def fill_schedule(self):
        for h, c in self.day_test_case.items():
            while self.day_test_case[h] < self.day_totes_schedule[h]:
                for agent_start in self.agent_list:
                    # if (day_test_case[agent_start.counter] <= day_totes_schedule[agent_start.counter]) and (day_test_case[agent_start.counter + 1] <= day_totes_schedule[agent_start.counter + 1]) and (day_test_case[agent_start.counter + 2] <= day_totes_schedule[agent_start.counter + 2]):
                    if (self.day_test_case[agent_start.counter] <= self.day_totes_schedule[agent_start.counter]):
                        self.add_agent(agent_start)
                    else:
                        break
                break

            while self.day_test_case[h] < self.day_totes_schedule[h]:
                self.calculate_needs()
                if len(self.potential_fills) == 1:
                    self.add_agent(self.potential_fills[0])
                else:
                    print(self.potential_fills[0])
                    while self.potential_fills[0].start not in peak_hours:
                        if self.day_test_case[self.potential_fills[0].start] > self.day_totes_schedule[self.potential_fills[0].start]:
                            self.potential_fills.pop()
                        else:
                            self.add_agent(self.potential_fills[0])
                    self.add_agent(self.potential_fills[0])

        # for h, c in day_test_case.items():
        #     while day_test_case[h] < day_totes_schedule[h]:
        #         potential_fills = calculate_needs(day_test_case, day_totes_schedule)
        #         add_agent(potential_fills[0], day_test_case)

        # for h, c in self.day_test_case.items():


        for h, c in self.day_test_case.items():
            print("{:.0f} | Forecasted: {:.2f}, Scheduled: {:.2f}".format(h, self.day_totes_schedule[h], self.day_test_case[h]))
