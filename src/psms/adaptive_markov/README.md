# Adaptive Password-Strength Meter

## Implement

关键点在于，当频次更新时，如何高效地为其他前缀增加频次。

假设Adaptive的添加概率为$\gamma$。
假设马尔可夫模型为$l$-gram，马尔可夫的字典空间为$D=\{ prev_i : prev_i=c_0,c_1,\dots,c_{l-1} \}$。
假设所有用于训练的口令数为$Q$。由于每次添加都符合伯努利实验，那么为$prev_i$增加的噪声$x_i$满足$x_i \sim B(Q, \gamma)$。
那么为所有前缀的频次增加噪声的过程就可以看成为每个前缀计算一个随机噪声$x_i$并加入当前统计的频次中。
具体实现方案如下：

```python
import numpy as np

r <- input()
M <- training
Q = sum(M.values())

for prefix in M.keys():
    M[prefix] += np.random.binomial(Q, r, 1)

```
