//**simple_model.java**
// @ agent based computational model for network autocorrelation
// DellaPosta, Daniel, Yongren Shi and Michael W. Macy. Why do Liberals Drink Lattes?
// If you have any comment or question about the code, please contact Yongren Shi at ys334@cornell.edu 
// note: the code need to have the network structure prepared before it can be run.
// Terms that might be confusing in the code are dynamic==flexible==opinion; static==fixed==demographic trait.

// each agent is represented in the MyNode class, which contains a vector of flexible attributes and a vector of fixed attributes. Media hub is represented in Media class.

import java.util.*;
import java.lang.Math;
import java.io.*;

public class simple_model extends Thread{
	private int netsize, flex, fixed;
	private int ntraits, rep;
	MyNode [] node_array;
	double NormedDistance;
	Random rand;
	double corr;
	private int cave_size, ncaves, rewiring;
	double indv_effect, neg_percent;
	Media [] media_hubs;
	double media_strength;
	int Nhubs;
	String condition;
	String is_influence, is_sta_dyn;

	public simple_model(int fixed, int flex, double indv_effect, int ntraits, int rep, int ncaves,
			int rewiring, double neg_percent, int Nhubs, double media_strength, String is_influence,
			String is_sta_dyn){ 
		// is_influence controls for whether the influence is switched on.
		// is_sta_dyn controls for if the individual effect is from first static dimension or from the first dynamic dimension.
		this.is_influence = is_influence;
		this.is_sta_dyn = is_sta_dyn;
		this.condition = is_influence+"_"+is_sta_dyn;
		this.cave_size=100;
		this.netsize=cave_size*ncaves;
		this.flex=flex; this.fixed=fixed;
		this.indv_effect = indv_effect;
		this.ntraits=ntraits;
		this.rep=rep;
		this.ncaves=ncaves;
		this.rewiring = rewiring;
		this.neg_percent=neg_percent;
		this.media_strength = media_strength;
		this.Nhubs = Nhubs;
	}

	public void netConstruction(){ //initialize the network and agent's attributes
		rand = new Random();
		corr=0.;
		node_array = new MyNode[netsize]; //initialize all the agents
		media_hubs = new Media[Nhubs]; //initialize hubs
		try{ //read in the network data from an external file
			String filename = "final/MS_rewiring/MS_rewiring_"+Integer.toString(netsize)+"_"+Integer.toString(rewiring)+".0.txt";
			BufferedReader in = new BufferedReader(new FileReader(filename));
		    String str;
		    while ((str = in.readLine()) != null) {
		    	if (str.startsWith("#")==false){
		    		String [] row = str.split(" ");
		    		int nd_id = Integer.parseInt(row[0]);
		    		MyNode nd = new MyNode(nd_id, fixed, flex, ntraits);
		    		nd.neighbors = new int[row.length-1];
		    		nd.distances = new double[row.length-1];
		    		for (int i=0; i<nd.neighbors.length; i++) nd.neighbors[i]=Integer.parseInt(row[i+1]);		    			
		    		node_array[nd_id] = nd ;	
		    	}
		    }
		    in.close();
		}catch (IOException e) {}
		
		for (int i=0; i<media_hubs.length; i++){
			media_hubs[i]=new Media(5, 20);
		}
		
		// find out the expected distance E(d) at iteration 0, when fixed and dynamic attributes are randomly distributed.
		int edge_count = 0;
		for (int i=0; i<node_array.length;i++){
			MyNode nd = node_array[i];
			for (int j=0; j<nd.neighbors.length; j++){
				int indx = nd.neighbors[j];
				double distance = euclidean(nd, node_array[indx]);
				NormedDistance += distance;
				nd.distances[j] = distance;
				edge_count++;
			}
		}
		NormedDistance = NormedDistance/edge_count;
	}
	
	public static double correlation(double[] scores1,double[] scores2){
		double result = 0; 
		double sum_sq_x = 0, sum_sq_y = 0; 
		double sum_coproduct = 0; 
		double mean_x = scores1[0],  mean_y = scores2[0]; 
		for(int i=2;i<scores1.length+1;i+=1){ 
			double sweep =(double)(i-1)/i; 
			double delta_x = scores1[i-1]-mean_x; 
			double delta_y = scores2[i-1]-mean_y; 
			sum_sq_x += delta_x * delta_x * sweep; 
			sum_sq_y += delta_y * delta_y * sweep; 
			sum_coproduct += delta_x * delta_y * sweep; 
			mean_x += delta_x / i; mean_y += delta_y / i; 
		} 
		double pop_sd_x = Math.sqrt(sum_sq_x/scores1.length); 
		double pop_sd_y = Math.sqrt(sum_sq_y/scores1.length); 
		double cov_x_y = sum_coproduct / scores1.length; 
		result = cov_x_y / (pop_sd_x*pop_sd_y); 
		return result; 
	}
	
	public double [] one_simulation(){ //start the simulation
		Boolean equil= false;
		long max_iterations = (long)(netsize*flex)*1000;
		long iteration = 0;
		double current_energy = 0., previous_energy = 0.;
		int count=0;		
		int sample_size=100; // used for equilibrium test
		double [] sample1 = new double[sample_size];
		double [] sample2 = new double[sample_size];
		boolean drop=false; //initial drop in the equilibrium test

		while(equil==false & iteration<max_iterations){
			/* The simulation stops if it meets either one of the following rules. 
			1. the sim reaches the maximal limit of iterations, which should be a very large number. We use a limit that is compatible with network size and dimensions of opinions.
			2. the system reaches a static equilirbrium, that is that the energy level remains exactly same for a 10000 iteration interval.
			3. the system has an significant drop in energy at the initial stage, that is when the energy drops below -0.1, then to the system reaches the stochastic equilibrium in a two-way t-test using two samples of the energies from consecutive 10000*100 interations and each sample is composed of 100 energies that are separately by 10000 interations among them. For instance, after passing the test of the initial drop, the code collects the sample 1 data from iteration 1000000, 1000100, 1000200, 1000300, ..., 1009900, and collects the sample 2 data from iteration 1010000, 1010100, 1010200, 1010300,..., 1019900, and compare these two samples in a two-way t-test. 
			*/
			/*
			if (iteration%100000==0) {
				current_energy = energy();
				//System.out.println(iteration+" "+current_energy);
			}
			*/
			if (Nhubs==0){influence_weighted_sampling();} //influence function when there is no network hubs.
			else {influence_weighted_sampling_with_media();} //influence function when network hubs exist.
			
			if (iteration%10000==0 & drop==false){
				current_energy = energy();				
				if (previous_energy - current_energy==0) equil=true; //static equilibrium
				previous_energy = current_energy;
				if (current_energy<-0.1) drop=true; //if intial drop is true
			}
			///two sided t test with 100 observations in each sample, and 10000 intervals between obs
			if ((iteration%10000==0 & drop==true)){
				current_energy = energy();
				sample1[(int)(iteration/10000)%sample_size]=current_energy;						
				if ((iteration/10000)%sample_size==sample_size-1){
					if (t_test(sample1, sample2)==false & iteration>10000*100){equil=true;}
					sample2=sample1.clone();
				}
			}
			iteration++;
		}

		//correlation, averaged over all the value of correlation between flex dims.
		double [][] dimension_array = new double[flex][netsize];
		for (int i=0; i<flex; i++)
			for (int j=0; j<netsize; j++){
				MyNode nd = node_array[j];
				dimension_array[i][j] = nd.flex_array[i];
			}
		double abs_corr = 0., corr = 0.;
		
		for (int i=0; i<flex; i++) for (int j=0; j<flex; j++) if (i!=j){
			abs_corr += Math.abs(correlation(dimension_array[i], dimension_array[j]));	
			corr += correlation(dimension_array[i], dimension_array[j]);
		} 
		abs_corr = abs_corr/(flex*(flex-1)); //average of absolute correlations between dynamic/flexible dimensions
		corr = corr/(flex*(flex-1)); //average of correlations between dynamic/flexible dimensions
		
		/*
		int count_ = 0;
		for (int i=0; i<1; i++) for (int j=1; j<flex; j++) if (i!=j){
			count_ += 1 ;
			abs_corr += Math.abs(correlation(dimension_array[i], dimension_array[j]));	
			corr += correlation(dimension_array[i], dimension_array[j]);
		} 
		abs_corr = abs_corr/count_; //average of absolute correlations between dynamic/flexible dimensions
		corr = corr/count_; //average of correlations between dynamic/flexible dimensions
		*/

		//largest correlation between one demog and all the opinion dimensions. 
		//specifically, compute average correlations between every fixed/demog dimensions with all the dynamic/opinion dimensions and pick one that has largest magnitude. 
		double largest_abs_do= -1., largest_do= -1.;
		double smallest_abs_do=1., smallest_do=1.;
		double temp_abs_do = 0., temp_do = 0.;
		double [] one_fixed = new double[netsize];
		for (int d=0; d<fixed; d++){
			for (int i=0; i<netsize; i++){
				MyNode nd = node_array[i];
				one_fixed[i] = nd.fixed_array[d];
			}
			for (int i=0; i<flex; i++){
				temp_abs_do += Math.abs(correlation(dimension_array[i], one_fixed));	
				temp_do += correlation(dimension_array[i],one_fixed);
			}
			temp_abs_do = temp_abs_do/flex;
			temp_do = temp_do/flex;
			if (largest_abs_do<temp_abs_do) largest_abs_do=temp_abs_do;
			if (largest_do<temp_do) largest_do=temp_do;
			if (smallest_abs_do>temp_abs_do) smallest_abs_do=temp_abs_do;
			if (smallest_do>temp_do) smallest_do=temp_do;
		}				
		double [] results = new double[9];
		results[0]=abs_corr;
		results[1]=corr;
		results[2]=largest_abs_do;
		results[3]=largest_do;
		results[4]=smallest_abs_do;
		results[5]=smallest_do;
		results[6]=current_energy;
		results[7]=iteration;
		results[8]=max_iterations;
		return results;
	}
	
	public boolean t_test(double [] sample1, double [] sample2){
		// two sided t test at 0.01 significance level, from http://en.wikipedia.org/wiki/Student%27s_t-distribution#Table_of_selected_values
		int size = sample1.length;
		double m1 = mean(sample1);
		double m2 = mean(sample2);
		double s1 = std_squared(sample1);
		double s2 = std_squared(sample2);
		double t=(m1-m2)/Math.sqrt(s1/size+s2/size);
		if (t>2.576 | t<-2.576)//2.576
			return true;
		else return false;
	}
	
	public double mean(double [] sample){
		double mean_=0.;
		for (int i=0; i<sample.length; i++){ mean_ += sample[i]; }
		return mean_/sample.length;
	}
	public double std_squared(double [] sample){	
		double m=mean(sample);
		double std=0.;
		for (int i=0; i<sample.length; i++){ std+=(sample[i]-m)*(sample[i]-m); }
		std=std/sample.length;
		return std;
	}
		
	public void influence_weighted_sampling(){
		// at each iteration, choose a random dynamic/flexible dimension and a random person from the population.
		int rand_dim = rand.nextInt(flex); 
		int chosen_id = rand.nextInt(netsize);
		double temp_weight=0.;
		MyNode chosen_node = node_array[chosen_id];
		int nbr_size = chosen_node.neighbors.length;
		if (indv_effect > rand.nextDouble()){
			// mechanism of within-individual effect: if the indv_effect is larger than a random number between 0 and 1, the person (chosen_id) puts the trait on the first dimension of its fixed attributes and replaces it to the dimension (rand_dim) on the flexible attributes.
			// there are two different options for within-individual effect. First is hardwired between the first static dimension and the dynamic dimensions. Second is hardwired between the first dynamic dimension and the rest of the dyn dimensions.
			if (is_sta_dyn=="sta"){ node_array[chosen_id].flex_array[rand_dim] = chosen_node.fixed_array[0];}
			else {node_array[chosen_id].flex_array[rand_dim] = chosen_node.flex_array[0];}
			}
		
		else if (is_influence=="off"){ //when there is no peer influence, uncomment this statement
			node_array[chosen_id].flex_array[rand_dim]=rand.nextInt(2);
		}
		else if (is_influence=="on") { // when there is peer influence.
			double [] nbr_actual_weight = new double [nbr_size];
			double [] nbr_weight_prob = new double [nbr_size];
			double [] nbr_flex = new double [nbr_size];
			double wght_sum=0.;
			for (int i=0; i<nbr_size; i++){
				MyNode nbr_node = node_array[chosen_node.neighbors[i]];
				// weight is computed as the difference between the mean distance when all the traits are randomly assigned and distance between two agents.
				temp_weight = NormedDistance - euclidean(chosen_node, nbr_node);
				nbr_actual_weight[i] = temp_weight;
				nbr_weight_prob[i] = Math.abs(temp_weight);
				nbr_flex[i] = nbr_node.flex_array[rand_dim];
				wght_sum += Math.abs(temp_weight);
			}
			for (int i=0; i<nbr_size; i++){
				nbr_weight_prob[i] = nbr_weight_prob[i]/wght_sum;
			}
			//sampling discrete distribution (urn model)
			//in nbr_weight_prob, the values are the absolute values of weights between the focal agent and its neighbors.
			//the sampler will give a neighbor index based on the probability distribution of abs weights in the entire neighborhood. 
			WAMsampler wamsampler_weights= new WAMsampler(nbr_weight_prob.length, nbr_weight_prob);
			int index = wamsampler_weights.sample();
			// if the valence of weight with the chosen neighbor is positivive, copy the trait of the neighbor
			// if the valence is negative, take the opposite of the trait of the neighor. 
			// we do have a version that works for the condition that traits are discrete, that is that agent need to randomly select one of the traits on that dimension other than the trait already taken by the neighbor. 
			if (nbr_actual_weight[index]>=0){
				node_array[chosen_id].flex_array[rand_dim]=nbr_flex[index];
			}
			else if(nbr_actual_weight[index]<0){
				if (rand.nextDouble()<this.neg_percent){
					node_array[chosen_id].flex_array[rand_dim]=1-nbr_flex[index];
				}
			}
		}
	}
	
	public void influence_weighted_sampling_with_media(){ // this function is applied only when the media hub condition is included. Media hub is one of the three coordination mechanisms discussed in the paper. 
		int rand_dim = rand.nextInt(flex);
		int chosen_id = rand.nextInt(netsize);
		double temp_weight=0.;
		MyNode chosen_node = node_array[chosen_id];
		if (media_strength>rand.nextDouble()){
			int hub_size = media_hubs.length;
			double [] hub_actual_weight = new double [hub_size];
			double [] hub_weight_prob = new double [hub_size];
			double [] hub_opinions = new double [hub_size];
			double wght_sum=0.;
			for (int i=0; i<hub_size; i++){
				Media hub = media_hubs[i];
				temp_weight = NormedDistance - euclidean(chosen_node, hub);
				hub_actual_weight[i] = temp_weight;
				hub_weight_prob[i] = Math.abs(temp_weight);
				hub_opinions[i] = hub.opinion_arrays[rand_dim];
				wght_sum += Math.abs(temp_weight);
			}
			for (int i=0; i<hub_size; i++){
				hub_weight_prob[i] = hub_weight_prob[i]/wght_sum;
				}
			WAMsampler wamsampler_weights= new WAMsampler(hub_weight_prob.length, hub_weight_prob);
			int index = wamsampler_weights.sample();
			if (hub_actual_weight[index]>=0){node_array[chosen_id].flex_array[rand_dim]=hub_opinions[index];}
			else if(hub_actual_weight[index]<0 & rand.nextDouble()<this.neg_percent){
				node_array[chosen_id].flex_array[rand_dim]=1-hub_opinions[index];
				
			}
		}
		else if (is_influence=="off") { //when there is no peer influence
			node_array[chosen_id].flex_array[rand_dim]=rand.nextInt(2);
		}
		else if (is_influence=="on") { //peer influence
			int nbr_size = chosen_node.neighbors.length;
			double [] nbr_actual_weight = new double [nbr_size];
			double [] nbr_weight_prob = new double [nbr_size];
			double [] nbr_opinions = new double [nbr_size];
			double wght_sum=0.;
			for (int i=0; i<nbr_size; i++){
				MyNode nbr_node = node_array[chosen_node.neighbors[i]];
				temp_weight = NormedDistance - euclidean(chosen_node, nbr_node);
				nbr_actual_weight[i] = temp_weight;
				nbr_weight_prob[i] = Math.abs(temp_weight);
				nbr_opinions[i] = nbr_node.flex_array[rand_dim];
				wght_sum += Math.abs(temp_weight);
			}
			for (int i=0; i<nbr_size; i++){
				nbr_weight_prob[i] = nbr_weight_prob[i]/wght_sum;
			}
			WAMsampler wamsampler_weights= new WAMsampler(nbr_weight_prob.length, nbr_weight_prob);
			int index = wamsampler_weights.sample();
			if (nbr_actual_weight[index]>=0){node_array[chosen_id].flex_array[rand_dim]=nbr_opinions[index];}
			else if(nbr_actual_weight[index]<0 & rand.nextDouble()<this.neg_percent){
				node_array[chosen_id].flex_array[rand_dim]=1-nbr_opinions[index];
			}
		}
	}
		
	public double  energy(){ //energy is same as the "structural dissonance" in the paper.
		double  [][] f_energy = new double[netsize][fixed];
		double  [][] o_energy = new double[netsize][flex];
		//to calculate the means
		int edge_count=0;
		for (int i=0; i<netsize; i++){
			MyNode ni=node_array[i];
			for (int f=0; f<fixed; f++){f_energy[i][f]= 0.;}
			for (int o=0; o<flex; o++){o_energy[i][o]= 0.;}
			for (int j=0; j<ni.neighbors.length; j++){
					edge_count++;
					MyNode nbr=node_array[ni.neighbors[j]];
					double w = NormedDistance - euclidean(ni, nbr);
					for (int o=0; o<flex; o++){o_energy[i][o] += w*(2*Math.abs(ni.flex_array[o] - nbr.flex_array[o])-1);}
			}
		}
		double ttl_energy =0.;
		for (int i=0; i<netsize; i++)
			for (int o=0; o<flex; o++){ttl_energy+=o_energy[i][o];}
		ttl_energy = ttl_energy/(edge_count*(flex));
		return ttl_energy;
	}

	public double euclidean(MyNode nd1, MyNode nd2){ // agent and agent distance
		double dis = 0.,temp=0.;
		for (int i=0; i<fixed; i++){
			temp = (nd1.fixed_array[i]-nd2.fixed_array[i]);
			dis += temp*temp;
			}
		for (int i=0; i<flex; i++){
			temp = (nd1.flex_array[i]-nd2.flex_array[i]);
			dis += temp*temp;
			}
		dis=Math.sqrt(dis/(fixed+flex));
		return dis;
	}
	
	public double euclidean(MyNode nd1, Media m){ // agent and hub distance
		double dis = 0.,temp=0.;
		for (int i=0; i<fixed; i++){
			temp = (nd1.fixed_array[i]-m.demog_arrays[i]);
			dis += temp*temp;
			}
		for (int i=0; i<flex; i++){
			temp = (nd1.flex_array[i]-m.opinion_arrays[i]);
			dis += temp*temp;
			}
		dis=Math.sqrt(dis/(fixed+flex));	
		return dis;
	}
	
	public void run(){
		netConstruction();
		double [] results = one_simulation();
		String s = indv_effect+" "+fixed+" "+flex+" "+media_strength+" "+Nhubs+" "+netsize+" "+rep+" "+ncaves+" "+rewiring+
					" "+neg_percent+
					" "+String.format("%.4g", results[0])+ //abs_corr
					" "+String.format("%.4g", results[1])+ //corr
					" "+String.format("%.4g", results[2])+ //largest_abs_do
					" "+String.format("%.4g", results[3])+ //largest_do
					" "+String.format("%.4g", results[4])+ //smallest_abs_do
					" "+String.format("%.4g", results[5])+ //smallest_do
					" "+String.format("%.4g", results[6])+ //energy
					" "+results[7]+ //iteration
					" "+results[8]+ // max_iter
					"\n"; 
		// save results
		try{
			//String fname = "results/"+ncaves+"_"+cave_size+"_outcome_figure51.txt";
			String fname = "results/outcome_figure4_"+condition+".txt";
			//The data will be written into the existed file with the same name. It will not delete the existed file first!
			//It is useful in the batch mode.
			BufferedWriter out = new BufferedWriter(new FileWriter(fname, true)); 
			System.out.println(s);
			out.write(s);
			out.close();
		}catch (IOException e) {}
		// save raw data
		try{
			String fname = "results/data/"+indv_effect+"_"+rep+"_"+Nhubs+"_"+netsize+"_"+condition+".txt";
			BufferedWriter out = new BufferedWriter(new FileWriter(fname, true)); 
			out.write("# "+s); // write the simuation condition in the first line of the data file
			for (int i=0; i<netsize; i++){
				String fixedArray = Arrays.toString(node_array[i].fixed_array);
				fixedArray = fixedArray.replace("[", ""); 
				fixedArray = fixedArray.replace("]", "");
				out.write(fixedArray);
				out.write(", ");

				String flexArray = Arrays.toString(node_array[i].flex_array);
				flexArray = flexArray.replace("[", ""); 
				flexArray = flexArray.replace("]", "");
				out.write(flexArray);
				out.write("\n");
			}
			out.close();
		}catch(IOException e) {}

	}
	
	class Media{ // hub class
		int fixed, flex;
		private double [] opinion_arrays;
		private double [] demog_arrays;
		public Media(int fixed, int flex){
			this.fixed=fixed;
			this.flex=flex;
			this.demog_arrays = new double[fixed];
			this.opinion_arrays = new double[flex];
			for (int i=0; i<fixed; i++){demog_arrays[i] = rand.nextInt(2);}
			for (int i=0; i<flex; i++){opinion_arrays[i] = rand.nextInt(2);}
		}	
	}
	
	class MyNode{ // agent class
		int id;
		int fixed,flex;
		int ntraits, cave;
		double [] fixed_array, flex_array;
		int [] neighbors;
		double [] distances;
		public MyNode(int id, int fixed, int flex, int ntraits){
			this.id=id;
			this.cave=(int)(id/100+1);
			this.flex=flex;
			this.fixed=fixed;
			this.ntraits=ntraits;
			init(this.ntraits);
		}
		public void init(int ntraits){
			fixed_array = new double[fixed];
			flex_array = new double[flex];
			Random rand = new Random();
			for (int i=0; i<fixed; i++){fixed_array[i] = rand.nextInt(ntraits)/(double)(ntraits-1);}
			for (int i=0; i<flex; i++){flex_array[i] = rand.nextInt(ntraits)/(double)(ntraits-1);}
		}	
	}
	
	class WAMsampler {  
		// code is adapted from http://ramen.physics.und.edu/~yloh/RESOURCES/wamdemo.java
		  Random random; int N; double ff[]; int aa[];
		  public WAMsampler (final int N, final double pp[]) {
		    int i,j,jmin,jmax;
		    double bmin,bmax,s,oon,tol = 1E-8d;
		    double bb[] = new double[N];
		    random = new Random();
		    this.N = N;
		    ff = new double[N];
		    aa = new int[N];
		    oon = 1.0d/N;
		    //----- Verify that user-supplied pp[]'s sum to unity!
		    s=0;
		    for (i=0; i<N; i++) {s+=pp[i];}
		    if (Math.abs(s-1) > tol) {System.out.println("not norm!");Runtime.getRuntime().exit(1);}
		    //----- Set up arrays
		    for (i=0; i<N; i++) {bb[i]=pp[i]-oon; aa[i]=i; ff[i]=1.0;}
		    for (i=0; i<N; i++) {
		      bmin=+1E10; jmin=-1; bmax=-1E10; jmax=-1;
		      for (j=0; j<N; j++) {
			if (bmin>bb[j]) {bmin=bb[j]; jmin=j;}
			if (bmax<bb[j]) {bmax=bb[j]; jmax=j;}
		      }
		      if (bmax-bmin<tol) break;
		      aa[jmin]=jmax; ff[jmin]=1+bmin*N; bb[jmin]=0; bb[jmax]=bmax+bmin;
		    }
		  }

		  public int sample () {
		    int n=random.nextInt(N); if (random.nextDouble()>ff[n]) n=aa[n]; return n;
		  }
		}
}

