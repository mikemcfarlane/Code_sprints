/*
Demonstrates method overloading - when a class has two or more methods with the same
name but different parameters.
*/

public class MethodOverloading{
	public static void main(String[] args){
		int a = 11;
		int b = 6;
		double c = 7.3;
		double d = 9.4;

		// First method called for variable type int
		int result1 = minFunction(a, b);
		// Second method called for variable type float
		double result2 = minFunction(c, d);

		System.out.println("Min int: " + result1);
		System.out.println("Min double: " + result2);
	}

	// For integer
	public static int minFunction(int n1, int n2){
		int min;
		if (n1 > n2)
			min = n2;
		else
			min = n1;

		return min;
	}

	// For double
	public static double minFunction(double n1, double n2){
		double min;
		if (n1 > n2)
			min = n2;
		else
			min = n1;

		return min;	
	}
}