/*
Simple program to demonstrate enums which restrict a variable to predefined values.
*/

class FreshJuice {
	// Enumerate the FreshJuice
	enum FreshJuiceSize{SMALL, MEDIUM, LARGE}
	FreshJuiceSize size;
}

public class FreshJuiceTest{
	public static void main(String args[]){
		FreshJuice juice = new FreshJuice();
		juice.size = FreshJuice.FreshJuiceSize.MEDIUM;
		System.out.println("Size: " + juice.size);
	}
}