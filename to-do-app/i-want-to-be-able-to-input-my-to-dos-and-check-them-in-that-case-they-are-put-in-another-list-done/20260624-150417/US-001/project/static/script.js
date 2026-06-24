document.getElementById('todo-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = document.getElementById('todo-input');
    const text = input.value.trim();
    if (text) {
        fetch('/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const li = document.createElement('li');
                li.textContent = text;
                document.getElementById('todo-list').appendChild(li);
                input.value = '';
            }
        });
    }
});