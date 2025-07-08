# StatiPy: Simple, Fast, and Python-Powered Static Site Generation

## Overview

StatiPy is a lightweight, command-line static site generator written in Python. It transforms your Markdown content into a clean, modern, and fast-loading static website. It's perfect for personal blogs, project documentation, or any website where content is the primary focus.

## Features

*   **Markdown-First:** Write your content in simple Markdown files.
*   **Template-Based:** Uses a single HTML template for consistent page layout.
*   **Recursive Processing:** Automatically finds and processes all content and static files in their respective directories.
*   **Standard Markdown Support:** Handles headings, paragraphs, ordered and unordered lists, code blocks, blockquotes, bold and italic text, links, and images.
*   **Built-in Dev Server:** Comes with a simple command to build the site and serve it locally.
*   **Zero Dependencies:** Built entirely with the Python standard library.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Prerequisites:**
    Ensure you have Python 3 installed. No other dependencies are required.
    ```bash
    python3 --version
    ```

## Usage

1.  **Add Your Content:**
    *   Place your Markdown files (`.md`) in the `content/` directory. You can create subdirectories to organize your content.
    *   The title of each page is extracted from the first H1 heading (e.g., `# My Page Title`).

2.  **Add Static Files:**
    *   Place your static assets (CSS, images, etc.) in the `static/` directory. The directory structure will be preserved in the final output.

3.  **Customize the Template:**
    *   Modify `template.html` to change the overall layout of your site. Use the `{{ Title }}` and `{{ Content }}` placeholders to indicate where the page title and content should be inserted.

4.  **Build and Serve:**
    *   Run the build script from the project root:
        ```bash
        ./main.sh
        ```
    *   This command will:
        1.  Delete the old `docs/` directory.
        2.  Generate your site from the `content/` and `static/` directories into the `docs/` directory.
        3.  Start a local web server.
    *   You can view your site at `http://localhost:8888`.

### Advanced Usage: Deploying to a Subdirectory

If you plan to deploy your site to a subdirectory (e.g., `yourdomain.com/my-site/`), you can specify a `basepath` to ensure all links and asset paths are correct.

```bash
python3 src/main.py /my-site/
```

This will prepend `/my-site/` to all root-relative URLs in your generated HTML.
