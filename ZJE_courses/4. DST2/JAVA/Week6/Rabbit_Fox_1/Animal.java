package DST.Week6.Rabbit_Fox_1;


import java.util.List;

public abstract class Animal {

//    创建狐狸和兔子必须有的参数：年龄，是否活着，位置在哪。
    private int age;
    private boolean alive;
    private Location location;

//    构造新Animal, fox&rabbit can use this (super())
    public Animal() {
        age = 0;
        alive = true;
    }

//    创建一些访问器
    public int getAge(){
        return age;
    }

    public Location getLocation(){
        return location;
    }

    public boolean isAlive(){
        return alive;
    }

//    创建设置年龄指令和死亡指令
    public void setAge(int age){
        this.age = age;
    }

    public void setDead(){
        alive = false;
    }

//    创建位置（使用重写函数）
    public void setLocation(int row, int col){
        this.location = new Location(row, col);
    }

    public void setLocation(Location location){
        this.location = location;
    }

//    创建最重要的部分：使用act代替原本rabbit中的run和fox中的hunt
    public abstract void act(Field currentField, Field updatedField, List<Animal> newAnimals);

}
