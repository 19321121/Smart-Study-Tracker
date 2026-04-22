let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

function populateModuleFilter() {
  const moduleFilter = document.getElementById('moduleFilter');
  const modules = [...new Set(tasks.map(task => task.module))];

  moduleFilter.innerHTML = '<option value="all">All</option>';

  modules.forEach(module => {
    const option = document.createElement('option');
    option.value = module;
    option.textContent = module;
    moduleFilter.appendChild(option);
  });
}

function displayTasks() {
  const list = document.getElementById('taskList');
  list.innerHTML = '';

  const selectedModule = document.getElementById('moduleFilter').value;
  const selectedDate = document.getElementById('dateFilter').value;

  let filteredTasks = tasks.filter(task => {
    const moduleMatch = selectedModule === 'all' || task.module === selectedModule;
    const dateMatch = !selectedDate || task.deadline === selectedDate;
    return moduleMatch && dateMatch;
  });

  const groupedTasks = {};

  filteredTasks.forEach((task) => {
    const index = tasks.indexOf(task);

    if (!groupedTasks[task.module]) {
      groupedTasks[task.module] = [];
    }
    groupedTasks[task.module].push({ ...task, index });
  });

  for (let module in groupedTasks) {
    const moduleHeader = document.createElement('h3');
    moduleHeader.textContent = module;
    list.appendChild(moduleHeader);

    groupedTasks[module].forEach((taskObj) => {
      const li = document.createElement('li');
      li.textContent = `${taskObj.title} - ${taskObj.deadline} `;

      const completeBtn = document.createElement('button');
      completeBtn.textContent = taskObj.complete ? 'Completed' : 'Mark Complete';
      completeBtn.onclick = () => markComplete(taskObj.index);
      li.appendChild(completeBtn);

      const editBtn = document.createElement('button');
      editBtn.textContent = 'Edit';
      editBtn.onclick = () => editTask(taskObj.index);
      li.appendChild(editBtn);

      const deleteBtn = document.createElement('button');
      deleteBtn.textContent = 'Delete';
      deleteBtn.onclick = () => deleteTask(taskObj.index);
      li.appendChild(deleteBtn);

      if (taskObj.complete) {
        li.classList.add('completed');
      }

      list.appendChild(li);
    });
  }
}

document.getElementById('taskForm').addEventListener('submit', (e) => {
  e.preventDefault();

  const title = document.getElementById('title').value;
  const module = document.getElementById('module').value;
  const deadline = document.getElementById('deadline').value;

  tasks.push({ title, module, deadline, complete: false });
  localStorage.setItem('tasks', JSON.stringify(tasks));

  populateModuleFilter();
  displayTasks();
  document.getElementById('taskForm').reset();
});

document.getElementById('moduleFilter').addEventListener('change', displayTasks);
document.getElementById('dateFilter').addEventListener('change', displayTasks);

function markComplete(index) {
  tasks[index].complete = !tasks[index].complete;
  localStorage.setItem('tasks', JSON.stringify(tasks));
  displayTasks();
}

function editTask(index) {
  const task = tasks[index];
  const newTitle = prompt("Edit Task Title:", task.title);
  const newModule = prompt("Edit Module:", task.module);
  const newDeadline = prompt("Edit Deadline:", task.deadline);

  if (newTitle && newModule && newDeadline) {
    tasks[index] = {
      title: newTitle,
      module: newModule,
      deadline: newDeadline,
      complete: task.complete
    };
    localStorage.setItem('tasks', JSON.stringify(tasks));

    populateModuleFilter();
    displayTasks();
  }
}

function deleteTask(index) {
  if (confirm("Are you sure you want to delete this task?")) {
    tasks.splice(index, 1);
    localStorage.setItem('tasks', JSON.stringify(tasks));

    populateModuleFilter();
    displayTasks();
  }
}

populateModuleFilter();
displayTasks();
