package DST.Week3;


import com.sun.source.tree.Tree;

import java.util.*;

//class Point {
//    private double x;
//    private double y;
//    public String toString() {
//        return "("+this.x+","+this.y+")";
//    }
//
//
////    Point (){
////        this.x = 0;
////        this.y = 0;
////    }
//    Point (double x, double y){
//        this.x = x;
//        this.y = y;
//    }
//    Point (Point b){
//        this.x = b.x;
//        this.y = b.y;
//    }
//    void setX (double z){
//        this.x = z;
//    }
//    void setY (double z){
//        this.y = z;
//    }
//    double getX (){
//        return this.x;
//    }
//    double getY (){
//        return this.y;
//    }
//    Point add (Point c){
//        double m = c.x + this.x;
//        double n = c.y + this.y;
//        return new Point(m, n);
//    }
//
//
//}
//

//}


//public class Main3 {
//    public static void main(String[] args) {
//        Point a = new Point();  //    default ctor, x and y are zeros
//        Scanner sc = new Scanner(System.in);
//        double x,y,z;
//        x = sc.nextDouble();
//        y = sc.nextDouble();
//        z = sc.nextDouble();
//        Point b = new Point(x, y);    //  ctor by x and y
//        Point c = new Point(b);       //  ctor by another Point
//        a.setY(z);
//        System.out.println(a);
//        System.out.println(b);
//        System.out.println(c);
//        c.setX(z);
//        a = b.add(c);
//        System.out.println(a);
//        System.out.println("b.x="+b.getX()+" b.y="+b.getY());
//        sc.close();
//    }
//}
//
//public class Main3 {
//    public static void main(String[] args) {
//
////        stumap contains the relationship between student objects and id.
//        TreeMap<String, Student> stumap = new TreeMap<>();
//
////        subject obtains the set of all subjects.
//        TreeSet<String> subject = new TreeSet<>();
//
//
//        Scanner in = new Scanner(System.in);
//        while (true) {
//            String line = in.nextLine();
//            if (line.equals("END")) break;
//            String[] record = line.split(",");
//
//            if (record.length == 2) {
//                String ID = record[0];
//                String name = record[1];
//                if (stumap.containsKey(ID)) {
//                    stumap.get(ID).setName(name);
//                } else {
//                    stumap.put(ID, new Student(ID, name));
//                }
//            }
//
//            if (line.split(",").length == 3) {
//                String ID = record[0];
//                String course = record[1];
//                double score = Double.parseDouble(record[2]);
//                if (stumap.containsKey(ID)) {
//                    stumap.get(ID).addScore(course, score);
//                } else {
//                    stumap.put(ID, new Student(ID, course, score));
//                }
//
//            }
//        }
//
//        for (String id : stumap.keySet()){
//            subject.addAll(stumap.get(id).score.keySet());
//        }
//
//
//        //        输入第一行。
//        System.out.print("student id, name,");
//        for (String i : subject){
//            System.out.print(i + ",");
//        }
//        System.out.println(" average");
//
////        开始输入学生信息。
//        for (String id : stumap.keySet()){
//            System.out.print(id + ",");
//            Student index = stumap.get(id);
//            System.out.print(index.getName() + ",");
//            for (String subj : subject){
//                if (index.score.containsKey(subj)){
//                    System.out.print(" " + index.score.get(subj) + ",");
//                } else {
//                    System.out.print(" ,");
//                }
//            }
//            index.getAverage();
//            System.out.println();
//        }
//    }
//}
//
//class Student {
//    private final String ID;
//    private String name;
//    private double sum;
//
////    score is a map to record one student's course and mark.
//    public TreeMap <String, Double> score = new TreeMap<>();
//
//    Student (String id, String name){
//        this.ID = id;
//        this.name = name;
//    }
//
//    Student (String id, String course, double score){
//        this.ID = id;
//        this.score.put(course, score);
//    }
//    void getAverage(){
//        // 课程数目
//        int number = score.size();
//        for (double v : score.values()){
//           sum += v;
//        }
//        double average =  sum / number;
//        System.out.printf(" %.1f", average );
//    }
//
//
//    String getName() {
//        return name;
//    }
//
//    void setName (String name) {
//        this.name = name;
//    }
//
//    void addScore (String course, double score) {
//        this.score.put(course, score);
//    }
//}



