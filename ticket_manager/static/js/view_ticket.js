

const task_buttons = document.getElementsByClassName('button-task-done');

for(const button of task_buttons){
        button.addEventListener('click', (e)=>{
            const elem = e.currentTarget;
            const task_id = elem.dataset.task_id;
            const task_status = elem.dataset.task_status;
            const origin = document.location['origin'];
            let path;
            if ( task_status == 0){// 0--> means the task is open, the request means to close it, 
                path =  '/ticket_man/close_task/'+String(task_id);
            }else{ // if it's not zero it means we are reopening this task
                path =  '/ticket_man/re_open_task/'+String(task_id);
            }
            window.location = origin + path;
        });
}


const create_task_form_button = document.getElementById('button-create-task');
const create_task_form_overlay = document.getElementById('create-task-overlay');
const close_overlay = document.getElementById('close-overlay');

create_task_form_button.addEventListener('click', (e)=>{
    create_task_form_overlay.style.display = 'flex';
})

close_overlay.addEventListener('click', (e)=>{
    
    create_task_form_overlay.style.display = 'none';
    window.location.reload()
    
})