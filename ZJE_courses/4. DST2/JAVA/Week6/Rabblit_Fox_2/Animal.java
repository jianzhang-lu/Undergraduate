package DST.Week6.Rabblit_Fox_2;
import java.util.List;

/**
 * Animal is an abstract superclass for animals.
 * It provides features common to all animals,
 * such as the location and age.
 * 
 * @author David J. Barnes and Michael Kolling
 * @version 2006.03.30
 */
public abstract class Animal
{
    // The animal's age.
    private int age;
    // Whether the animal is alive or not.
    private boolean alive;
    // The animal's position
    private Location location;

    /**
     * Create a new animal with age zero (a new born).
     */
    public Animal()
    {
        age = 0;
        alive = true;
    }
    
    /**
     * Make this animal act - that is: make it do whatever
     * it wants/needs to do.
     * @param currentField The field currently occupied.
     * @param updatedField The field to transfer to.
     * @param newAnimals A list to add newly born animals to.
     */
    abstract public void act(Field currentField, 
                             Field updatedField, 
                             List<Animal> newAnimals);
    
    /**
     * Check whether the animal is alive or not.
     * @return True if the animal is still alive.
     */
    public boolean isAlive()
    {
        return alive;
    }

    /**
     * Tell the animal that it's dead now :(
     */
    public void setDead()
    {
        alive = false;
    }
    
    /**
     * Return the animal's age.
     * @return The animal's age.
     */
    public int getAge()
    {
        return age;
    }

    /**
     * Set the animal's age.
     * @param age The animal's age.
     */
    public void setAge(int age)
    {
        this.age = age;
    }
    
    /**
     * Return the animal's location.
     * @return The animal's location.
     */
    public Location getLocation()
    {
        return location;
    }

    /**
     * Set the animal's location.
     * @param row The vertical coordinate of the location.
     * @param col The horizontal coordinate of the location.
     */
    public void setLocation(int row, int col)
    {
        this.location = new Location(row, col);
    }

    /**
     * Set the animal's location.
     * @param location The animal's location.
     */
    public void setLocation(Location location)
    {
        this.location = location;
    }
}
