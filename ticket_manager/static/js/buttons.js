const create_ticket_button = document.getElementById("button-create-ticket");
const close_create_ticket_button = document.getElementById("button-close-form");

if(create_ticket_button){
    create_ticket_button.addEventListener('click', (e)=>{
        const origin = document.location['origin']
        const path =  '/ticket_man/create_ticket/';
        window.location = origin + path;
    })
}

if(close_create_ticket_button){
    close_create_ticket_button.addEventListener('click', (e)=>{
        const res = confirm("Are you sure you want to close ticket before submitting ?")
        if(res){
            history.go(-1);
        }
    })
    
}

