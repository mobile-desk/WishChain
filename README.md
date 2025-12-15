# WishChain

A platform connecting people in need with those who can help, one wish at a time.

## Features

- Create and manage wishes
- Browse and fulfill wishes
- Secure donation processing
- Impact tracking
- Partner/NGO integration

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL (recommended)
- Redis (for caching and async tasks)

### Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements/development.txt`
4. Set up environment variables (copy .env.example to .env and configure)
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

## Project Structure

```
WishChain/
├── config/            # Project configuration
├── apps/              # Django apps
├── static/            # Static files
└── templates/         # Base templates
```

## Development

- Run tests: `python manage.py test`
- Run with debug toolbar: `python manage.py runserver_plus`
- Run linter: `flake8`
- Run formatter: `black .`

## License

MIT

