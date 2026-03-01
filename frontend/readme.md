# AI Study Companion - Frontend Application

Welcome to the frontend repository for the AI Study Companion. This application is designed to help users streamline their study process by allowing them to easily create subjects and define their source materials (textbooks).

This README outlines the core features, user flow, and setup instructions for the frontend interface.

## 📖 Project Overview

The AI Study Companion frontend serves as the user interface for onboarding students to a new study topic. It guides the user from login to successfully defining what they want to study and which textbook they will use.

## ✨ Key Features

Based on the current implementation, the frontend supports the following features:

* **User Authentication:** Secure login portal for users to access their accounts.
* **Dashboard Portal:** A landing area where users can view their status and initiate new study goals.
* **Subject Creation:** A streamlined flow for adding new study topics.
* **Dual-Option Material Selection:** Users can choose between uploading their own PDF textbook or selecting from a curated list of recommended books.

## 🔄 Application User Flow

The primary goal of this frontend is to facilitate the following user journey:

1.  **Initial Launch:** The user opens the web application.
2.  **Authentication:** The user is presented with a login screen and must authenticate to proceed.
3.  **Portal Dashboard:** Upon successful login, the user lands on the main portal.
4.  **Initiate New Subject:** The user clicks the "Add a New Subject" button/card.
5.  **Subject Definition:** A prompt appears asking the user to enter the "Subject Title" (e.g., "Biology 101") and confirms by clicking enter/next.
6.  **Material Selection:** The final screen in this flow presents two distinct options for the chosen subject:
    * **Upload Textbook:** An area to drag-and-drop or select a local PDF file.
    * **Recommended Textbooks:** A selectable list of pre-defined textbooks relevant to the subject.

## 🛠️ Tech Stack

This project is built using the following technologies:

* **Frontend Framework:** [Name of Framework used, e.g., React.js, Vue.js, Angular, Svelte]
* **Language:** [e.g., JavaScript or TypeScript]
* **Build Tool:** [e.g., Vite, Webpack, Create React App]
* **Styling:** [e.g., CSS Modules, Tailwind CSS, Styled Components, SASS]
* **State Management:** [Optional: e.g., Redux, Context API, Pinia]
* **Routing:** [Optional: e.g., React Router, Vue Router]

## ⚙️ Getting Started / Local Setup

Follow these steps to run the frontend project locally on your machine.

### Prerequisites

Make sure you have the following installed:
* [Node.js](https://nodejs.org/) (Version [e.g., v16+] recommended)
* npm (Node Package Manager) or yarn

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [insert your repository URL here]
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd [name-of-your-project-folder]
    ```

3.  **Install dependencies:**
    ```bash
    # Using npm
    npm install

    # OR using yarn
    yarn install
    ```

4.  **Run the development server:**
    ```bash
    # Using npm
    npm start [or 'npm run dev', depending on your package.json scripts]

    # OR using yarn
    yarn start [or 'yarn dev']
    ```

5.  **Access the App:**
    Open your browser and navigate to `http://localhost:3000` (or the port specified in your terminal).

## 📁 Project Structure

A brief overview of the important files and directories: