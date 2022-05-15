//**MultiProcessing.java**
// @ agent based computational model for network autocorrelation
// DellaPosta, Daniel, Yongren Shi and Michael W. Macy. Why do Liberals Drink Lattes?
// If you have any comment or question about the code, please contact Yongren Shi at ys334@cornell.edu 
// note: the code need to have the network structure prepared before it can be run.
// Terms might be confusing in the code: dynamic==flexible==opinion; static==fixed==demographic trait.

/*
conditions of the figures in the paper:
Figure 3:
	fixeds=5; flex=20; caves=[5,10,20,30,40,50]; rewire=10; indv_effect=0; neg_percent_=0.1; media_strength_=0; NHubs=0
	
Figure 4:
	fixeds=5; flex=20; caves=50; rewire=10; indv_effect=[0,0.01,...,0.19,0.20]; neg_percent_=0.1; media_strength_=0; NHubs=0
	
Figure 5:
	fixeds=5; flex=20; caves=50; rewire=10; indv_effect=0; neg_percent_=0.1; media_strength_=[0,0.02,0.04,...,0.18,0.20]; NHubs=2
	Make sure influence_weighted_sampling_with_media is turned on in the simple_model.java.
	
Figure A3:
	fixeds=5; flex=20; caves=50; rewire=10; indv_effect=0; neg_percent_=0.1; media_strength_=0.05; NHubs=[2,3,4,5]
	Make sure influence_weighted_sampling_with_media is turned on in the simple_model.java.

*/

import java.util.*; 
public class MultiProcessing { //batch mode. 
	public static void main(String[] args) throws InterruptedException{
		ArrayList<Thread> myThreads = new ArrayList<Thread>();
		int count_ap=0; //record the cpu cores being used
				
		ArrayList<Integer> fixeds = new ArrayList<Integer>();
		fixeds.add(5); //static dimensions, e.g. sociodemographic traits
		/*
		fixeds.add(4);
		fixeds.add(3);
		fixeds.add(2);
		fixeds.add(1);
		*/

		ArrayList<Integer> flex_ = new ArrayList<Integer>();
		flex_.add(20); //dynamic dimensions, e.g. opinions
		/*
		flex_.add(19);flex_.add(18);
		flex_.add(17);flex_.add(16);
		flex_.add(15);flex_.add(14);		
		flex_.add(13);flex_.add(12);		
		flex_.add(11);flex_.add(10);		
		flex_.add(9);flex_.add(8);		
		flex_.add(7);flex_.add(6);		
		flex_.add(5);flex_.add(4);		
		flex_.add(3);flex_.add(2);
		*/
		
		ArrayList<Integer> caves_ = new ArrayList<Integer>();
		caves_.add(50); //number of caves
		/*
		caves_.add(20);
		caves_.add(50);
		caves_.add(40);
		caves_.add(30);
		caves_.add(10);
		caves_.add(5);
		*/
		
		ArrayList<Integer> rewire_ = new ArrayList<Integer>();
		rewire_.add(10); // the percentage of ties are rewired. Options are at every 5% from 0 to 100%.
		// the realization of the rewiring process can be found in access_network.py
		/*
		rewire_.add(0);
		rewire_.add(5);
		rewire_.add(15);
		rewire_.add(20);
		rewire_.add(25);
		rewire_.add(30);
		*/
		
		ArrayList<Double> indv_effects = new ArrayList<Double>();
		//indv_effects.add(.0); //within-individual effect
		
		indv_effects.add(0.);
		
		indv_effects.add(0.01);
		indv_effects.add(0.02);
		indv_effects.add(0.03);
		indv_effects.add(0.04);
		indv_effects.add(0.05);
		indv_effects.add(0.06);
		indv_effects.add(0.07);
		indv_effects.add(0.08);
		indv_effects.add(0.09);
		indv_effects.add(0.10);
		indv_effects.add(0.11);
		indv_effects.add(0.12);
		indv_effects.add(0.13);
		indv_effects.add(0.14);
		indv_effects.add(0.15);
		indv_effects.add(0.16);
		indv_effects.add(0.17);
		indv_effects.add(0.18);
		indv_effects.add(0.19);
		indv_effects.add(0.20);
		

		ArrayList<Double> neg_percent_ = new ArrayList<Double>();
		neg_percent_.add(0.1); //negativity
		/*
		neg_percent_.add(0.3);
		neg_percent_.add(0.5);
		neg_percent_.add(0.8);
		neg_percent_.add(1.);*/
		
		ArrayList<Double> media_strength_ = new ArrayList<Double>();
		media_strength_.add(0.0); //hub strength
		/*
		media_strength_.add(.0);
		media_strength_.add(.02);
		media_strength_.add(.04);
		media_strength_.add(.06);
		media_strength_.add(.08);
		media_strength_.add(.10);
		media_strength_.add(.12);
		media_strength_.add(.14);
		media_strength_.add(.16);
		media_strength_.add(.18);
		media_strength_.add(.20);
		*/
		
		ArrayList<Integer> Nhubs_ = new ArrayList<Integer>();
		Nhubs_.add(0);
		/*
		Nhubs_.add(2); //number of hubs
		Nhubs_.add(3);
		Nhubs_.add(4);
		Nhubs_.add(5);
		*/
		int count=0;
		
		int reps=100;
		String is_influence = "on"; //on and off
		String is_sta_dyn = "sta"; //sta or dyn
		int total_count = reps*(flex_.size())*(fixeds.size())*(caves_.size())*(rewire_.size())*(neg_percent_.size())*(media_strength_.size())*(Nhubs_.size())*(indv_effects.size());

		Boolean next=false;
		for (int rep=1; rep <= reps; rep++ ) //replications
		for (int flex: flex_)
		for(int fixed: fixeds)
		for (int ncaves : caves_)
		for (int rewire: rewire_)
		for (double neg_percent: neg_percent_)
		for (double indv_effect : indv_effects)
		for (double media_strength: media_strength_)
		for (int Nhubs: Nhubs_){
			count+=1;
			System.out.println(count+" out of "+total_count);
			next=false;
			while(next==false){
				count_ap=0;
				for (Iterator i=myThreads.iterator(); i.hasNext(); ){
					if (((Thread) i.next()).isAlive()==true){
						count_ap++;
					}
				}
				if (count_ap<40){ 
					Thread newt = new simple_model(fixed, flex, indv_effect, 2, rep, ncaves, rewire, 
							neg_percent, Nhubs, media_strength, is_influence, is_sta_dyn);
					myThreads.add(newt);
					newt.start();
					next=true;
				}
				else Thread.sleep(1000);
				for (Iterator i=myThreads.iterator(); i.hasNext(); ){
					if (((Thread) i.next()).isAlive()==false){
						i.remove();
					}
				}
			}
		}				
	}
}
