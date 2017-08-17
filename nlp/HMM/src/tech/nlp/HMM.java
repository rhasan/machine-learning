package tech.nlp;

import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;
import java.util.Set;
import java.util.regex.Pattern;

public class HMM {
	
	final String initialCountFile = "files/h1-p/gene.counts";
	final String initialTrainingFile = "files/h1-p/gene.train";
	final String trainingFile = "files/h1-p/gene.new.train";
	
	final String devFile = "files/h1-p/gene.dev";
	final String part1DevOutFile = "files/h1-p/gene_dev.p1.out";
	final String part2DevOutFile = "files/h1-p/gene_dev.p2.out";
	final String part3DevOutFile = "files/h1-p/gene_dev.p3.out";
	
	final String testFile = "files/h1-p/gene.test";
	final String part1TestOutFile = "files/h1-p/gene_test.p1.out";
	final String part2TestOutFile = "files/h1-p/gene_test.p2.out";
	final String part3TestOutFile = "files/h1-p/gene_test.p3.out";

	final String countFreqs = "C:\\Users\\Rakebul\\git\\nlp\\files\\h1-p\\count_freqs.py";
	final String geneTrainFullPath = "C:\\Users\\Rakebul\\git\\nlp\\files\\h1-p\\gene.new.train";
	final String geneCountFullPath = "C:\\Users\\Rakebul\\git\\nlp\\files\\h1-p\\gene.new.counts";
	
	final String WORDTAG = "WORDTAG";
	final String UNIGRAM = "1-GRAM";
	final String BIGRAM = "2-GRAM";
	final String TRIGRAM = "3-GRAM";
	final int REPLACE_TH = 5;
	
	final String RARE = "_RARE_";
	final String LAST_CAPITAL = "_LAST_CAPITAL_";
	final String CAPITALS = "_CAPITALS_";
	final String NUMERIC = "_NUMERIC_";
	
	final String START = "*";
	final String STOP = "STOP";
	
	
	//mapped as "[consensus][I-GENE]" = 13	
	Map<String, Integer> wordTagCounts = 
			new HashMap<String, Integer>();
	//1-gram mapped as "I-GENE" = 41072
	//2-gram mapped as  [I-GENE][O] = 16624
	//2-gram mapped as [][][] = 
	Map<String,Integer> chainCount = new HashMap<String, Integer>();
	
	Map<String,Integer> wordCount = new HashMap<String, Integer>();
	Map<String,String> frequencyClass = new HashMap<String, String>();
	Set<String> tagSet = new HashSet<String>();
	
	private void loadCounts(String countFile) throws IOException {
		FileInputStream fis = new FileInputStream(countFile);
		Scanner in = new Scanner(fis);
		
		while(in.hasNext()) {
			String str = in.nextLine();
			String[] words = str.trim().split("\\s+");
			if(words[1].equals(WORDTAG)) {
				//13 WORDTAG I-GENE consensus
				String key = "["+words[3]+"]"+"["+words[2]+"]";
				int value = Integer.valueOf(words[0]);
				wordTagCounts.put(key, value);
			}
			else if(words[1].equals(UNIGRAM)) {
				//41072 1-GRAM I-GENE
				String key  = words[2];
				int value = Integer.valueOf(words[0]);
				chainCount.put(key, value);
			}
			else if(words[1].equals(BIGRAM)) {
				//16624 2-GRAM I-GENE O
				String key  = "["+words[2]+"]"+"["+words[3]+"]";
				int value = Integer.valueOf(words[0]);
				chainCount.put(key, value);
			}
			else if(words[1].equals(TRIGRAM)) {
				//9622 3-GRAM I-GENE I-GENE O
				String key  = "["+words[2]+"]"+"["+words[3]+"]"+"["+words[4]+"]";
				int value = Integer.valueOf(words[0]);
				chainCount.put(key, value);
			}

		}
		in.close();
	}
	
	public void replaceLowFrequency() throws IOException {
		FileInputStream fis = new FileInputStream(initialCountFile);
		Scanner in = new Scanner(fis);
		
		while(in.hasNext()) {
			String str = in.nextLine();
			String[] words = str.trim().split("\\s+");
			if(words[1].equals(WORDTAG)) {
				//13 WORDTAG I-GENE consensus
				String key = words[3];
				int value = Integer.valueOf(words[0]);
				if(wordCount.containsKey(key)) {
					value = wordCount.get(key)+value;					
				}
				wordCount.put(key, value);
				
				String tag = words[2];
				tagSet.add(tag);
			}
		}
		in.close();
	    for(Entry<String, Integer> entry:wordCount.entrySet()) {
	    	String word = entry.getKey();
	    	int value = entry.getValue();
	    	if(value<REPLACE_TH) {
	    		//frequencyClass.put(word, RARE);
	    		String rare = rareClass(word);
	    		frequencyClass.put(word, rare);
	    	} else {
	    		frequencyClass.put(word, word);
	    	}
	    }

	    Scanner inTraining = 
				new Scanner(new FileInputStream(initialTrainingFile));
	    FileWriter fw = new FileWriter(trainingFile);
	    BufferedWriter out = new BufferedWriter(fw);
		
		while(inTraining.hasNext()) {
			String line = inTraining.nextLine();
			out.write(replaceEach(line));
			out.newLine();
		}
		inTraining.close();
		out.close();

	    
	}
	
	public String rareClass(String s) {
		if(containsNumeric(s))
			return NUMERIC;
		else if(containsAllCapitals(s)) {
			return CAPITALS;
		}
		else if(containsLastCapital(s)) {
			return LAST_CAPITAL;
		}
		return RARE;
	}

	public boolean containsNumeric(String s){
		return s.matches("^.*\\d+.*$");
	}

	public boolean containsAllCapitals(String s){
		return s.matches("^[A-Z]+$");
	}

	public boolean containsLastCapital(String s){
		return containsAllCapitals(s)==false && s.matches("^.*[A-Z]$");
	}
	
	String replaceEach(String str) {
		String[] ss = str.split("\\s+");
		String word = ss.length>0?ss[0]:"";
		if(frequencyClass.containsKey(word)) {
			//return StringUtils.replace(text, searchString, replacement)(str,word,frequencyClass.get(word));
			return str.replaceFirst(Pattern.quote(word), frequencyClass.get(word));
		}
		
		return str;
	}
	
	public void generateCountFile() throws IOException, InterruptedException {
		String cmd = "cmd /c python "+ countFreqs + " " + geneTrainFullPath +" > "+geneCountFullPath;
		Process proc = Runtime.getRuntime().exec(cmd);
		int exitCode = proc.waitFor();
		//System.out.println(exitCode);

	}
	
	/**
	 * returns how many times the word x was tagged as y
	 * @param y
	 * @param x
	 * @return
	 */
	public int countWordTag(String y, String x) {
		String key = "["+x+"]"+"["+y+"]";
		
		
		if(wordTagCounts.containsKey(key)) {
			//System.out.println("Key: "+key+" value: "+wordTagCounts.get(key));
			return wordTagCounts.get(key);
		}
		//System.out.println("Key: "+key+" value: "+0);

		return 0;
	}
	
	/**
	 * uni-gram count of tag y
	 * @param y
	 * @return
	 */
	public int countUnigram(String y) {
		if(chainCount.containsKey(y)) return chainCount.get(y);
		return 0;
	}
	/**
	 * bi-gram count of tag sequence yn_1 and yn
	 * @param yn_1
	 * @param yn
	 * @return
	 */
	
	public int countBigram(String yn_1, String yn) {
		String key = "["+yn_1+"]"+"["+yn+"]";
		if(chainCount.containsKey(key)) return chainCount.get(key);
		return 0;
	}
	
	/**
	 * tri-gram count of tag sequence yn_2, yn_1 and yn
	 * @param yn_1
	 * @param yn
	 * @return
	 */
	
	public int countTrigram(String yn_2,String yn_1,String yn) {
		String key = "["+yn_2+"]"+"["+yn_1+"]"+"["+yn+"]";
		if(chainCount.containsKey(key)) return chainCount.get(key);
		return 0;
	}
	
	public double emission(String x, String y) {
		
		double num = countWordTag(y, x);
		double den = countUnigram(y);
		
		
		return num/den;
	}
	
	public void init() throws IOException, InterruptedException {
		replaceLowFrequency();
		generateCountFile();
		loadCounts(geneCountFullPath);

	}
	
	public String getReplacedWord(String x) {
		if(frequencyClass.containsKey(x)) 
			return frequencyClass.get(x);
		//return RARE;
		return rareClass(x);
	}
	public String wordTaggerUnigram(String x) {
		
		double max = Double.NEGATIVE_INFINITY;
		String yArgMax = "";
		String xNew = getReplacedWord(x);
		//System.out.println("Word: "+xNew);
		for(String y:tagSet) {
			
			double e = emission(xNew, y);
			//System.out.println("Tag: "+y+" e: "+e);
			if(e>max) {
				max = e;
				yArgMax = y;
				
			}
		}
		
		return yArgMax;
	}

	
	
	public double q(String yAti,String yAti_2, String yAti_1) {
		double num = countTrigram(yAti_2, yAti_1, yAti);
		double den = countBigram(yAti_1, yAti);
		return num/den;
	}
	
	
	
	public double getPi(int k,String u,String v, Map<String,Double> table) {
		if(k==0 && u.equals("*") && v.equals("*")) {
			return 1.0;
		}

		return getFromTable(k, u, v, table);
		
	}
	
	public double getMax(int k, String u, String v, Map<String,Double> table, String x,int n,Map<String,String> path) {
		double max = Double.NEGATIVE_INFINITY;
		List<String> Sk_2 = getSk(k-2, n);
		//System.out.println("Sk-2:"+Sk_2);
		String wMax = "";
		for(String w:Sk_2) {
			//System.out.println("w:"+w);
			
			double val = getPi(k-1, w, u, table) * q(v, w, u) * emission(x, v);
			if(val>max) {
				max = val;
				wMax = w;
			}
			//System.out.println("pi("+(k-1)+","+w+","+u+") * q("+v+"|"+w+","+u+") * e("+x+"|"+v+")");
			//System.out.println(val);
		}
		
		putInBp(k, u, v, wMax, path);
		//System.out.println("bp("+k+","+u+","+v+") : "+wMax);
		return max;
	}
	
	public String getMapKey(int k,String u, String v) {
		String key = "["+String.valueOf(k)+"]["+u+"]["+v+"]";
		return key;
	}
	public void putInTable(int k,String u, String v, double value, Map<String,Double> table) {
		String key = getMapKey(k, u, v);
		table.put(key, value);
	}
	public double getFromTable(int k,String u, String v, Map<String,Double> table) {
		String key = getMapKey(k, u, v);
		return table.get(key);
	}
	
	public List<String> getSk(int k,int n) {
		List<String> res = new ArrayList<String>();
		if(k==-1 || k==0) {
			res.add("*");
			return res;
		}
		
		assert(k>=1 && k<=n);
		
		res.addAll(tagSet);
		return res;
		
	}
	
	public String bp(int k,String u, String v,Map<String,String> path) {
		String key = getMapKey(k, u, v);
		//System.out.println(key);
		return path.get(key);
	}
	
	public void putInBp(int k,String u, String v, String w,Map<String,String> path) {
		String key = getMapKey(k, u, v);
		//System.out.println(key);
		path.put(key, w);
	}
	
	public List<String> getPath(Map<String,Double> table, Map<String,String> path, int n) {
		List<String> res = new ArrayList<String>();
		
		double max = Double.NEGATIVE_INFINITY;
		List<String> Sk = getSk(n, n);
		List<String> Sk_1 = getSk(n-1, n);
		
		String uMax = "";
		String vMax = "";
		for(String u:Sk_1) {
			//String u = Sk_1.get(ui);
			for(String v:Sk) {
				//String w = Sk_2.get(wi);
				double val = getPi(n, u, v, table) * q(STOP, u, v);
				//System.out.println("u:"+u+" v:"+v+" pi:"+val);
				if(val>max) {
					max = val;
					uMax = u;
					vMax = v;
				}
			}
		}
		
		//System.out.println(max);
		for(int i=0;i<=n;i++) {
			res.add("NA");
		}

		

		res.set(n-1, uMax);
		res.set(n,vMax);
		
		
		for(int k=n-2;k>=1;k--) {
			
			String yk1 = res.get(k+1);
			
			String yk2 = res.get(k+2);
			
			//System.out.println("k:"+k);
			//System.out.println("k+1:"+(k+1)+" val:"+yk1);
			//System.out.println("k+2:"+(k+2)+" val:"+yk2);
			
			String yk = bp(k+2, yk1, yk2, path);
			res.set(k, yk);
			
		}
		
		res.remove(0); //removes the extra element and shifts the result array
		return res;
	}
	
	public List<String> viterbi(List<String> xWords) {
		int n = xWords.size();
		Map<String,Double> table = new HashMap<String, Double>();
		Map<String,String> path = new HashMap<String,String>();
		//double[][][] table = new double[n][sizeS+2][sizeS+2];
		
		putInTable(0, "*", "*", 1.0, table);
		
		for(int k=1;k<=n;k++) {
			int kk = k-1; // for zero based index in the list
			String x = getReplacedWord(xWords.get(kk));
			List<String> Sk = getSk(k, n);
			List<String> Sk_1 = getSk(k-1, n);
			
			//System.out.println("Word:"+x);
			//System.out.println("k:"+k);
			//System.out.println("Sk:"+Sk);
			//System.out.println("Sk-1"+Sk_1);
			
			for(String u:Sk_1) {
				//System.out.println("u:"+u);
				for(String v:Sk) {
					//System.out.println("v:"+v);
					double maxVal = getMax(k, u, v, table, x, n, path);
					putInTable(k, u, v, maxVal, table);
				}
			}
		}		
		
		return getPath(table, path, n);
	}
	
	public void a1p2(boolean test) throws IOException {

		String inFile = devFile;
		String outFile = part2DevOutFile;
		if(test) {
			inFile = testFile;
			outFile = part2TestOutFile;
		}
		
		FileInputStream fis = new FileInputStream(inFile);
		BufferedWriter out = new BufferedWriter(new FileWriter(outFile));
		
		Scanner in = new Scanner(fis);
		while(in.hasNext()) {
			List<String> x = new ArrayList<String>();
			
			while(true) {
				
				String word = in.nextLine();
				if(word.trim().isEmpty()==false) {
					x.add(word);
					
				} else {
					
					break;
				}
			}
			
			if(x.size()>0)
			{
				List<String> y = viterbi(x);
				for(int i=0;i<x.size();i++) {
					out.write(x.get(i)+" "+y.get(i));
					out.newLine();
				}
			}
			out.newLine();
			
		}
		in.close();
		out.close();
	}
	
	
	public void a1p3(boolean test) throws IOException {

		String inFile = devFile;
		String outFile = part3DevOutFile;
		if(test) {
			inFile = testFile;
			outFile = part3TestOutFile;
		}
		
		FileInputStream fis = new FileInputStream(inFile);
		BufferedWriter out = new BufferedWriter(new FileWriter(outFile));
		
		Scanner in = new Scanner(fis);
		while(in.hasNext()) {
			List<String> x = new ArrayList<String>();
			
			while(true) {
				
				String word = in.nextLine();
				if(word.trim().isEmpty()==false) {
					x.add(word);
					
				} else {
					
					break;
				}
			}
			
			if(x.size()>0)
			{
				List<String> y = viterbi(x);
				for(int i=0;i<x.size();i++) {
					out.write(x.get(i)+" "+y.get(i));
					out.newLine();
				}
			}
			out.newLine();
			
		}
		in.close();
		out.close();
	}
	
	
	public void a1p1(boolean test) throws IOException {
		String inFile = devFile;
		String outFile = part1DevOutFile;
		if(test) {
			inFile = testFile;
			outFile = part1TestOutFile;
		}
		
		FileInputStream fis = new FileInputStream(inFile);
		BufferedWriter out = new BufferedWriter(new FileWriter(outFile));
		
		Scanner in = new Scanner(fis);
		while(in.hasNext()) {
			String word = in.nextLine();
			if(word.trim().isEmpty()==false) {
				String tag = wordTaggerUnigram(word);
				out.write(word+" "+tag);	
			}
			out.newLine();
		}
		out.newLine();
		in.close();
		out.close();
	}	
	/**
	 * @param args
	 * @throws IOException 
	 * @throws InterruptedException 
	 */
	public static void main(String[] args) throws IOException, InterruptedException {

		HMM hmm = new HMM();
		hmm.init();
		//hmm.a1p1(true);
		//hmm.a1p2(true);
		hmm.a1p3(true);

	}

}
