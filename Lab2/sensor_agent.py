import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio
from environment import get_disaster_status


class SensorAgent(Agent):
    class MonitorBehaviour(CyclicBehaviour):
        async def run(self):
            severity = get_disaster_status()
            print(f"[SensorAgent] Disaster severity: {severity}")

            with open("event_log.txt", "a") as f:
                f.write(f"Detected severity: {severity}\n")

            await asyncio.sleep(5)

    async def setup(self):
        print("SensorAgent started...")
        self.add_behaviour(self.MonitorBehaviour())


async def main():
    agent = SensorAgent("sensor@localhost", "1234567890")
    await agent.start()
    await asyncio.sleep(30)
    await agent.stop()

if __name__ == "__main__":
    spade.run(main())
