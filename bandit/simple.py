#test git checkin capability
#test git checkin capability AGAIN

# configuration of actions
import numpy as np
import matplotlib.pyplot as plt
import time
import component_simple as rl
import config


ts = time.time()

# basic simulation configuration
np.random.seed(config.initial_seed)
optimal_since = []

number_actions = config.number_actions
number_try = config.number_try
prob_exploration = config.prob_exploration    

#binary reward
env = rl.Environment(number_actions)
#reward_est = rl.Estimator(number_actions)
policy = rl.Policy(number_actions, prob_exploration)

#sequential events
for t in np.arange(number_try):
    # select an action    
    action, explore = policy.get_action()
    #print(action)
    
    # observe reward
    reward = env.get_reward(action)

    # learning
    policy.learn(action, explore, reward)    
      
#for s in reward_est.history():
#    print("step=%d action=%d reward estimate=%.3f"%s)
optimal_since.append(policy.get_learner().optimal_since())
    
final_estimate = policy.get_learner().get()

for a in sorted(range(len(env.reward())), key=lambda x: env.reward()[x], reverse=True):
    print(a,policy.get_action_frequency(a), env.reward()[a])        
print("optimal policy = %d"%policy.get_learner().optimal_action())
print("the policy is optimal since %d"%policy.get_learner().optimal_since())
for a in range(number_actions):
    x,y = zip(*[(s[0],s[2]) for s in policy.get_learner().history() if s[1] == a])
    #y = [s[2] for s in reward_est.history() if s[1] == a]
    plt.plot(x, y, '-', label=str(a))
plt.legend(loc='best')
plt.show()    

print("programming running time = %.3f"%(time.time()-ts))
