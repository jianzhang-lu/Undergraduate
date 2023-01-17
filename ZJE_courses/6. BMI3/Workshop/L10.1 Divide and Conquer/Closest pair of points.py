import math
def Distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y1-y2)**2)

# [[2,1], [1,3], [4,6], [7,2], [3,5]]
# points_x: [1, 2, 3, 4, 7]
# points_y: [3, 1, 5, 6, 2]
def Closest_pair(cur_x, points_x: list, points_y: list, n: int):
    # 边界
    if n == 2:
        distance = Distance(points_x[0], points_y[0], points_x[1], points_y[1])
        return [distance, ((points_x[0], points_y[0]), (points_x[1], points_y[1]))]
    if n == 1:
        return [float('inf'), (points_x[0], points_y[0])]

    #  按照x轴排序大小，将点集对半分，落在中线的点算右侧区域
    mid = n//2
    left_points_x = points_x[0:mid]
    right_points_x = points_x[mid:n]

    # 中线横坐标
    if n % 2 != 0:
        mid_x = points_x[mid]
    else:
        mid_x = (points_x[mid] + points_x[mid-1])/2

    left_info = Closest_pair(left_points_x, points_x, points_y, len(left_points_x))
    dis_left = left_info[0]
    min_left_points = left_info[1]

    right_info = Closest_pair(right_points_x, points_x, points_y, len(right_points_x))
    dis_right = right_info[0]
    min_right_points = right_info[1]

    # 分而治之中的合并过程
    min_dis = min(dis_left, dis_right)
    if min_dis == dis_left:
        min_points = min_left_points
    else:
        min_points = min_right_points
    candidates = []

    # x_block为mid_x加减min_dis
    x_block = [(mid_x-min_dis), (mid_x+min_dis)]
    for index in range(len(points_x)):
        cur_x = points_x[index]
        cur_y = points_y[index]
        if x_block[0] <= cur_x <= x_block[1]:
            candidates.append((cur_x, cur_y))

    # 遍历candidates中所有元素
    if len(candidates) == 1:
        return min_dis
    for i in range(len(candidates)-1):
        y_block = [points_y[i]-min_dis, points_y[i]+min_dis]
        for j in range(i+1, len(candidates)):
            if y_block[0] <= points_y[j] <= y_block[1]:
                one = candidates[i]
                other = candidates[j]
                cur_dis = Distance(one[0], one[1], other[0], other[1])
                if cur_dis < min_dis:
                    min_dis = cur_dis
                    min_points = (one, other)
    return [min_dis, min_points]


alist = [[1, 1], [4, 3], [6, 6], [10, 2], [12, 5]]
alist2 = [[1, 3], [1, 5], [1, 1], [1, 6], [1, 10]]
sort_list = sorted(alist2, key=lambda s: s[0])
points_x = [i[0] for i in sort_list]
points_y = [i[1] for i in sort_list]

print(Closest_pair(points_x, points_x, points_y, len(points_y)))

