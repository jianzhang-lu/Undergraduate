package DST.Week4;


public class Test {
    public static void main(String[] args) {
        SecondHandVehicle first;
        SecondHandVehicle second;
        first = new SecondHandVehicle("No.1", "China", 1998, 200.0, 3);
        second = new SecondHandVehicle("No.2", "England", 2003, 400.3, 1);
        System.out.println("The RegNo of the first vehicle: " + first.getRegNo());
        System.out.println("The make of the second vehicle: " + second.getMake());
        System.out.println("The year of manufacture of the first vehicle: " + first.getYearOfManufacture());
        System.out.println("The original value of the second vehicle: " + second.getValue());
        second.setValue(543.74);
        System.out.println("The adjusted value of the second vehicle: " + second.getValue());
        System.out.println("The age of the first vehicle: " + first.calculateAge(2021));
        System.out.println("The number of owners of the first vehicle: " + first.getNumberOfOwners());
        System.out.println("Does the first vehicle have multiple owners?: " + first.hasMultipleOwners());
        System.out.println("Does the second vehicle have multiple owners?: " + second.hasMultipleOwners());
    }
}

