/*
Some loop structures including Enhanced for loop which handles arrays.
*/

public class Loop{
	public static void main(String args[]){
		int x = 10;

		// while loop
		while (x <20){
			System.out.print("value: " + x);
			x++;
			System.out.print("\n");
		}

		x = 10;

		// do...while loop
		do{
			System.out.print("value: " + x);
			x++;
			System.out.print("\n");	
		}while(x < 20);


		// for loop
		for(int y = 10; x < 20; x=x+1){
			System.out.print("value: " + x);
			System.out.print("\n");
		}

		// enhanced for loop
		int [] numbers = {10, 20, 30, 40};
		for (int z : numbers){
			System.out.print("value: " + z);
			System.out.print("\n");
		}

	}
}