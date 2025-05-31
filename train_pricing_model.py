import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

# Custom Pricing Environment
class PricingEnv(gym.Env):
    def __init__(self):
        super(PricingEnv, self).__init__()
        # Observation: [demand, sentiment, competitor_price]
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(3,), dtype=np.float32)
        # Action: Price adjustment (continuous)
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)
        self.state = None
        self.step_count = 0
        self.max_steps = 1000

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Initialize state: [demand, sentiment, competitor_price]
        self.state = np.array([1.0, 0.0, 0.5], dtype=np.float32)
        self.step_count = 0
        return self.state, {}

    def step(self, action):
        # Simulate environment dynamics
        demand, sentiment, competitor_price = self.state
        price = action[0] * 0.1 + 0.1  # Scale action to price
        # Simple reward: Higher demand increases reward, deviation from competitor price reduces reward
        reward = demand * price - abs(price - competitor_price)
        # Update state (simulate demand increasing with lower price)
        demand += max(0, 1.0 - price)
        sentiment = min(1.0, sentiment + 0.01)
        competitor_price = max(0.1, competitor_price + np.random.uniform(-0.05, 0.05))
        self.state = np.array([demand, sentiment, competitor_price], dtype=np.float32)
        self.step_count += 1
        done = self.step_count >= self.max_steps
        return self.state, reward, done, False, {}

    def render(self):
        pass

# Verify environment
env = PricingEnv()
check_env(env)

# Create PPO model with a smaller policy network
model = PPO(
    "MlpPolicy",
    env,
    policy_kwargs={"net_arch": [32, 32]},  # Smaller network
    learning_rate=0.001,
    batch_size=64,
    n_epochs=2,
    gamma=0.9,
    gae_lambda=0.95,
    clip_range=0.2,
    vf_coef=0.5,
    ent_coef=0.01,
    verbose=1
)

# Train for 10,000 timesteps
model.learn(total_timesteps=10000)

# Save the model to the new location
model.save("models/ppo_model")