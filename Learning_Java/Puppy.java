/*
Puppy class.
*/

public class Puppy{

	int puppyAge;

	public Puppy(String name){
		// This constructor has one paramter - name.
		System.out.println("Passed name is: " + name);
	}

	public void setAge(int age){
		puppyAge = age;
	}

	public int getAge(){
		System.out.println("Puppy's age is: " + puppyAge);
		return puppyAge;
	}

	public static void main(String []args){

		// Create local variable for age.
		int puppyAgeLocal;

		// Following statement would create an object - myPuppy.
		Puppy myPuppy = new Puppy("tommy");

		// Call class metho to set puppy's age
		myPuppy.setAge(2);

		// Call another class method to get the puppy's age.
		puppyAgeLocal = myPuppy.getAge();

		// Access an instance variable.
		System.out.println("Instance variable value: " + myPuppy.puppyAge);

		// Access the local variable.
		System.out.println("Local variable set by method return: " + puppyAgeLocal);
	}
}