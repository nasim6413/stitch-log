# StitchLog
A web-based tool for managing cross-stitch and embroidery projects, track embroidery floss inventory, and converting between thread brands (DMC and Anchor). Built using Flask and SQLite3.

## Features

📦 **Track Floss Inventory** – View and manage your current stock of embroidery floss.

🔄 **Convert Between Brands** – Convert between different floss brands (e.g., DMC ↔ Anchor).

🧵 **Project Management** – Create and track cross-stitch or embroidery projects, including required colors and progress. (Currently reworking)

📄 **Pattern PDF Upload** – Upload a pattern in PDF format and extract the list of required floss colors.

![Alt Text](https://i.imgur.com/hluPyym.gif)

## Getting Started
### Requiremegithub readms
- Raspberry Pi
- Docker

### Installation

1. Clone the repository

```bash
git clone https://github.com/nasim6413/stitch-log.git
cd stitch-log
```

2. Build and start app using Docker

```bash
docker compose up --build
```

The app will be available at http://localhost, or `http://<raspberrypi-ip>` if accessing from another device. 

### (Optional) Backups
You can set up a cron job to create a regular backup using https://crontab.guru/.

To set up the backups:

1. Create a `backups` folder in the directory

```bash
mkdir -p /home/pi/stitch-log/backups
```

2. Open the crontab editor on the Raspberry Pi

```
crontab -e
```

3. At the bottom, add the following line:
```bash
0 12 * * 7 tar -czf /home/pi/stitch-log/backups/backup-$(date '+\%Y-\%m-\%d').tar.gz -C /home/pi/stitch-log instance
```

(Adjust the `0 12 * * 7` to change the schedule.)

4. Save and exit the editor: `Ctrl + O` -> `Enter` -> `Ctrl + X`

## Credits

- Background image: "Aesthetic Anime City at Dusk" by ruslan-abaev_97 from Wallpapers.com.
- Fonts: 
    - "Mystery Quest" by Astigmatic, from Google Fonts.
