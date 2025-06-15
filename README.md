# Self-Edu

This is a minimalist offline organizer for systematizing the learning process, allowing you to plan your schedule, manage tasks with completion marks, and store and categorize useful links and materials with a flexible tagging system.

> **Currently, Russian is set as the default language in the app, but English will be available soon.**
---

## Instalation 

### 1. Requirements

- Python 3.10 or higher ([download here](https://www.python.org/downloads/))
- [Git](https://git-scm.com/downloads) (optional, only if cloning the repository)

****

### 2. Installing from Source

For developers or users who want the latest version, follow these steps:

1. Clone the repository

```bash
git clone https://github.com/cyweee/self-edu.git
```

2. Change to the project directory

```bash
cd self-edu
```

3. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS  
.\venv\Scripts\activate       # Windows
```

4. Install requirements:

```bash
pip install -r requirements.txt
```

5. Run the application using the module syntax:

```bash
python -m app.main # Windows
python3 -m app.main # Linux/macOS
```

****

### 3. Installing from Release (for end users)

If you do not intend to modify the source code, it is recommended to use a pre-built version from the [Releases](https://github.com/cyweee/self-edu/releases) section.

#### Steps:

1. Download the appropriate archive (`.zip` or `.tar.gz`) for your operating system.
2. Extract the archive to a directory of your choice.
3. Navigate to the extracted folder and run the executable or startup script:

**Windows:**
- Launch using `Self-Edu.exe`, `start.bat`, or another provided executable file.

**Linux:**

- Open a terminal and navigate to the extracted folder.
- Make the binary executable (if necessary):

```bash
chmod +x self-edu
```

- Then run the application:
> !!! If execution is blocked due to permissions, ensure the file has executable rights and that your system allows running binaries from that location.

**macOS:**

- Launch `Self-Edu.app` if available.
- If a script or binary is provided:
1. Open System Settings > Privacy & Security.
2. Scroll down to the warning about the blocked app and click "Allow Anyway".
3. Try launching the app again.
- Alternatively, you can launch it from the terminal:

```bash
open Self-Edu.app
```
****

## Issues

If you see any issues, just drop them in the [Issue](https://github.com/cyweee/self-edu/issues) section, and we'll figure it out together.

****

## Future of project 

The project will continue to develop and be updated to new, better, and more advanced versions. Technical documentation will also be added in the near future.