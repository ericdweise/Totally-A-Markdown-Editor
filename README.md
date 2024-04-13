TAME is Totally A Markdown Editor!


# Running TAME
## Running TAME in Docker
Run the following commands from the tame directory:

1. Build the Docker container
```bash
docker compose build
```

2. Add users to the `auth.db`. This can also be done after the Docker container has started.
```bash
python add_user.py <USERNAME> -p <PASSWORD>
```

3. Start the Docker container
```bash
TAMENOTESDIR='<YOUR-NOTES-DIRECTORY>' docker compose up -d
```


## Running on your Host
This is only for debug purposes
```bash
python3 tame.py -D
```


# License
TAME - Totally A Markdown Editor
Copyright (C) 2021 Eric D. Weise

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
