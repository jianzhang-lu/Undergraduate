package DST.Week4;

import java.util.ArrayList;
import java.util.HashMap;

public class Room {

//    description 是房间的名字。
    private final String description;
//    ExitNum 是出口个数
    protected int ExitsNum;

//    exits的key是方向，value是对应的出口Room。
    public final HashMap <String, Room> exits = new HashMap<>();

//    该Room是否有monster或者princess。
    private boolean monster = false;
    private boolean princess = false;
    private boolean randomDoor = false;

//    构造Room类。
    public Room (String description){
        this.description = description;
    }

//    setExits将信息遍历后填入exits字典。
    public void setExits (String[] direction, Room[] room){
        for (int i = 0; i < direction.length; i++) {
            exits.put(direction[i], room[i]);
        }
    }

//    获得该Room所有出口的列表。
    public ArrayList <String> getAllExits () {
        ArrayList <String> Exitlist = new ArrayList<>();
        for (String i : this.exits.keySet()){
            if (this.exits.get(i) != null){
                Exitlist.add(i);
            }
        }
        return Exitlist;
    }

//    定义一个空的show函数，方便子类重载。
    public void show(){
    }

    //    重写toString函数，print直接返回Room的名字。
    public String toString(){
        return this.description;
    }

//    getExits函数返回当前房间所有出口房间。
    public HashMap <String, Room> getExits (){
        return this.exits;
    }

    public void setMonster (boolean mon) {
        this.monster = mon;
    }

    public void setPrincess (boolean pri) {
        this.princess = pri;
    }

    public void setRandomDoor (boolean ran) { this.randomDoor = ran; }

    public boolean getMonster(){
        return monster;
    }
    public boolean getPrincess() {
        return princess;
    }
    public boolean getRandomDoor(){ return randomDoor; }

}

// 根据出口数量创建Room子类。方便输出。

class OneExitRoom extends Room {

    OneExitRoom (String description){
        super (description);
        ExitsNum = 1;
    }

    public void show() {
        ArrayList <String> a = this.getAllExits();
        System.out.print("Welcome to the " + this);
        System.out.print(". There are " + a.size());
        System.out.println(" exit as: " + a.get(0) + ".");
        System.out.println();
    }

}
class TwoExitRoom extends Room {

    TwoExitRoom (String description){
        super (description);
        ExitsNum = 2;
    }

    public void show() {
        ArrayList <String> a = this.getAllExits();
        System.out.print("Welcome to the " + this);
        System.out.print(". There are " + a.size());
        System.out.println(" exits as: " + a.get(0) + " and " + a.get(1));
        System.out.println();
    }

}
class ThreeExitRoom extends Room {

    ThreeExitRoom (String description){
        super (description);
        ExitsNum = 3;
    }

    public void show() {
        ArrayList <String> a = this.getAllExits();
        System.out.print("Welcome to the " + this);
        System.out.print(". There are " + a.size());
        System.out.println(" exits as: " + a.get(0) + ", " + a.get(1) + " and " + a.get(2) + ".");
        System.out.println();
    }

}
class FourExitRoom extends Room {

    FourExitRoom (String description){
        super (description);
        ExitsNum = 4;
    }

    public void show() {
        ArrayList <String> a = this.getAllExits();
        System.out.print("Welcome to the " + this);
        System.out.print(". There are " + a.size());
        System.out.println(" exits as: " + a.get(0) + ", " + a.get(1) + ", " + a.get(2) + " and " + a.get(3) + ".");
        System.out.println();
    }
}