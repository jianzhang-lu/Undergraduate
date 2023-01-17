package Week2;

import java.util.*;

//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int n = in.nextInt();
//        int a = in.nextInt();
//        int b = in.nextInt();
//        int c = in.nextInt();
//        int count = 0;
//        StringBuffer sb = new StringBuffer();
//        for (int i = 0; i < n + 1; i++) {
//            sb.append(i);
//        }
//        String s = sb.toString();
//        String sub_s = s.substring(a, b+1);
//        for (int j = 0; j < sub_s.length(); j++) {
//            if (sub_s.charAt(j) - '0' == c){
//                count ++;
//            }
//        }
//        System.out.print(s.length() + " ");
//        System.out.print(count);
//
//    }
//}

public class Main2 {
    public static void main(String[] args) {
        int count = 0;
        Scanner in = new Scanner(System.in);
        String a = in.next();
//        while (in.hasNext()){
//            System.out.println(a);
//        }
        String[] b = a.split(" ");
        for(String i : b){
            if (i.equals("pass")){
                count ++;
            }
        }
        System.out.print(count);
    }
}

//public class Main2 {
//    public static void main(String[] args) {
//        int[] a = new int[(int)(Math.random()*10)];
//        for ( int i=0; i<a.length; ++i )
//            a[i] = (int)(Math.random()*100);
//        for ( int i=0; i<a.length; ++i )
//            System.out.println(a[i]);
//            }
//        }

//public class Main2 {
//    public static void main(String[] args) {
//        int sum_a = 0, sum_b = 0, sum_c = 0;
//        Scanner in = new Scanner(System.in);
//        int[][] table = new int[4][3];
//        for (int i = 0; i < table.length; i++) {
//            for (int j = 0; j < table[i].length; j++) {
//
//                    table[i][j] = in.nextInt();
//
//            }
//        }
//        for (int i = 0; i < table.length; i++) {
//            sum_a += table[i][0];
//            sum_b += table[i][1];
//            sum_c += table[i][2];
//        }
//        System.out.print(sum_a + " " + sum_b + " " + sum_c + " ");
//    }
//}
//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int n = in.nextInt();
//        int sum = 0;
//        int x = 6;
//        int digit = 0;
//        for (int i = 0; i < n; i++) {
//            digit = x + digit*10;
//            sum += digit;
//        }
//        System.out.print(sum);
//    }
//}

//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int number = in.nextInt();
//        int[] list= new int[number];
//        for (int i = 0; i < list.length; i++) {
//            if (in.hasNext()) {
//                list[i] = in.nextInt();
//            }
//        }
//        for (int j = list.length-1; j >= 0 ; j--) {
//            System.out.print(list[j]);
//            if (j != 0){
//                System.out.print(" ");
//            }
//        }
//        System.out.println("");
//    }
//}
//
//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int number = in.nextInt();
//        int[] list= new int[number];
//        for (int i = 0; i < list.length; i++) {
//            if (in.hasNext()) {
//                list[i] = in.nextInt();
//            }
//        }
//        for (int i = 0; i < list.length; i+=2) {
//            if (i != 0) {
//                System.out.print(" " + list[i]);
//            } else{
//                System.out.print(list[i]);
//            }
//        }
//        System.out.println();
//        for (int i = 1; i < list.length; i+=2) {
//            if (i != 1) {
//                System.out.print(" " + list[i]);
//            } else {
//                System.out.print(list[i]);
//            }
//        }
//        System.out.println();
//    }
//}

//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int number = in.nextInt();
//        int[] list= new int[number];
//        for (int i = 0; i < list.length; i++) {
//            if (in.hasNext()) {
//                list[i] = in.nextInt();
//            }
//        }
//        for (int i = 0; i <= number/2 - 1; i++) {
//            System.out.println(list[i] + " " + list[number-1-i]);
//        }
//    }
//}

//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int number = in.nextInt();
//        boolean finish = true;
//        int[] list = new int[number];
//        for (int i = 0; i < list.length; i++) {
//            if (in.hasNext()) {
//                list[i] = in.nextInt();
//            }
//        }
//        for (int i = list.length-1; i >= 0 ; i--) {
//            for (int j = 0; j < i; j++) {
//                if (list[j] == list[i]){
//                    finish = false;
//                    break;
//                }
//            }
//            if (finish){
//                System.out.print(i);
//                break;
//            }
//            finish = true;
//        }
//    }
//}

//class Exchange{
//    static int[] change(int [] list){
//        int media;
//        for (int i = 0; i < list.length-1; i++) {
//            for (int j = 0; j < list.length-i-1; j++) {
//                if(list[j] > list[j+1]){
//                    media = list[j];
//                    list[j] = list[j+1];
//                    list[j+1] = media;
//                }
//            }
//        }
//        return list;
//    }
//}
//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int number = in.nextInt();
//        int count = 0;
//        int[] list = new int[number];
//        for (int i = 0; i < list.length; i++) {
//            if (in.hasNext()) {
//                list[i] = in.nextInt();
//            }
//        }
//        int [] new_list = new int[list.length];
//        new_list = Exchange.change(list);
//        for (int i = 0; i < new_list.length-2; i++) {
//            if (new_list[i] == new_list[i+1]-1 && new_list[i+1] == new_list[i+2]-1){
//                count ++;
//                i += 2;
//            }
//        }
//        System.out.print(count);
//    }
//}

//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        String a = in.nextLine();
//        int b= in.nextInt();
//        for (int i = 0; i < b; i++) {
//            int count = 0;
//            int B = in.nextInt();
//            int E = in.nextInt();
//            String c = in.next();
//            for (int j = B; j <= E; j++) {
//                if (a.substring(j, j+1).equals(c)){
//                    count ++;
//                }
//            }
//            System.out.println(count);
//        }
//    }
//}

//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int number = in.nextInt();
//        boolean finish = false;
//        int[] list = new int[number];
//        for (int i = 0; i < list.length; i++) {
//            if (in.hasNext()) {
//                list[i] = in.nextInt();
//            }
//        }
//
//
//        for (int index = 0; index < list.length; index++) {
//            if (index == list.length-1){
//                System.out.print(index);
//                return;
//            }
//            for (int i = index + 1; i < list.length; i++) {
//                for (int j = 0; j <= index; j++) {
//                    if (list[j] == list[i]){
//                        finish = true;
//                        break;
//                    }
//                }
//                if (!finish){
//                    break;
//                } else if (i == list.length-1){
//                    System.out.print(index);
//                    return;
//                }
//                finish = false;
//            }
//        }
//        }
//    }

//import java.util.Scanner;
//public class Main2 {
//
//    public static void main(String[] args) {
//        int N,x;
//        Scanner scan=new Scanner(System.in);
//        N=scan.nextInt();
//        int i,sum=0;
//        int []num=new int[101];
//        for(i=1;i<=N;i++) {
//            x=scan.nextInt();
//            num[x]++;
//        }
//
//        for(i=1;i<=N-2;i++) {
//            if(num[i]!=0&&num[i+1]!=0&&num[i+2]!=0) {
//                int max = (num[i]<num[i+1])?num[i]:num[i+1];
//                max = (max<num[i+2])?max:num[i+2];
//                sum+=max;
//                num[i]-=max;
//                num[i+1]-=max;
//                num[i+2]-=max;
//            }
//        }
//        System.out.println(sum);
//    }
//}

//import java.util.Scanner;
//public class Main2 {
//    public static void main(String[] args)
//    throws NumberFormatException {
//        Scanner in = new Scanner(System.in);
//        String letters = in.nextLine();
//        int k = in.nextInt();
//        String [][] table = new String[k][3];
//        for (int i = 0; i < table.length; i++) {
//            for (int j = 0; j < table[i].length; j++) {
//                table[i][j] = in.next();
//            }
//        }
//        for (String[] strings : table) {
//            int x = Integer.parseInt (strings[0]);
//            int y = Integer.parseInt (strings[1]);
//            String letter = letters.substring(x, y);
//            String tar = strings[2];
//            String S1 = letter.replace(tar, "");
//            int len1 = letter.length();
//            int len2 = S1.length();
//            System.out.println(len1 - len2);
//        }
//        in.close();
//    }
//}

// 贴花问题改正
//public class Main2 {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int num = in.nextInt();
//        TreeMap<Integer, Integer> dic = new TreeMap<>();
//        for (int i = 0; i < num; i++) {
//            int picture = in.nextInt();
//            if (dic.containsKey(picture)){
//                dic.replace(picture, dic.get(picture)+1);
//            }else{
//                dic.put(picture, 1);
//            }
//        }
//
//        int result = 0;
//        for (int i : dic.keySet()) {
//            while (true) {
//                if (dic.containsKey(i+1) && dic.containsKey(i+2)) {
//                    if(dic.get(i) != 0 && dic.get(i+1) != 0 && dic.get(i+2) != 0){
//                        result ++;
//                        dic.replace(i, dic.get(i)-1);
//                        dic.replace(i+1, dic.get(i+1)-1);
//                        dic.replace(i+2, dic.get(i+2)-1);
//                    }else break;
//                }else break;
//            }
//        }
//        System.out.println(result);
//    }
//}