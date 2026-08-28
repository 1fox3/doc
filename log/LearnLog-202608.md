# 2026年8月份找工作期间的学习记录

## 2026-08-28
### English
 - Duolingo Phase 6: 55 - 56 two units
### Algorithm
- 
### Knowledge Base
#### Milvus
- [Milvus Doc](https://milvus.io/docs/zh/overview.md)
  - [SKILL](https://github.com/zilliztech/milvus-skill)
  - Install Milvus
  - Overview
  - Architecture
  - Concepts
- [Agent 10连问](https://www.youtube.com/watch?v=x-s1Dbp4BE4)
- Java Guide
  - 
### Interview
- 

## 2026-08-27
### English
 - Duolingo Phase 6: 53 - 54 two units
### Algorithm
- [69. Sqrt(x)（简单）](https://leetcode.cn/problems/sqrtx/)
- [415. Add Strings（简单）](https://leetcode.cn/problems/add-strings/)
- [43. Add Two Numbers（中等）](https://leetcode.cn/problems/add-two-numbers/)
- [面试题 01.06. 字符串压缩](https://leetcode.cn/problems/compress-string-lcci/)
- [3. Longest Substring Without Repeating Characters（中等）](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)
### Knowledge Base
#### Milvus
- [bilibili video: Milvus](https://www.bilibili.com/video/BV1HZgV6TEen?spm_id_from=333.788.videopod.episodes&vd_source=b29fb44a83d8060aa11af87c5b052812):
  - Milvus 3.0 新特性
- [Milvus Doc](https://milvus.io/docs/zh/overview.md)
  - [SKILL](https://github.com/zilliztech/milvus-skill)

- Java Guide
  - 2.3 多线程
### Interview
- 浦银1面

## 2026-08-26
### English
 - Duolingo Phase 6: 51 - 52 two units

### Algorithm
- [53. Maximum Subarray（中等）](https://leetcode.cn/problems/maximum-subarray/)
- [918. Maximum Sum Circular Subarray（中等）](https://leetcode.cn/problems/maximum-sum-circular-subarray/)
- [1186. Maximum Subarray Sum with One Deletion（中等）](https://leetcode.cn/problems/maximum-subarray-sum-with-one-deletion/)
### Knowledge Base
#### Post-Train
- [bilibili video: Post-Train](https://www.bilibili.com/video/BV14YopBEEGs?spm_id_from=333.788.player.switch&vd_source=b29fb44a83d8060aa11af87c5b052812&p=18):

| 分类维度 | 子类别 | 代表算法 | 备注 |
| :--- | :--- | :--- | :--- |
| **环境模型** | 基于模型 (Model-Based) | Dyna, PILCO, World Models, I2A, MBMF, PETS, PlaNet, MBPO, Dreamer, MuZero, AlphaGo/AlphaZero | 学习或利用环境模型进行规划，样本效率高但模型可能不准确 |
| **环境模型** | 无模型 (Model-Free) | Q-learning, SARSA, DQN, Policy Gradient, PPO, DDPG | 直接从交互中学习，通用性强但样本效率低 |
| **学习目标** | 基于价值 (Value-Based) | Q-learning, SARSA, DQN, Double DQN, Dueling DQN, Rainbow | 适合离散动作空间 |
| **学习目标** | 基于策略 (Policy-Based) | REINFORCE, TRPO, PPO, DDPG | 适合连续动作空间 |
| **学习目标** | 演员-评论家 (Actor-Critic) | A2C, A3C, DDPG, TD3, SAC, PPO, TRPO | 结合价值与策略，兼具稳定性和灵活性 |
| **更新方式** | 同轨策略 (On-Policy) | SARSA, REINFORCE, VPG, TRPO, PPO, A2C/A3C | 用当前策略产生的数据更新，更稳定但样本效率低 |
| **更新方式** | 离轨策略 (Off-Policy) | Q-learning, DQN, DDPG, TD3, SAC | 可用任何策略产生的数据更新，样本效率高 |
| **学习过程** | 在线学习 (Online Learning) | Q-learning, SARSA, DQN, PPO, DDPG, A3C 等 | 学习的同时与环境实时交互 |
| **学习过程** | 离线学习 (Offline Learning) | 行为克隆 (Behavioral Cloning), BCQ, IQL, BRAC | 仅使用预先收集的静态数据集学习 |

- Java Guide
  - 2.1 Java 基础
  - 2.2 Java 集合
### Interview

## 2026-08-25
### English
 - Duolingo Phase 6: 49 - 50 two units

### Algorithm
- [1312. Minimum Insertion Steps to Make a String Palindrome（困难）](https://leetcode.cn/problems/minimum-insertion-steps-to-make-a-string-palindrome/)
- [407. Trapping Rain Water II（困难）](https://leetcode.cn/problems/trapping-rain-water-ii/)
### Knowledge Base
#### vLLM
- [AI INFRA 学习](https://www.bilibili.com/video/BV1T2EGzLEHi?spm_id_from=333.788.videopod.sections&vd_source=b29fb44a83d8060aa11af87c5b052812):
  - GitHub: https://github.com/cr7258/ai-infra-learning
  - V4: Speculative Decoding
  - V5: Chunked-Prefills
  - V6: Prefile Decode分离
  - V7: Inference Platform
  - V8: vLLM code 浅读
### Interview


## 2026-08-24
### English
- Duolingo Phase 6: 47 - 48 two units
### Algorithm
- [1092. Shortest Common Supersequence（困难）](https://leetcode.cn/problems/shortest-common-supersequence/)
- [10. Regular Expression Matching（困难）](https://leetcode.cn/problems/regular-expression-matching/)
- [115. Distinct Subsequences（困难）](https://leetcode.cn/problems/distinct-subsequences/)
### Knowledge Base
#### vLLM
- [AI INFRA 学习](https://www.bilibili.com/video/BV1T2EGzLEHi?spm_id_from=333.788.videopod.sections&vd_source=b29fb44a83d8060aa11af87c5b052812):
  - GitHub: https://github.com/cr7258/ai-infra-learning
  - zotero: 读paper的工具
  - LMCache: 存放KVCache
  - Video 2: PageAttention
  - Video 3: Prefix Caching & Prefix Cache Aware Routing
### Interview
#### ByteDance OD
- Algorithm: [LeetCode 15](https://leetcode.cn/problems/3sum/description/)
- Mysql事务隔离级别
- Mysql主从复制
- Redis expire time
- Redis ReHash