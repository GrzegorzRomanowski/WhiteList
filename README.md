# White List

## Quick introduce
The application checks whether the given company is listed on the Polish government website for taxes,
called the <i>'White List of VAT Payers'</i>. Is possible to check a single payer or multiple payers at once
(using an Excel spreadsheet) without opening a web browser.

## Single and bulk mode

The application have two tabs. One for single validation by using bank account, NIP or REGON number.
In this mode result will be printed directly in text frame in the app interface.

The second tab is for bulk validations using Excel files. On the first run folder <i>data</i> with 
<i>input.xlsx</i> will be created. Input Excel file contains one column for a bank accounts. Only polish
bank accounts with 26 digits are allowed. After the first run in bulk mode <i>output.xlsx</i> file will 
be created with 3 columns. Be careful because the Output file will always be overwritten after 
every bulk mode run!

## How to prepare and run the App?

<details>
<summary><b>1. First way: Simply using <i>WhiteList.exe</i> file. (recommended)</b></summary>

1. Copy <i>WhiteList.exe</i> file from <i>dist</i> folder and run it.
2. Excel files with bulk files will be available in folder <i>data</i> which will be made in the same
directory where <i>WhiteList.exe</i> is.
</details>

<details>
<summary><b>2. Second way: Clone repository if Python interpreter is installed.</b></summary>


1. Clone this project.
2. You need to have installed Python 3 (the script was developed on version 3.11).
3. Create a virtual environment and install requirements:
- go to the folder where you cloned the project from the repository
~~~Windows PowerShell
PS> cd "path_with_cloned_project"
~~~
- create a virtual environment
~~~Windows PowerShell
PS> python -m venv venv
~~~
- activate it
~~~Windows PowerShell
PS> venv\Scripts\activate
~~~
- ensure you are using a virtual environment by checking the prefix (venv) in your console and
then install the requirements
~~~Windows PowerShell
(venv) PS> python -m pip install -r requirements.txt
~~~
4. Run the "<i>main.py</i>" file.
5. Other Python files '<i>(...).py</i>' shouldn't be launched directly.
6. Excel files with bulk results will be available in folder <i>data</i>.
</details>
