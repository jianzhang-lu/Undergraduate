package DST.Week1;
//import java.util.Scanner;
//
//public class Main {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int count = 0;
//        String hex = in.next();
//        String a = in.next();
//        String b = in.next();
//        String c = in.next();
//
//        int nhex = Integer.parseInt(hex, 16);
//        int na = Integer.parseInt(a, 16);
//        int nb = Integer.parseInt(b, 16);
//
//        StringBuffer sb = new StringBuffer();
//        for (int i = 0; i <= nhex; i++) {
//            String hexa = Integer.toHexString(i);
//            sb.append(hexa);
//        }
//
//        String result = sb.toString();
//        String subResult = result.substring(na, nb+1);
//
//        System.out.println(subResult);
//        for (int i = 0; i < subResult.length(); i++) {
//            if (subResult.substring(i, i+1).equals(c.toLowerCase())){
//                count ++;
//            }
//        }
//        System.out.println(result.length());
//        System.out.println(count);
//    }
//}


//import java.util.Scanner;


//import java.util.Scanner;
//public class Main {
//    public static void main (String[] args) {
//        Scanner in = new Scanner(System.in);
//        int a = in.nextInt();
//        int b = in.nextInt();
//        System.out.print(a + b);
//    }
//}


//import java.util.Scanner;
//public class Main {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int digit = in.nextInt();
//        int a = digit / 100;
//        int b = digit / 10 - 10 * a;
//        int c = digit % 10;
//        System.out.print(a + c*100 + b*10 );
//        in.close();
//    }
//}

//import java.util.Scanner;
//public class Main {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int h1 = in.nextInt();
//        int m1 = in.nextInt();
//        int h2 = in.nextInt();
//        int m2 = in.nextInt();
//        int d = h2 * 60 + m2 - (h1 * 60 +m1);
//        System.out.println((d/60)+ " " + (d%60));
//        in.close();
//    }
//}


//import java.util.Scanner;
//public class Main{
//    public static void main(String[] args) {
//        Scanner inr = new Scanner(System.in);
//        int a = inr.nextInt();
//        int b = inr.nextInt();
//        if (a > b){
//            System.out.print(a);
//        }
//        else {
//            System.out.print(b);
//        }
//    }
//}

//import java.util.Scanner;
//public class Main{
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int a = in.nextInt();
//        int sum = 0;
//        while(a > 0){
//            int digit = a % 10;
//            a = a / 10;
//            sum += digit;
//        }
//        System.out.print(sum);
//    }
//}

//import java.util.Scanner;
//public class Main{
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int cm = in.nextInt();
//        double foot = cm/30.48;
//
//        int f = (int) foot;
//        int i = (int) ((foot - f) * 12);
//        System.out.print(f + " " + i);
//    }
//}


//public class Main{
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int a = in.nextInt();
//        boolean prime = true;
//        if (a == 1){
//            System.out.print(a + " is not a prime number.");
//            return;
//        }
//        for (int i = 2; i < a; i++) {
//            if (a % i == 0) {
//                prime = false;
//                break;
//            }
//        }
//        if (prime) {
//            System.out.print(a + " is a prime number.");
//        }
//        else {
//            System.out.print(a + " is not a prime number.");
//        }
//    }
//}


//import java.util.Scanner;
//public class Main{
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int min = in.nextInt();
//        int max = in.nextInt();
//        boolean prime;
//        int sum = 0;
//        for (int i = min; i <= max ; i++) {
//            if (i == 1){
//                prime = false;
//            }
//            else{
//                prime = true;
//            }
//            for (int j = 2; j < i ; j++) {
//                if (i % j == 0){
//                    prime = false;
//                    break;
//                }
//            }
//            if (prime) {
//                sum += i;
//            }
//        }
//        System.out.print(sum);
//    }
//}


//class Kaprekar_operation {
//    public static void main(String[] args) {
//        int [] list;
//        Scanner in = new Scanner(System.in);
//        int a = in.nextInt();
//        while (true) {
//            int b = a;
//            list = Change_number.get_all_digit(a);
//            int max = Change_number.change_max(list);
//            int min = Change_number.change_min(list);
//            a = max - min;
//            System.out.print(max + " - " + min + " = " + a + "\n");
//            if (a == b) break;
//        }
//
//    }
//}

//class Change_number {
//     static int[] get_all_digit (int a){
//        int [] list = new int[3];
//        int index = 0;
//        while (a > 0){
//            list[index] = a % 10;
//            a /= 10;
//            index ++;
//        }
//         for (int i = 0; i < list.length-1; i++){
//             for (int j = 0; j < list.length-1-i; j++){
//                 if (list[j] > list[j+1]){
//                     int temp = list[j];
//                     list[j] = list[j+1];
//                     list[j+1] = temp;
//                 }
//             }
//         }
//        return list;
//    }
//
//    static int change_min (int [] list){
//         int min;
//         min = list[0]*100 + list[1]*10 + list[2];
//         return min;
//    }
//    static int change_max (int [] list){
//         int max;
//         max = list[2]*100 + list[1]*10 + list[0];
//         return max;
//    }
//}



//import java.util.Scanner;
//public class Main {
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int first = in.nextInt();
//        int sum = first;
//        int count = 1;
//        if (first < 0) {
//            System.out.print("None");
//        } else {
//            while (true) {
//                int a = in.nextInt();
//                if (a < 0) {
//                    break;
//                } else {
//                    sum += a;
//                    count ++;
//                }
//            }
//            System.out.printf("%.2f\n", (double) sum / count);
//        }
//    }
//}

//import java.util.Scanner;
//public class Main{
//    public static void main(String[] args) {
//        Scanner in = new Scanner(System.in);
//        int a = in.nextInt();
//        boolean prime = true;
//        int sum = 0;
//        int count = 0;
//        for (int i = 2 ; ; i++) {
//            if (count >= a){
//                break;
//            }
//            for (int j = 2; j < i; j++) {
//                if (i % j == 0){
//                    prime = false;
//                    break;
//                }
//                prime = true;
//            }
//            if (prime) {
//                count ++;
//                sum += i;
//            }
//        }
//        System.out.print(sum);
//
//    }
//}
