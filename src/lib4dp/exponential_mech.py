'''
Exponential Mechanism
Generate a differenitial prevate password frequencies list from given distribution
'''

import math
import random

class ExpMech:
    def __init__(self, f, eps, delta):
        self.dp = {}
        self.f = f 
        self.eps = eps
        self.delta = delta
        # N为f中所有数字之和
        self.N = sum(f)
        
    def search_for_minimal_idx(self, U, i):
        for j in range(len(self.f)):
            if j > i or self.f[j] > U:
                return j-1
        return j

    def search_for_maximal_idx(self, L, i):
        for j in range(len(self.f)-1, -1, -1):
            if j < i or self.f[j] < L:
                return j+1
        return j

    def get_upper_bound(self, i, d):
        '''
        f是一个频次数组,且满足f[i]>=f[i+1]
        '''
        U = self.f[i] if i < len(self.f) else 0
        A = 2*d
        while A >= 0:
            j = self.search_for_minimal_idx(U, i)
            delta_A = i-j+1
            A = A - delta_A
            if A >= 0:
                U = U + 1
            else:
                return U
            pass
        return U

    def get_lower_bound(self, i, d):
        L = self.f[i] if i < len(self.f) else 0
        R = 2*d 
        while R >= 0 and L > 0:
            j = self.search_for_maximal_idx(L, i)
            delta_R = j-i+1
            R = R-delta_R
            if R>=0 and L > 0:
                L = L-1
        return L

    def comp_weights(self, U, i, d):
        key = (U, i)
        
        if key in self.dp:
            return self.dp[key]
        U_i = self.get_upper_bound(i, d)
        L_i = self.get_lower_bound(i, d)
        f_i =  self.f[i] if i < len(self.f) else 0
        if U < L_i or U > U_i:
            return 0
        if f_i == 0 and U == 0:
            return 1
        U_i_1 = self.get_upper_bound(i+1, d)
        L_i_1 = self.get_lower_bound(i+1, d)
        val = 0
        if U >= L_i + 1:
            delta_U_i = 1 if U >= f_i + 1 else -1
            w_1 = self.comp_weights(U-1, i, d)
            val += math.exp(-self.eps*delta_U_i/2)*w_1 
            if U <= U_i_1:
                w_2 = self.comp_weights(U, i+1, d)
                val += math.exp(-self.eps*abs(U-f_i)/2)*w_2
            self.dp[key] = val 
        else:
            for U_ in range(L_i+1, min(U_i, U_i_1)+1):
                W_U_ = self.comp_weights(U_, i+1, d)
                # 原来的伪代码里面是W, 这里可能会出问题
                val += math.exp(-self.eps*abs(U-f_i)/2)*W_U_ 
        return val

    def distance(self, delta):
        o_1 = 0
        c1 = 2*math.pi*math.sqrt(2/3) + o_1
        c2 = 2 + o_1
        return math.floor((c1*math.sqrt(self.N) - c2*math.log(delta)) / self.eps)

    def publish_vector(self):
        d = self.distance(self.delta)
        print("d:",d)
        
        U = []
        L = []
        for i in range(0, self.N+d):
            U.append(self.get_upper_bound(i, d))
            L.append(self.get_lower_bound(i, d))
        print(L, U)
        _f = [0]
        _f[0] = self.f[0] + d
        
        for i in range(0, self.N+d):
            U_max = min(_f[i], U[i])
            W = 0
            steps = {}
            for U_ in range(L[i], U_max+1):
                step = self.comp_weights(U_, i+1, d)
                steps[U_] = step
                W += step 
            r = random.random()
            for U_ in range(L[i], U_max+1):
                r = r - (steps[U_] / W)
                if r <= 0:
                    _f.append(U_)
                    # _f[i] = U_
                    break 
        res = [_f[i] for i in range(1, self.N+d+1)]
        return res

def main():
    eps = 1
    delta = 1
    f = [10,8,5,3,2,1,1,1]
    model = ExpMech(f, eps, delta)
    print(model.publish_vector())
    pass

if __name__ == '__main__':
    main()

