First of all python and mysql should be installed

Open Command Prompt in this directory

Run : pip install -r Requirements.txt


Open MYSQL TERMINAL:

Command 1 : create database Flask;

Command 2 :

CREATE TABLE `flask` (
  `UserName` varchar(50) NOT NULL,
  `Email` varchar(600) NOT NULL,
  `Passwd` varchar(600) NOT NULL,
  `UDate` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`UserName`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


####################	Run the Index.py file and let it run in the background	####################


Open your web browser and type

http://localhost:5000/

Your website should now be running 