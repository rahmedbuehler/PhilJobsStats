import csv
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns


# Pull full datalist from .csv file and only keep entries 0-8 and 10.  First list is labels.
datalist = []

with open(r"E:\Dropbox\Programming\PhilJobsStats\alljobs.csv", newline='', encoding='utf-8') as f:
	reader = csv.reader(f)
	for row in reader:
		datalist.append(row[0:9]+[row[10]])

# Presorted Area List
## Make sure more specific areas are listed first since keys are deleted from raw after use.
pre = {'Formal Epistemology':0, 'Epistemology':0, 'Decision':0, 'Political':0, 'Ancient':0, 'AI':0, 'Race':0, 'Gender':0, 'Technology':0, 'Language':0, 'Law':0, 'Applied Ethics':0, 'Business Ethics':0, 'Metaethics':0, 'Bioethics':0, 'Ethics':0, 'History of Philosophy':0, 'Religion':0, 'Data Science':0, 'Science':0, 'Mind':0, 'Modern':0, 'Metaphysics':0, 'Open':0, 'Feminist':0, 'Logic':0, 'Formal Methods':0, 'Math':0, 'Continental':0, 'Analytic':0, 'Social Choice':0, 'Cognitive':0, 'Medieval':0, 'Physics':0, 'Moral Psych':0, 'Environment':0, 'Asian':0, 'Chinese':0, 'Buddhist':0, 'Theology':0, 'African':0, 'Latin':0, 'Aesthetics':0, 'Islam':0, 'Native American':0, 'Indian':0, 'Rhetoric':0, 'Game':0, 'Biology':0, 'Kant':0, 'Psychology':0, '20th Century':0, '19th Century':0, '18th Century':0, '17th Century':0, '16th Century':0, 'Value Theory':0, 'Jewish':0, 'German':0, 'Non-Western':0, 'Pragmatism':0, 'Catholic':0, 'Phenomenology':0, 'Action':0, 'Economic':0, 'Perception':0, 'American':0, 'European':0, 'Experimental':0, 'Statistics':0, 'Practical':0, 'Critical Thinking':0, 'Theoretical':0, 'Public Policy':0, 'Set Theory':0, 'Category Theory':0, 'Arabic':0, 'Neuro':0, 'Marx':0, 'Japanese':0, 'Linguistics':0, 'French':0,'Western Philosophy':0}


def coarse_areas(specific_dict):
	'''
	Expects a dictionary where keys are the specific area and values are the number of occurrences.  Returns a new dictionary with general areas as keys and the number of occurrences as values.
	'''
	coarse = {'Epistemology':0, 'Formal Methods':0, 'Political':0, 'Western History':0, 'Non-Western History':0, 'Ethics':0, 'Language':0, 'Science':0, 'Mind':0, 'Aesthetics':0, 'Technology':0, 'Metaphysics':0, 'Religion':0, 'Social':0}
	for k,v in specific_dict.items():
		if k=='Epistemology' or k=='Formal Epistemology':
			coarse['Epistemology']+=v
		elif k=='Formal Methods' or k=='Logic' or k=='Decision' or	k=='Math' or k=='Game' or k=='Statistics' or k=='Set Theory' or k=='Category Theory' or k=='Social Choice' or k=='Critical Thinking':
			coarse['Formal Methods']+=v
		elif k=='Political' or k=='Law':
			coarse['Political']+=v
		elif k=='Western History' or k=='Ancient' or k=='History of Philosophy' or k=='Modern' or k=='Continental' or k=='Analytic' or k=='Medieval' or k=='Kant' or k=='Ancient' or k=='20th Century' or k=='19th Century' or k=='18th Century' or k=='17th Century' or k=='16th Century' or k=='German' or k=='Pragmatism' or k=='American' or k=='European' or k=='Marx' or k=='French' or k=='Western Philosophy':
			coarse['Western History']+=v
		elif k=='Non-Western History' or k=='Asian' or k=='Chinese' or k=='African' or k=='Latin' or k=='Native American' or k=='Indian' or k=='Non-Western' or k=='Arabic' or k=='Japanese':
			coarse['Non-Western History']+=v
		elif k=='Ethics' or k=='Applied Ethics' or k=='Business Ethics' or k=='Metaethics' or k=='Bioethics' or k=='Public Policy' or k=='Value Theory':
			coarse['Ethics']+=v
		elif k=='Language' or k=='Linguistics':
			coarse['Language']+=v
		elif k=='Science' or k=='Cognitive' or k=='Physics' or k=='Biology' or k=='Neuro' or k=='Economic':
			coarse['Science']+=v
		elif k=='Mind' or k=='Moral Psych' or k=='Perception' or k=='Psychology' or k=='Phenomenology':
			coarse['Mind']+=v
		elif k=='Aesthetics':
			coarse['Aesthetics']+=v
		elif k=='Technology' or k=='AI' or k=='Data Science':
			coarse['Technology']+=v
		elif k=='Metaphysics':
			coarse['Metaphysics']+=v
		elif k=='Religion' or k=='Buddhist' or k=='Jewish'  or k=='Islam' or k=='Catholic' or k=='Theology':
			coarse['Religion']+=v
		elif k=='Social' or k=='Race' or k=='Feminist' or k=='Gender':
			coarse['Social']+=v
	return coarse


# List of synonymous tags
syn = {'AI':['ai','intelligence'], 'Formal Epistemology':['formal epistemology', 'probability'], 'Epistemology':['epistemology', 'knowledge'], 'Decision':['decision', 'rational choice'], 'Technology':['technology','technologies'], 'Law':['law','legal'], 'Bioethics':['bioethics', 'medicine', 'medical', 'health'], 'Business Ethics':['business ethics', 'business'], 'Ethics':['ethics', 'ethical theory', 'ethical theories', 'moral philosophy', 'morality', 'moral theory', 'moral theories', 'moral responsibility', 'virtue theory'], 'Metaphysics':['metaphysics','ontology'], 'Ancient':['ancient','greek','roman'], 'Formal Methods':['formal methods', 'quantitative methods', 'mathematical methods', 'modeling'], 'Data Science':['data science', 'data'], '20th Century':['20th','twentieth'], '19th Century':['19th','nineteenth'], '18th Century':['18th','eighteenth'], '17th Century':['17th','seventeenth'], '16th Century':['16th','sixteenth'],'Economics':['economic'], 'Buddhist':['buddhist', 'buddhism'], 'Asian':['asian','eastern'], 'Religion':['religion', 'religious'], 'Non-Western':['non-western','non-european'], 'Critical Thinking':['critical thinking', 'critical reasoning', 'reasoning'], 'Value Theory':['value theory', 'theory of value'], 'Aesthetics':['aesthetics','art'], 'Feminist':['feminist','feminism'], 'Physics':['physics','cosmology','quantum'], 'Environment':['environment','climate']}

def presorted_parse(terms, syn, data):
	'''
	Search a list of strings <data> for particular terms---the keys in the dictionary <terms>---with possible synonyms from the list <syn>.  Returns an updated copy of <terms> where values are the number of time each key or a synonym was found.
	'''
	pre=terms.copy()
	for entry in data:
		raw = entry.lower()
		sorted = False
		for key in pre:
			if key in syn:
				synSorted = False
				for s in syn[key]:
					if not synSorted and s in raw:
						pre[key] = pre[key]+1
						synSorted = True
						sorted = True
					raw = raw.replace(s,'')
			elif key.lower() in raw:
				pre[key] = pre[key]+1
				sorted = True
				raw = raw.replace(key.lower(),'')
		# See Unsorted Inputs
		#if len(raw) > 10:
		#	sorted = False
		#if not sorted:
		#	print(raw)
	return pre
	
def sns_hbar_plot(input_dict,filename='hbar.png', chart_title='Bar Plot', x_label='Count', y_label='', small_bar_labels = False, order=None):
	'''
	Takes a dictionary <input_dict> and creates a horizontal bar plot using Seaborn.
	'''
	sns.set(style="whitegrid")

	# Initialize the matplotlib figure
	fig = plt.figure(figsize=(10,10))
	
	# Build Pandas Dataframe
	df = pd.DataFrame.from_dict(input_dict, orient='index').reset_index()
	df = df.rename(columns={'index':'y', 0:'count'})
	df = df.sort_values(by=['count'],ascending=False)
	
	#Plotting and Labeling
	ax= sns.barplot(x=df["count"], y=df['y'], data=df,order=order)
	ax.set_title(chart_title)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	if small_bar_labels:
		ax.tick_params(axis='y', labelsize=5)
	#plt.show() 
	plt.savefig("E:\\Dropbox\\Programming\\PhilJobsStats\\"+filename, bbox_inches='tight', dpi = 400)
	return df

def sns_line_plot(input_dict,filename='lplot.png', chart_title='Line Plot', x_label='Count', y_label='', x_values=range(2013,2020), col_order=None):
	'''
	Takes a dictionary <input_dict> and creates a line plot using Seaborn.
	'''
	# Begin Plotting
	sns.set(style="whitegrid")
	# Initialize the matplotlib figure
	fig = plt.figure(figsize=(10,10))

	# Build Pandas Dataframe
	df = pd.DataFrame.from_dict(input_dict, orient='columns')
	if col_order == None:
		df=df.sort_values(by=0,axis=1,ascending=False)
	else:
		df = df[col_order]
	df.index=x_values
	
	#Plotting and Labeling
	dashes = ["", (4, 1.5), (1, 1), (3, 1, 1.5, 1), (5, 1, 1, 1), (5, 1, 2, 1, 2, 1), (2, 2, 3, 1.5), (1, 2.5, 3, 1.2)]
	dashes = dashes*2
	ax= sns.lineplot(data=df, dashes=dashes)
	ax.set_title(chart_title)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	plt.xlim(x_values[0],x_values[-1])
	plt.ylim(bottom=0)
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	#plt.show() 
	plt.savefig("E:\\Dropbox\\Programming\\PhilJobsStats\\"+filename, bbox_inches='tight', dpi = 400)
	return df
	
	
#AOS
aos_datalist = [entry[3] for entry in datalist[1:]]
aos_dict=presorted_parse(pre,syn,aos_datalist)
aos_df=sns_hbar_plot(aos_dict, filename='AoS.png', chart_title='Advertised AoS on PhilJobs (2013-Present)', x_label='\nNumber of Occurrences in PhilJobs Advertisements', y_label='Area of Specialization\n', small_bar_labels = True)
coarse_aos_dict=coarse_areas(aos_dict)
coarse_aos_df=sns_hbar_plot(coarse_aos_dict, filename='CoarseAoS.png', chart_title='General AoS on PhilJobs (2013-Present)', x_label='\nNumber of PhilJobs Advertisements', y_label='General Area of Specialization\n')

# Pull 2019 and 2020 AoS Data
recent_aos_datalist = [entry[3] for entry in datalist[1:] if '2020' in entry[9] or '2019' in entry[9]]
recent_aos_dict=presorted_parse(pre,syn,recent_aos_datalist)
recent_aos_df=sns_hbar_plot(recent_aos_dict, filename='recentAoS.png', chart_title='Advertised AoS on PhilJobs (2019-2020)', x_label='\nNumber of Occurrences in PhilJobs Advertisements', y_label='Area of Specialization\n', small_bar_labels = True, order=aos_df['y'])

# Pull AoS Data By Year
first=True
for year in range(2013,2020):
	temp_aos_datalist = [entry[3] for entry in datalist[1:] if str(year) in entry[9]]
	temp_coarse_aos_dict = coarse_areas(presorted_parse(pre,syn,temp_aos_datalist))
	if first:
		yearly_coarse_aos_dict = {}
		first=False
		for k,v in temp_coarse_aos_dict.items():
			yearly_coarse_aos_dict[k]=[v]
	else:
		for k,v in temp_coarse_aos_dict.items():
			yearly_coarse_aos_dict[k].append(v)
sns_line_plot(yearly_coarse_aos_dict,filename='CoarseAoSoverTime.png', chart_title='General AoS on PhilJobs from 2013-2019', x_label='\nYear', y_label='Number of PhilJobs Advertisements\n', x_values=range(2013,2020), col_order = coarse_aos_df['y'].tolist())

#AOC
aoc_datalist = [entry[4] for entry in datalist[1:]]
aoc_dict=presorted_parse(pre,syn,aoc_datalist)
aoc_df=sns_hbar_plot(aoc_dict, filename='AoC.png', chart_title='Advertised AoC on PhilJobs (2013-Present)', x_label='\nNumber of Occurrences in PhilJobs Advertisements', y_label='Area of Concentration\n', small_bar_labels = True)
coarse_aoc_dict=coarse_areas(aoc_dict)
coarse_aoc_df=sns_hbar_plot(coarse_aoc_dict, filename='CoarseAoC.png', chart_title='General AoC on PhilJobs (2013-Present)', x_label='\nNumber of PhilJobs Advertisements', y_label='General Area of Concentration\n')

# Pull 2019 and 2020 AOC Data
recent_aoc_datalist = [entry[4] for entry in datalist[1:] if '2020' in entry[9] or '2019' in entry[9]]
recent_aoc_dict=presorted_parse(pre,syn,recent_aoc_datalist)
sns_hbar_plot(recent_aoc_dict, filename='recentAoC.png', chart_title='Advertised AoC on PhilJobs (2019-2020)', x_label='\nNumber of Occurrences in PhilJobs Advertisements', y_label='Area of Concentration\n', small_bar_labels = True, order=aoc_df['y'])

# Pull Coarse AoC Data For Completed Years
first=True
for year in range(2013,2020):
	temp_aoc_datalist = [entry[4] for entry in datalist[1:] if str(year) in entry[9]]
	temp_coarse_aoc_dict = coarse_areas(presorted_parse(pre,syn,temp_aoc_datalist))
	if first:
		yearly_coarse_aoc_dict = {}
		first=False
		for k,v in temp_coarse_aoc_dict.items():
			yearly_coarse_aoc_dict[k]=[v]
	else:
		for k,v in temp_coarse_aoc_dict.items():
			yearly_coarse_aoc_dict[k].append(v)
sns_line_plot(yearly_coarse_aoc_dict,filename='CoarseAoCoverTime.png', chart_title='General AoC on PhilJobs from 2013-2019', x_label='\nYear', y_label='Number of PhilJobs Advertisements\n', x_values=range(2013,2020), col_order = coarse_aoc_df['y'].tolist())

# VS
vs_dict={}
rel_vs_dict={}
for k,v in aos_dict.items():
	vs_dict[k] = v-aoc_dict[k]
	rel_vs_dict[k]=100*(v/(v+aoc_dict[k]))-50

coarse_vs_dict={}
coarse_rel_vs_dict={}
for k,v in coarse_aos_dict.items():
	coarse_vs_dict[k] = v-coarse_aoc_dict[k]
	coarse_rel_vs_dict[k] = 100*(v/(v+coarse_aoc_dict[k]))-50

sns_hbar_plot(vs_dict, filename='AbsVs.png', chart_title='AoS-AoC Difference on PhilJobs (2013-Present)', x_label='\nDifference in Number of PhilJobs Advertisements', y_label='Area\n',small_bar_labels = True)
sns_hbar_plot(coarse_vs_dict, filename='CoarseAbsVs.png', chart_title='General Field AoS-AoC Difference on PhilJobs (2013-Present)', x_label='\nDifference in Number of PhilJobs Advertisements', y_label='General Field\n')
sns_hbar_plot(rel_vs_dict, filename='RelVs.png', chart_title='Percentage-AoS Above Neutral(2013-Present)', x_label='\nPercentage-AoS Difference from 50%', y_label='Area\n',small_bar_labels = True)
sns_hbar_plot(coarse_rel_vs_dict, filename='CoarseRelVs.png', chart_title='General Field Percentage-AoS Above Neutral (2013-Present)', x_label='\nPercentage-AoS Difference from 50%', y_label='General Field\n')
