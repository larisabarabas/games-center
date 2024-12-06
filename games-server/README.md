# Technical Test

This API provides access to a list of games. You can:

- Retrieve a paginated list of games.
- Filter games by platform.
- Sort games by title or release date.
- Fetch details of a specific game by ID.

## Build

1. Ensure you have Docker installed (Download from [here](https://www.docker.com/products/docker-desktop/)).
2. Build the Docker image:

```bash
docker build -t games-server .
```

3. Run the Docker container:

```bash
docker run -p 8000:8000 games-server
```

The API will be available at [http://localhost:8000/games](http://localhost:8000/games).

## API Endpoints

### Get List of Games

Retrieves a paginated list of games with optional filtering and sorting.

- **URL**: `/games`
- **Method**: `GET`
- **Query Parameters**:

  - `page`: (Optional) Page number, defaults to `1`.
  - `limit`: (Optional) Number of results per page, defaults to `10`.
  - `sort_by`: (Optional) Field to sort by (`title` or `release_date`).
  - `order`: (Optional) Sort order (`asc` for ascending, `desc` for descending), defaults to `asc`.
  - `filter_platform`: (Optional) Filter by platform (e.g., `PlayStation 5`).

- **Example Request**

```bash
GET /games?page=1&limit=5&sort_by=release_date&order=desc&filter_platform=PlayStation%205
```

- **Response**:

```json
{
  "total": 2,
  "page": 1,
  "limit": 5,
  "games": [
    {
      "id": 4,
      "title": "Gran Turismo 7",
      "release_date": "2022-03-04"
    },
    {
      "id": 6,
      "title": "Ratchet & Clank: Rift Apart",
      "release_date": "2021-06-11"
    }
  ]
}
```

### Get Game Details by ID

Retrieves the details of a specific game by its ID.

- **URL**: /games/{game_id}
- **Method**: GET
- **URL Parameters**:

  - `game_id`: The ID of the game to retrieve.

- **Example Request**:

```bash
GET /games/1
```

- **Response**:

```json
{
  "game": {
    "id": 1,
    "title": "Marvel's Spider-Man 2",
    "release_date": "2023-10-20",
    "studio": "Insomniac Games",
    "platform": "PlayStation 5",
    "enabled": true,
    "telemetry_events": [
      {
        "event_name": "Player_Login",
        "enabled": true
      },
      {
        "event_name": "Mission_Complete",
        "enabled": true
      },
      {
        "event_name": "Boss_Fight_Started",
        "enabled": true
      },
      {
        "event_name": "Bug_Report_Submitted",
        "enabled": false
      }
    ]
  }
}
```

### Error Handling

#### 404 Not Found

Returned if a game with the specified ID does not exist.

- **Response**:

```json
{
  "detail": "Game not found"
}
```

### Notes

- Query parameters like page, limit, sort_by, and filter_platform are optional and can be used to control pagination, sorting, and filtering of the results.
- Pagination is supported via the page and limit parameters.
- Sorting is available by title or release_date and can be ordered in ascending or descending order.
- You can filter games by platform (e.g., PlayStation 4, PlayStation 5).
