# Coffee Machine E-commerce Application

This is a web-based e-commerce application built with Django, HTML, CSS, and Bootstrap for a coffee machine company. The application allows customers to purchase coffee machines and related accessories online.

## Features

The key features of the application are:

- User authentication: Users can create accounts, log in, and log out.
- Product catalog: Users can browse through a range of coffee machines and accessories available for purchase.
- Product details: User can add see details of product purchase it.
- Shopping cart: Users can add products to their shopping carts and proceed to checkout.

## Installation

To run this application on your local machine, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/lytsl/decom.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the following commands to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Finally, start the development server:

```bash
python manage.py runserver
```
