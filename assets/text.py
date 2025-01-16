PageHeaders = {

	"PageTitle" : "Visualising machine learning in a search for dark matter",
	"DMTitle" : "Searching for dark matter",
	"CutSubTitle" : "Why not use cut optimisation",
	"MLTitle" : "Using machine learning",
	"NNSubTitle": "Play with neural network designs",
	"DesignSubTitle" : "Which design is best?",
	"UsingMLTitle" : "How do we use our machine learning output?"	
}

PageText = {

	"DMSearches" : "POPULATE TEXT HERE",
	
	"CutOptimisation1" : "In some cases, bold cut-optimisation approach can be challenging. \
                          Suppose we are searching for a *dark matter* particle among results of a proton-proton collision. \
                          We assume that *dark matter* is made of hypothetical particles - WIMPs (weakly interacting \
                          massive particles). \
                          They are produced when Z-boson decays into a pair of WIMPs and a dilepton pair. \
                          Such event would leave traces similar to other processes, which we know do happen. \
                          On a graph below, try to play with different combinations of parameters. \
                          As you may find, the dark matter traces can be easily distinguished from **Non-resonant dilepton** \
                          and **Z+jets** processes. \
                          However, **WZ** and **ZZ** events have such large variety, that they practically hinder the other \
                          processes.",

	"CutOptimisation2" : "As you may find, the dark matter traces can be easily distinguished from **Non-resonant \
			dilepton** and **Z+jets** processes. \
                          However, **WZ** and **ZZ** events have such large variety, that they practically hinder the other \
                          processes.",


	"MLInfo1" :  "For convenience, we can approximate our complex 10-dimensional data set to a 2D projection. \
                         Popular algorithms for such visualisation are UMAP, PCA and t-SNE (check the tabs). \
                         Now there is no need to go through multiple combinations of parameters. \
                         However, the setback is that we sacrificied data variance.\
                         And still hardly can isolate the signal (Dark Matter) by optimising the cut(s).",
                         
	"MLInfo2" :  "Imagine there are not 10, but 40+ parameters to consider... In such case machine learning \
			inventory can come handy. \
                         Machine learning algorithms are capable of identifying (very) complex patterns and classifying the \
                         Signal (dark matter) from the Background (the other events). \
                         Among different algorithms, *neural networks* (NN) often produce the best results in HEP. \
                         Below you can find a model of NN: Multilayer Perceptron (MLP). \
                         It is pre-trained on Monte Carlo simulated data, and you can tinker with its configuration to check the \
                         difference in output. \
                         Select the number of hidden layers (NN depth) and vary the amount of neurons. \
                         Then, choose a specific event from the dropdown menu and press the *power button*. \
                         But don't forget to turn on the *scaler switch* - NN work best with normalised data.",	
                        
	"DesignOptimise" : "INSERT TEXT HERE",
	
	"UsingMLOut" : "Histogram above shows distribution of the NN outputs of the whole data set. \
                            Move the slider to select the (signal) data to the right cutting out (background) data to the left",
                            
	"Conclusions" : "Insert final thoughts"
}

PageLinks = {

}