- 2.0.4 introduces major database improvements, comprehensive documentation updates, and code quality enhancements for better reliability and maintainability.

### Database Improvements

- **New DatabaseService class** with proper connection pooling and context managers for safe resource cleanup
- **Refactored all database queries** to use the new connection pooling system, eliminating connection leaks
- Fixed database connection race condition on container startup with retry logic and exponential backoff
- Updated docker-compose.yml to use health checks, ensuring PostgreSQL is fully ready before bot starts
- Pinned PostgreSQL to version 15 for stability
- Added fail-fast behavior if database connection fails after all retry attempts

### Documentation

- Added comprehensive **Installation Guide** with step-by-step setup instructions
- Updated README with installation quick-start section
- Reorganized documentation structure for better navigation

### Music & Playback

- Updated Youtube-Source plugin from 1.12.0 to 1.16.0 for improved playback stability

### Code Quality

- Improved code organization and maintainability across multiple modules
