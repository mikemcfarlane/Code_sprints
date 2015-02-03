/*
Demonstrates multithreading.
*/

class RunnableDemo implements Runnable{
	private Thread t;
	private String threadName;

	int result = 1;

	RunnableDemo(String name){
		threadName = name;
		System.out.println("Creating " + threadName);
	}
	public void run(){
		System.out.println("Running " + threadName);
		try{
			for(int i = 40; i > 0; i--){
				System.out.println("Thread: " + threadName + ", " + i);
				result *= i;
				System.out.println("Thread: " + threadName + ", " + result);
				// Let the thread sleep for a while.
				Thread.sleep(50);
			}
		}
		catch (InterruptedException e){
			System.out.println("Thread " + threadName + " interrupted");
		}
		System.out.println("Thread " + threadName + " exiting");
	}

	public void start(){
		System.out.println("Starting " + threadName);
		if (t == null){
			t = new Thread(this, threadName);
			t.start();
		}
	}
}

public class TestThread{
	public static void main(String[] args){

		RunnableDemo R1 = new RunnableDemo("Thread1");
		R1.start();

		RunnableDemo R2 = new RunnableDemo("Thread2");
		R2.start();

		RunnableDemo R3 = new RunnableDemo("Thread3");
		R3.start();

		RunnableDemo R4 = new RunnableDemo("Thread4");
		R4.start();

		RunnableDemo R5 = new RunnableDemo("Thread5");
		R5.start();
	}
}