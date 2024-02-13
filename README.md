# UR In-Country Missions App

This is a Django project that uses PostgreSQL as its database. The project is containerized using Docker and uses Nginx to serve static and media files.

## Prerequisites

- Python
- Docker
- Docker Compose

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

## Local Development

For local development, you need to create a `.env.dev` file in the root directory of the project with the following content:

```prod
DJANGO_ENV=dev
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DJANGO_SECRET_KEY=your_secret_key
ALLOWED_HOST=localhost,web
CORS_ORIGIN_WHITELIST=http://localhost,http://localhost:8000
CSRF_TRUSTED_ORIGINS=http://localhost,http://localhost:8000
```

Replace `your_postgres_user`, `your_postgres_password`, `your_postgres_db`, and `your_secret_key` with your actual PostgreSQL user, password, database name, and Django secret key.

Then, you can start the development server using Docker Compose:

```bash
docker-compose up
```

The application will be available at `http://localhost:8000`.

## Production Deployment

For production, you need to create a `.env.prod` file in the root directory of the project with the following content:

```prod
DJANGO_ENV=prod
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DJANGO_SECRET_KEY=your_secret_key
ALLOWED_HOST=your_domain_name,web
CORS_ORIGIN_WHITELIST=http://localhost,http://web
CSRF_TRUSTED_ORIGINS=http://localhost,http://web
```

Replace `your_postgres_user`, `your_postgres_password`, `your_postgres_db`, `your_secret_key`, and `your_domain_name` with your actual PostgreSQL user, password, database name, Django secret key, and the domain name of your application.

Then, you can start the production server using Docker Compose:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

The application will be available at `http://your_domain_name` or `http://localhost` (when running production locally).

## Static and Media Files

Static and media files are served by Nginx in both development and production environments. The static files are collected into the `staticfiles` directory and the media files are stored in the `mediafiles` directory. These directories are created in the same directory as your `manage.py` file.

In the production environment, you need to run the `collectstatic` command to collect all static files into the `staticfiles` directory:

```bash
docker-compose -f docker-compose.prod.yml run web python manage.py collectstatic --no-input
```

## Database

This project uses PostgreSQL as its database. The database is run in its own Docker container and is accessible from the Django application through the `db` service.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.