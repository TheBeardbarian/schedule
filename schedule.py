from functions import *

tuesday = Schedule(tuesday_totes_schedule, tuesday_test_case, count_list, agent_list)

tuesday.fill_schedule()

for agent in agent_list:
    print("{:.0f} o'clock agents: {:.0f}".format(agent.start, count_list[agent_list.index(agent)]))
#
# print(peak_hours)
