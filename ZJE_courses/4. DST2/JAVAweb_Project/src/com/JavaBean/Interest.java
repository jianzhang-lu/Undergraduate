package JavaBean;

public class Interest {
    private String Name;
    private String Information;

    @Override
    public String toString() {
        return "Interest{" +
                "Name='" + Name + '\'' +
                ", Information='" + Information + '\'' +
                '}';
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        Name = name;
    }

    public String getInformation() {
        return Information;
    }

    public void setInformation(String information) {
        Information = information;
    }
}
