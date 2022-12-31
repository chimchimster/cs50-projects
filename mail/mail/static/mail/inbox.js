

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archive').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;
  document.querySelector('#back-to-mailbox').addEventListener('click', () => load_mailbox('inbox'));
  // By default, load the inbox

  load_mailbox('inbox')

});


function compose_email() {
  clear_all_emails();
  deactivate_current_button('compose')
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Update to null view one particular email
  document.querySelector('#view-email').innerHTML = '';

  // List which stores mailbox buttons
  let all_buttons = ['inbox', 'sent', 'archive', 'compose'];
  console.log(all_buttons)
  let filteredButtons = all_buttons.filter(function(e) {return e !== mailbox})
  all_buttons.forEach(box => {
    activate_disabled_button(box);
  });
  deactivate_current_button(mailbox);
  filteredButtons.push(mailbox);
  all_buttons = filteredButtons;
  // Show the emails of particular mailbox
  if (mailbox === 'inbox') {
    get_all_emails(mailbox);
  } else {
    clear_all_emails();
  }

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector('#back-to-mailbox').style.display = 'none';


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

function get_all_emails(mailbox) {
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        emails.forEach(email => {
            let btn = document.createElement('button');
            btn.setAttribute("id", "archive-email")
            let div = document.createElement('div');
            if (email.read === false) {
                div.style.backgroundColor = 'white';
            } else {
                div.style.backgroundColor = 'gray';
            }
            div.setAttribute("id", "unique-email");
            div.innerHTML = `FROM: ${email.sender}<br>SUBJECT: ${email.subject}<br>TIMESTAMP: ${email.timestamp}`;
            document.querySelector('#emails-view').append(div);
            div.addEventListener('click', function() {
                view_email(email.id, mailbox, email);
            });
        });
    });
}

function clear_all_emails() {
    document.querySelector('#emails-list').innerHTML = "";
}

function deactivate_current_button(mailbox) {
    document.querySelector(`#${mailbox}`).disabled = true;
}


function activate_disabled_button(mailbox) {
    if (mailbox == 'archive') {
        document.querySelector('#archive').disabled = false;
    } else {
    document.querySelector(`#${mailbox}`).disabled = false;
    }
}

function view_email(email_id, mailbox, email) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
                read: true,
                })
            })
            document.querySelector('#emails-view').innerHTML = '';
            if (mailbox === "inbox") {
                document.querySelector('#view-email').innerHTML = `From: ${email.sender}<br>Subject: ${email.subject}<br>Email:<br>${email.body}`;
            }
        document.querySelector('#back-to-mailbox').style.display = 'block';

    }

