# Overview

A desktop App to interface with ANY database connection and easily filter and extract the data you need to an excel file. 

## About The Project

### Built With

* Python
   * ODBC connection library for backend database connection
   * QT library for UI
* SQL Server

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

The app itself can by run using python on your local machine (on any OS). 

Not included in this repo is the .app version of the project that let's you launch the app with a click of a button. If you would like this, either: 

* email me and ask for it
* use a tool (such as ```pyinstaller```, depending on your OS) to create the packaged version. 

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/rhudaj/DatabaseInterfaceApp.git
   ```

2. Install Dependencies & launch the app

   ```sh
   cd 'DatabaseInterfaceApp/SOURCE code'
   pip install -r requirements.txt
   python main.py
   ```

<!-- USAGE EXAMPLES -->
## Usage

The app itself walks you through how to setup a DB connection (using the start page, DB connection settings) and the UI elements for selecting/filtering from the DB are layed out intuitively. Simply use the UI to build your query, and output the results on the final page. 


<!-- CONTACT -->
## Contact

Roman Hudaj - rhudaj@uwaterloo.ca

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

N/A
