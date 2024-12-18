# PTCG Auto Tools

A collection of automation tools for PTCG (Pokemon Trading Card Game), including auto friend adding and email notifications.

## Features

- **Auto Add Friend**: Automatically monitors and clicks the add friend button
- **Email Notifications**: Sends alerts when the button remains dark for 1 minute
- **Button Finder**: Utility to find screen coordinates for buttons

## Prerequisites

- Python 3.7 or higher
- Gmail account (for email notifications)

## Installation

1. Clone the repository: 

``` bash
git clone https://github.com/yourusername/ptcg.git
cd ptcg
```

2. Install required packages:

``` bash
pip install -r requirements.txt
```


3. Create a `.env` file in the project root with your email settings:
   
```env
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=recipient_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```


## Usage

### Button Finder
To find the coordinates of a button: