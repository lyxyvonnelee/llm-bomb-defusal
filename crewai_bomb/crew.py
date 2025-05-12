from ml_collections import ConfigDict
from crewai import Agent, Crew, Task, LLM, Process
from crewai_bomb.tools import DefuserTool, ExpertTool

model_config = ConfigDict()
model_config.extra = 'allow'
llm = LLM(
    model='ollama/qwen2.5',
    model_config=model_config
)

defuser_tool = DefuserTool()
expert_tool  = ExpertTool()

defuser_agent = Agent(
    name='DefuserAgent',
    role='Defuser',
    goal='Describe module state, ask Expert, then act until disarmed or exploded.',
    backstory='You see the bomb’s modules but cannot view the manual.',
    llm=llm,
    tools=[defuser_tool]
)

expert_agent = Agent(
    name='ExpertAgent',
    role='Expert',
    goal='Provide precise instructions from the manual to disarm modules.',
    backstory='You have the manual but cannot see the bomb’s display.',
    llm=llm,
    tools=[expert_tool]
)

if __name__ == '__main__':
    # Game loop: always build each Crew with both agents + the single Task
    while True:
        # a) Defuser asks for bomb state
        task_state = Task(
            agent=defuser_agent,     
            tool='defuser_action',
            input='state',
            description='Retrieve current bomb module state',
            expected_output='Text describing the module state'
        )
        crew_state = Crew(
            agents=[defuser_agent, expert_agent],
            tasks=[task_state],
            process=Process.sequential,
            verbose=False
        )
        state = crew_state.kickoff().raw
        print(f"\n[Defuser received state:]\n{state}")
        if 'BOOM!' in state or 'DISARMED' in state:
            break

        # b) Expert provides instructions based on that state
        task_manual = Task(
            agent=expert_agent,     
            tool='expert_manual',
            input=state,
            description='Get manual instructions for this state',
            expected_output='Manual excerpt text'
        )
        crew_manual = Crew(
            agents=[defuser_agent, expert_agent],
            tasks=[task_manual],
            process=Process.sequential,
            verbose=False
        )
        instruction = crew_manual.kickoff().raw
        print(f"\n[Expert suggests:]\n{instruction}")

        # c) Defuser executes the Expert’s instruction
        task_action = Task(
            agent=defuser_agent,     
            tool='defuser_action',
            input=instruction,
            description='Execute the expert instruction',
            expected_output='Result of the action'
        )
        crew_action = Crew(
            agents=[defuser_agent, expert_agent],
            tasks=[task_action],
            process=Process.sequential,
            verbose=False
        )
        result = crew_action.kickoff().raw
        print(f"\n[Defuser executes:]\n{result}")
        if 'BOOM!' in result or 'DISARMED' in result:
            break