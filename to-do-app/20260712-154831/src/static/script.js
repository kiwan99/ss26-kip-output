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
     * Toggle the completed status of a task via API.
     * On success, re-renders the full list for instant visual update.
     */
    async function toggleTask(taskId) {
        try {
            const response = await fetch("/api/tasks/" + taskId + "/toggle", {
                method: "POST",
            });

            if (!response.ok) {
                console.error("Failed to toggle task");
                return;
            }

            // Re-render the full list to reflect changes instantly
            renderTasks();
        } catch (error) {
            console.error("Error toggling task:", error);
        }
    }

    /**
     * Delete a task via API.
     * On success, re-renders the full list so the removed task disappears instantly.
     */
    async function deleteTask(taskId) {
        try {
            const response = await fetch("/api/tasks/" + taskId, {
                method: "DELETE",
            });

            if (!response.ok) {
                console.error("Failed to delete task");
                return;
            }

            // Re-render the full list to reflect changes instantly
            renderTasks();
        } catch (error) {
            console.error("Error deleting task:", error);
        }
    }

    /**
     * Render the task list in the DOM from an array of task objects.
     * Shows/hides the empty state message accordingly.
     * Each task displays a checkbox, text, and delete button.
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

            // Checkbox for toggling completion
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.className = "task-checkbox";
            checkbox.checked = task.completed;
            checkbox.setAttribute("aria-label", "Mark task as " + (task.completed ? "incomplete" : "complete"));
            checkbox.addEventListener("change", function () {
                toggleTask(task.id);
            });
            li.appendChild(checkbox);

            // Task text span (with strikethrough if completed)
            const textSpan = document.createElement("span");
            textSpan.className = "task-text" + (task.completed ? " completed" : "");
            textSpan.textContent = task.text;
            li.appendChild(textSpan);

            // Delete button
            const deleteBtn = document.createElement("button");
            deleteBtn.className = "delete-btn";
            deleteBtn.type = "button";
            deleteBtn.textContent = "Delete";
            deleteBtn.setAttribute("aria-label", "Delete task: " + task.text);
            deleteBtn.addEventListener("click", function () {
                deleteTask(task.id);
            });
            li.appendChild(deleteBtn);

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
