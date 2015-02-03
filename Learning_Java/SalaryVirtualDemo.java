/*
Part of VirtualDemo that demonstrates polymorphism.
*/

public class SalaryVirtualDemo extends EmployeeVirtualDemo{
	private double salary;

	public SalaryVirtualDemo(String name, String address, int number, double salary){
		super(name, address, number);
		setSalary(salary);
	}

	public void mailCheck(){
		System.out.println("Within mailCheck of SalaryVirtualDemo class");
		System.out.println("Mailing cheque to " + getName() + " with salary " + salary);
	}

	public double getSalary(){
		return salary;
	}

	public void setSalary(double newSalary){
		if (newSalary >= 0.0){
			salary = newSalary;
		}
	}

	public double computePay(){
		System.out.println("Computing salary pay for " + getName());
		return salary/52;
	}
}