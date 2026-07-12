/**
 * To-Do App - Client-side JavaScript
 *
 * Handles task input, API communication with Flask backend,
 * and DOM rendering for the to-do list.
 */

(function () {
    "use strict";

    // DOM elements
    const taskInput = document.getElementById("task-input");
    const addBtn = document.getElementById("add-btn");
    const taskList = document.getElementById("task-list");
    const emptyMessage = document.getElementById("empty-message");

    /**
     * Add a new task by sending a POST request to the API.
     * On success, re-renders the list and clears the input.
     */
    async function addTask() {
        const text = taskInput.value;

        // Submitting empty input does not create a blank task
        if (!text || !text.trim()) {
            return;
        }

        try {
            const response = await fetch("/api/tasks", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: text }),
            });

            if (!response.ok) {
                // Server rejected the task (e.g., empty text)
                return;
            }

            const newTask = await response.json();

            // Clear input after successfully adding a task
            taskInput.value = "";

            // Re-render the full list to reflect changes
            renderTasks();

            // Focus back on input for convenience
            taskInput.focus();
        } catch (error) {
            console.error("Failed to add task:", error);
        }
    }

    /**
     * Fetch all tasks from the API and render them in the DOM.
     */
    async function loadTasks() {
        try {
            const response = await fetch("/api/tasks");
            if (!response.ok) {
                console.error("Failed to load tasks");
                return;
            }

            const tasks = await response.json();
            renderTaskList(tasks);
        } catch (error) {
            console.error("Error loading tasks:", error);
        }
    }

    /**
     * Render the task list in the DOM from an array of task objects.
     * Shows/hides the empty state message accordingly.
     */
    function renderTaskList(tasks) {
        // Clear existing list items
        taskList.innerHTML = "";

        if (tasks.length === 0) {
            emptyMessage.style.display = "block";
            return;
        }

        emptyMessage.style.display = "none";

        tasks.forEach(function (task) {
            const li = document.createElement("li");
            li.dataset.taskId = task.id;

            // Task text span
            const textSpan = document.createElement("span");
            textSpan.className = "task-text";
            textSpan.textContent = task.text;
            li.appendChild(textSpan);

            taskList.appendChild(li);
        });
    }

    /**
     * Re-render the current tasks by fetching from API.
     */
    async function renderTasks() {
        await loadTasks();
    }

    // Event listener: Add button click triggers addTask
    addBtn.addEventListener("click", addTask);

    // Event listener: Enter key on input triggers addTask
    taskInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            addTask();
        }
    });

    // Load tasks when the page loads (DOMContentLoaded)
    document.addEventListener("DOMContentLoaded", loadTasks);
})();
