

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

const ticket_history_button = document.getElementById("button-ticket-history");
const ticket_history_overlay = document.getElementById("ticket-history-overlay");
const ticket_history_close_overlay = document.getElementById("close-overlay-history");

ticket_history_button.addEventListener('click', (e)=>{
    ticket_history_overlay.style.display = 'flex';
    console.log(ticket_history_button)
});

ticket_history_close_overlay.addEventListener('click', (e)=>{
    ticket_history_overlay.style.display = 'none';
})

const delete_task_buttons = document.getElementsByClassName("delete-task-bin");

for(const bin of delete_task_buttons){
    bin.addEventListener('click', (e)=>{
       const task_id = e.target.dataset.task_id;
       const origin = document.location['origin'];
       const path = '/ticket_man/delete_task/'+String(task_id)
       window.location = origin + path;
    });
}


const create_task_form_button = document.getElementById('button-create-task');
const create_task_form_overlay = document.getElementById('create-task-overlay');
const close_overlay = document.getElementById('close-overlay');
if(create_task_form_button){
    create_task_form_button.addEventListener('click', (e)=>{
        create_task_form_overlay.style.display = 'flex';
    });
    
    close_overlay.addEventListener('click', (e)=>{
        
        create_task_form_overlay.style.display = 'none';
        window.location.reload()
    });    
}

const re_assign_ticket_button = document.getElementById("button-reassign-tick");
const re_assign_ticket_overlay = document.getElementById("re-assign-ticket-overlay");
const re_assign_close_overlay = document.getElementById("close-overlay-2");

if(re_assign_ticket_button){
    re_assign_ticket_button.addEventListener('click', (e)=>{
        re_assign_ticket_overlay.style.display = 'flex';
    });
    
    re_assign_close_overlay.addEventListener('click', (e)=>{
        re_assign_ticket_overlay.style.display = 'none';
    });
}




