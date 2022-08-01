# W5 Project - Geoqueries
​
## Premise
​
The following task has been assigned to me:

You recently created a new company in the GAMING industry. The company will have the following scheme:

- 20 Designers
- 5 UI/UX Engineers
- 10 Frontend Developers
- 15 Data Engineers
- 5 Backend Developers
- 20 Account Managers
- 1 Maintenance guy that loves basketball
- 10 Executives
- 1 CEO/President.
As a data engineer you have asked all the employees to show their preferences on where to place the new office. Your goal is to place the new company offices in the best place for the company to grow. You have to find a place that more or less covers all the following requirements (note that it's impossible to cover all requirements, so you have to prioritize at your glance):

- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company staff have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not too far.
- Account managers need to travel a lot.
- Everyone in the company is between 25 and 40, give them some place to go party.
- The CEO is vegan.
- If you want to make the maintenance guy happy, a basketball stadium must be around 10 Km.
- The office dog—"Dobby" needs a hairdresser every month. Ensure there's one not too far away.
​
## Approach
​
From a dataset of 18000 companies around the world and all of their offices I will try to pick the one that better fulfills my requirements. For simplicity I have picked the subset of only the offices located in Barcelona, Madrid and Valencia, but the code is scalable to pick the best venue in the whole world.

The criteria for which venue is the best is based on distance to the places that fulfill each of the requirements, how many employees are affected by them, the importance of an affected employee to the company and the relative importace of each requirement to an employee. The details are written in the notebook.

At the end of the notebbok there are three maps, one for the best venue in each city and all of the surrounding nearest places that fulfill the requirements.
​
## Project files
​
The main directory has 2 subdirectories:

* Output: Contains files created from the original data (enriched and cleaned dataframes, plots, etc.) that are used multiple times through the project.
* src: Contains python files with all functions created specifically for this analysis.
​
In the root directory there is a Jupyter Notebook file that includes all the code used in the project, explaining the process at the same time