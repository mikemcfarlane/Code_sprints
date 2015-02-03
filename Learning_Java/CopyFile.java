/*
Simple example of copying one file to another. 
Takes command line arguments for input and output files.
Catches exceptions if not correct arguments.
*/

import java.io.*;

public class CopyFile{
	public static void main(String[] args) throws IOException{
		FileInputStream in = null;
		FileOutputStream out = null;	

		try{
			System.out.println("Will copy " + args[0] + " to " + args[1]);
			in = new FileInputStream(args[0]);
			out = new FileOutputStream(args[1]);

			int c;
			while((c = in.read()) != -1){
				out.write(c);
			}
		}
		catch(IOException e1){
			System.out.println("Failed to copy file, exception " + e1);
		}
		finally{
			if (in != null){
				in.close();
			}
			if (out != null){
				out.close();
			}
		}
	}
}