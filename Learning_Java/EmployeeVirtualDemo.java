/*
Part of VirtualDemo that demonstrates polymorphism.
*/

public class EmployeeVirtualDemo{
	private String name;
	private String address;
	private int number;
	public EmployeeVirtualDemo(String name, String address, int number){
		System.out.println("Constructing an employee");
		this.name = name;
		this.address = address;
		this.number = number;
	}

	public void mailCheck(){
		System.out.println("Mailing a cheque to " + this.name + " at " + this.address);
	}

	public String toString(){
		return name + " " + address + " " + number;
	}

	public String getName(){
		return name;
	}

	public String getAddress(){
		return address;
	}

	public void setAddress(String newAddress){
		address = newAddress;
	}

	public int getNumber(){
		return number;
	}
}