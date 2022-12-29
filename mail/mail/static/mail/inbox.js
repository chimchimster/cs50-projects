

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;
  // By default, load the inbox



});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the emails of particular mailbox
  get_all_emails();
}


function send_email() {
    const recipients = document.querySelector('#compose-recipients').value
    const subject = document.querySelector('#compose-subject').value
    const body = document.querySelector('#compose-body').value

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
    })
    .then(response => response.json())
        .then(result => {
            if ("message" in result) {
                console.log(result);
                load_mailbox('sent');
                }
            if ("error" in result) {
                console.log(result);
                document.querySelector('#error-occurs').innerHTML = result["error"]
                }
            })
            .catch(error => {
                console.log(error);
        });
    return false;
    }

function get_all_emails() {
    fetch('emails/inbox')
    .then(response => response.json())
    .then(emails => {
        emails.forEach(email => {
            let div = document.createElement('div');
            div.innerHTML = `FROM: ${email.sender}<br>SUBJECT: ${email.subject}<br>CONTENT: ${email.body}`;
            console.log(div);
            document.querySelector('#emails-list').innerHTML += `${div.innerHTML}<br>`
            });
        console.log(emails);
        });
    }
