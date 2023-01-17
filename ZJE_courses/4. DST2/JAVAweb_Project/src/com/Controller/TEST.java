package Controller;
interface Shape{
    double getPerimeter();
    double getArea();
    void print();
}

class Circle implements Shape{
    double radius;
    Circle(double r){
        this.radius = r;
    }
    @Override
    public double getPerimeter() {
        return 2*3.14*radius;
    }

    @Override
    public double getArea() {
        return 3.14*radius*radius;
    }

    @Override
    public void print() {
        System.out.println("The perimeter of this circle is " + getPerimeter());
        System.out.println("The area of this circle is " + getArea());
    }
}

class Rectangle implements Shape{
    double width;
    double height;
    Rectangle(double w, double h){
        this.width = w;
        this.height = h;
    }
    @Override
    public double getPerimeter() {
        return 2*(width+height);
    }

    @Override
    public double getArea() {
        return width*height;
    }

    @Override
    public void print() {
        System.out.println("The perimeter of this rectangle is " + getPerimeter());
        System.out.println("The area of this rectangle is " + getArea());
    }
}

class Test{
    public static void main(String[] args) {
        Circle circle = new Circle(4);
        Rectangle rectangle = new Rectangle(3,5);
        circle.print();
        rectangle.print();
    }
}
