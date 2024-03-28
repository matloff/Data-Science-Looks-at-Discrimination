
# DSLD: Data Science Looks at Discrimination (An R Package)

Authors: 
- Norm Matloff
- Taha Abdulla
- Aditya Mittal
- Arjun Ashok
- Shubhada Martha
- Billy Ouattara
- Jonathan Tran
- Brandon Zarate

## Overview

Discrimination is a key social issue in the US and in a number of other
countries. There is lots of available data with which one might
investigate possible discrimination. But how might such investigations
be conducted?

Our **DSLD** provides statistical and graphical tools for detecting and 
measuring discrimination and bias; be it racial, gender, age or other. 
This is an R package. It is widely applicable, here are just a few use cases:

- Quantitative analysis in instruction and research in the social sciences.
- Corporate HR analysis and research.
- Litigation involving discrimination and related issues.
- Concerned citizenry.

## Installation:

The package can be installed using the **devtools** package:

```R
library(devtools)
install_github("matloff/dsld", force = TRUE)
```

[WAITING TO PUT ON CRAN]

## Analysis categories:

- In the estimation realm, say investigating a possible gender pay gap.
In doing so, we must be careful to account for *confounders*, variables
that may affect wages other than through gender.

- In a prediction context, with concern that an AI algorithm has built-in
bias against some racial group.  We want to eliminate race from the
analysis, and to also limit the effect of *proxies*, other variables
that may be strongly related to race.

In the first case, we are checking for *societal* or *institutional*
bias. In the second, the issue is *algorithmic* bias.

To distinguished between a "fair ML" dataset and a "statistics" one. Here is a side-by-side comparison:

<table border="1">

   <tr>
   <th>statistics</th>
   <th>fair ML</th>
   </tr>

   <tr>
   <td>estimate an effect</td>
   <td>predict an outcome</td>
   </tr>

   <tr>
   <td>harm comes from society</td>
   <td>harm comes from an algorithm</td>
   </tr>

   <tr>
   <td>include sensitive variables</td>
   <td>exclude sensitive variables</td>
   </tr>

   <tr>
   <td>adjust for covariates</td>
   <td>use proxies but limit their impact</td>
   </tr>

</table>

## Quarto Book

A quarto book is provided to serve as a guide to key statistical principles and their applications, providing a more detailed analysis of the examples denoted below. 

## Part One: Adjustment for Confounders 

In this case, we wish to *estimate the impact* of a sensitive variable S on an outcome variable Y, 
while *accounting for confounders* C. Let's call such analysis "confounder adjustment." The package 
provides several graphical and analytical tools for this purpose.

### Example

We are investigating a possible gender pay gap using **svcensus** data. [Y] is wage and [S] is gender. 
We will treat age as a confounder [C], using a linear model.

```R
> data(svcensus)
> svcensus <- svcensus[,c(1,4,6)]  # subset: age, wage, gender
> z <- dsldLinear(svcensus,'wageinc','gender')
> coef(z)

$gender
(Intercept)         age  gendermale 
 31079.9174    489.5728  13098.2091 
```
Our linear model can be written as: 

> E(W) = $\beta_0$ + $\beta_1$ A + $\beta_2$ M

Here *W* indicates wage income, *A* is age and *M* denotes an indicator variable, with M = 1 for men and M = 0 for women.

Thus, we can speak of $\beta_2$ as *the* gender wage gap, at any age. According to the model, younger men earn an estimated $13,000 more than
younger women, with the *same-sized* gap between older men and older women. 

Note that we chose only one [C] variable here, age.  We might also choose "occupation", or any other combination depending on the dataset.

## Part Two: Discovering/Mitigating Bias in Machine Learning

In this case, our goal is to predict [Y] from [X] and [O], omitting [S]. We are concerned that we may be indirectly using [S] via proxies [O] and want to limit their usage.
The inherent tradeoff of increasing fairness is reduced utility (reduced predictive power/accuracy). The package provides wrappers for several functions for this purpose.

### Example

Consider the **svcensus** example again. We are predicting the wage [Y], the sensitive variable [S] is gender, with the proxy [O] as occupation. 
The proxy [O] "occupation" will be deweighted to 0.2 using the *dsldQeFairKNN* function to limit its predictive power.

<table border="1">

   <tr>
   <th>Fairness/Utility Tradeoff</th>
   <th>Fairness</th>
   <th>Accuracy</th>
   </tr>

   <tr>
   <td>K-Nearest Neighbors</td>
   <td>0.1943313</td>
   <td>25452.08</td>
   </tr>

   <tr>
   <td>Fair K-NN (via EDFFair)</td>
   <td>0.0814919</td>
   <td>26291.38</td>
   </tr>
</table>

We can see that the correlation between predicted wage income and gender has decreased significantly. Conversely, test Accuracy increased by about \$700 dollars. Thus, we see an increase in fairness at some expense of accuracy.

## Function List
- **DsldLinear**/**DsldLogit**: Comparison of conditions for sensitive groups via linear/logistic models
- **DsldML**: Comparison of conditions for sensitive groups via ML algorithm
- **DsldTakeLookAround**: Evaluates feature sets for predicting Y while considering correlation with sensitive variable S
- **DsldScatterPlot3D**: Plots a dataset on 3 axes, with the color of the point depending on a 4th variable
- **DsldCHunting**: Confounder hunting--searches for variables C that predict both Y and S  
- **DsldOHunting**: Proxy hunting--searches for variables O that predict S.
- **DsldConditsDisparity**: Plots mean Y against X for each level of S, revealing potential Simpson's Paradox-like differences under specified conditions
- **DsldConfounders**: Analyzes confounding variables in a dataframe 
- **DsldFreqPCoord**:  Wrapper for the freqparcoord function from the freqparcoord package
- **FairML wrappers**: Wrappers for several FairML functions via the FairML package
- **EDFFair Wrappers**: Wrappers for several EDFFair functions via the EDFFair package
