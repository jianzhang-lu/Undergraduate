import numpy as np
import numpy.typing as npt
import pandas as pd
import matplotlib.pyplot as plt


def Distance(p1: npt.NDArray, p2: npt.NDArray):
    return np.sqrt(np.sum(np.square(p2-p1)))


# 建立一个dataframe: df，每一行代表一个point对所有centers的距离，用于重分配center
def Distances_from_centers(expressions: npt.NDArray, centers: npt.NDArray):
    all_distances = []
    for i in expressions:
        distances = []
        for center in centers:
            distances.append(Distance(i, center))
        all_distances.append(distances)
    df = pd.DataFrame(all_distances)
    return df


# 根据center的index(center在expressions中的index), 重新分配所有point所属的cluster
def Assign_points(expressions: npt.NDArray, centers: npt.NDArray):
    df = Distances_from_centers(expressions, centers)
    # sample_label就是每行的最小值的id
    # sample_label长度应该为n_points，值表示这个point属于哪个center
    # 完成所有点的分配
    sample_label = list(df.idxmin(axis=1))
    return sample_label, centers


# 给定一个cluster中center_index和这个cluster中所有点的index，计算这个cluster的cost
def Cost(center_index: int, points_index: list, expressions: npt.NDArray):
    center_pos = expressions[center_index]
    dist = 0
    for point_index in points_index:
        point_pos = expressions[point_index]
        dist += Distance(center_pos, point_pos)
    return dist


def k_medoids(n_clusters: int, n_iter: int, expressions: npt.NDArray):
    # 初始化centers
    centers_index = np.random.choice(range(len(expressions)), n_clusters, replace=False)
    centers = expressions[centers_index]
    iter = 0
    while True:
        n_iter += 1
        # 开始重分配点
        sample_label, centers = Assign_points(expressions, centers)
        # 保存一下centers 后续检测用
        test_centers = centers[:]

        # center_dict的key是center的index, values是属于该center的所有点的index
        center_dict = {}
        for index, center_index in enumerate(sample_label):
            if center_index not in center_dict:
                center_dict[center_index] = [index]
            else:
                center_dict[center_index].append(index)

        # 遍历所有的cluster 找到其中最符合条件的点作为新的center
        # 所有cluster的center组合成新的centers
        for center_index in center_dict:
            points_index = center_dict[center_index]
            # 先计算这个cluster内现有的cost和现有的center
            cur_center = center_index
            min_cost = Cost(center_index, points_index, expressions)
            # 每个cluster内除了原有center的点依次作为新的center计算
            for new_center in points_index:
                # 如果这个point已经是center了, 则不需要计算这个点
                if new_center not in center_dict:
                    new_cost = Cost(new_center, points_index, expressions)
                    if new_cost < min_cost:
                        min_cost = new_cost
                        cur_center = new_center
            centers[center_index] = cur_center
        # 此时一次循环结束 然后对所有点进行重分配
        # 退出条件
        if iter > n_iter or (test_centers == centers).all():
            break
    return sample_label


expre_list = [-37.449352, 21.611952,
              -33.506973,17.574236,
              -35.67528,-17.508074,
              4.713328,-11.507023,
              -57.07458,-1.4497656,
              39.677692,-14.91781,
              41.20371,7.3340263,
              3.953493,22.250006,
              -26.01725,16.44428,
              -34.032124,-24.679379,
              23.846012,36.1376,
              35.954247,-19.144575,
              13.327395,-16.775587,
              3.3798356,35.053375,
              35.140553,35.035503,
              4.5024605,6.6868467,
              -51.316032,-38.146957,
              -45.457535,17.94122,
              0.5901732,-25.159208,
              -48.988434,-39.05256,
              36.402973,-14.933696,
              34.15698,-0.06712348,
              -5.1508203,-16.740244,
              19.927364,-19.338253,
              17.418865,34.04944,
              5.806861,27.26732,
              53.13704,-20.47132,
              -47.62437,18.741598,
              -9.651687,-0.624601,
              6.756117,-5.712882,
              15.653191,31.090227,
              -32.045567,-5.4174013,
              -44.27953,-35.939053,
              34.046413,-23.090315,
              50.293865,-4.434306,
              14.390377,33.335033,
              -30.694786,29.53441,
              38.641285,31.114433,
              12.814272,30.150368,
              -13.015722,1.6875323,
              12.289281,-19.80311,
              1.1714202,30.939053,
              25.44119,-26.507416,
              10.508111,29.472496,
              7.6368423,21.494747,
              32.65058,-10.265993,
              -36.966236,24.489271,
              21.32583,29.820856,
              -58.579147,-24.68949,
              -44.25933,-19.363518,
              33.448956,21.21069,
              -3.308532,-5.651153]
length = len(expre_list)
expression = np.array(expre_list).reshape(int(length/2), 2)
labels = k_medoids(5, 10, expression)


# labels is the result of your function
plt.scatter(x=expression[:, 0], y=expression[:, 1], c=labels, s=20)
plt.show()




