package DST.Week4;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class Game {

//    创建当前房间。
    private DST.Week4.Room CurrentRoom;

    public DST.Week4.Room getCurrentRoom() {
        return CurrentRoom;
    }

    public void setCurrentRoom (DST.Week4.Room currentRoom) {
        this.CurrentRoom = currentRoom;
    }

    public void move (String direction){
        HashMap <String, DST.Week4.Room> Map = CurrentRoom.getExits();
        DST.Week4.Room nextRoom = Map.get(direction);
        if (nextRoom != null){
            this.CurrentRoom = nextRoom;
            this.CurrentRoom.show();
        } else {
            System.out.println("No door here!!!");
        }
    }


    public Room random (ArrayList<Room> roomSet) {
        int location = (int) (Math.random()*7);
        return roomSet.get(location);
    }

//  开玩！！！
    public static void main(String[] args) {
//        成功与否。
        boolean success = false;
        boolean hasprincess = false;
        int princessSite;
        int monsterSite;
        int randomSite;
        ArrayList<Room> roomSet = new ArrayList<> ();
        Scanner in = new Scanner(System.in);
        Game game = new Game();

//    创造其他房间
//        新建8个房间和方向列表。
        ThreeExitRoom lobby = new ThreeExitRoom("lobby");
        TwoExitRoom bedroom = new TwoExitRoom("bedroom");
        roomSet.add(bedroom);
        TwoExitRoom shop = new TwoExitRoom("shop");
        roomSet.add(shop);
        OneExitRoom library = new OneExitRoom("library");
        roomSet.add(library);
        ThreeExitRoom study = new ThreeExitRoom("study");
        roomSet.add(study);
        TwoExitRoom supply = new TwoExitRoom("supply");
        roomSet.add(supply);
        FourExitRoom pub = new FourExitRoom("pub");
        roomSet.add(pub);
        OneExitRoom inside = new OneExitRoom("inside");
        roomSet.add(inside);
        String [] dirList = {"east", "south", "west", "north"};

//        填入字典
        Room[] lobbyExit = {shop, null, bedroom, pub};
        lobby.setExits(dirList, lobbyExit);

        Room[] bedroomExit = {lobby, null, null, supply};
        bedroom.setExits(dirList, bedroomExit);

        Room[] shopExit = {null, null, lobby, study};
        shop.setExits(dirList, shopExit);

        Room[] libraryExit = {null, null, study, null};
        library.setExits(dirList, libraryExit);

        Room[] studyExit = {library, shop, pub, null};
        study.setExits(dirList, studyExit);

        Room[] pubExit = {study, lobby, supply, inside};
        pub.setExits(dirList, pubExit);

        Room[] insideExit = {null, pub, null, null};
        inside.setExits(dirList, insideExit);


        Room[] supplyExit = {pub, bedroom, null, null};
        supply.setExits(dirList, supplyExit);

//        设置怪兽和公主的位置 (lobby除外)。并且不让公主和怪兽出现在同一间屋子。
        while (true) {
            princessSite = (int) (Math.random()*7);
            monsterSite = (int) (Math.random()*7);
            if (princessSite != monsterSite){
                roomSet.get(princessSite).setPrincess(true);
                roomSet.get(monsterSite).setMonster(true);
                break;
            }
        }

//        设置任意门的位置 (lobby除外)。
        randomSite = (int) (Math.random()*7);
        roomSet.get(randomSite).setRandomDoor(true);

//        从大厅开始。
        game.setCurrentRoom(lobby);
        System.out.println("Welcome to the game! It is a little more interesting than teacher's!");
        game.CurrentRoom.show();
        System.out.println("Enter your command: ");
        while (true) {
            String cmd = in.nextLine();
            String[] cmdList = cmd.split(" ");
            String direction = cmdList[1];
            game.move(direction);

            if (game.getCurrentRoom().getMonster()){
                break;
            }
            if (game.getCurrentRoom().getPrincess()){
                hasprincess = true;
                System.out.println("You found the princess, now try to go out of the castle!");
            }

//            如果遇到了任意门。
            if (game.getCurrentRoom().getRandomDoor()){
                System.out.println("Congratulations! You have found the random door. It will lead you to another room.");
                System.out.println("You can choose whether to use random door or not.");
                System.out.println("        YES                     NO         ");
                while (true) {
                    String cmd2 = in.nextLine();
                    if (cmd2.equals("YES")) {
                        System.out.println("You use the random door.");
                        Room select = game.random(roomSet);
                        game.setCurrentRoom(select);
                        game.getCurrentRoom().show();
                        break;

                    } else if (cmd2.equals("NO")) {
                        System.out.println("You do not use the random door.");
                        System.out.println("Please go ahead! ");
                        game.getCurrentRoom().show();
                        break;

                    } else {
                        System.out.println("Command not invalid! Please input again.");
                    }
                }
            }

            if (hasprincess && game.getCurrentRoom() == lobby){
                success = true;
                break;
            }
        }

        if (!success){
            System.out.println("Monster here. Game over. Good luck next time !");
        } else {
            System.out.println("Good job, you succeed.");
        }

    }
}
