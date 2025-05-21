PageHeaders = {

	"PageTitle" : "Visualising machine learning in a search for dark matter",
	"DMTitle" : "Searching for dark matter",
	"CutSubTitle" : "Why not use cut optimisation?",
	"MLTitle" : "Using machine learning",
	"NNSubTitle": "Play with neural network designs",
	"DesignSubTitle" : "Which design is best?",
	"UsingMLTitle" : "How do we use our machine learning output?"	
}

PageText = {

	"DMSearches" : 
			"Although particle physicists have the **Standard Model** to explain the 'ordinary' matter we see \
			and most of its forces, this can only account for about **5%** of the content of the Universe. Experimental \
			evidence from observations of distant galaxies indicate that 70% of the Universe's energy content can be \
			labelled as **dark energy** - some force which drives the accelerating expansion of the Universe although its \
			exact origins are still unknown. The remaining 25% of the Universe's energy content is something called **dark matter**, \
			so called because its gravitational effects on galaxies can be observed although the matter itself is invisible to direct \
			observation. \n \
			Despite the Standard Model being one of the best tested in physics, it isn't a so-called *theory of everything*: \
			it *cannot* describe gravitational interactions, dark energy, nor can it describe *dark matter*. \
			This is why particle physicists are interested in conducting *searches* for **new physics** beyond the Standard Model, \
			such as for candidate dark matter particles. One such type of dark matter candidate 	are **WIMPS**, or *weakly \
			interacting massive particles* which we can try to find at the large hadron collider.",
	
	"CutOptimisation1" : 
			"In the first instance, particle physicists may try some bold cult-optimisation approach to select candidate events. \
			 However, this can be challenging. \
                          Suppose we are searching for a WIMP *dark matter* particle among results of a proton-proton collision. \
                          They are produced when *Z*-boson decays into a pair of WIMPs and a dilepton pair. \
                          Such event would leave traces similar to other known processes which we have observed and continue to see quite regularly.\n \
                         	 Some of these known processes are called **irreducible backgrounds** because their observed behaviour is too similar to \
	 		 be easily distinguished from the process of interest. Whether or not a background is *irreducible* depends on what we can see in \
			 our measurements. For every event, processes are measured for a range of *variables*. If one or more variables clearly show different \
			 trends, then a background process is easily reducible. If not, then it is irreducible and a more complex approach is probably needed.\n \
                          On a graph below, try to play with different combinations of measured variables to determine the separation between the dark matter \
                          signal and its backgrounds. Are some variables more powerful than others? Which backgrounds are reducible and which are irreducible?",

	"CutOptimisation2" : 
			"Text on what someone should expect to see.",


	"MLInfo1" :  
			"For convenience, we *could* approximate our complex 10-dimensional dataset to a lower-dimensional projection, \
			much like taking the 2D image of a 3D object. One popular method is through *principle component analysis* or PCA \
			and it would allow us to see the signal vs. background separation in a less complex parameter space. \
                         However, the setback is that we sacrifice data variance and we still wouldn't be able to isolate the dark matter signal \
                         sufficiently in a cut-optimised search.",
                         
	"MLInfo2" :  
			"Imagine there are not 10, but 40+ parameters to consider, and we *still* can't separate out the dark matter signal \
			using a cut-based approach.  In such case machine learning can be a really powerful tool. \
                         Machine learning algorithms are capable of identifying (very) complex patterns and classifying the \
                         Signal (dark matter) from the background (the other events). \
                         Among different algorithms, *neural networks* (NN) often produce the best results in particle physics.\n \
                         Below you can find a model of one type of NN called a **multilayer perceptron** (MLP). \
                         Several variations of this model has been pre-trained on Monte Carlo simulated data to separate \
                         dark matter signal from its backgrounds. You can tinker with the configuration to check the difference in *performance*. \
                         In machine learning, comparing different variations of the same model to select the best one is called *hyper-parameter \
                         optimisation* and it is a critical step in particle physics to make sure we get the best results we can.\n \
                         1) Make your choice of *hyper-parameters* below by selecting the number of hidden layers and varying the size of each layer.\n \
                         2) Select the 'Power on' icon to discover what the model's *overall performance* is from its **accuracy** and **F1-score** metrics.\n \
                         3) Choose a specific event from the dropdown menu to see how its *input* (measurement of key variables) is used in the MLP and how \
                         it is categorised by the model in the *output*.\n Which variation(s) work best? Which processes are well separated and which are not?. \
                         **Have a play!**",	
                        
	"DesignOptimise" : 
			"In the above visualisation you are given only a discrete number of simulated events from which to compare the signal and background \
			probabilities determined by the MLP model. However, *in reality* a machine learning model should be optimised *generally* to best separate \
			as many signal events from background as possible. This is where overall or *aggregate* metrics can be useful measures of comparison. However, \
			scores such as total **accuracy** and **F1-score** may not show the complete story and have their own limitations. In the case presented here, we know \
			the dark matter signal is significantly smaller than the total background. This means that overall accuracy may be reported to be, say, 98% even if the model \
			is extremely poor at identifying dark matter events correctly as signal.\n \
			This is where comparing the classification of a *range* of events is often more prescriptive. The plot below shows how unseen simulated data is classified into \
			signal and background based on the trained model's output. The dark matter signal is in orange while the other background events are in blue. For a perfect classifier, \
			we would observe signal and background sorted perfectly between 0 and 1. **To see this, turn off the MLP above...**\n \
			In reality, machine learning models will not achieve such perfect separation. However, comparing distributions such as the one below can help to maximise the separation for \
			a range of events. **For different variations of the MLP,**\n \
			1) Have a look at the distribution of the background event classification. How does this compare between variations of the MLP?\n \
			2) Have a look at the distribution of the signal event classification. Does this change much between MLP variations? How well separated can this get from the background?",
	
	"UsingMLOut" : 
			"As you may have observed, even after our hyper-parameter optimisation, we still reach a limitation in the maximum separation of our dark matter signal from its background. \
			At any given MLP output probability, the model will output some number of both signal and background events with this classification. Therefore, rather than attempt to seek \
			some 100% pure signal selection, particle physics aims to maximise the **significance** of selected signal above its background in any given selection. This is a *statistical* \
			measure for how well a selection targets the signal of interest where the higher the significance (measured in $\sigma$), the better the selection. In particle physics, 3$\sigma$ \
			is brilliant for raising a few eyebrows, but 5$\sigma$ is the 'gold standard' when trying to claim a discovery. So the final step is to look for a selection cut on our machine learning output \
			probability which maximise the measured significance of the signal. \n \
			Move the slider to select as much signal to the right while cutting out background to the left in order to maximise the signal significance. What's the best you can achieve? What about for \
			different MLP configurations?",
                            
	"Conclusions" : "Insert final thoughts"
}

PageLinks = {

}