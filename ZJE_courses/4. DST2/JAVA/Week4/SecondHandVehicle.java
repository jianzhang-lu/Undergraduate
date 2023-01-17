package DST.Week4;

public class SecondHandVehicle extends DST.Week4.Vehicle {
    private final int numberOfOwners;

    public SecondHandVehicle(String regNo, String make, int yearOfManufacture, double value, int numberOfOwners) {
        super(regNo, make, yearOfManufacture, value);
        this.numberOfOwners = numberOfOwners;
    }

    public int getNumberOfOwners() {
        return numberOfOwners;
    }

    public boolean hasMultipleOwners() {
        if (this.numberOfOwners > 1){
            return true;
        } else {
            return false;
        }
    }
}
