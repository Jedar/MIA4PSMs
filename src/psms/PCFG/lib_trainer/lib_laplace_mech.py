import numpy as np 

# 隐私预算
EPSILON = 1
# 计数敏感度，默认为1
SENSITIVITY=1

# 拉普拉斯机制
def laplace_mech(scale):
    return np.random.laplace(loc=0, scale=scale)

# 为类似[key, count]的字典添加拉普拉斯噪声，噪声大小默认为`敏感度/伊普西隆`
def apply_probability_differential_privacy(counter):
    for k in counter.keys():
        counter[k] = counter[k] + laplace_mech(SENSITIVITY / EPSILON)
