# NLI-Process-Data-Querying
This project contains the files required to replicate the experiments described in the published paper "An intent-based Natural Language Interface for Process Execution Data" using the BPIC'17 event log.

The user should first populate an LPG graph in Neo4j with the BPIC'17 data, then make minor changes to the files, and finally run the code to get the messaging interface to ask and receive questions.

The detailed instructions are described below:

1- Download Neo4j Desktop and create a DBMS (to store the graph of the  data set).

2- Open the python code with Pycharm or any other python IDEs.

3- In the ReadRealData.py file:
	i- Change the authentication parameteres of the graph in Neo4j by the the user's username and password (L. 24).
	ii- Change the location path of BPI Challenge 2017 (filtered2) file(L. 27).
  
5- In the QueryConstructor.py file:
	i- Change the authentication parameteres of the graph in Neo4j by the the user's username and password (L. 7).

Evaluation with BPI data set (Loan application):
----------------------------------------
* To populate the graph in Neo4j with the dataset, start a DBMS in Neo4j and run the ReadRealData file. 
* Run the ChatBotGUI class to display the conversational interface for asking a question and receiving an answer.

Note: In the program's console, the user can see the extracted entities, the constructed query, 
      and the answer to the question.
      
      
Evaluation with other data set:
-------------------------------
  * Change the code in the ReadRealData.py file to match the data set file structure, so that it reads the data from the data file and creates the corresponding LPG with this data. 
