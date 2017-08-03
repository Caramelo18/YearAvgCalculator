This script allows you to compare your grades with the remaining ones.
It calculates how many people are above or below your grade, and it also calculates each semester/year average.

In order to run, you must follow this steps:

Create a virtual environment using:
python3 -m .

Activate virtual environment:
cd bin
source activate
cd ..

Install the necessary packages:
pip install -r requirements.txt

Copy the chromedriver to your PATH. This command should work:
sudo cp chromedriver /usr/bin

After this steps you shold be fine to run this:
python3 average.py

It will ask your username (don't forget to include "up") and your password. This will not store your password.


Any suggestions are welcome.
