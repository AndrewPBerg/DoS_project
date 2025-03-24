# Project Overview 🌐

This project consists of three main components:

1. **Frontend**: A Django web application with a Google Gemini API integration. 🖥️
2. **Backend**: A Java microservice built with Maven and Spring Boot. ⚙️
3. **DoS Demo**: A collection of Python scripts demonstrating various Denial of Service (DoS) attack techniques. 🐍


## Frontend 🖥️

The frontend is a Django web application located in the `Frontend` directory. It integrates with the Google Gemini API for enhanced functionality.

### Setup 🔧

1. Set up the Google Gemini API:
   - Create a [Google Gemini API](https://ai.google.dev/gemini-api/docs/api-key) account and generate an API key. - Create a `.env` file in the `frontend/dictionary` directory.
   - Set the `GOOGLE_API_KEY` environment variable to your API key in the `.env` file:
     ```
     GOOGLE_API_KEY="your_api_key_here"
     ```
> [💡 Copy the .env.example to a .env filee](https://github.com/AndrewPBerg/DoS_project/blob/main/Frontend/dictionary/.env.example)
2. Install Python dependencies and run using the uv package manager:
   ```bash
   cd Frontend
   uv run manage.py runserver
   ```
> [💡See the UV docs on installation](https://docs.astral.sh/uv/getting-started/installation/)


## Backend ⚙️

The backend is a Java microservice built with Maven and Spring Boot. It is located in the `Backend/HashTableService` directory.

### Setup 🔧

1. Ensure Maven is installed:
   ```bash
   mvn --version
   ```
> [💡 If not installed, download Maven from ](https://maven.apache.org/download.cgi).

2. Verify the Java version in the `pom.xml` file:
   ```xml
   <properties>
       <java.version>example_version</java.version>
   </properties>
   ```
> Check your current Java version with `java -version` and update the `pom.xml` if needed.

3. Start the Maven service:
   ```bash
   cd Backend
   mvn clean compile
   mvn spring-boot:run
   ```

## DoS Demo 🐍

The `dos_demo` directory contains a collection of Python scripts that demonstrate various Denial of Service (DoS) attack techniques. These scripts are for educational purposes only and should be used responsibly in controlled environments.

### Setup 🔧

1. Install dependencies using the uv package manager:
   ```bash
   cd dos_demo
   uv run multi_threaded.py
   ```

### Scripts 🦾

- `single_thread.py`: A single-threaded DoS script.
- `multi_threaded.py`: A multi-threaded DoS script with improved performance and error handling.

> [Refer to the `dos_demo/README.md` file for detailed usage instructions and important disclaimers.](https://github.com/AndrewPBerg/DoS_project/tree/main/dos_demo)

## Getting Started 🚀

1. Set up and start the Frontend Django server.
2. Set up and start the Backend Maven service.
3. Explore the DoS demo scripts in the `dos_demo` directory.

Please use the DoS demo scripts responsibly and only in authorized environments for educational purposes.