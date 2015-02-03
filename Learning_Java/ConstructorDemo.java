/*
Example using a constructor to initialise an object.
*/

public class ConstructorDemo{
	public static void main(String[] args){
		MyClass t1 = new MyClass(10);
		MyClass t2 = new MyClass(20);

		System.out.println(t1.x + " " + t2.x);
	}

	// Then finalise to ensure clean termination before the garbage collector comes calling!
	protected void finalize(){
		// Do something!
	}
}