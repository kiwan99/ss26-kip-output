/* To-Do App — Client-side interactivity for US-001: Add New Tasks, US-002: View Task List */

(function () {
  "use strict";

  // DOM references
  var form = document.getElementById("addTaskForm");
  var input = document.getElementById("taskInput");
  var button = document.getElementById("addTaskBtn");
  var validationMsg = document.getElementById("validationMsg");
  var taskList = document.getElementById("taskList");

  /**
   * Validate the input text. Returns true if valid (non-empty after trim).
   */
  function validateInput(text) {
    return text && text.trim().length > 0;
  }

  /**
   * Show a validation error message.
   */
  function showValidationMessage(message) {
    validationMsg.textContent = message;
  }

  /**
   * Clear the validation message.
   */
  function clearValidationMessage() {
    validationMsg.textContent = "";
  }

  /**
   * Clear the input field value.
   */
  function clearInput() {
    input.value = "";
  }

  /**
   * Create a DOM element for a task and append it to the list.
   * Also removes the "No tasks yet" placeholder if present.
   */
  function renderTask(task) {
    // Remove placeholder if it exists
    var placeholder = taskList.querySelector(".no-tasks");
    if (placeholder) {
      placeholder.remove();
    }

    var li = document.createElement("li");
    li.className = "task-item";
    li.setAttribute("data-task-id", task.id);
    if (task.created_at) {
      li.setAttribute("data-created-at", task.created_at);
    }
    li.textContent = task.text;
    taskList.appendChild(li);

    return li;
  }

  /**
   * Fetch all tasks from server and render them in chronological order.
   */
  function loadTasks() {
    fetch("/api/tasks")
      .then(function (response) {
        if (!response.ok) throw new Error("Failed to load tasks.");
        return response.json();
      })
      .then(function (data) {
        var tasks = data.tasks;

        // Clear existing list
        taskList.innerHTML = "";

        if (!tasks || tasks.length === 0) {
          // Show placeholder when no tasks exist
          var p = document.createElement("p");
          p.className = "no-tasks";
          p.textContent = "No tasks yet";
          taskList.appendChild(p);
          return;
        }

        // Sort by created_at to ensure chronological order
        tasks.sort(function (a, b) {
          return (a.created_at || 0) - (b.created_at || 0);
        });

        // Render each task in order
        for (var i = 0; i < tasks.length; i++) {
          renderTask(tasks[i]);
        }
      })
      .catch(function (err) {
        console.error("Error loading tasks:", err.message);
      });
  }

  /**
   * Main handler: add a new task.
   * Called on form submit (button click triggers form submission).
   */
  function addTask(event) {
    // Prevent page reload
    if (event) {
      event.preventDefault();
    }

    var text = input.value;

    // Client-side validation
    if (!validateInput(text)) {
      showValidationMessage("Please enter a task.");
      return;
    }

    clearValidationMessage();

    // Send to server API
    fetch("/api/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    })
      .then(function (response) {
        if (!response.ok) {
          return response.json().then(function (errData) {
            throw new Error(errData.message || "Failed to add task.");
          });
        }
        return response.json();
      })
      .then(function (data) {
        // Server confirmed the task was added — update DOM
        renderTask(data.task);

        // Clear input for next entry
        clearInput();

        // Focus back on input for convenience
        input.focus();
      })
      .catch(function (err) {
        showValidationMessage(err.message || "Could not add task. Please try again.");
      });
  }

  // ---- Event Bindings ----

  // Form submit → addTask (handles both button click and Enter key)
  form.addEventListener("submit", addTask);

  // Input typing → clear validation message so user can retry
  input.addEventListener("input", function () {
    if (validationMsg.textContent) {
      clearValidationMessage();
    }
  });

  // Load all existing tasks on page load for US-002
  loadTasks();
})();
