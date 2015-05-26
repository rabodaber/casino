from scipy import stats
import numpy as np

DICE_1 = 0
DICE_2 = 1
STATES = (DICE_1, DICE_2)


def build_distribution(dist, name=None):
    return stats.rv_discrete(values=(np.array(dist.keys()), np.array(dist.values())),
                             name=name)


def generate_sample(dice_1, dice_2, trans_p, start_p, size=50):
    d1 = build_distribution(dice_1, str(DICE_1))
    d2 = build_distribution(dice_2, str(DICE_2))
    d1_to_d2 = build_distribution(trans_p[DICE_1])
    d2_to_d1 = build_distribution(trans_p[DICE_2])
    start_dist = build_distribution(start_p)
    # current == 0 -> DICE_1
    # current == 1 -> DICE_2
    distributions, current = [d1, d2], 0 if start_dist.rvs() == DICE_1 else 1
    obs, states = [], []
    for i in range(size):
        d = distributions[current]
        obs.append(d.rvs())
        states.append(current)
        # if d is DICE_1 distribution and we need swap
        if current == 0 and d1_to_d2.rvs() == DICE_2:
            current = 1 - current
        # if d is DICE_2 distribution and we need swap
        elif current == 1 and d2_to_d1.rvs() == DICE_1:
            current = 1 - current
    return obs, states