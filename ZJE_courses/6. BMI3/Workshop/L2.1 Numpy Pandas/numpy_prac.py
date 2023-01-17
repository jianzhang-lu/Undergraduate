import numpy as np
import json
l = input()
nums = np.array(json.loads(l))
## 1. Sort array by column or rows
# print(np.sort(nums, axis=1))
# print(np.sort(nums, axis=0))

## 2. Get the unique elements
# print(np.unique(nums))

## 3. The count of non zero
# print((nums != 0).sum())

## 4. Reverse an array
# print(list(reversed(nums)))
# print(nums[::-1])

## 5. Comparison
# l1 = input()
# nums1 = np.array(json.loads(l1))
# print('Original numbers:')
# print(nums)
# print(nums1)
# print('Comparison - greater')
# print(nums > nums1)
# print('Comparison - greater_equal')
# print(nums >= nums1)
# print('Comparison - less')
# print(nums < nums1)
# print('Comparison - less_equal')
# print(nums <= nums1)

## 6. Multiply the values of two given vectors
# l1 = input()
# nums1 = np.array(json.loads(l1))
# print(nums * nums1)

## 7. Sum
# print('Sum of all elements:')
# print(np.sum(nums))
# print('Sum of each column:')
# print(np.sum(nums, axis=0))
# print('Sum of each row:')
# print(np.sum(nums, axis=1))

## 8. Numbers of rows and columns
# print(np.shape(nums))