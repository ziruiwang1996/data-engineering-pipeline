CREATE TABLE "LearnCode" (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "LearnCode" (name) VALUES
    ('Books / Physical media'),
    ('Coding Bootcamp'), 
    ('Colleague'),
    ('Friend or family member'),
    ('Online Courses or Certification'), 
    ('On the job training'),
    ('Other online resources (e.g., videos, blogs, forum, online community)'), 
    ('School (i.e., University, College, etc)');

CREATE TABLE "ProgrammingLanguage" (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "ProgrammingLanguage" (name) VALUES
    ('Ada'), ('Apex'), ('Assembly'), ('Bash/Shell (all shells)'), ('C'), ('C#'), ('C++'), ('Clojure'), 
    ('Cobol'), ('Crystal'), ('Dart'), ('Delphi'), ('Elixir'), ('Erlang'), ('F#'), ('Fortran'), ('GDScript'), 
    ('Go'), ('Groovy'), ('Haskell'), ('HTML/CSS'), ('Java'), ('JavaScript'), ('Julia'), ('Kotlin'), ('Lisp'), 
    ('Lua'), ('MATLAB'), ('MicroPython'), ('Nim'), ('Objective-C'), ('OCaml'), ('Perl'), ('PHP'), ('PowerShell'), 
    ('Prolog'), ('Python'), ('R'), ('Ruby'), ('Rust'), ('Scala'), ('Solidity'), ('SQL'), ('Swift'), ('TypeScript'), 
    ('VBA'), ('Visual Basic (.Net)'), ('Zephyr'), ('Zig');

CREATE TABLE "Database" (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "Database" (name) VALUES
    ('BigQuery'), ('Cassandra'), ('Clickhouse'), ('Cloud Firestore'), ('Cockroachdb'), ('Cosmos DB'), ('Couch DB'), 
    ('Couchbase'), ('Databricks SQL'), ('Datomic'), ('DuckDB'), ('Dynamodb'), ('Elasticsearch'), ('EventStoreDB'),
    ('Firebase Realtime Database'), ('Firebird'), ('H2'), ('IBM DB2'), ('InfluxDB'), ('MariaDB'), ('Microsoft Access'),
    ('Microsoft SQL Server'), ('MongoDB'), ('MySQL'), ('Neo4J'), ('Oracle'), ('PostgreSQL'), ('Presto'), ('RavenDB'),
    ('Redis'), ('Snowflake'), ('Solr'), ('SQLite'), ('Supabase'), ('TiDB');

CREATE TABLE "Cloud" ( 
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "Cloud" (name) VALUES
    ('Alibaba Cloud'), ('Amazon Web Services (AWS)'), ('Cloudflare'), ('Colocation'), ('Databricks'), ('Digital Ocean'), 
    ('Firebase'), ('Fly.io'), ('Google Cloud'), ('Heroku'), ('Hetzner'), ('IBM Cloud Or Watson'), ('Linode'), 
    ('Managed Hosting'), ('Microsoft Azure'), ('Netlify'), ('OpenShift'), ('OpenStack'), ('Oracle Cloud Infrastructure (OCI)'), 
    ('OVH'), ('PythonAnywhere'), ('Render'), ('Scaleway'), ('Supabase'), ('Vercel'), ('VMware'), ('Vultr');

CREATE TABLE "WebFramework" ( 
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "WebFramework" (name) VALUES
    ('Angular'), ('AngularJS'), ('ASP.NET'), ('ASP.NET CORE'), ('Astro'), ('Blazor'), ('CodeIgniter'), ('Deno'), ('Django'),
    ('Drupal'), ('Elm'), ('Express'), ('FastAPI'), ('Fastify'), ('Flask'), ('Gatsby'), ('Htmx'), ('jQuery'), ('Laravel'),
    ('NestJS'), ('Next.js'), ('Node.js'), ('Nuxt.js'), ('Phoenix'), ('Play Framework'), ('React'), ('Remix'), ('Ruby on Rails'), 
    ('Solid.js'), ('Spring Boot'), ('Strapi'), ('Svelte'), ('Symfony'), ('Vue.js'), ('WordPress'), ('Yii 2');

CREATE TABLE "EmbeddedSystem" (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);      

INSERT INTO "EmbeddedSystem" (name) VALUES
    ('Arduino'), ('Boost.Test'), ('build2'), ('Catch2'), ('CMake'), ('Cargo'), ('cppunit'), ('CUTE'), ('doctest'), ('GNU GCC'),
    ('LLVM''s Clang'), ('Meson'), ('Micronaut'), ('MSVC'), ('Ninja'), ('PlatformIO'), ('QMake'), ('Rasberry Pi'), ('SCons'), ('ZMK');

CREATE TABLE "MiscTech" ( 
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "MiscTech" (name) VALUES
    ('.NET (5+)'), ('.NET Framework (1.0 - 4.8)'), ('.NET MAUI'), ('Apache Kafka'), ('Apache Spark'), ('Capacitor'), ('Cordova'),
    ('CUDA'), ('DirectX'), ('Electron'), ('Flutter'), ('GTK'), ('Hadoop'), ('Hugging Face Transformers'), ('Ionic'), ('JAX'),
    ('Keras'), ('Ktor'), ('MFC'), ('mlflow'), ('NumPy'), ('OpenCL'), ('Opencv'), ('OpenGL'), ('Pandas'), ('Qt'),
    ('Quarkus'), ('RabbitMQ'), ('React Native'), ('Roslyn'), ('Ruff'), ('Scikit-Learn'), ('Spring Framework'), ('SwiftUI'),
    ('Tauri'), ('TensorFlow'), ('Tidyverse'), ('Torch/PyTorch'), ('Xamarin');

CREATE TABLE "DevTool" (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "DevTool" (name) VALUES
    ('Ansible'), ('Ant'), ('APT'), ('Bun'), ('Chef'), ('Chocolatey'), ('Composer'), ('Dagger'), ('Docker'), ('Godot'),
    ('Google Test'), ('Gradle'), ('Homebrew'), ('Kubernetes'), ('Make'), ('Maven (build tool)'), ('MSBuild'), ('Ninja'),
    ('Nix'), ('npm'), ('NuGet'), ('Pacman'), ('Pip'), ('pnpm'), ('Podman'), ('Pulumi'), ('Puppet'), ('Terraform'),
    ('Unity 3D'), ('Unreal Engine'), ('Visual Studio Solution'), ('Vite'), ('Webpack'), ('Yarn');

CREATE TABLE "IDE" (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);  

INSERT INTO "IDE" (name) VALUES
    ('Android Studio'), ('BBEdit'), ('CLion'), ('Code::Blocks'), ('DataGrip'), ('Eclipse'), ('Emacs'), ('Fleet'), ('Geany'),
    ('Goland'), ('Helix'), ('IntelliJ IDEA'), ('IPython'), ('Jupyter Notebook/JupyterLab'), ('Kate'), ('Nano'), ('Neovim'),
    ('Netbeans'), ('Notepad++'), ('PhpStorm'), ('PyCharm'), ('Qt Creator'), ('Rad Studio (Delphi, C++ Builder)'), ('Rider'),
    ('RStudio'), ('RubyMine'), ('Spacemacs'), ('Spyder'), ('Sublime Text'), ('Vim'), ('Visual Studio'),
    ('Visual Studio Code'), ('VSCodium'), ('WebStorm'), ('Xcode');

CREATE TABLE "OS" (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "OS" (name) VALUES
    ('AIX'), ('Android'), ('Arch'), ('BSD'), ('ChromeOS'), ('Cygwin'), ('Debian'), ('Fedora'), ('Haiku'), ('iOS'), ('iPadOS'),
    ('MacOS'), ('Other Linux-based'), ('Red Hat'), ('Solaris'), ('Ubuntu'), ('Windows'), ('Windows Subsystem for Linux (WSL)');

CREATE TABLE "AITool" (   
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "AITool" (name) VALUES
    ('Andi'), ('AskCodi'), ('Amazon Q'), ('Bing AI'), ('ChatGPT'), ('Claude'), ('Codeium'), ('Cody'), ('GitHub Copilot'),
    ('Google Gemini'), ('Lightning AI'), ('Meta AI'), ('Metaphor'), ('Neeva AI'), ('OpenAI Codex'), ('Perplexity AI'),
    ('Phind'), ('Quora Poe'), ('Replit Ghostwriter'), ('WolframAlpha'), ('Snyk Code'), ('Tabnine'),
    ('Visual Studio Intellicode'), ('Whispr AI'), ('You.com');

CREATE TABLE "DevWorkflow" (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO "DevWorkflow" (name) VALUES
    ('Learning about a codebase'),
    ('Project planning'),
    ('Writing code'),
    ('Documenting code'),
    ('Debugging and getting help'),
    ('Testing code'),
    ('Committing and reviewing code'),
    ('Deployment and monitoring'),
    ('Predictive analytics'),
    ('Search for answers'),
    ('Generating content or synthetic data');