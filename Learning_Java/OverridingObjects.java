/*
Simple object based example to demonstrate inheritance and overriding methods.
*/

class Animal{
	public void move(){
		System.out.println("Animals can move");
	}
}

// Extends the class Animal and hence inherits all the properties.
class Dog extends Animal{
	public void move(){
		System.out.println("Dogs can walk and run");
	}
}

public class OverridingObjects{
	public static void main(String[] args){
		Animal a = new Animal(); // Animal reference and object
		Animal b = new Dog(); //Animal reference but Dog object

		a.move();
		b.move();
	}
}