
const ticket_rows = document.getElementsByClassName("ticket-row");

console.log(ticket_rows)

for(var i = 0; i< ticket_rows.length; i++){
    ticket_rows[i].addEventListener('click', (e)=>{
        const row_object = e.currentTarget;
        const id = row_object.dataset.ticket_id;

        const origin = document.location['origin']
        const path =  '/ticket_man/view_ticket/'+String(id);
        console.log(path);
        window.location = origin + path;
    })
}