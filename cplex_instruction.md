## Instruction for CPLEX Python API

#### 1. Download and install CPLEX Optimization Studio
Download [IBM ILOG CPLEX Optimizer](
http://www-01.ibm.com/software/websphere/products/optimization/cplex-studio-community-edition/), then install it step by step.

####  2. Download and install "Visual C++ Redistributable Packages for Visual Studio 2013"(Windows only)
[Visual C++ Redistributable Packages for Visual Studio 2013](https://www.microsoft.com/en-US/download/details.aspx?id=40784)

####  3. Install python.
SPSS Modeler prefer [Anaconda python (2.7)](https://www.continuum.io/downloads).

####  4. Install CPLEX python package
Go to {CPLEX Optimization Studio install folder}\cplex\python\2.7\{os} and run "python setup.py install"

Notes: 
- a. refer to this [link](
http://www.ibm.com/support/knowledgecenter/SSSA5P_12.5.1/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html) for more detail information.

####  5. Run "pip install docplex"
Ensure pip enable, and run `pip install docplex` to install [docplex](https://pypi.python.org/pypi/docplex) package.

####  6. Download sample code 
Download sample code from [github docplex example](https://github.com/IBMDecisionOptimization/docplex-examples).

####  7. In console run 
`python \examples\mp\modeling\diet.py`

#### Configure success if get result.
```
Model: diet
 - number of variables: 9
   - binary=0, integer=0, continuous=9
 - number of constraints: 7
   - linear=7
 - parameters: defaults
* model solved as function:
objective: 2.690
  "Spaghetti W/ Sauce"=2.155
  "Lowfat Milk"=1.831
  "Chocolate Chip Cookies"=10.000
  "Hotdog"=0.930
* KPI: Total Calories=2000.000
* KPI: Total Calcium=800.000
* KPI: Total Iron=11.278
* KPI: Total Vit_A=8518.433
* KPI: Total Dietary_Fiber=25.000
* KPI: Total Carbohydrates=256.806
* KPI: Total Protein=51.174
```
