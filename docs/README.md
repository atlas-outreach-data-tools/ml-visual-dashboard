# ml-visual-dashboard
Web-app and backend code for ML visual dashboard
The App is built in Dash framework (https://dash.plotly.com) and can be run in any IDE supporting Python. 

## Quick start (local tests)
### Conda setup
If you have Conda, simply run
```
source setup.sh
```
First time initialisation creates a suitable Conda Python environment with the appropriate dependencies for this App.

### Running the App
To run the ML visual dashboard in a local environment, do
```
python runApp.py
```
and copy the provided link into a web browser. It should look something like
```
http://127.0.0.1:7777
```

## Docker Image
A Dockerfile is provided to allow deployment of this webapp as a Docker image which also indicated the commands needed to run the ML WebApp if one wishes to bypass pakcage installation in conda and use menv instead.

## Package components

## Backend data

Backend data needed to power the various plots and displays on the UI are generated and stored in **csv** format.
Once **RegenerateModels.py** has been called once (either through **setup.sh** or in isolation), the ML visual 
dashboard can run entirely disconnected from the internet.

The backend data is generated using ATLAS Open Data and using it to train and assess various scikit-learn neural 
network configurations. The setup is seeded so should lead to reproducible results accross machines. 

## Licensing

## Dash
The Dash framework is a free toolkit for powering web-apps using Python-based templates and functions.
The core features are given [here](https://dash.plotly.com/dash-core-components). For details relevant 
to parts of this Web-App, please refer to the following:

- [Scatter plot](https://plotly.com/python/reference/scatter)
- [Neural network plot](https://plotly.com/python/reference/sankey)
- [Histograms](https://plotly.com/python/reference/histogram)
- [Layout](https://dash.plotly.com/layout) and [creating figures](https://plotly.com/python/creating-and-updating-figures/)  

## Maintainers and developers

- Caley Yardley, University of Sussex
(caley.luce.yardley@cern.ch).
Developer & maintainer.

- Giovanni Guerrieri, CERN
(giovanni.guerrieri@cern.ch).
Maintainer.

- Andrey Kukhmay, University of Sussex.
Prototype developer.
