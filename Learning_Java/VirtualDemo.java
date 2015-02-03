/*
Part of VirtualDemo that demonstrates polymorphism.
*/

public class VirtualDemo{
	public static void main(String[] args){
		SalaryVirtualDemo s = new SalaryVirtualDemo("bob", "Scotland", 3, 10.0);
		EmployeeVirtualDemo e = new SalaryVirtualDemo("sally", "Scotland", 2, 5.0);
		System.out.println("Call mailCheck using SalaryVirtualDemo reference");
		s.mailCheck();
		System.out.println("\nCall mailCheck using EmployeeVirtualDemo reference");
		e.mailCheck();
	}
}