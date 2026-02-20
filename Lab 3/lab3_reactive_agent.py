# lab3_reactive_agent.py
"""
LAB 3: Goals, Events, and Reactive Behavior
A RescueAgent that responds to disaster events using a Finite State Machine.
"""

import asyncio
import random
from datetime import datetime
from enum import Enum
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class AgentState(Enum):
    """
    Finite State Machine states for the RescueAgent.
    """
    IDLE = "IDLE"
    RESPONDING = "RESPONDING"
    RESCUING = "RESCUING"
    RETURNING = "RETURNING"


class DisasterEvent:
    """Represents a disaster event that needs response"""
    def __init__(self, location, disaster_type, severity):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.location = location
        self.disaster_type = disaster_type
        self.severity = severity
        self.id = f"EVENT-{random.randint(1000, 9999)}"


class RescueAgent(Agent):
    """
    An agent that responds to disaster events based on its current state.
    Uses a Finite State Machine (FSM) to manage behavior.
    """
    
    class RescueBehaviour(CyclicBehaviour):
        """
        This behavior runs continuously and implements the FSM logic.
        """
        
        async def on_start(self):
            """Initialize the agent's state and goals"""
            self.state = AgentState.IDLE
            self.current_event = None
            self.events_handled = 0
            self.goal = "Respond to disasters and save lives"
            
            print(f"RescueAgent initialized")
            print(f"Goal: {self.goal}")
            print(f"Initial State: {self.state.value}\n")
        
        async def run(self):
            """
            Main FSM logic - runs continuously.
            The agent transitions between states based on events.
            """
            
            # IDLE STATE: Waiting for disaster events
            if self.state == AgentState.IDLE:
                await self.handle_idle_state()
            
            # RESPONDING STATE: Moving to disaster location
            elif self.state == AgentState.RESPONDING:
                await self.handle_responding_state()
            
            # RESCUING STATE: Performing rescue operations
            elif self.state == AgentState.RESCUING:
                await self.handle_rescuing_state()
            
            # RETURNING STATE: Going back to base
            elif self.state == AgentState.RETURNING:
                await self.handle_returning_state()
            
            # Wait a bit before next cycle
            await asyncio.sleep(2)
        
        async def handle_idle_state(self):
            """Handle behavior when agent is IDLE"""
            print(f"[{self.state.value}] Monitoring for disaster events...")
            
            # Simulate receiving a disaster event (50% chance)
            if random.random() < 0.5:
                # Create a new disaster event
                locations = ["North Zone", "South Zone", "East Zone", "West Zone"]
                disaster_types = ["Flood", "Fire", "Earthquake"]
                
                self.current_event = DisasterEvent(
                    location=random.choice(locations),
                    disaster_type=random.choice(disaster_types),
                    severity=random.randint(1, 10)
                )
                
                print(f"\n🚨 NEW EVENT DETECTED: {self.current_event.id}")
                print(f"   Type: {self.current_event.disaster_type}")
                print(f"   Location: {self.current_event.location}")
                print(f"   Severity: {self.current_event.severity}/10")
                
                # Transition to RESPONDING state
                self.transition_to(AgentState.RESPONDING)
        
        async def handle_responding_state(self):
            """Handle behavior when agent is RESPONDING to an event"""
            print(f"[{self.state.value}] En route to {self.current_event.location}...")
            
            # Simulate travel time
            await asyncio.sleep(1)
            
            print(f"[{self.state.value}] Arrived at {self.current_event.location}")
            
            # Transition to RESCUING state
            self.transition_to(AgentState.RESCUING)
        
        async def handle_rescuing_state(self):
            """Handle behavior when agent is RESCUING"""
            print(f"[{self.state.value}] Performing rescue operations...")
            print(f"   Handling {self.current_event.disaster_type} disaster")
            print(f"   Severity level: {self.current_event.severity}/10")
            
            # Simulate rescue operations (time varies with severity)
            rescue_time = self.current_event.severity * 0.5
            await asyncio.sleep(rescue_time)
            
            print(f"[{self.state.value}] ✓ Rescue operation completed!")
            self.events_handled += 1
            
            # Transition to RETURNING state
            self.transition_to(AgentState.RETURNING)
        
        async def handle_returning_state(self):
            """Handle behavior when agent is RETURNING to base"""
            print(f"[{self.state.value}] Returning to base...")
            
            # Simulate return travel
            await asyncio.sleep(1)
            
            print(f"[{self.state.value}] Returned to base")
            print(f"   Events handled so far: {self.events_handled}\n")
            
            # Clear current event
            self.current_event = None
            
            # Transition back to IDLE state
            self.transition_to(AgentState.IDLE)
        
        def transition_to(self, new_state):
            """Transition to a new state"""
            print(f">>> STATE TRANSITION: {self.state.value} → {new_state.value}\n")
            self.state = new_state
    
    async def setup(self):
        """Initialize the agent"""
        print(f"RescueAgent {self.jid} is starting...\n")
        
        # Add the rescue behavior
        rescue_behaviour = self.RescueBehaviour()
        self.add_behaviour(rescue_behaviour)


async def main():
    """Main function to run the rescue agent"""
    
    # Configure your XMPP credentials
    AGENT_JID = "rescueagent@localhost"
    AGENT_PASSWORD = "P@ssW0rd"
    
    print("=" * 70)
    print("LAB 3: Reactive Agent with Finite State Machine")
    print("=" * 70)
    print()
    
    # Create and start the rescue agent
    agent = RescueAgent(AGENT_JID, AGENT_PASSWORD)
    await agent.start()
    
    print("Agent is running... (will run for 30 seconds)")
    print("Watch the state transitions!\n")
    print("-" * 70)
    
    # Let it run for 30 seconds
    await asyncio.sleep(30)
    
    # Stop the agent
    await agent.stop()
    
    print("-" * 70)
    print("\nLab 3 Complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())