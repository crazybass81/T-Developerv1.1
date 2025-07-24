import React, { useState, useEffect } from 'react';

interface Agent {
  name: string;
  type: string;
}

function App() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [systemStatus, setSystemStatus] = useState('Loading...');

  useEffect(() => {
    fetchSystemData();
  }, []);

  const fetchSystemData = async () => {
    try {
      const response = await fetch('http://localhost:8000/agents');
      if (response.ok) {
        const data = await response.json();
        setAgents(data.agents || []);
        setSystemStatus('Online');
      }
    } catch (error) {
      setSystemStatus('Offline');
    }
  };

  const orchestrateGoal = async () => {
    const goal = prompt('Enter your goal:');
    if (!goal) return;

    try {
      const response = await fetch('http://localhost:8000/orchestrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal })
      });
      
      if (response.ok) {
        alert('Orchestration completed!');
      }
    } catch (error) {
      alert('Orchestration failed');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>T-Developer Dashboard</h1>
      <p>Status: <strong>{systemStatus}</strong></p>
      
      <h2>Active Agents ({agents.length})</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '10px' }}>
        {agents.map((agent, index) => (
          <div key={index} style={{ border: '1px solid #ccc', padding: '10px', borderRadius: '5px' }}>
            <h3>{agent.name}</h3>
            <p>Type: {agent.type}</p>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '20px' }}>
        <button onClick={orchestrateGoal} style={{ padding: '10px 20px', fontSize: '16px' }}>
          Orchestrate Goal
        </button>
      </div>
    </div>
  );
}

export default App;