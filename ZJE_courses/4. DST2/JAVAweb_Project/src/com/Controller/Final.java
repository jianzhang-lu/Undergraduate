package Controller;

import java.util.ArrayList;
import java.util.Scanner;
import java.util.TreeSet;

public class Final {
    public static void main(String[] args) {
        TreeSet<Integer> nums_set = new TreeSet<>();

        Scanner in = new Scanner(System.in);
        String num = in.nextLine();
        String[] nums = num.split(" ");
        for(String num_index : nums){
            nums_set.add(Integer.parseInt(num_index));
        }
        ArrayList<Integer> nums_list = new ArrayList<>(nums_set);
        for (int i = nums_list.size()-1; i >= 0; i--) {
            System.out.print(nums_list.get(i));
            System.out.print(" ");
        }
    }
}

